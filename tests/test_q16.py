import json
from pathlib import Path

from depth_gap_gain import analyze_dgg


def test_loo_does_not_recompute_bootstrap():
    root = Path(__file__).resolve().parents[1]
    result = analyze_dgg(json.loads((root / "examples/toy_dgg/late16_case.json").read_text()))
    assert result["Q16"]["leave_one_target_out"]["bootstrap_recomputed"] is False
    assert result["Q16"]["leave_one_target_out"]["all_positive_s16_gain"] is True


def test_r16_can_be_outside_unit_interval():
    # The implementation deliberately does not clamp a mathematical ratio.
    root = Path(__file__).resolve().parents[1]
    payload = json.loads((root / "examples/toy_dgg/late16_case.json").read_text())
    for row in payload["conditions"]["s16"]:
        row["edit_distance"] = 10
    result = analyze_dgg(payload)
    assert result["Q16"]["R16"] > 1
