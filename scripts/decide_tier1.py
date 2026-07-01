#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from engram.tier1 import tier1_decision


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--a-csv", required=True)
    parser.add_argument("--b-csv", required=True)
    parser.add_argument("--b-summary-json", required=True)
    parser.add_argument("--output-json", default="results/injected_facts_decision.json")
    args = parser.parse_args()
    decision = tier1_decision(args.a_csv, args.b_csv, args.b_summary_json)
    Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_json).write_text(json.dumps(decision, indent=2))
    print(json.dumps(decision, indent=2))


if __name__ == "__main__":
    main()
