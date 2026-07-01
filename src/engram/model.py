from __future__ import annotations

import math
import os
from dataclasses import dataclass

import torch
from torch import nn
from torch.nn import functional as F

from .config import ModelShape
from .engram_read import EngramRead, EngramReadConfig
from .losses import linear_cross_entropy


class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dim))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y = x * torch.rsqrt(x.pow(2).mean(dim=-1, keepdim=True) + self.eps)
        return y * self.weight


def rotate_half(x: torch.Tensor) -> torch.Tensor:
    x_even = x[..., ::2]
    x_odd = x[..., 1::2]
    return torch.stack((-x_odd, x_even), dim=-1).flatten(-2)


class CausalSelfAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int, rope_theta: float = 10_000.0, use_rope: bool = True):
        super().__init__()
        assert d_model % n_heads == 0
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        if self.head_dim % 2 != 0:
            raise ValueError("RoPE requires an even attention head dimension")
        self.use_rope = use_rope
        self.rope_theta = rope_theta
        inv_freq = 1.0 / (rope_theta ** (torch.arange(0, self.head_dim, 2, dtype=torch.float32) / self.head_dim))
        self.register_buffer("rope_inv_freq", inv_freq, persistent=False)
        self.qkv = nn.Linear(d_model, 3 * d_model, bias=False)
        self.out = nn.Linear(d_model, d_model, bias=False)

    def _apply_rope(self, q: torch.Tensor, k: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        if not self.use_rope:
            return q, k
        seq_len = q.shape[-2]
        pos = torch.arange(seq_len, device=q.device, dtype=self.rope_inv_freq.dtype)
        freqs = torch.outer(pos, self.rope_inv_freq)
        cos = freqs.cos().repeat_interleave(2, dim=-1).to(dtype=q.dtype)[None, None, :, :]
        sin = freqs.sin().repeat_interleave(2, dim=-1).to(dtype=q.dtype)[None, None, :, :]
        return (q * cos) + (rotate_half(q) * sin), (k * cos) + (rotate_half(k) * sin)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        bsz, seq_len, d_model = x.shape
        qkv = self.qkv(x).view(bsz, seq_len, 3, self.n_heads, self.head_dim)
        q, k, v = qkv.unbind(dim=2)
        q = q.transpose(1, 2)
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)
        q, k = self._apply_rope(q, k)
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        y = y.transpose(1, 2).contiguous().view(bsz, seq_len, d_model)
        return self.out(y)


class ExpertBank(nn.Module):
    def __init__(self, num_experts: int, d_model: int, hidden: int):
        super().__init__()
        self.num_experts = num_experts
        self.w_gate = nn.Parameter(torch.empty(num_experts, d_model, hidden))
        self.w_up = nn.Parameter(torch.empty(num_experts, d_model, hidden))
        self.w_down = nn.Parameter(torch.empty(num_experts, hidden, d_model))
        self.reset_parameters()

    def reset_parameters(self) -> None:
        scale = 0.02
        nn.init.normal_(self.w_gate, mean=0.0, std=scale)
        nn.init.normal_(self.w_up, mean=0.0, std=scale)
        nn.init.normal_(self.w_down, mean=0.0, std=scale)

    def forward_expert(self, expert_idx: int, x: torch.Tensor) -> torch.Tensor:
        gate = x @ self.w_gate[expert_idx]
        up = x @ self.w_up[expert_idx]
        return (F.silu(gate) * up) @ self.w_down[expert_idx]


@dataclass
class MoEOutput:
    hidden: torch.Tensor
    aux_loss: torch.Tensor
    router_entropy: torch.Tensor


