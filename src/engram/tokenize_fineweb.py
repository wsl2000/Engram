from __future__ import annotations

import argparse
import json
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
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    eos_id = tokenizer.eos_token_id
    if eos_id is None:
        eos_id = tokenizer.convert_tokens_to_ids(tokenizer.eos_token or "<｜end▁of▁sentence｜>")
    ds = load_dataset(args.dataset, name=args.subset, split=args.split, streaming=True)

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

    def flush() -> None:
        nonlocal shard_idx, shard_tokens, shard_count
        if shard_count == 0:
            return
        path = out_dir / f"{args.split}_{shard_idx:05d}.bin"
        np.concatenate(shard_tokens).astype(np.uint32).tofile(path)
        manifest["shards"].append({"path": str(path), "tokens": shard_count})
        shard_idx += 1
        shard_tokens = []
        shard_count = 0
        (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    pbar = tqdm(total=args.max_tokens, unit="tok")
    for row in ds:
        text = row.get(args.text_field) or ""
        ids = tokenizer.encode(text, add_special_tokens=False)
        if eos_id is not None:
            ids.append(int(eos_id))
        arr = np.asarray(ids, dtype=np.uint32)
        shard_tokens.append(arr)
        shard_count += int(arr.shape[0])
        total += int(arr.shape[0])
        pbar.update(int(arr.shape[0]))
        if shard_count >= args.tokens_per_shard:
            flush()
        if args.max_tokens is not None and total >= args.max_tokens:
            break
    flush()
    manifest["total_tokens"] = total
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

