import json

import numpy as np
import torch

from engram.losses import linear_cross_entropy
from engram.offline_data import assert_data_gate
from engram.ops import latest_checkpoint, rotate_checkpoints


def test_data_gate_requires_tokens_and_doc_manifest(tmp_path):
    shard = tmp_path / "x.u32"
    np.arange(10, dtype=np.uint32).tofile(shard)
    (tmp_path / "summary.json").write_text(json.dumps({"token_count": 10, "doc_count": 1}))
    (tmp_path / "shards.csv").write_text(f"path,token_count,first_doc_id,last_doc_id\n{shard},10,a,a\n")
    (tmp_path / "docs.jsonl").write_text("{}\n")
    assert assert_data_gate(tmp_path, min_tokens=10)["gate_passed"] is True


def test_checkpoint_rotation_keeps_latest(tmp_path):
    for step in [1, 2, 3]:
        (tmp_path / f"ckpt_step{step:06d}.pt").write_text("x")
    removed = rotate_checkpoints(tmp_path, keep_last=1)
    assert len(removed) == 2
    assert latest_checkpoint(tmp_path).name == "ckpt_step000003.pt"


def test_linear_cross_entropy_fallback_backward():
    hidden = torch.randn(2, 3, 8, requires_grad=True)
    weight = torch.randn(11, 8, requires_grad=True)
    labels = torch.randint(0, 11, (2, 3))
    loss = linear_cross_entropy(hidden, weight, labels, chunk_tokens=2, implementation="chunked")
    assert loss.isfinite()
    loss.backward()
    assert hidden.grad is not None
    assert weight.grad is not None


def test_memory_efficient_linear_cross_entropy_matches_chunked():
    torch.manual_seed(0)
    hidden_a = torch.randn(2, 4, 6, requires_grad=True)
    hidden_b = hidden_a.detach().clone().requires_grad_(True)
    weight_a = torch.randn(9, 6, requires_grad=True)
    weight_b = weight_a.detach().clone().requires_grad_(True)
    labels = torch.randint(0, 9, (2, 4))
    labels[0, 0] = -100
    loss_a = linear_cross_entropy(hidden_a, weight_a, labels, chunk_tokens=3, implementation="chunked")
    loss_b = linear_cross_entropy(hidden_b, weight_b, labels, chunk_tokens=3, implementation="memory_efficient")
    assert torch.allclose(loss_a, loss_b, atol=1e-6, rtol=1e-6)
    loss_a.backward()
    loss_b.backward()
    assert torch.allclose(hidden_a.grad, hidden_b.grad, atol=1e-5, rtol=1e-5)
    assert torch.allclose(weight_a.grad, weight_b.grad, atol=1e-5, rtol=1e-5)
