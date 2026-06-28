#!/usr/bin/env python
from __future__ import annotations

import argparse

from engram.data import LoaderConfig, hash_first_batches


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--token-files", nargs="+", required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--seq-len", type=int, default=2048)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--num-batches", type=int, default=100)
    args = parser.parse_args()
    cfg_a = LoaderConfig(tuple(args.token_files), args.seq_len, args.batch_size, args.seed)
    cfg_b = LoaderConfig(tuple(args.token_files), args.seq_len, args.batch_size, args.seed)
    ha = hash_first_batches(cfg_a, args.num_batches)
    hb = hash_first_batches(cfg_b, args.num_batches)
    print(f"A {ha}")
    print(f"B {hb}")
    if ha != hb:
        raise SystemExit("paired loader hash mismatch")


if __name__ == "__main__":
    main()

