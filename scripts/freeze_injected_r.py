#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from engram.injected_facts import choose_freeze_r


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sweep-csv", required=True, help="CSV with columns R,a_recall")
    parser.add_argument("--max-a-recall", type=float, default=0.10)
    parser.add_argument("--output-json", default="results/injected_facts_freeze_r.json")
    args = parser.parse_args()
    values: dict[int, float] = {}
    with open(args.sweep_csv, newline="") as f:
        for row in csv.DictReader(f):
            values[int(row["R"])] = float(row["a_recall"])
    frozen = choose_freeze_r(values, max_recall=args.max_a_recall)
    out = {
        "sweep_csv": args.sweep_csv,
        "max_a_recall": args.max_a_recall,
        "frozen_R": frozen,
        "a_recall_at_frozen_R": values[frozen],
        "note": "R is frozen from A-only difficulty; do not retune toward B pass.",
    }
    Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_json).write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
