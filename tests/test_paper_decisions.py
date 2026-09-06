"""Guard the frozen public paper-summary decisions without recomputing data."""

import json
from pathlib import Path

from depth_gap_gain import decide_depth


ROOT = Path(__file__).resolve().parents[1]


def test_four_paper_summary_decisions_are_unchanged():
    summary = json.loads((ROOT / "results/paper/dgg/development_dgg_summary.json").read_text())
    expected = {
        "khmer": "Full-28",
        "lao": "Late-16",
        "burmese": "Full-28",
        "finnish": "Full-28",
    }
    for language, expected_decision in expected.items():
        row = summary["languages"][language]
        q16 = {"Q16": row["q16"] == "PASS"}
        dgg = {"point": row["point"], "ci95": row["ci95"]}
        assert decide_depth(dgg, q16, probe_eligible=True) == expected_decision


def test_khmer_omniasr_summary_decision_is_full28():
    summary = json.loads((ROOT / "results/paper/dgg/development_dgg_summary.json").read_text())
    row = summary["languages"]["khmer_omniasr"]
    q16 = {"Q16": row["q16"] == "PASS"}
    dgg = {"point": row["point"], "ci95": row["ci95"]}
    assert decide_depth(dgg, q16, probe_eligible=True) == "Full-28"

