import torch
import pytest

from engram.config import ModelShape
from engram.model import EngramTransformerLM, MoELayer


@pytest.mark.skipif(not torch.cuda.is_available(), reason="requires CUDA grouped-mm kernel")
def test_grouped_mm_moe_matches_loop_forward_backward():
    torch.manual_seed(0)
    moe = MoELayer(d_model=32, expert_hidden=16, routed_experts=5, top_k=2).cuda().to(torch.bfloat16)
    x_loop = torch.randn(2, 9, 32, device="cuda", dtype=torch.bfloat16, requires_grad=True)
    x_grouped = x_loop.detach().clone().requires_grad_(True)

    with torch.autocast("cuda", dtype=torch.bfloat16):
        loop = moe._forward_loop(x_loop)
        grouped = moe._forward_grouped_mm(x_grouped)

    assert torch.allclose(loop.hidden.float(), grouped.hidden.float(), atol=5e-2, rtol=5e-2)
    assert torch.allclose(loop.aux_loss.float(), grouped.aux_loss.float(), atol=1e-6, rtol=1e-6)
    assert torch.allclose(loop.router_entropy.float(), grouped.router_entropy.float(), atol=1e-6, rtol=1e-6)

    loop_loss = loop.hidden.float().square().mean() + loop.aux_loss + loop.router_entropy
    grouped_loss = grouped.hidden.float().square().mean() + grouped.aux_loss + grouped.router_entropy
    loop_loss.backward()
    grouped_loss.backward()
    assert torch.allclose(x_loop.grad.float(), x_grouped.grad.float(), atol=5e-2, rtol=5e-2)


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
