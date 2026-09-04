#!/usr/bin/env python3
"""Run frozen DGG/Q16 logic on target-level edit-count records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from depth_gap_gain import analyze_dgg


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="JSON payload with Base, Full-SFT, S16, and A28 target records")
    parser.add_argument("--output", type=Path, help="Optional JSON destination; directories are created when needed")
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = analyze_dgg(payload)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
