from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
from datasets import load_dataset
from tqdm import tqdm
from transformers import AutoTokenizer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--tokenizer", default="deepseek-ai/DeepSeek-V3")
    parser.add_argument("--dataset", default="HuggingFaceFW/fineweb-edu")
    parser.add_argument("--subset", default="sample-350BT")
    parser.add_argument("--split", default="train")
    parser.add_argument("--tokens-per-shard", type=int, default=1_000_000_000)
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--text-field", default="text")
    parser.add_argument("--batch-docs", type=int, default=256)
    parser.add_argument("--num-workers", type=int, default=1)
    parser.add_argument("--worker-index", type=int, default=0)
    parser.add_argument("--load-retries", type=int, default=6)
    parser.add_argument("--retry-sleep", type=float, default=20.0)
    args = parser.parse_args()
    if not 0 <= args.worker_index < args.num_workers:
        raise ValueError("worker-index must be in [0, num-workers)")

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    eos_id = tokenizer.eos_token_id
    if eos_id is None:
        eos_id = tokenizer.convert_tokens_to_ids(tokenizer.eos_token or "<｜end▁of▁sentence｜>")
    last_load_error: BaseException | None = None
    for attempt in range(args.load_retries + 1):
        try:
            ds = load_dataset(args.dataset, name=args.subset, split=args.split, streaming=True)
            break
        except BaseException as exc:
            last_load_error = exc
            if attempt >= args.load_retries:
                raise
            sleep_s = args.retry_sleep * (2**attempt)
            print(
                f"load_dataset failed on attempt {attempt + 1}/{args.load_retries + 1}: {exc!r}; "
                f"sleeping {sleep_s:.1f}s",
                file=sys.stderr,
                flush=True,
            )
            time.sleep(sleep_s)
    else:
        raise RuntimeError("unreachable load_dataset retry state") from last_load_error
    if args.num_workers > 1:
        ds = ds.shard(num_shards=args.num_workers, index=args.worker_index)

    shard_idx = 0
    shard_tokens: list[np.ndarray] = []
    shard_count = 0
    total = 0
    manifest = {
        "tokenizer": args.tokenizer,
        "dataset": args.dataset,
        "subset": args.subset,
        "split": args.split,
        "dtype": "uint32",
        "shards": [],
    }
    manifest_path = out_dir / f"manifest_w{args.worker_index:03d}.json"

    def flush() -> None:
        nonlocal shard_idx, shard_tokens, shard_count
        if shard_count == 0:
            return
        path = out_dir / f"{args.split}_w{args.worker_index:03d}_{shard_idx:05d}.bin"
        np.concatenate(shard_tokens).astype(np.uint32).tofile(path)
        manifest["shards"].append({"path": str(path), "tokens": shard_count})
        shard_idx += 1
        shard_tokens = []
        shard_count = 0
        manifest_path.write_text(json.dumps(manifest, indent=2))

    manifest["num_workers"] = args.num_workers
    manifest["worker_index"] = args.worker_index
    manifest["batch_docs"] = args.batch_docs

    def encode_texts(texts: list[str]) -> None:
        nonlocal shard_count, total
        encoded = tokenizer(texts, add_special_tokens=False)["input_ids"]
        for ids in encoded:
            if eos_id is not None:
                ids.append(int(eos_id))
            arr = np.asarray(ids, dtype=np.uint32)
            shard_tokens.append(arr)
            shard_count += int(arr.shape[0])
            total += int(arr.shape[0])
            pbar.update(int(arr.shape[0]))
            if shard_count >= args.tokens_per_shard:
                flush()

    pbar = tqdm(total=args.max_tokens, unit="tok", disable=not sys.stderr.isatty())
    batch: list[str] = []
    try:
        for row in ds:
            batch.append(row.get(args.text_field) or "")
            if len(batch) >= args.batch_docs:
                encode_texts(batch)
                batch = []
            if args.max_tokens is not None and total >= args.max_tokens:
                break
        if batch and (args.max_tokens is None or total < args.max_tokens):
            encode_texts(batch)
    except BaseException as exc:
        manifest["error"] = repr(exc)
        raise
    finally:
        flush()
        manifest["total_tokens"] = total
        manifest_path.write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
