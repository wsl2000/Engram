#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any

import torch
from torch.nn import functional as F
from transformers import AutoTokenizer

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from engram.config import ModelShape
from engram.data import LoaderConfig, PackedMemmapLoader
from engram.train import build_model_on_device


def resolve_token_files(args: argparse.Namespace) -> list[str]:
    paths: list[str] = []
    if args.token_files_list:
        paths.extend(line.strip() for line in Path(args.token_files_list).read_text().splitlines() if line.strip())
    if args.token_files:
        paths.extend(args.token_files)
    if not paths:
        raise ValueError("provide --token-files or --token-files-list")
    return paths


def load_model(args: argparse.Namespace) -> tuple[Any, dict[str, Any], torch.device]:
    cfg = json.loads(Path(args.config).read_text())
    shape = ModelShape(**cfg["model"])
    device = torch.device("cuda", 0) if torch.cuda.is_available() else torch.device("cpu")
    moe_backend = args.moe_backend or ("grouped" if device.type == "cuda" and hasattr(torch, "_grouped_mm") else "loop")
    os.environ["ENGRAM_MOE_BACKEND"] = moe_backend
    model = build_model_on_device(
        shape=shape,
        routed_experts=int(cfg["routed_experts"]),
        engram_rows=int(cfg["engram_rows"]),
        engram_enabled=bool(cfg["engram_enabled"]),
        device=device,
        dtype=torch.bfloat16,
    )
    ckpt = torch.load(args.checkpoint, map_location="cpu")
    model.load_state_dict(ckpt["model"])
    del ckpt
    model.eval()
    return model, cfg, device


def repeated_ngram_mask(full_ids: torch.Tensor) -> torch.Tensor:
    ids = [int(x) for x in full_ids.cpu().tolist()]
    mask = torch.zeros(len(ids) - 1, dtype=torch.bool)
    seen2: set[tuple[int, int]] = set()
    seen3: set[tuple[int, int, int]] = set()
    for pos in range(len(ids) - 1):
        if pos >= 1 and (ids[pos], ids[pos + 1]) in seen2:
            mask[pos] = True
        if pos >= 2 and (ids[pos - 1], ids[pos], ids[pos + 1]) in seen3:
            mask[pos] = True
        if pos >= 1:
            seen2.add((ids[pos - 1], ids[pos]))
        if pos >= 2:
            seen3.add((ids[pos - 2], ids[pos - 1], ids[pos]))
    return mask


def looks_entityish(token: str) -> bool:
    text = token.lstrip(" _\t\n\r").lstrip("\u2581\u0120").strip()
    text = text.strip(".,;:!?()[]{}<>\"'`")
    if len(text) < 2 or not any(ch.isalpha() for ch in text):
        return False
    return text[0].isupper() and any(ch.islower() for ch in text[1:])


def entity_proxy_mask(full_ids: torch.Tensor, tokenizer: Any) -> torch.Tensor:
    tokens = tokenizer.convert_ids_to_tokens([int(x) for x in full_ids.cpu().tolist()])
    mask = torch.zeros(len(tokens) - 1, dtype=torch.bool)
    for pos, token in enumerate(tokens[1:]):
        if looks_entityish(str(token)):
            mask[pos] = True
    return mask


def per_token_nll(
    model: Any,
    x: torch.Tensor,
    y: torch.Tensor,
    chunk_tokens: int,
    knockout: bool,
) -> torch.Tensor:
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16, enabled=x.is_cuda):
        hidden, _, _ = model.forward_hidden(x, knockout=knockout)
    flat_h = hidden.reshape(-1, hidden.shape[-1])
    flat_y = y.reshape(-1)
    losses = torch.empty(flat_y.shape[0], dtype=torch.float32, device="cpu")
    with torch.inference_mode():
        for start in range(0, flat_h.shape[0], chunk_tokens):
            end = min(start + chunk_tokens, flat_h.shape[0])
            logits = model.logits_for_hidden(flat_h[start:end])
            loss = F.cross_entropy(logits.float(), flat_y[start:end], reduction="none")
            losses[start:end] = loss.detach().cpu()
    return losses.reshape(y.shape)


