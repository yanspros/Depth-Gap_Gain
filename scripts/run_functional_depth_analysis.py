#!/usr/bin/env python3
"""Render a descriptive functional-depth landscape from public summary JSON."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("results/paper/functional_depth/functional_depth_summary.json"))
    parser.add_argument("--output", type=Path, default=Path("artifacts/functional_depth.csv"))
    args = parser.parse_args()
    value = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["language", "configuration", "cer", "delta_vs_a28", "ci95_lower", "ci95_upper"])
        writer.writeheader()
        for language, item in sorted(value["languages"].items()):
            for configuration in ("S12", "S16", "S20", "S24", "A28"):
                effect = item["delta_vs_a28"].get(configuration, {"point": 0.0, "ci95": [0.0, 0.0]})
                writer.writerow({
                    "language": language,
                    "configuration": configuration,
                    "cer": item["cer"][configuration],
                    "delta_vs_a28": effect["point"],
                    "ci95_lower": effect["ci95"][0],
                    "ci95_upper": effect["ci95"][1],
                })
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
