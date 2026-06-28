from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import numpy as np
import torch


@dataclass(frozen=True)
class LoaderConfig:
    token_files: tuple[str, ...]
    seq_len: int = 2048
    batch_size: int = 1
    seed: int = 1337


class PackedMemmapLoader:
    """Deterministic paired token loader over uint32 token memmaps."""

    def __init__(self, cfg: LoaderConfig):
        if not cfg.token_files:
            raise ValueError("token_files must not be empty")
        self.cfg = cfg
        self.arrays = [np.memmap(path, dtype=np.uint32, mode="r") for path in cfg.token_files]
        for path, arr in zip(cfg.token_files, self.arrays):
            if len(arr) <= cfg.seq_len + 1:
                raise ValueError(f"{path} is too short for seq_len={cfg.seq_len}")
        self.rng = np.random.default_rng(cfg.seed)

    def __iter__(self) -> Iterator[tuple[torch.Tensor, torch.Tensor]]:
        while True:
            x_batch = np.empty((self.cfg.batch_size, self.cfg.seq_len), dtype=np.int64)
            y_batch = np.empty((self.cfg.batch_size, self.cfg.seq_len), dtype=np.int64)
            for row in range(self.cfg.batch_size):
                shard_idx = int(self.rng.integers(0, len(self.arrays)))
                arr = self.arrays[shard_idx]
                start = int(self.rng.integers(0, len(arr) - self.cfg.seq_len - 1))
                chunk = np.asarray(arr[start : start + self.cfg.seq_len + 1], dtype=np.int64)
                x_batch[row] = chunk[:-1]
                y_batch[row] = chunk[1:]
            yield torch.from_numpy(x_batch), torch.from_numpy(y_batch)


def hash_first_batches(cfg: LoaderConfig, num_batches: int = 100) -> str:
    loader = iter(PackedMemmapLoader(cfg))
    h = hashlib.blake2b(digest_size=32)
    for _ in range(num_batches):
        x, y = next(loader)
        h.update(x.numpy().tobytes())
        h.update(y.numpy().tobytes())
    return h.hexdigest()


def write_synthetic_tokens(path: str | Path, num_tokens: int = 100_000, vocab_size: int = 128_000, seed: int = 0) -> None:
    rng = np.random.default_rng(seed)
    data = rng.integers(0, vocab_size, size=num_tokens, dtype=np.uint32)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data.tofile(path)

