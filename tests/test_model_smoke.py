import torch

from engram.config import ModelShape
from engram.model import EngramTransformerLM


def test_small_model_forward_backward_with_engram():
    torch.manual_seed(0)
    shape = ModelShape(
        vocab_size=128,
        seq_len=16,
        n_layers=3,
        d_model=32,
        n_heads=4,
        expert_hidden=16,
        routed_experts_a=4,
        routed_experts_b=3,
        top_k=2,
        engram_layers=(1,),
        engram_heads=2,
        engram_dim=8,
        engram_conv_kernel=3,
    )
    model = EngramTransformerLM(shape, routed_experts=3, engram_rows=23, engram_enabled=True)
    x = torch.randint(0, shape.vocab_size, (2, shape.seq_len))
    y = torch.randint(0, shape.vocab_size, (2, shape.seq_len))
    out = model(x, labels=y)
    assert out["loss"].isfinite()
    assert out["aux_loss"].isfinite()
    (out["loss"] + 0.01 * out["aux_loss"]).backward()
    grad_norm = sum(p.grad.abs().sum().item() for p in model.parameters() if p.grad is not None)
    assert grad_norm > 0


def test_small_model_knockout_changes_engram_arm_outputs():
    torch.manual_seed(0)
    shape = ModelShape(
        vocab_size=64,
        seq_len=8,
        n_layers=2,
        d_model=16,
        n_heads=4,
        expert_hidden=8,
        routed_experts_a=4,
        routed_experts_b=3,
        top_k=2,
        engram_layers=(1,),
        engram_heads=2,
        engram_dim=8,
    )
    model = EngramTransformerLM(shape, routed_experts=3, engram_rows=19, engram_enabled=True).eval()
    x = torch.randint(0, shape.vocab_size, (1, shape.seq_len))
    with torch.no_grad():
        normal = model(x, knockout=False)["hidden"]
        knocked = model(x, knockout=True)["hidden"]
    assert not torch.allclose(normal, knocked)

