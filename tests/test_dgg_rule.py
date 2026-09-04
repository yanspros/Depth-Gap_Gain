import json
from pathlib import Path

from depth_gap_gain import analyze_dgg


ROOT = Path(__file__).resolve().parents[1]


def run_case(name: str):
    return analyze_dgg(json.loads((ROOT / "examples/toy_dgg" / name).read_text()))


def test_positive_dgg_predicts_full28():
    assert run_case("full28_case.json")["decision"] == "Full-28"


def test_crossing_zero_with_q16_predicts_late16():
    result = run_case("late16_case.json")
    assert result["Q16"]["Q16"]
    assert result["DGG"]["ci95"][0] <= 0 <= result["DGG"]["ci95"][1]
    assert result["decision"] == "Late-16"


def test_negative_dgg_is_not_late16():
    result = run_case("no_prediction_case.json")
    assert result["DGG"]["point"] < 0
    assert result["decision"] == "No Prediction"
