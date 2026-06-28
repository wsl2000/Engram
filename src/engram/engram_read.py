from __future__ import annotations

import math
from dataclasses import dataclass

import torch
from torch import nn
from torch.nn import functional as F


DEFAULT_SALTS = (
    0x9E3779B1,
    0x85EBCA77,
    0xC2B2AE3D,
    0x27D4EB2F,
    0x165667B1,
    0xD3A2646C,
    0xFD7046C5,
    0xB55A4F09,
)

DEFAULT_COEFFS = (
    1_000_003,
    1_000_033,
    1_000_087,
    1_000_109,
    1_000_133,
    1_000_151,
    1_000_181,
    1_000_207,
)


def _left_shift_with_zero(token_ids: torch.Tensor, offset: int) -> torch.Tensor:
    if offset == 0:
        return token_ids
    out = torch.zeros_like(token_ids)
    out[:, offset:] = token_ids[:, :-offset]
    return out


def ngram_hash_ids(
    token_ids: torch.Tensor,
    num_rows: int,
    num_heads: int = 8,
    orders: tuple[int, ...] = (2, 3),
    salts: tuple[int, ...] = DEFAULT_SALTS,
) -> torch.Tensor:
    """Vectorized causal multiplicative-XOR suffix hashes.

    Returns int64 ids with shape [batch, seq, len(orders), num_heads].
    The suffix for position t uses only tokens <= t.
    """
    if token_ids.ndim != 2:
        raise ValueError("token_ids must have shape [batch, seq]")
    if num_heads > len(salts):
        raise ValueError("provide at least num_heads salts")
    device = token_ids.device
    x = token_ids.to(torch.int64) + 1
    salts_t = torch.tensor(salts[:num_heads], dtype=torch.int64, device=device).view(1, 1, num_heads)
    coeffs_t = torch.tensor(DEFAULT_COEFFS[:num_heads], dtype=torch.int64, device=device).view(1, 1, num_heads)
    all_orders = []
    for order in orders:
        h = salts_t.expand(x.shape[0], x.shape[1], num_heads).clone()
        for pos in range(order):
            offset = order - 1 - pos
            tok = _left_shift_with_zero(x, offset).unsqueeze(-1)
            mixed = (tok * (coeffs_t + 97 * pos) + salts_t * (pos + 1)) % 2_147_483_647
            h = torch.bitwise_xor(h, mixed)
        all_orders.append(torch.remainder(h, num_rows))
    return torch.stack(all_orders, dim=2).to(torch.long)


def rms_norm_no_weight(x: torch.Tensor, eps: float = 1e-6) -> torch.Tensor:
    return x * torch.rsqrt(x.pow(2).mean(dim=-1, keepdim=True) + eps)


@dataclass(frozen=True)
class EngramReadConfig:
    d_model: int = 1280
    value_dim: int = 256
    num_rows: int = 119_918
    orders: tuple[int, ...] = (2, 3)
    num_heads: int = 8
    conv_kernel: int = 4


class EngramRead(nn.Module):
    """Flat conditional N-gram memory read with eval-time knockout."""

    def __init__(self, cfg: EngramReadConfig):
        super().__init__()
        self.cfg = cfg
        self.tables = nn.ModuleList(
            [
                nn.Embedding(cfg.num_rows, cfg.value_dim)
                for _ in range(len(cfg.orders) * cfg.num_heads)
            ]
        )
        self.proj = nn.Linear(cfg.value_dim, cfg.d_model)
        self.conv = nn.Conv1d(
            cfg.d_model,
            cfg.d_model,
            kernel_size=cfg.conv_kernel,
            groups=cfg.d_model,
        )
        self.reset_parameters()

    def reset_parameters(self) -> None:
        for table in self.tables:
            nn.init.normal_(table.weight, mean=0.0, std=0.02)
        nn.init.normal_(self.proj.weight, mean=0.0, std=0.02)
        nn.init.zeros_(self.proj.bias)
        nn.init.normal_(self.conv.weight, mean=0.0, std=0.02)
        nn.init.zeros_(self.conv.bias)

    def table_index(self, order_idx: int, head_idx: int) -> int:
        return order_idx * self.cfg.num_heads + head_idx

    def lookup(self, token_ids: torch.Tensor) -> torch.Tensor:
        ids = ngram_hash_ids(
            token_ids,
            num_rows=self.cfg.num_rows,
            num_heads=self.cfg.num_heads,
            orders=self.cfg.orders,
        )
        order_values = []
        for order_idx in range(len(self.cfg.orders)):
            head_values = []
            for head_idx in range(self.cfg.num_heads):
                table = self.tables[self.table_index(order_idx, head_idx)]
                head_values.append(table(ids[:, :, order_idx, head_idx]))
            order_values.append(torch.stack(head_values, dim=0).mean(dim=0))
        return torch.stack(order_values, dim=0).sum(dim=0)

    def forward(
        self,
        hidden: torch.Tensor,
        token_ids: torch.Tensor,
        knockout: bool = False,
    ) -> torch.Tensor:
        if knockout:
            return hidden
        raw = self.lookup(token_ids)
        mem = self.proj(raw)
        conv_in = mem.transpose(1, 2)
        conv_in = F.pad(conv_in, (self.cfg.conv_kernel - 1, 0))
        mem = F.silu(self.conv(conv_in).transpose(1, 2))
        alpha = torch.sigmoid(
            (rms_norm_no_weight(hidden) * rms_norm_no_weight(mem)).sum(dim=-1, keepdim=True)
            / math.sqrt(hidden.shape[-1])
        )
        return hidden + alpha * mem

