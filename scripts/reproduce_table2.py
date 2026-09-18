#!/usr/bin/env python3
"""Copy curated cross-PEFT Table 2 data and declare human evidence status."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("results/paper/dgg/table2_selector_cross_peft.csv"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/table2.csv"))
    parser.add_argument("--status-output", type=Path, default=Path("artifacts/table2_human_evidence_status.json"))
    args = parser.parse_args()
    with args.input.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("paper Table 2 asset is empty")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    args.status_output.parent.mkdir(parents=True, exist_ok=True)
    status_source = Path(__file__).resolve().parents[1] / "results/paper/dgg/human_evidence_status.json"
    status = json.loads(status_source.read_text(encoding="utf-8"))
    args.status_output.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
