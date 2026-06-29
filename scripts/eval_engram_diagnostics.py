#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

import torch
from torch.nn import functional as F

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from engram.config import ModelShape
from engram.data import LoaderConfig, PackedMemmapLoader
from engram.engram_read import EngramRead, rms_norm_no_weight
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


def engram_components(module: EngramRead, hidden: torch.Tensor, token_ids: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    raw = module.lookup(token_ids)
    mem = module.proj(raw)
    conv_in = mem.transpose(1, 2)
    conv_in = F.pad(conv_in, (module.cfg.conv_kernel - 1, 0))
    mem = F.silu(module.conv(conv_in).transpose(1, 2))
    alpha = torch.sigmoid(
        (rms_norm_no_weight(hidden) * rms_norm_no_weight(mem)).sum(dim=-1, keepdim=True)
        / math.sqrt(hidden.shape[-1])
    )
    contribution = alpha * mem
    return alpha, mem, contribution


def new_layer_metric(layer: int) -> dict[str, float]:
    return {
        "layer": float(layer),
        "tokens": 0.0,
        "alpha_sum": 0.0,
        "alpha_sumsq": 0.0,
        "alpha_gt_0_5": 0.0,
        "hidden_sumsq": 0.0,
        "mem_sumsq": 0.0,
        "contribution_sumsq": 0.0,
        "vector_elements": 0.0,
    }


def update_layer_metric(metric: dict[str, float], hidden: torch.Tensor, alpha: torch.Tensor, mem: torch.Tensor, contribution: torch.Tensor) -> None:
    alpha_f = alpha.detach().float()
    hidden_f = hidden.detach().float()
    mem_f = mem.detach().float()
    contribution_f = contribution.detach().float()
    metric["tokens"] += float(alpha_f.numel())
    metric["alpha_sum"] += float(alpha_f.sum().item())
    metric["alpha_sumsq"] += float(alpha_f.square().sum().item())
    metric["alpha_gt_0_5"] += float((alpha_f > 0.5).sum().item())
    metric["hidden_sumsq"] += float(hidden_f.square().sum().item())
    metric["mem_sumsq"] += float(mem_f.square().sum().item())
    metric["contribution_sumsq"] += float(contribution_f.square().sum().item())
    metric["vector_elements"] += float(hidden_f.numel())


def finalize_layer_metric(metric: dict[str, float]) -> dict[str, float | int]:
    tokens = metric["tokens"]
    vector_elements = metric["vector_elements"]
    alpha_mean = metric["alpha_sum"] / tokens if tokens else None
    alpha_var = metric["alpha_sumsq"] / tokens - alpha_mean * alpha_mean if tokens and alpha_mean is not None else None
    hidden_rms = math.sqrt(metric["hidden_sumsq"] / vector_elements) if vector_elements else None
    mem_rms = math.sqrt(metric["mem_sumsq"] / vector_elements) if vector_elements else None
    contribution_rms = math.sqrt(metric["contribution_sumsq"] / vector_elements) if vector_elements else None
    return {
        "layer": int(metric["layer"]),
        "tokens": int(tokens),
        "alpha_mean": alpha_mean,
        "alpha_std": math.sqrt(max(alpha_var, 0.0)) if alpha_var is not None else None,
        "alpha_gt_0_5_frac": metric["alpha_gt_0_5"] / tokens if tokens else None,
        "hidden_rms": hidden_rms,
        "mem_rms": mem_rms,
        "contribution_rms": contribution_rms,
        "contribution_hidden_rms_ratio": contribution_rms / hidden_rms if hidden_rms else None,
    }


def forward_with_diagnostics(model: Any, input_ids: torch.Tensor) -> tuple[torch.Tensor, dict[int, dict[str, torch.Tensor]]]:
    x = model.token_embedding(input_ids)
    layer_data: dict[int, dict[str, torch.Tensor]] = {}
    for layer_idx, block in enumerate(model.blocks):
        x = x + block.attn(block.attn_norm(x))
        moe_out = block.moe(block.moe_norm(x))
        x = x + moe_out.hidden
        if block.engram is not None:
            hidden_before = x
            alpha, mem, contribution = engram_components(block.engram, hidden_before, input_ids)
            layer_data[layer_idx] = {
                "hidden": hidden_before,
                "alpha": alpha,
                "mem": mem,
                "contribution": contribution,
            }
            x = x + contribution
    return model.final_norm(x), layer_data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--token-files", nargs="*")
    parser.add_argument("--token-files-list")
    parser.add_argument("--output-csv", required=True)
    parser.add_argument("--summary-json", required=True)
    parser.add_argument("--num-batches", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--eval-seed", type=int, default=616161)
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
                batch_size=args.batch_size,
                seed=args.eval_seed,
            )
        )
    )

    layer_metrics = {layer: new_layer_metric(layer) for layer in shape.engram_layers}
    final_delta_sumsq = 0.0
    final_delta_elements = 0.0
    logit_abs_delta_sum = 0.0
    logit_abs_delta_count = 0.0
    logit_abs_delta_max = 0.0

    for _ in range(args.num_batches):
        x_cpu, _ = next(loader)
        input_ids = x_cpu.to(device=device, non_blocking=True)
        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16, enabled=device.type == "cuda"):
            normal_hidden, data = forward_with_diagnostics(model, input_ids)
            knockout_hidden, _, _ = model.forward_hidden(input_ids, knockout=True)
            for layer, values in data.items():
                update_layer_metric(
                    layer_metrics[layer],
                    hidden=values["hidden"],
                    alpha=values["alpha"],
                    mem=values["mem"],
                    contribution=values["contribution"],
                )
            delta = (normal_hidden - knockout_hidden).detach().float()
            final_delta_sumsq += float(delta.square().sum().item())
            final_delta_elements += float(delta.numel())
            normal_logits = model.logits_for_hidden(normal_hidden[:, -1:]).detach().float()
            knockout_logits = model.logits_for_hidden(knockout_hidden[:, -1:]).detach().float()
            logit_delta = (normal_logits - knockout_logits).abs()
            logit_abs_delta_sum += float(logit_delta.sum().item())
            logit_abs_delta_count += float(logit_delta.numel())
            logit_abs_delta_max = max(logit_abs_delta_max, float(logit_delta.max().item()))

    rows = [finalize_layer_metric(layer_metrics[layer]) for layer in sorted(layer_metrics)]
    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.output_csv).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["layer"])
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "checkpoint": args.checkpoint,
        "arm": cfg["arm"],
        "seed": cfg["seed"],
        "engram_enabled": bool(cfg["engram_enabled"]),
        "moe_backend": os.environ.get("ENGRAM_MOE_BACKEND"),
        "token_files": len(token_files),
        "eval_seed": args.eval_seed,
        "num_batches": args.num_batches,
        "batch_size": args.batch_size,
        "final_hidden_delta_rms": math.sqrt(final_delta_sumsq / final_delta_elements) if final_delta_elements else None,
        "last_logit_abs_delta_mean": logit_abs_delta_sum / logit_abs_delta_count if logit_abs_delta_count else None,
        "last_logit_abs_delta_max": logit_abs_delta_max,
        "layers": rows,
    }
    Path(args.summary_json).write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
