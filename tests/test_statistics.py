from depth_gap_gain.statistics import holm_adjust


def test_holm_is_deterministic_and_order_preserving():
    assert holm_adjust([0.01, 0.04, 0.03, 0.2]) == [0.04, 0.09, 0.09, 0.2]
