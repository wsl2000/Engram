from __future__ import annotations

import argparse
import json

from .offline_data import tokenize_local_parquet


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Compatibility entrypoint for FineWeb-Edu tokenization. "
            "Handoff v3 forbids HF dataset streaming; this only tokenizes local parquet files."
        )
    )
    parser.add_argument("--parquet-glob", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--tokenizer", default="deepseek-ai/DeepSeek-V3")
    parser.add_argument("--tokens-per-shard", type=int, default=100_000_000)
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--text-field", "--text-column", dest="text_column", default="text")
    parser.add_argument("--id-column")
    parser.add_argument("--batch-docs", type=int, default=256)
    # Deprecated v1 streaming args kept only so old wrappers fail with a clear
    # local-parquet requirement rather than silently reopening streaming mode.
    parser.add_argument("--dataset", default="HuggingFaceFW/fineweb-edu")
    parser.add_argument("--subset", default="sample-350BT")
    parser.add_argument("--split", default="train")
    parser.add_argument("--num-workers", type=int, default=1)
    parser.add_argument("--worker-index", type=int, default=0)
    parser.add_argument("--skip-tokens", type=int, default=0)
    args = parser.parse_args()
    if args.skip_tokens:
        raise SystemExit("skip-tokens is deprecated; build doc-ID-disjoint parquet/token pools instead")
    summary = tokenize_local_parquet(
        parquet_glob=args.parquet_glob,
        output_dir=args.output_dir,
        tokenizer_name=args.tokenizer,
        text_column=args.text_column,
        id_column=args.id_column,
        tokens_per_shard=args.tokens_per_shard,
        max_tokens=args.max_tokens,
        batch_docs=args.batch_docs,
        num_workers=args.num_workers,
        worker_index=args.worker_index,
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
