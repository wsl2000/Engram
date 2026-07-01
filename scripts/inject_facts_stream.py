#!/usr/bin/env python
from __future__ import annotations

import argparse
import json

from engram.injected_facts import make_examples, read_facts, write_injected_stream


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--facts-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--repeats", type=int, required=True)
    parser.add_argument("--eos-id", type=int, required=True)
    parser.add_argument("--split", default="train")
    parser.add_argument("--tokens-per-shard", type=int, default=100_000_000)
    args = parser.parse_args()
    facts = read_facts(args.facts_csv)
    examples = make_examples(facts, repeats=args.repeats, eos_id=args.eos_id, split=args.split)
    summary = write_injected_stream(examples, args.output_dir, tokens_per_shard=args.tokens_per_shard)
    summary.update({"facts_csv": args.facts_csv, "repeats": args.repeats, "split": args.split})
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
