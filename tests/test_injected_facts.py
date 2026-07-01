from engram.injected_facts import (
    assert_key_identity,
    choose_freeze_r,
    make_examples,
    paired_stats,
    smoke_factset,
    write_injected_stream,
)


def test_rung0_smoke_fact_stream_and_identity(tmp_path):
    facts, eos = smoke_factset(8)
    train = make_examples(facts, repeats=2, eos_id=eos, split="train")
    evals = make_examples(facts, repeats=1, eos_id=eos, split="eval")
    assert_key_identity(train, evals)
    summary = write_injected_stream(train, tmp_path, tokens_per_shard=16)
    assert summary["doc_count"] == 16
    assert summary["token_count"] > 0
    assert (tmp_path / "docs.jsonl").exists()
    assert (tmp_path / "shards.csv").exists()


def test_freeze_r_uses_a_only_threshold():
    assert choose_freeze_r({1: 0.5, 2: 0.09, 3: 0.01}) == 2


def test_paired_stats_mcnemar_collapse():
    rows = [
        {"normal_nll": 1.0, "knockout_nll": 2.0, "normal_em": 1, "knockout_em": 0},
        {"normal_nll": 1.5, "knockout_nll": 3.0, "normal_em": 1, "knockout_em": 0},
    ]
    stats = paired_stats(rows)
    assert stats["mean_delta_knockout_minus_normal"] > 0
    assert stats["normal_em"] == 1.0
    assert stats["knockout_em"] == 0.0
    assert stats["mcnemar_b_normal_only"] == 2
