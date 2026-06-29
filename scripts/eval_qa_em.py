#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import string
import sys
from pathlib import Path
from typing import Any

import torch
from transformers import AutoTokenizer

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
SCRIPT_DIR = REPO_ROOT / "scripts"
for path in (SRC_DIR, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from engram.config import ModelShape
from engram.train import build_model_on_device
from eval_answer_nll import load_records


def normalize_answer(text: str) -> str:
    text = text.lower()
    text = "".join(ch for ch in text if ch not in string.punctuation)
    text = re.sub(r"\b(a|an|the)\b", " ", text)
    return " ".join(text.split())


def first_answer(record: dict[str, Any]) -> str:
    for answer in record["answers"]:
        if str(answer).strip():
            return str(answer)
    return ""


def fewshot_prompt(record: dict[str, Any], shots: list[dict[str, Any]]) -> str:
    parts = []
    for shot in shots:
        answer = first_answer(shot)
        if answer:
            parts.append(f"Question: {shot['question']}\nAnswer: {answer}\n")
    parts.append(f"Question: {record['question']}\nAnswer:")
    return "\n".join(parts)


def load_model(args: argparse.Namespace) -> tuple[Any, dict[str, Any], torch.device]:
    cfg = json.loads(Path(args.config).read_text())
    shape = ModelShape(**cfg["model"])
    device = torch.device("cuda", 0) if torch.cuda.is_available() else torch.device("cpu")
    dtype = torch.bfloat16 if device.type == "cuda" else torch.float32
    moe_backend = args.moe_backend or ("grouped" if device.type == "cuda" and hasattr(torch, "_grouped_mm") else "loop")
    os.environ["ENGRAM_MOE_BACKEND"] = moe_backend
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
    return model, cfg, device


def generate_answer(
    model: Any,
    tokenizer: Any,
    prompt: str,
    device: torch.device,
    seq_len: int,
    max_new_tokens: int,
    knockout: bool,
) -> str:
    context = tokenizer(prompt, add_special_tokens=False)["input_ids"]
    generated: list[int] = []
    eos_id = tokenizer.eos_token_id
    for _ in range(max_new_tokens):
        window = (context + generated)[-seq_len:]
        input_ids = torch.tensor(window, dtype=torch.long, device=device).unsqueeze(0)
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16, enabled=device.type == "cuda"):
            out = model(input_ids, knockout=knockout)
            logits = model.logits_for_hidden(out["hidden"][:, -1:])
        next_id = int(torch.argmax(logits[0, -1]).detach().cpu())
        if eos_id is not None and next_id == eos_id:
            break
        generated.append(next_id)
        decoded = tokenizer.decode(generated, skip_special_tokens=True)
        if "\n" in decoded:
            break
    return tokenizer.decode(generated, skip_special_tokens=True).splitlines()[0].strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--summary-json", required=True)
    parser.add_argument("--task", choices=("triviaqa", "popqa"), default="triviaqa")
    parser.add_argument("--split")
    parser.add_argument("--jsonl")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--num-shots", type=int, default=5)
    parser.add_argument("--max-new-tokens", type=int, default=16)
    parser.add_argument("--moe-backend", choices=("loop", "grouped", "auto"))
    parser.add_argument("--tokenizer", default="deepseek-ai/DeepSeek-V3")
    args = parser.parse_args()

    model, cfg, device = load_model(args)
    shape = ModelShape(**cfg["model"])
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)

    original_limit = args.limit
    args.limit = args.limit + args.num_shots
    records = load_records(args)
    shots = records[: args.num_shots]
    eval_records = records[args.num_shots : args.num_shots + original_limit]

    rows = []
    for idx, record in enumerate(eval_records):
        prompt = fewshot_prompt(record, shots)
        aliases = [normalize_answer(str(answer)) for answer in record["answers"] if str(answer).strip()]
        normal_pred = generate_answer(model, tokenizer, prompt, device, shape.seq_len, args.max_new_tokens, knockout=False)
        knockout_pred = generate_answer(model, tokenizer, prompt, device, shape.seq_len, args.max_new_tokens, knockout=True)
        normal_norm = normalize_answer(normal_pred)
        knockout_norm = normalize_answer(knockout_pred)
        rows.append(
            {
                "idx": idx,
                "id": record.get("id", idx),
                "normal_pred": normal_pred,
                "knockout_pred": knockout_pred,
                "normal_em": int(normal_norm in aliases),
                "knockout_em": int(knockout_norm in aliases),
                "answers": "|".join(str(a) for a in record["answers"][:5]),
            }
        )

    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.output_csv).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["idx"])
        writer.writeheader()
        writer.writerows(rows)

    normal_em = sum(row["normal_em"] for row in rows) / len(rows) if rows else None
    knockout_em = sum(row["knockout_em"] for row in rows) / len(rows) if rows else None
    summary = {
        "task": args.task if not args.jsonl else "jsonl",
        "checkpoint": args.checkpoint,
        "arm": cfg["arm"],
        "seed": cfg["seed"],
        "engram_enabled": bool(cfg["engram_enabled"]),
        "moe_backend": os.environ.get("ENGRAM_MOE_BACKEND"),
        "records": len(rows),
        "num_shots": args.num_shots,
        "max_new_tokens": args.max_new_tokens,
        "normal_em": normal_em,
        "knockout_em": knockout_em,
        "retention_ratio": knockout_em / normal_em if normal_em and knockout_em is not None else None,
    }
    Path(args.summary_json).write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
