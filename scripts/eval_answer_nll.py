#!/usr/bin/env python
from __future__ import annotations

import argparse
import ast
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import torch
from datasets import load_dataset
from transformers import AutoTokenizer

from engram.config import ModelShape
from engram.model import EngramTransformerLM
from engram.train import build_model_on_device


def load_dataset_with_fallback(path: str, *args: str, splits: tuple[str, ...]) -> Any:
    last_exc: Exception | None = None
    for split in splits:
        try:
            return load_dataset(path, *args, split=split)
        except ValueError as exc:
            last_exc = exc
    if last_exc is not None:
        raise last_exc
    raise RuntimeError("no dataset splits were provided")


def load_records(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.jsonl:
        records = []
        with Path(args.jsonl).open() as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
        return records[: args.limit]
    if args.task == "triviaqa":
        ds = load_dataset_with_fallback("trivia_qa", "rc.nocontext", splits=(args.split or "validation",))
        records = []
        for row in ds.select(range(min(args.limit, len(ds)))):
            answer = row.get("answer") or {}
            aliases = []
            for key in ("aliases", "normalized_aliases"):
                aliases.extend(answer.get(key) or [])
            if answer.get("value"):
                aliases.append(answer["value"])
            records.append({"id": row.get("question_id"), "question": row["question"], "answers": sorted(set(aliases))})
        return records
    if args.task == "popqa":
        splits = (args.split,) if args.split else ("test", "validation", "train")
        ds = load_dataset_with_fallback("akariasai/PopQA", splits=splits)
        records = []
        for row in ds.select(range(min(args.limit, len(ds)))):
            question = row.get("question") or row.get("Question")
            if question is None and row.get("subj") and row.get("prop"):
                question = f"{row['subj']} {row['prop']}?"
            answers = row.get("possible_answers") or row.get("answers") or row.get("obj") or row.get("Object")
            if isinstance(answers, str):
                try:
                    parsed = ast.literal_eval(answers)
                    answers = parsed if isinstance(parsed, list) else [answers]
                except (ValueError, SyntaxError):
                    answers = [answers]
            records.append({"id": row.get("id"), "question": question, "answers": answers or []})
        return [r for r in records if r["question"] and r["answers"]]
    raise ValueError(f"unknown task: {args.task}")


def prompt_for(question: str) -> str:
    return f"Question: {question}\nAnswer:"


def answer_loss(
    model: EngramTransformerLM,
    tokenizer: Any,
    prompt: str,
    answer: str,
    device: torch.device,
    seq_len: int,
    knockout: bool,
) -> tuple[float, int]:
    prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
    answer_ids = tokenizer(" " + answer, add_special_tokens=False)["input_ids"]
    full_ids = prompt_ids + answer_ids
    if len(full_ids) < 2 or len(full_ids) > seq_len + 1:
        return float("nan"), 0
    input_ids = torch.tensor(full_ids[:-1], dtype=torch.long, device=device).unsqueeze(0)
    labels = torch.tensor(full_ids[1:], dtype=torch.long, device=device).unsqueeze(0)
    mask_until = max(len(prompt_ids) - 1, 0)
    labels[:, :mask_until] = -100
    valid = int((labels != -100).sum().item())
    if valid == 0:
        return float("nan"), 0
    with torch.inference_mode(), torch.autocast(device_type="cuda", dtype=torch.bfloat16, enabled=device.type == "cuda"):
        out = model(input_ids, labels=labels, knockout=knockout)
    return float(out["loss"].detach().cpu()), valid


def best_record_loss(
    model: EngramTransformerLM,
    tokenizer: Any,
    record: dict[str, Any],
    device: torch.device,
    seq_len: int,
    knockout: bool,
) -> tuple[float, int, str]:
    prompt = prompt_for(str(record["question"]))
    best = (float("inf"), 0, "")
    for answer in record["answers"]:
        loss, tokens = answer_loss(model, tokenizer, prompt, str(answer), device, seq_len, knockout)
        if tokens and loss < best[0]:
            best = (loss, tokens, str(answer))
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--summary-json", required=True)
    parser.add_argument("--task", choices=("triviaqa", "popqa"), default="triviaqa")
    parser.add_argument("--split")
    parser.add_argument("--jsonl")
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--moe-backend", choices=("loop", "grouped", "auto"))
    parser.add_argument("--tokenizer", default="deepseek-ai/DeepSeek-V3")
    args = parser.parse_args()

    cfg = json.loads(Path(args.config).read_text())
    shape = ModelShape(**cfg["model"])
    device = torch.device("cuda", 0) if torch.cuda.is_available() else torch.device("cpu")
    dtype = torch.bfloat16 if device.type == "cuda" else torch.float32
    moe_backend = args.moe_backend or ("grouped" if device.type == "cuda" and hasattr(torch, "_grouped_mm") else "loop")
    os.environ["ENGRAM_MOE_BACKEND"] = moe_backend
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    model = build_model_on_device(
        shape=shape,
        routed_experts=int(cfg["routed_experts"]),
        engram_rows=int(cfg["engram_rows"]),
        engram_enabled=bool(cfg["engram_enabled"]),
        device=device,
        dtype=dtype,
    )
    ckpt = torch.load(args.checkpoint, map_location="cpu")
    model.load_state_dict(ckpt["model"])
    del ckpt
    model.eval()

    rows = []
    records = load_records(args)
    for idx, record in enumerate(records):
        normal_loss, normal_tokens, normal_answer = best_record_loss(model, tokenizer, record, device, shape.seq_len, False)
        knockout_loss, knockout_tokens, knockout_answer = best_record_loss(model, tokenizer, record, device, shape.seq_len, True)
        if not normal_tokens or not knockout_tokens:
            continue
        rows.append(
            {
                "idx": idx,
                "id": record.get("id", idx),
                "normal_nll": normal_loss,
                "knockout_nll": knockout_loss,
                "delta_knockout_minus_normal": knockout_loss - normal_loss,
                "normal_tokens": normal_tokens,
                "knockout_tokens": knockout_tokens,
                "normal_answer": normal_answer,
                "knockout_answer": knockout_answer,
            }
        )

    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.output_csv).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["idx"])
        writer.writeheader()
        writer.writerows(rows)

    deltas = [r["delta_knockout_minus_normal"] for r in rows]
    summary = {
        "task": args.task if not args.jsonl else "jsonl",
        "checkpoint": args.checkpoint,
        "split": args.split,
        "limit": args.limit,
        "moe_backend": moe_backend,
        "engram_enabled": bool(cfg["engram_enabled"]),
        "records": len(rows),
        "mean_normal_nll": sum(r["normal_nll"] for r in rows) / len(rows) if rows else None,
        "mean_knockout_nll": sum(r["knockout_nll"] for r in rows) / len(rows) if rows else None,
        "mean_delta_knockout_minus_normal": sum(deltas) / len(deltas) if deltas else None,
        "positive_delta_frac": sum(1 for d in deltas if d > 0) / len(deltas) if deltas else None,
    }
    Path(args.summary_json).write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
