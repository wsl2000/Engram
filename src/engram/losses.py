from __future__ import annotations

import os
from typing import Callable

import torch
from torch.nn import functional as F


def _load_cut_cross_entropy() -> Callable[..., torch.Tensor] | None:
    try:
        from cut_cross_entropy import linear_cross_entropy as fn  # type: ignore

        return fn
    except Exception:
        return None


def _load_liger_linear_ce() -> Callable[..., torch.Tensor] | None:
    try:
        from liger_kernel.transformers.functional import liger_cross_entropy  # type: ignore

        return liger_cross_entropy
    except Exception:
        return None


def chunked_linear_cross_entropy(
    hidden: torch.Tensor,
    weight: torch.Tensor,
    labels: torch.Tensor,
    chunk_tokens: int,
) -> torch.Tensor:
    flat_h = hidden.reshape(-1, hidden.shape[-1])
    flat_y = labels.reshape(-1)
    losses = []
    counts = []
    for start in range(0, flat_h.shape[0], chunk_tokens):
        end = min(start + chunk_tokens, flat_h.shape[0])
        y = flat_y[start:end]
        valid = y != -100
        if not torch.any(valid):
            continue
        logits = F.linear(flat_h[start:end][valid], weight)
        losses.append(F.cross_entropy(logits.float(), y[valid], reduction="sum"))
        counts.append(valid.sum())
    if not losses:
        return flat_h.sum() * 0.0
    return torch.stack(losses).sum() / torch.stack(counts).sum()


def linear_cross_entropy(
    hidden: torch.Tensor,
    weight: torch.Tensor,
    labels: torch.Tensor,
    chunk_tokens: int = 256,
    implementation: str | None = None,
) -> torch.Tensor:
    """Linear-head CE with optional fused backends and a faithful chunked fallback.

    The installed cluster image does not currently ship Liger or cut-cross-entropy.
    Keeping the dispatch here lets calibration prove the fast path when an image
    with either backend is available, while preserving old behavior otherwise.
    """

    impl = (implementation or os.environ.get("ENGRAM_CE_IMPL", "auto")).lower()
    if impl not in {"auto", "chunked", "cut_cross_entropy", "liger"}:
        raise ValueError(f"unknown ENGRAM_CE_IMPL={impl!r}")
    flat_h = hidden.reshape(-1, hidden.shape[-1])
    flat_y = labels.reshape(-1)
    if impl in {"auto", "cut_cross_entropy"}:
        fn = _load_cut_cross_entropy()
        if fn is not None:
            try:
                return fn(flat_h, weight, flat_y, ignore_index=-100)
            except TypeError:
                return fn(flat_h, weight, flat_y)
        if impl == "cut_cross_entropy":
            raise RuntimeError("cut_cross_entropy requested but package/API is unavailable")
    if impl in {"auto", "liger"}:
        fn = _load_liger_linear_ce()
        if fn is not None:
            logits = F.linear(flat_h, weight)
            return fn(logits.float(), flat_y, ignore_index=-100)
        if impl == "liger":
            raise RuntimeError("liger requested but package/API is unavailable")
    return chunked_linear_cross_entropy(hidden, weight, labels, chunk_tokens=chunk_tokens)
