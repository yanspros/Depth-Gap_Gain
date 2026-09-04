#!/usr/bin/env python3
"""Render the public development-only suffix-restoration Figure 2 asset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("results/paper/figures/figure2_suffix_restoration_profiles.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    args = parser.parse_args()
    import matplotlib.pyplot as plt

    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    figure, axes = plt.subplots(1, 2, figsize=(6.8, 2.25), constrained_layout=True)
    for axis, language in zip(axes, ("Burmese", "Lao"), strict=True):
        rows = data["languages"][language]
        x = list(range(len(rows)))
        y = [row["difference_pp"] for row in rows]
        lower = [row["difference_pp"] - row["ci95_pp"][0] for row in rows]
        upper = [row["ci95_pp"][1] - row["difference_pp"] for row in rows]
        axis.axhline(0, color="0.65", linewidth=0.75, linestyle="--", zorder=0)
        axis.plot(x, y, color="0.18", linewidth=0.9, zorder=1)
        for index, row in enumerate(rows):
            marker = "s" if row["configuration"] == "A28" else "o"
            axis.errorbar(index, y[index], yerr=[[lower[index]], [upper[index]]], fmt=marker, color="0.12", markersize=4.2, capsize=2.2, linewidth=0.85, zorder=2)
        axis.set_title(f"({chr(97 + (language == 'Lao'))}) {language}", fontsize=8.5, pad=3)
        axis.set_xticks(x, [row["configuration"] for row in rows], fontsize=8)
        axis.grid(axis="y", color="0.90", linewidth=0.55)
        axis.spines[["top", "right"]].set_visible(False)
        axis.tick_params(axis="y", labelsize=7.5)
    figure.supxlabel("Restoration configuration", fontsize=8.5)
    figure.supylabel("CER difference vs. A28 (pp)", fontsize=8.5)
    for suffix in ("pdf", "png", "svg"):
        figure.savefig(args.output_dir / f"fig2.{suffix}", dpi=300 if suffix == "png" else None, bbox_inches="tight")
    print(args.output_dir / "fig2.pdf")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
