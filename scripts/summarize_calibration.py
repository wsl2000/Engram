#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-log", required=True)
    parser.add_argument("--output-csv", default="progress/results/calibration.csv")
    parser.add_argument("--label", required=True)
    parser.add_argument("--tail", type=int, default=100)
    args = parser.parse_args()
    rows = []
    with open(args.train_log) as f:
        for line in f:
            if line.startswith("{"):
                rows.append(json.loads(line))
    if not rows:
        raise SystemExit(f"no JSON rows in {args.train_log}")
    tail = rows[-args.tail :]
    summary = {
        "label": args.label,
        "steps": len(rows),
        "last_step": rows[-1]["step"],
        "last_tokens": rows[-1]["tokens_seen"],
        "mean_tail_tokens_per_s": sum(float(r["tokens_per_s"]) for r in tail) / len(tail),
        "mean_tail_mfu": sum(float(r["mfu"]) for r in tail) / len(tail),
        "world_size": rows[-1].get("world_size"),
        "micro_batch_size": rows[-1].get("micro_batch_size"),
        "grad_accum_steps": rows[-1].get("grad_accum_steps"),
        "moe_backend": rows[-1].get("moe_backend"),
        "ce_chunk_tokens": rows[-1].get("ce_chunk_tokens"),
    }
    out = Path(args.output_csv)
    out.parent.mkdir(parents=True, exist_ok=True)
    exists = out.exists()
    with out.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary.keys()))
        if not exists:
            w.writeheader()
        w.writerow(summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
