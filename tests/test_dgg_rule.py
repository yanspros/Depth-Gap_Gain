import json
from pathlib import Path

from depth_gap_gain import analyze_dgg, decide_depth


ROOT = Path(__file__).resolve().parents[1]


def run_case(name: str):
    return analyze_dgg(json.loads((ROOT / "examples/toy_dgg" / name).read_text()))


def test_positive_dgg_predicts_full28():
    result = run_case("full28_case.json")
    assert result["probe_eligibility"]["passed"] is True
    assert result["decision"] == "Full-28"


def test_crossing_zero_with_q16_predicts_late16():
    result = run_case("late16_case.json")
    assert result["Q16"]["Q16"]
    assert result["DGG"]["ci95"][0] <= 0 <= result["DGG"]["ci95"][1]
    assert result["decision"] == "Late-16"


def test_negative_point_with_zero_crossing_ci_and_q16_predicts_late16():
    dgg = {"point": -0.10, "ci95": [-0.30, 0.10]}
    assert decide_depth(dgg, {"Q16": True}, probe_eligible=True) == "Late-16"


def test_positive_point_with_zero_crossing_ci_and_q16_predicts_late16():
    dgg = {"point": 0.10, "ci95": [-0.10, 0.30]}
    assert decide_depth(dgg, {"Q16": True}, probe_eligible=True) == "Late-16"


def test_ci_touching_zero_is_late16_not_full28_when_q16_passes():
    dgg = {"point": 0.10, "ci95": [0.0, 0.30]}
    assert decide_depth(dgg, {"Q16": True}, probe_eligible=True) == "Late-16"


def test_wholly_negative_dgg_ci_is_not_late16():
    result = run_case("no_prediction_case.json")
    assert result["DGG"]["point"] < 0
    assert result["DGG"]["ci95"][1] < 0
    assert result["decision"] == "No Prediction"


def test_q16_failure_returns_no_prediction_when_dgg_crosses_zero():
    dgg = {"point": 0.0, "ci95": [-0.10, 0.10]}
    assert decide_depth(dgg, {"Q16": False}, probe_eligible=True) == "No Prediction"


def test_probe_ineligible_blocks_a_strongly_positive_dgg():
    payload = json.loads((ROOT / "examples/toy_dgg/full28_case.json").read_text())
    for base, full_sft in zip(payload["conditions"]["base"], payload["conditions"]["full_sft"], strict=True):
        full_sft["edit_distance"] = base["edit_distance"]
    result = analyze_dgg(payload)
    assert result["DGG"]["ci95"][0] > 0
    assert result["probe_eligibility"] == {
        "passed": False,
        "reason": "Full-SFT gain lower bound <= 0",
    }
    assert result["decision"] == "No Prediction"


def test_ineligible_probe_with_positive_dgg_predicts_no_prediction():
    """Regression test 1: ineligible probe + positive DGG -> No Prediction."""
    dgg = {"point": 0.15, "ci95": [0.05, 0.25]}
    assert decide_depth(dgg, {"Q16": True}, probe_eligible=False) == "No Prediction"
    assert decide_depth(dgg, {"Q16": False}, probe_eligible=False) == "No Prediction"


def test_negative_dgg_point_ci_crosses_zero_q16_true_predicts_late16():
    """Regression test 2: negative DGG point + CI crosses 0 + Q16=1 -> Late-16."""
    dgg = {"point": -0.08, "ci95": [-0.20, 0.05]}
    assert decide_depth(dgg, {"Q16": True}, probe_eligible=True) == "Late-16"


def test_positive_ci_dgg_predicts_full28_even_when_q16_is_zero():
    """Regression test 3: positive-CI DGG + Q16=0 -> Full-28."""
    dgg = {"point": 0.12, "ci95": [0.03, 0.22]}
    assert decide_depth(dgg, {"Q16": False}, probe_eligible=True) == "Full-28"


def test_fully_negative_dgg_interval_predicts_no_prediction():
    """Regression test 4: fully negative DGG interval -> No Prediction."""
    dgg = {"point": -0.15, "ci95": [-0.25, -0.05]}
    assert decide_depth(dgg, {"Q16": True}, probe_eligible=True) == "No Prediction"
    assert decide_depth(dgg, {"Q16": False}, probe_eligible=True) == "No Prediction"

