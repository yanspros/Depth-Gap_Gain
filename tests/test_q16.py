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


def test_near_zero_full_sft_denominator_fails_closed_without_nan_minimum():
    root = Path(__file__).resolve().parents[1]
    payload = json.loads((root / "examples/toy_dgg/late16_case.json").read_text())
    for base, full_sft in zip(payload["conditions"]["base"], payload["conditions"]["full_sft"], strict=True):
        full_sft["edit_distance"] = base["edit_distance"]
    result = analyze_dgg(payload)
    assert result["Q16"]["R16"] is None
    assert result["Q16"]["Q16"] is False
    assert result["Q16"]["leave_one_target_out"]["minimum_R16"] is None
    assert result["probe_eligibility"]["passed"] is False
    assert result["decision"] == "No Prediction"
