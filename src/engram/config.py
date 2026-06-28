from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


SEEDS = (1337, 2024, 7)


@dataclass(frozen=True)
class ModelShape:
    vocab_size: int = 128_000
    seq_len: int = 2048
    n_layers: int = 20
    d_model: int = 1280
    n_heads: int = 16
    expert_hidden: int = 640
    shared_experts: int = 1
    routed_experts_a: int = 88
    routed_experts_b: int = 68
    top_k: int = 6
    engram_layers: tuple[int, ...] = (2, 6)
    engram_orders: tuple[int, ...] = (2, 3)
    engram_heads: int = 8
    engram_dim: int = 256
    engram_conv_kernel: int = 4

    @property
    def head_dim(self) -> int:
        assert self.d_model % self.n_heads == 0
        return self.d_model // self.n_heads


@dataclass(frozen=True)
class TrainShape:
    precision: str = "bf16"
    optimizer: str = "adamw"
    adam_beta1: float = 0.9
    adam_beta2: float = 0.95
    weight_decay: float = 0.1
    peak_lr: float = 1.5e-3
    min_lr_ratio: float = 0.1
    warmup_frac: float = 0.02
    grad_clip: float = 1.0
    router_aux_loss_coef: float = 0.01
    micro_batch_size: int = 1
    grad_accum_steps_80gpu: int = 26
    target_tokens_per_run: int = 70_000_000_000
    checkpoint_minutes: int = 25
    val_interval_steps: int = 500

    @property
    def tokens_per_step_80gpu(self) -> int:
        return 80 * self.micro_batch_size * 2048 * self.grad_accum_steps_80gpu

    @property
    def max_steps_80gpu(self) -> int:
        return self.target_tokens_per_run // self.tokens_per_step_80gpu


def expert_params(shape: ModelShape) -> int:
    return 3 * shape.d_model * shape.expert_hidden


def attention_params_per_layer(shape: ModelShape) -> int:
    return 4 * shape.d_model * shape.d_model


def moe_params(shape: ModelShape, routed_experts: int) -> int:
    return (shape.shared_experts + routed_experts) * expert_params(shape) * shape.n_layers


def active_params(shape: ModelShape) -> int:
    return (
        attention_params_per_layer(shape) * shape.n_layers
        + (shape.shared_experts + shape.top_k) * expert_params(shape) * shape.n_layers
    )


def engram_overhead_per_site(shape: ModelShape) -> int:
    # Projection 256->d_model plus depthwise causal conv over d_model.
    proj = shape.engram_dim * shape.d_model + shape.d_model
    conv = shape.d_model * shape.engram_conv_kernel + shape.d_model
    return proj + conv


def exact_engram_rows(shape: ModelShape) -> int:
    freed = (
        (shape.routed_experts_a - shape.routed_experts_b)
        * expert_params(shape)
        * shape.n_layers
    )
    per_row = (
        len(shape.engram_layers)
        * len(shape.engram_orders)
        * shape.engram_heads
        * shape.engram_dim
    )
    overhead = len(shape.engram_layers) * engram_overhead_per_site(shape)
    return (freed - overhead) // per_row


def engram_params(shape: ModelShape, rows: int | None = None) -> int:
    if rows is None:
        rows = exact_engram_rows(shape)
    tables = (
        len(shape.engram_layers)
        * len(shape.engram_orders)
        * shape.engram_heads
        * rows
        * shape.engram_dim
    )
    return tables + len(shape.engram_layers) * engram_overhead_per_site(shape)


def non_embedding_params(shape: ModelShape, arm: str, rows: int | None = None) -> int:
    attn = attention_params_per_layer(shape) * shape.n_layers
    if arm == "A":
        return attn + moe_params(shape, shape.routed_experts_a)
    if arm == "B":
        return attn + moe_params(shape, shape.routed_experts_b) + engram_params(shape, rows)
    raise ValueError(f"unknown arm: {arm}")


def invariant_report(shape: ModelShape | None = None) -> dict[str, Any]:
    shape = shape or ModelShape()
    rows = exact_engram_rows(shape)
    a_non_embed = non_embedding_params(shape, "A", rows)
    b_non_embed = non_embedding_params(shape, "B", rows)
    freed = (
        (shape.routed_experts_a - shape.routed_experts_b)
        * expert_params(shape)
        * shape.n_layers
    )
    sparse_budget_a = moe_params(shape, shape.routed_experts_a)
    report = {
        "expert_params": expert_params(shape),
        "attention_params_per_layer": attention_params_per_layer(shape),
        "active_params": active_params(shape),
        "engram_rows_per_head_order_site": rows,
        "engram_params": engram_params(shape, rows),
        "freed_routed_expert_params": freed,
        "sparse_budget_to_engram_frac": engram_params(shape, rows) / sparse_budget_a,
        "arm_a_non_embedding_params": a_non_embed,
        "arm_b_non_embedding_params": b_non_embed,
        "iso_param_abs_delta": abs(a_non_embed - b_non_embed),
        "iso_active_param_abs_delta": 0,
        "tokens_per_step_80gpu": TrainShape().tokens_per_step_80gpu,
        "max_steps_70b_80gpu": TrainShape().max_steps_80gpu,
    }
    row_quantum = len(shape.engram_layers) * len(shape.engram_orders) * shape.engram_heads * shape.engram_dim
    assert report["iso_param_abs_delta"] <= row_quantum
    assert shape.top_k == 6
    assert shape.routed_experts_a == 88 and shape.routed_experts_b == 68
    assert 0.20 <= report["sparse_budget_to_engram_frac"] <= 0.25
    return report


def build_arm_config(
    arm: str,
    seed: int,
    shape: ModelShape | None = None,
    train: TrainShape | None = None,
) -> dict[str, Any]:
    shape = shape or ModelShape()
    train = train or TrainShape()
    rows = exact_engram_rows(shape)
    if arm not in {"A", "B"}:
        raise ValueError("arm must be A or B")
    routed = shape.routed_experts_a if arm == "A" else shape.routed_experts_b
    cfg = {
        "arm": arm,
        "seed": seed,
        "model": asdict(shape),
        "train": asdict(train),
        "derived": invariant_report(shape),
        "routed_experts": routed,
        "engram_enabled": arm == "B",
        "engram_rows": rows,
        "knockout_default": False,
        "notes": [
            "24h handoff plan: DDP full expert replication; no expert parallelism.",
            "Optimizer fixed to AdamW unless Muon is separately vetted before launch.",
            "Engram layers are zero-based module indices 2 and 6.",
        ],
    }
    cfg["train"]["max_steps"] = train.max_steps_80gpu
    cfg["train"]["tokens_per_step_80gpu"] = train.tokens_per_step_80gpu
    return cfg


def build_experiment_configs(seeds: tuple[int, ...] = SEEDS) -> dict[str, dict[str, Any]]:
    invariant_report(ModelShape())
    out: dict[str, dict[str, Any]] = {}
    for seed in seeds:
        for arm in ("A", "B"):
            out[f"{arm}_seed{seed}"] = build_arm_config(arm, seed)
    return out

