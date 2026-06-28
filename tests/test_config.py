from engram.config import ModelShape, exact_engram_rows, invariant_report


def test_invariants_match_handoff_budget():
    report = invariant_report(ModelShape())
    assert report["engram_rows_per_head_order_site"] == exact_engram_rows(ModelShape())
    assert report["iso_param_abs_delta"] <= 8192
    assert report["active_params"] == 475_136_000
    assert 0.22 <= report["sparse_budget_to_engram_frac"] <= 0.23

