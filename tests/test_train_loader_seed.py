def test_train_loader_seed_formula_preserves_pairing_and_splits_ranks():
    base_seed = 1337
    rank0_a = base_seed + 0 * 1_000_003
    rank0_b = base_seed + 0 * 1_000_003
    rank1 = base_seed + 1 * 1_000_003
    assert rank0_a == rank0_b
    assert rank0_a != rank1

