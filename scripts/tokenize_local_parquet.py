#!/usr/bin/env python
from __future__ import annotations

import argparse
import json

from engram.offline_data import tokenize_local_parquet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--parquet-glob", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--tokenizer", default="deepseek-ai/DeepSeek-V3")
    parser.add_argument("--text-column", default="text")
    parser.add_argument("--id-column")
    parser.add_argument("--tokens-per-shard", type=int, default=100_000_000)
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--batch-docs", type=int, default=256)
    args = parser.parse_args()
    summary = tokenize_local_parquet(
        parquet_glob=args.parquet_glob,
        output_dir=args.output_dir,
        tokenizer_name=args.tokenizer,
        text_column=args.text_column,
        id_column=args.id_column,
        tokens_per_shard=args.tokens_per_shard,
        max_tokens=args.max_tokens,
        batch_docs=args.batch_docs,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
