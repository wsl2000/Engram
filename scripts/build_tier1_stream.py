#!/usr/bin/env python
from __future__ import annotations

import argparse
import json

from engram.injected_facts import read_facts
from engram.tier1 import build_tier1_stream_from_facts, read_token_file_list


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--facts-csv", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--repeats", type=int, required=True)
    parser.add_argument("--eos-id", type=int, required=True)
    parser.add_argument("--base-token-files", nargs="*")
    parser.add_argument("--base-token-list")
    parser.add_argument("--base-chunk-tokens", type=int, default=2048)
    parser.add_argument("--auto-base-chunk", action="store_true")
    parser.add_argument("--tokens-per-shard", type=int, default=100_000_000)
    parser.add_argument("--target-tokens", type=int)
    parser.add_argument("--split", default="train")
    args = parser.parse_args()
    base_files = read_token_file_list(args.base_token_files, args.base_token_list)
    base_chunk_tokens = args.base_chunk_tokens
    if args.auto_base_chunk:
        if args.target_tokens is None:
            raise SystemExit("--auto-base-chunk requires --target-tokens")
        fact_count = len(read_facts(args.facts_csv))
        base_chunk_tokens = max(1, args.target_tokens // max(1, fact_count * args.repeats) - 8)
    summary = build_tier1_stream_from_facts(
        facts_csv=args.facts_csv,
        repeats=args.repeats,
        eos_id=args.eos_id,
        output_dir=args.output_dir,
        base_token_files=base_files,
        base_chunk_tokens=base_chunk_tokens,
        tokens_per_shard=args.tokens_per_shard,
        target_tokens=args.target_tokens,
        split=args.split,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
