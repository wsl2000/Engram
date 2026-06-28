from pathlib import Path

from engram.data import LoaderConfig, hash_first_batches, write_synthetic_tokens


def test_paired_loader_hash_identical(tmp_path: Path):
    token_path = tmp_path / "tokens.bin"
    write_synthetic_tokens(token_path, num_tokens=20_000, seed=123)
    cfg = LoaderConfig((str(token_path),), seq_len=64, batch_size=4, seed=1337)
    assert hash_first_batches(cfg, num_batches=100) == hash_first_batches(cfg, num_batches=100)


def test_paired_loader_hash_changes_with_seed(tmp_path: Path):
    token_path = tmp_path / "tokens.bin"
    write_synthetic_tokens(token_path, num_tokens=20_000, seed=123)
    cfg_a = LoaderConfig((str(token_path),), seq_len=64, batch_size=4, seed=1337)
    cfg_b = LoaderConfig((str(token_path),), seq_len=64, batch_size=4, seed=2024)
    assert hash_first_batches(cfg_a, num_batches=20) != hash_first_batches(cfg_b, num_batches=20)

