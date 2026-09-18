#!/usr/bin/env python3
"""Render audited Table 3 aggregates, or replay its estimator on authorized trials.

The aggregate-only command does not replay private raw judgments. With --trials,
the pooled-components estimator is the authoritative ci_table4.py algorithm;
strict input checks precede estimation. No raw records or IDs are written.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SUMMARY = ROOT / "results/paper/human_eval_table3.json"
Z = 1.959963984540054
CRITERIA = ("pronunciation", "naturalness", "speaker_similarity")


def pooled_components(grids):
    """Authoritative pooled MoM calculation; truncate only after pooling."""
    import numpy as np
    excess_l, excess_i = [], []
    for grid in grids:
        n_listeners, n_items = grid.shape
        p = grid.mean()
        excess_l.append(grid.mean(axis=1).var(ddof=1) - p * (1 - p) / n_items)
        excess_i.append(grid.mean(axis=0).var(ddof=1) - p * (1 - p) / n_listeners)
    tau_l2 = float(np.mean(excess_l))
    tau_i2 = float(np.mean(excess_i))
    return (float(np.sqrt(tau_l2)) if tau_l2 > 0 else 0.0,
            float(np.sqrt(tau_i2)) if tau_i2 > 0 else 0.0)


def replay(trials: Path, expected: dict):
    import numpy as np
    import pandas as pd
    df = pd.read_csv(trials)
    keys = ["setting", "comparison", "criterion", "listener_id", "item_id"]
    required = set(keys + ["choice"])
    if required - set(df.columns):
        raise ValueError("Missing required trial columns")
    if len(df) != 19200 or df[keys].isna().any().any():
        raise ValueError("Expected 19,200 complete trial records")
    if df[keys].astype(str).apply(lambda col: col.str.strip().eq("")).any().any():
        raise ValueError("Empty key or ID")
    df["choice"] = pd.to_numeric(df["choice"], errors="raise")
    if not df["choice"].isin([0, 1]).all():
        raise ValueError("Preferences must be binary 0/1; no missing values or ties")
    if df.duplicated(keys).any():
        raise ValueError("Duplicate trial keys")
    df["choice"] = df["choice"].astype(int)
    wanted = {(s, v["comparison"], c) for s, v in expected.items() for c in CRITERIA}
    grouped = list(df.groupby(["setting", "comparison", "criterion"], sort=False))
    if {k for k, _ in grouped} != wanted:
        raise ValueError("Unexpected or missing comparison cells")
    grids, language_ids = [], {}
    for key, group in grouped:
        grid = group.pivot_table(index="listener_id", columns="item_id", values="choice", aggfunc="mean")
        values = grid.to_numpy(dtype=float)
        if len(group) != 800 or values.shape != (20, 40) or np.isnan(values).any():
            raise ValueError("Each cell must be a complete 20 x 40 panel")
        language = key[0].rsplit(" ", 1)[0]
        ids = (set(grid.index), set(grid.columns))
        if language in language_ids and language_ids[language] != ids:
            raise ValueError("Listener/item IDs differ across cells within a language")
        language_ids[language] = ids
        grids.append(values)
    tau_l, tau_i = pooled_components(grids)
    cells = {}
    for (setting, comparison, criterion), grid in zip((k for k, _ in grouped), grids):
        n_listeners, n_items = grid.shape
        n = int(grid.size)
        p = float(grid.sum() / n)
        var = p * (1 - p) / n + tau_l ** 2 / n_listeners + tau_i ** 2 / n_items
        half = Z * float(np.sqrt(var))
        lower, upper = max(p - half, 0.0) * 100.0, min(p + half, 1.0) * 100.0
        cells.setdefault(setting, {
            "comparison": comparison,
            "selected_allocation": "Full-28" if comparison.startswith("Full") else "Late-16",
            "n_listeners": n_listeners, "n_items": n_items, "n_judgments": n,
            "criteria": {},
        })["criteria"][criterion] = {"preference_percent": p * 100.0, "ci95": [lower, upper]}
    return cells, tau_l * 100.0, tau_i * 100.0


def compare(cells: dict, expected: dict):
    if set(cells) != set(expected):
        raise ValueError("Setting mismatch")
    matches = 0
    for setting, reference in expected.items():
        result = cells[setting]
        for key in ("comparison", "selected_allocation", "n_listeners", "n_items", "n_judgments"):
            if result[key] != reference[key]:
                raise ValueError("Protocol mismatch")
        if set(result["criteria"]) != set(CRITERIA):
            raise ValueError("Criterion mismatch")
        for criterion in CRITERIA:
            observed, target = result["criteria"][criterion], reference["criteria"][criterion]
            values = [observed["preference_percent"], *observed["ci95"]]
            wanted = [target["preference_percent"], *target["ci95"]]
            if not all(math.isclose(x, y, rel_tol=0, abs_tol=1e-10) and f"{x:.1f}" == f"{y:.1f}"
                       for x, y in zip(values, wanted)):
                raise ValueError(f"Table 3 mismatch: {setting}, {criterion}")
            matches += 1
    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--trials", type=Path, help="Authorized local raw CSV; never bundled or uploaded")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "artifacts/human_eval")
    args = parser.parse_args()
    release = json.loads(args.summary.read_text(encoding="utf-8"))
    expected = release["cells"]
    cells = expected
    if args.trials:
        cells, tau_l, tau_i = replay(args.trials, expected)
        for value, name in [(tau_l, "tau_listener_pp"), (tau_i, "tau_item_pp")]:
            if not math.isclose(value, release["estimator"][name], rel_tol=0, abs_tol=1e-10):
                raise ValueError("Pooled component mismatch")
    matches = compare(cells, expected)
    flat = [v for s in cells.values() for v in s["criteria"].values()]
    positive = sum(v["preference_percent"] > 50 for v in flat)
    excluded = sum(v["ci95"][0] > 50 or v["ci95"][1] < 50 for v in flat)
    if (matches, positive, excluded, len(flat) - excluded) != (24, 24, 18, 6):
        raise ValueError("Frozen summary mismatch")
    lines = ["# Table 3 - Human preference for DGG-selected allocation (%)", "",
             "| Setting | Pronunciation | Naturalness | Speaker similarity |",
             "|---|---|---|---|"]
    for setting in expected:
        values = []
        for criterion in CRITERIA:
            value = cells[setting]["criteria"][criterion]
            lo, hi = value["ci95"]
            values.append(f"{value['preference_percent']:.1f} [{lo:.1f}, {hi:.1f}]")
        lines.append("| " + " | ".join([setting, *values]) + " |")
    lines += ["", "Raw proportions; per-comparison 95% normal CIs with pooled listener/item variance components. Parity is 50%."]
    report = {"status": "HUMAN_EVAL_REPRO_AUDIT_PASS" if args.trials else "HUMAN_EVAL_AGGREGATE_CHECK_PASS",
              "raw_replayed": bool(args.trials), "point_matches": matches,
              "lower_bound_matches": matches, "upper_bound_matches": matches,
              "point_estimates_above_50": positive, "ci_excludes_50": excluded,
              "ci_includes_50": len(flat) - excluded}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "table3.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (args.output_dir / "replayed_cells.json").write_text(json.dumps(cells, indent=2) + "\n", encoding="utf-8")
    (args.output_dir / "check.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
