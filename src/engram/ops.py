from __future__ import annotations

import json
import shutil
from pathlib import Path

import torch


def free_bytes(path: str | Path) -> int:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return shutil.disk_usage(path).free


def require_free_bytes(path: str | Path, min_free_bytes: int) -> None:
    free = free_bytes(path)
    if free < min_free_bytes:
        raise RuntimeError(
            f"insufficient free disk at {path}: free={free} bytes required={min_free_bytes} bytes"
        )


def latest_checkpoint(output_dir: str | Path) -> Path | None:
    ckpts = sorted(Path(output_dir).glob("ckpt_step*.pt"))
    return ckpts[-1] if ckpts else None


def rotate_checkpoints(output_dir: str | Path, keep_last: int = 2) -> list[Path]:
    output_dir = Path(output_dir)
    if keep_last < 0:
        raise ValueError("keep_last must be >= 0")
    ckpts = sorted(output_dir.glob("ckpt_step*.pt"))
    if keep_last == 0:
        removable = ckpts
    else:
        final = ckpts[-1:] if ckpts else []
        protected = set(ckpts[-keep_last:]) | set(final)
        removable = [p for p in ckpts if p not in protected]
    removed = []
    for path in removable:
        path.unlink(missing_ok=True)
        removed.append(path)
    return removed


def cuda_node_preflight() -> dict[str, object]:
    result: dict[str, object] = {
        "cuda_available": torch.cuda.is_available(),
        "device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "devices": [],
    }
    if not torch.cuda.is_available():
        return result
    devices = []
    for idx in range(torch.cuda.device_count()):
        torch.cuda.set_device(idx)
        x = torch.empty((1,), device=f"cuda:{idx}")
        free, total = torch.cuda.mem_get_info(idx)
        devices.append(
            {
                "index": idx,
                "name": torch.cuda.get_device_name(idx),
                "free_bytes": int(free),
                "total_bytes": int(total),
                "probe_value": float((x + 1).item()),
            }
        )
    result["devices"] = devices
    return result


def write_preflight(path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cuda_node_preflight(), indent=2))
