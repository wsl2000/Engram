import torch

from engram.engram_read import EngramRead, EngramReadConfig, ngram_hash_ids


def test_hash_shape_and_range():
    token_ids = torch.arange(12).view(2, 6)
    ids = ngram_hash_ids(token_ids, num_rows=101, num_heads=8, orders=(2, 3))
    assert ids.shape == (2, 6, 2, 8)
    assert int(ids.min()) >= 0
    assert int(ids.max()) < 101


def test_knockout_is_identity():
    cfg = EngramReadConfig(d_model=16, value_dim=8, num_rows=31, num_heads=2, orders=(2, 3))
    mod = EngramRead(cfg)
    hidden = torch.randn(2, 5, 16)
    token_ids = torch.randint(0, 100, (2, 5))
    out = mod(hidden, token_ids, knockout=True)
    assert torch.equal(out, hidden)


def test_no_future_token_leakage():
    torch.manual_seed(0)
    cfg = EngramReadConfig(d_model=16, value_dim=8, num_rows=127, num_heads=2, orders=(2, 3))
    mod = EngramRead(cfg).eval()
    hidden = torch.randn(1, 8, 16)
    token_ids = torch.randint(0, 1000, (1, 8))
    changed = token_ids.clone()
    changed[:, 6:] = changed[:, 6:] + 17
    with torch.no_grad():
        out_a = mod(hidden, token_ids)
        out_b = mod(hidden, changed)
    assert torch.allclose(out_a[:, :6], out_b[:, :6], atol=1e-6, rtol=0)

