from engram.train import resolve_max_steps


def test_resolve_max_steps_keeps_zero_override():
    assert resolve_max_steps(0, 123) == 0
    assert resolve_max_steps(None, 123) == 123

