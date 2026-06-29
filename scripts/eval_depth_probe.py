#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np
import torch

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


def layer_states(model: Any, input_ids: torch.Tensor, knockout: bool) -> tuple[list[torch.Tensor], torch.Tensor]:
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16, enabled=input_ids.is_cuda):
        hidden = model.token_embedding(input_ids)
        states = [hidden]
        for block in model.blocks:
            hidden, _, _ = block(hidden, input_ids, knockout=knockout)
            states.append(hidden)
        final_hidden = model.final_norm(hidden)
    return states, final_hidden


def choose_positions(seq_len: int, count: int, rng: np.random.Generator) -> np.ndarray:
    count = min(count, seq_len)
    positions = rng.choice(seq_len, size=count, replace=False)
    positions.sort()
    return positions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--token-files", nargs="*")
    parser.add_argument("--token-files-list")
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--summary-json", required=True)
    parser.add_argument("--num-batches", type=int, default=8)
    parser.add_argument("--positions-per-batch", type=int, default=256)
    parser.add_argument("--eval-seed", type=int, default=515151)
    parser.add_argument("--knockout", action="store_true")
    parser.add_argument("--moe-backend", choices=("loop", "grouped", "auto"))
    args = parser.parse_args()

    model, cfg, device = load_model(args)
    shape = ModelShape(**cfg["model"])
    token_files = resolve_token_files(args)
    loader = iter(
        PackedMemmapLoader(
            LoaderConfig(
                token_files=tuple(token_files),
                seq_len=shape.seq_len,
                batch_size=1,
                seed=args.eval_seed,
            )
        )
    )
    rng = np.random.default_rng(args.eval_seed)
    rows = []
    first_counts = {layer: 0 for layer in range(shape.n_layers + 1)}
    total = 0
    for batch_idx in range(args.num_batches):
        x_cpu, _ = next(loader)
        positions_np = choose_positions(shape.seq_len, args.positions_per_batch, rng)
        positions = torch.tensor(positions_np, dtype=torch.long, device=device)
        x = x_cpu.to(device=device, non_blocking=True)
        states, final_hidden = layer_states(model, x, knockout=args.knockout)
        with torch.inference_mode():
            final_logits = model.logits_for_hidden(final_hidden[0, positions])
            final_pred = torch.argmax(final_logits, dim=-1)
            earliest = torch.full((positions.numel(),), fill_value=shape.n_layers, dtype=torch.long, device=device)
            unresolved = torch.ones_like(earliest, dtype=torch.bool)
            for layer_idx, state in enumerate(states):
                lens_hidden = model.final_norm(state)[0, positions]
                pred = torch.argmax(model.logits_for_hidden(lens_hidden), dim=-1)
                matched = unresolved & (pred == final_pred)
                earliest[matched] = layer_idx
                unresolved &= ~matched
                if not bool(unresolved.any()):
                    break
        for pos, first_layer, pred in zip(positions_np, earliest.detach().cpu().tolist(), final_pred.detach().cpu().tolist(), strict=True):
            first_counts[int(first_layer)] += 1
            total += 1
            rows.append(
                {
                    "batch": batch_idx,
                    "position": int(pos),
                    "earliest_layer": int(first_layer),
                    "final_pred": int(pred),
                }
            )

    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.output_csv).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["batch"])
        writer.writeheader()
        writer.writerows(rows)

    earliest_values = [row["earliest_layer"] for row in rows]
    cumulative = {}
    running = 0
    for layer in range(shape.n_layers + 1):
        running += first_counts[layer]
        cumulative[f"resolved_by_layer_{layer}"] = running / total if total else None
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
        "positions": total,
        "mean_earliest_layer": float(np.mean(earliest_values)) if earliest_values else None,
        "median_earliest_layer": float(np.median(earliest_values)) if earliest_values else None,
        "first_layer_counts": {str(k): int(v) for k, v in first_counts.items()},
        **cumulative,
    }
    Path(args.summary_json).write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
