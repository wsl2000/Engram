from __future__ import annotations

import argparse
import json
import math
import os
import time
from pathlib import Path

import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

from .config import ModelShape
from .data import LoaderConfig, PackedMemmapLoader
from .model import EngramTransformerLM


def setup_dist() -> tuple[int, int, int]:
    if "RANK" not in os.environ:
        return 0, 1, 0
    dist.init_process_group(backend="nccl")
    rank = dist.get_rank()
    world = dist.get_world_size()
    local_rank = int(os.environ.get("LOCAL_RANK", "0"))
    torch.cuda.set_device(local_rank)
    return rank, world, local_rank


def cosine_lr(step: int, max_steps: int, peak_lr: float, warmup_frac: float, min_lr_ratio: float) -> float:
    warmup = max(1, int(max_steps * warmup_frac))
    if step < warmup:
        return peak_lr * (step + 1) / warmup
    progress = (step - warmup) / max(1, max_steps - warmup)
    return peak_lr * (min_lr_ratio + 0.5 * (1 - min_lr_ratio) * (1 + math.cos(math.pi * progress)))


def save_checkpoint(path: Path, model: DDP | EngramTransformerLM, optimizer: torch.optim.Optimizer, step: int) -> None:
    raw_model = model.module if isinstance(model, DDP) else model
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"model": raw_model.state_dict(), "optimizer": optimizer.state_dict(), "step": step}, path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--token-files", nargs="+", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-steps-override", type=int)
    parser.add_argument("--calibration", action="store_true")
    args = parser.parse_args()

    rank, world, local_rank = setup_dist()
    device = torch.device("cuda", local_rank) if torch.cuda.is_available() else torch.device("cpu")
    cfg = json.loads(Path(args.config).read_text())
    torch.manual_seed(int(cfg["seed"]))
    shape = ModelShape(**cfg["model"])
    model = EngramTransformerLM(
        shape=shape,
        routed_experts=int(cfg["routed_experts"]),
        engram_rows=int(cfg["engram_rows"]),
        engram_enabled=bool(cfg["engram_enabled"]),
    ).to(device=device, dtype=torch.bfloat16)
    if world > 1:
        model = DDP(model, device_ids=[local_rank], output_device=local_rank)

    train_cfg = cfg["train"]
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=float(train_cfg["peak_lr"]),
        betas=(float(train_cfg["adam_beta1"]), float(train_cfg["adam_beta2"])),
        weight_decay=float(train_cfg["weight_decay"]),
    )
    max_steps = int(args.max_steps_override or train_cfg["max_steps"])
    grad_accum = max(1, int(train_cfg["grad_accum_steps_80gpu"] * 80 / world))
    micro_bsz = int(train_cfg["micro_batch_size"])
    loader = iter(
        PackedMemmapLoader(
            LoaderConfig(
                token_files=tuple(args.token_files),
                seq_len=shape.seq_len,
                batch_size=micro_bsz,
                seed=int(cfg["seed"]),
            )
        )
    )
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / f"train_rank{rank}.jsonl"
    tokens_per_micro_global = world * micro_bsz * shape.seq_len
    last_ckpt = time.time()
    start_time = time.time()

    for step in range(max_steps):
        lr = cosine_lr(step, max_steps, train_cfg["peak_lr"], train_cfg["warmup_frac"], train_cfg["min_lr_ratio"])
        for group in optimizer.param_groups:
            group["lr"] = lr
        optimizer.zero_grad(set_to_none=True)
        step_loss = torch.zeros((), device=device)
        step_aux = torch.zeros((), device=device)
        step_entropy = torch.zeros((), device=device)
        step_t0 = time.time()
        for _ in range(grad_accum):
            x, y = next(loader)
            x = x.to(device=device, non_blocking=True)
            y = y.to(device=device, non_blocking=True)
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16, enabled=device.type == "cuda"):
                out = model(x, labels=y, knockout=False)
                loss = out["loss"] + float(train_cfg["router_aux_loss_coef"]) * out["aux_loss"]
            (loss / grad_accum).backward()
            step_loss += out["loss"].detach() / grad_accum
            step_aux += out["aux_loss"].detach() / grad_accum
            step_entropy += out["router_entropy"].detach() / grad_accum
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), float(train_cfg["grad_clip"]))
        optimizer.step()
        elapsed_step = time.time() - step_t0
        tokens_seen = (step + 1) * grad_accum * tokens_per_micro_global
        tok_s = grad_accum * tokens_per_micro_global / elapsed_step
        active_params = float(cfg["derived"]["active_params"])
        mfu = (6.0 * active_params * tok_s) / (world * 989.5e12)
        metrics = {
            "step": step + 1,
            "loss": float(step_loss.detach().cpu()),
            "aux_loss": float(step_aux.detach().cpu()),
            "router_entropy": float(step_entropy.detach().cpu()),
            "lr": lr,
            "grad_norm": float(grad_norm.detach().cpu()),
            "tokens_seen": tokens_seen,
            "step_time_s": elapsed_step,
            "tokens_per_s": tok_s,
            "mfu": mfu,
            "world_size": world,
            "arm": cfg["arm"],
            "seed": cfg["seed"],
        }
        if rank == 0:
            with log_path.open("a") as f:
                f.write(json.dumps(metrics) + "\n")
            print(json.dumps(metrics), flush=True)
            ckpt_due = (time.time() - last_ckpt) / 60 >= float(train_cfg["checkpoint_minutes"])
            if ckpt_due or step + 1 == max_steps or (args.calibration and step + 1 == max_steps):
                save_checkpoint(output_dir / f"ckpt_step{step+1:06d}.pt", model, optimizer, step + 1)
                last_ckpt = time.time()
    if dist.is_initialized():
        dist.destroy_process_group()


if __name__ == "__main__":
    main()

