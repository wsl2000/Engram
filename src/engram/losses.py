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


class _MemoryEfficientLinearCE(torch.autograd.Function):
    @staticmethod
    def forward(ctx, hidden: torch.Tensor, weight: torch.Tensor, labels: torch.Tensor, chunk_tokens: int) -> torch.Tensor:
        flat_h = hidden.reshape(-1, hidden.shape[-1])
        flat_y = labels.reshape(-1)
        valid_count = int((flat_y != -100).sum().item())
        ctx.save_for_backward(hidden, weight, labels)
        ctx.chunk_tokens = int(chunk_tokens)
        ctx.valid_count = valid_count
        if valid_count == 0:
            return flat_h.float().sum() * 0.0
        total = torch.zeros((), device=hidden.device, dtype=torch.float32)
        w = weight.float()
        for start in range(0, flat_h.shape[0], int(chunk_tokens)):
            end = min(start + int(chunk_tokens), flat_h.shape[0])
            y = flat_y[start:end]
            valid = y != -100
            if not torch.any(valid):
                continue
            h = flat_h[start:end][valid].float()
            yy = y[valid]
            logits = h @ w.t()
            total = total + (torch.logsumexp(logits, dim=-1) - logits[torch.arange(len(yy), device=yy.device), yy]).sum()
        return total / valid_count

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor):
        hidden, weight, labels = ctx.saved_tensors
        flat_h = hidden.reshape(-1, hidden.shape[-1])
        flat_y = labels.reshape(-1)
        grad_h = torch.zeros_like(flat_h)
        grad_w = torch.zeros_like(weight, dtype=torch.float32)
        if ctx.valid_count == 0:
            return grad_h.reshape_as(hidden), grad_w.to(weight.dtype), None, None
        scale = grad_output.float() / float(ctx.valid_count)
        w = weight.float()
        for start in range(0, flat_h.shape[0], ctx.chunk_tokens):
            end = min(start + ctx.chunk_tokens, flat_h.shape[0])
            y = flat_y[start:end]
            valid = y != -100
            if not torch.any(valid):
                continue
            h = flat_h[start:end][valid].float()
            yy = y[valid]
            logits = h @ w.t()
            probs = torch.softmax(logits, dim=-1)
            probs[torch.arange(len(yy), device=yy.device), yy] -= 1.0
            probs = probs * scale
            grad_h_valid = probs @ w
            grad_w = grad_w + probs.t() @ h
            rows = torch.nonzero(valid, as_tuple=True)[0] + start
            grad_h[rows] = grad_h_valid.to(grad_h.dtype)
        return grad_h.reshape_as(hidden), grad_w.to(weight.dtype), None, None


def memory_efficient_linear_cross_entropy(
    hidden: torch.Tensor,
    weight: torch.Tensor,
    labels: torch.Tensor,
    chunk_tokens: int = 256,
) -> torch.Tensor:
    return _MemoryEfficientLinearCE.apply(hidden, weight, labels, int(chunk_tokens))


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
    if impl not in {"auto", "chunked", "memory_efficient", "cut_cross_entropy", "liger"}:
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
    if impl in {"auto", "memory_efficient"}:
        return memory_efficient_linear_cross_entropy(hidden, weight, labels, chunk_tokens=chunk_tokens)
    return chunked_linear_cross_entropy(hidden, weight, labels, chunk_tokens=chunk_tokens)