class MoELayer(nn.Module):
    def __init__(
        self,
        d_model: int,
        expert_hidden: int,
        routed_experts: int,
        top_k: int,
        shared_experts: int = 1,
    ):
        super().__init__()
        if shared_experts != 1:
            raise ValueError("this implementation expects exactly one shared expert")
        self.routed_experts = routed_experts
        self.top_k = top_k
        self.router = nn.Linear(d_model, routed_experts, bias=False)
        self.shared = ExpertBank(1, d_model, expert_hidden)
        self.routed = ExpertBank(routed_experts, d_model, expert_hidden)

    def _route(self, flat: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        router_logits = self.router(flat.float())
        router_probs = F.softmax(router_logits, dim=-1)
        top_vals, top_idx = torch.topk(router_probs, k=self.top_k, dim=-1)
        top_vals = top_vals / top_vals.sum(dim=-1, keepdim=True).clamp_min(1e-9)
        return router_probs, top_vals, top_idx

    def _router_stats(self, router_probs: torch.Tensor, top_idx: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        mean_prob = router_probs.mean(dim=0)
        token_frac = torch.bincount(top_idx.reshape(-1), minlength=self.routed_experts).to(router_probs.dtype)
        token_frac = token_frac / top_idx.numel()
        aux_loss = self.routed_experts * torch.sum(mean_prob * token_frac)
        entropy = -(router_probs * torch.log(router_probs.clamp_min(1e-9))).sum(dim=-1).mean()
        return aux_loss, entropy

    def _forward_loop(self, x: torch.Tensor) -> MoEOutput:
        original_shape = x.shape
        flat = x.reshape(-1, x.shape[-1])
        router_probs, top_vals, top_idx = self._route(flat)

        out = self.shared.forward_expert(0, flat)
        for expert_idx in range(self.routed_experts):
            selected = top_idx == expert_idx
            if not torch.any(selected):
                continue
            rows, slots = torch.nonzero(selected, as_tuple=True)
            expert_out = self.routed.forward_expert(expert_idx, flat[rows])
            weighted = expert_out * top_vals[rows, slots].to(expert_out.dtype).unsqueeze(-1)
            out.index_add_(0, rows, weighted)

        aux_loss, entropy = self._router_stats(router_probs, top_idx)
        return MoEOutput(out.reshape(original_shape), aux_loss, entropy)

    def _forward_grouped_mm(self, x: torch.Tensor) -> MoEOutput:
        original_shape = x.shape
        flat = x.reshape(-1, x.shape[-1])
        router_probs, top_vals, top_idx = self._route(flat)
        expert_flat = flat if flat.dtype == torch.bfloat16 else flat.to(torch.bfloat16)

        num_tokens = expert_flat.shape[0]
        pair_experts = top_idx.reshape(-1)
        pair_rows = torch.arange(num_tokens, device=expert_flat.device).repeat_interleave(self.top_k)
        pair_weights = top_vals.reshape(-1)
        order = torch.argsort(pair_experts, stable=True)
        sorted_experts = pair_experts[order]
        sorted_rows = pair_rows[order]
        sorted_weights = pair_weights[order]
        counts = torch.bincount(sorted_experts, minlength=self.routed_experts).to(torch.int32)
        offsets = torch.cumsum(counts, dim=0, dtype=torch.int32)

        dispatched = expert_flat[sorted_rows]
        gate = torch._grouped_mm(dispatched, self.routed.w_gate, offs=offsets)
        up = torch._grouped_mm(dispatched, self.routed.w_up, offs=offsets)
        routed = torch._grouped_mm(F.silu(gate) * up, self.routed.w_down, offs=offsets)
        weighted = routed * sorted_weights.to(routed.dtype).unsqueeze(-1)

        out = self.shared.forward_expert(0, expert_flat)
        out.index_add_(0, sorted_rows, weighted)

        aux_loss, entropy = self._router_stats(router_probs, top_idx)
        return MoEOutput(out.reshape(original_shape), aux_loss, entropy)

    def forward(self, x: torch.Tensor) -> MoEOutput:
        backend = os.environ.get("ENGRAM_MOE_BACKEND", "loop").lower()
        if backend not in {"loop", "grouped", "auto"}:
            raise ValueError(f"unknown ENGRAM_MOE_BACKEND={backend!r}")
        use_grouped = backend == "grouped" or (
            backend == "auto" and x.is_cuda and x.dtype == torch.bfloat16 and hasattr(torch, "_grouped_mm")
        )
        if use_grouped:
            if not (x.is_cuda and hasattr(torch, "_grouped_mm")):
                raise RuntimeError("grouped MoE backend requires CUDA and torch._grouped_mm")
            return self._forward_grouped_mm(x)
        return self._forward_loop(x)


class TransformerBlock(nn.Module):
    def __init__(
        self,
        shape: ModelShape,
        routed_experts: int,
        engram_rows: int,
        use_engram: bool,
    ):
        super().__init__()
        self.attn_norm = RMSNorm(shape.d_model)
        self.attn = CausalSelfAttention(
            shape.d_model,
            shape.n_heads,
            rope_theta=shape.rope_theta,
            use_rope=shape.use_rope,
        )
        self.moe_norm = RMSNorm(shape.d_model)
        self.moe = MoELayer(
            d_model=shape.d_model,
            expert_hidden=shape.expert_hidden,
            routed_experts=routed_experts,
            top_k=shape.top_k,
            shared_experts=shape.shared_experts,
        )
        self.engram = (
            EngramRead(
                EngramReadConfig(
                    d_model=shape.d_model,
                    value_dim=shape.engram_dim,
                    num_rows=engram_rows,
                    orders=shape.engram_orders,
                    num_heads=shape.engram_heads,
                    conv_kernel=shape.engram_conv_kernel,
                )
            )
            if use_engram
            else None
        )

    def forward(self, x: torch.Tensor, token_ids: torch.Tensor, knockout: bool) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        x = x + self.attn(self.attn_norm(x))
        moe_out = self.moe(self.moe_norm(x))
        x = x + moe_out.hidden
        if self.engram is not None:
            x = self.engram(x, token_ids, knockout=knockout)
        return x, moe_out.aux_loss, moe_out.router_entropy


class EngramTransformerLM(nn.Module):
    def __init__(
        self,
        shape: ModelShape,
        routed_experts: int,
        engram_rows: int,
        engram_enabled: bool,
    ):
        super().__init__()
        self.shape = shape
        self.ce_chunk_tokens = int(os.environ.get("ENGRAM_CE_CHUNK_TOKENS", "256"))
        if self.ce_chunk_tokens <= 0:
            raise ValueError("ENGRAM_CE_CHUNK_TOKENS must be positive")
        self.token_embedding = nn.Embedding(shape.vocab_size, shape.d_model)
        self.blocks = nn.ModuleList()
        engram_layers = set(shape.engram_layers) if engram_enabled else set()
        for idx in range(shape.n_layers):
            self.blocks.append(
                TransformerBlock(
                    shape=shape,
                    routed_experts=routed_experts,
                    engram_rows=engram_rows,
                    use_engram=idx in engram_layers,
                )
            )
        self.final_norm = RMSNorm(shape.d_model)
        nn.init.normal_(self.token_embedding.weight, mean=0.0, std=0.02)

    def forward_hidden(
        self,
        input_ids: torch.Tensor,
        knockout: bool = False,
    ) -> tuple[torch.Tensor, torch.Tensor, dict[str, torch.Tensor]]:
        x = self.token_embedding(input_ids)
        aux_losses = []
        entropies = []
        for block in self.blocks:
            x, aux, entropy = block(x, input_ids, knockout=knockout)
            aux_losses.append(aux)
            entropies.append(entropy)
        x = self.final_norm(x)
        aux_loss = torch.stack(aux_losses).mean()
        stats = {"router_entropy": torch.stack(entropies).mean()}
        return x, aux_loss, stats

    def logits_for_hidden(self, hidden: torch.Tensor) -> torch.Tensor:
        return F.linear(hidden, self.token_embedding.weight)

    def chunked_cross_entropy(
        self,
        hidden: torch.Tensor,
        labels: torch.Tensor,
        chunk_tokens: int = 256,
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
            logits = self.logits_for_hidden(flat_h[start:end][valid])
            losses.append(F.cross_entropy(logits.float(), y[valid], reduction="sum"))
            counts.append(valid.sum())
        if not losses:
            return flat_h.sum() * 0.0
        return torch.stack(losses).sum() / torch.stack(counts).sum()

    def forward(
        self,
        input_ids: torch.Tensor,
        labels: torch.Tensor | None = None,
        knockout: bool = False,
    ) -> dict[str, torch.Tensor]:
        hidden, aux_loss, stats = self.forward_hidden(input_ids, knockout=knockout)
        out = {"hidden": hidden, "aux_loss": aux_loss, **stats}
        if labels is not None:
            out["loss"] = linear_cross_entropy(
                hidden,
                self.token_embedding.weight,
                labels,
                chunk_tokens=self.ce_chunk_tokens,
            )
        return out