def update_metric(metrics: dict[str, dict[str, float]], name: str, values: torch.Tensor, mask: torch.Tensor) -> None:
    count = int(mask.sum().item())
    if count == 0:
        return
    metrics[name]["sum"] += float(values[mask].sum().item())
    metrics[name]["count"] += count


def nll_from(sum_value: float, count: float) -> float | None:
    return sum_value / count if count else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--token-files", nargs="*")
    parser.add_argument("--token-files-list")
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--summary-json", required=True)
    parser.add_argument("--num-batches", type=int, default=16)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--eval-seed", type=int, default=424242)
    parser.add_argument("--chunk-tokens", type=int, default=128)
    parser.add_argument("--knockout", action="store_true")
    parser.add_argument("--moe-backend", choices=("loop", "grouped", "auto"))
    parser.add_argument("--tokenizer", default="deepseek-ai/DeepSeek-V3")
    args = parser.parse_args()

    model, cfg, device = load_model(args)
    shape = ModelShape(**cfg["model"])
    token_files = resolve_token_files(args)
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    loader = iter(
        PackedMemmapLoader(
            LoaderConfig(
                token_files=tuple(token_files),
                seq_len=shape.seq_len,
                batch_size=args.batch_size,
                seed=args.eval_seed,
            )
        )
    )

    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    metrics = {
        "global": {"sum": 0.0, "count": 0.0},
        "repeat_ngram": {"sum": 0.0, "count": 0.0},
        "entity_proxy": {"sum": 0.0, "count": 0.0},
    }
    rows = []
    for batch_idx in range(args.num_batches):
        x_cpu, y_cpu = next(loader)
        losses = per_token_nll(
            model=model,
            x=x_cpu.to(device=device, non_blocking=True),
            y=y_cpu.to(device=device, non_blocking=True),
            chunk_tokens=args.chunk_tokens,
            knockout=args.knockout,
        )
        for row_idx in range(x_cpu.shape[0]):
            full_ids = torch.cat([x_cpu[row_idx], y_cpu[row_idx, -1:]], dim=0)
            global_mask = torch.ones(shape.seq_len, dtype=torch.bool)
            repeat_mask = repeated_ngram_mask(full_ids)
            entity_mask = entity_proxy_mask(full_ids, tokenizer)
            row_losses = losses[row_idx]
            update_metric(metrics, "global", row_losses, global_mask)
            update_metric(metrics, "repeat_ngram", row_losses, repeat_mask)
            update_metric(metrics, "entity_proxy", row_losses, entity_mask)
            rows.append(
                {
                    "batch": batch_idx,
                    "row": row_idx,
                    "global_count": int(global_mask.sum().item()),
                    "global_nll": nll_from(float(row_losses.sum().item()), float(global_mask.sum().item())),
                    "repeat_ngram_count": int(repeat_mask.sum().item()),
                    "repeat_ngram_nll": nll_from(float(row_losses[repeat_mask].sum().item()), float(repeat_mask.sum().item())),
                    "entity_proxy_count": int(entity_mask.sum().item()),
                    "entity_proxy_nll": nll_from(float(row_losses[entity_mask].sum().item()), float(entity_mask.sum().item())),
                }
            )

    with Path(args.output_csv).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["batch"])
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "checkpoint": args.checkpoint,
        "arm": cfg["arm"],
        "seed": cfg["seed"],
        "engram_enabled": bool(cfg["engram_enabled"]),
        "knockout": bool(args.knockout),
        "moe_backend": os.environ.get("ENGRAM_MOE_BACKEND"),
        "token_files": len(token_files),
        "eval_seed": args.eval_seed,
        "num_batches": args.num_batches,
        "batch_size": args.batch_size,
        "entity_slice_method": "capitalized_token_proxy",
        "global_nll": nll_from(metrics["global"]["sum"], metrics["global"]["count"]),
        "global_tokens": int(metrics["global"]["count"]),
        "repeat_ngram_nll": nll_from(metrics["repeat_ngram"]["sum"], metrics["repeat_ngram"]["count"]),
        "repeat_ngram_tokens": int(metrics["repeat_ngram"]["count"]),
        "entity_proxy_nll": nll_from(metrics["entity_proxy"]["sum"], metrics["entity_proxy"]["count"]),
        "entity_proxy_tokens": int(metrics["entity_proxy"]["count"]),
    }
    Path(args.summary_json).write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
