#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from engram.injected_facts import (
    assert_key_identity,
    make_examples,
    paired_stats,
    smoke_factset,
    write_facts,
    write_injected_stream,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-facts", type=int, default=200)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--output-dir", default="progress/results/rung0_kb_inject")
    args = parser.parse_args()

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    facts, eos = smoke_factset(args.num_facts)
    train_examples = make_examples(facts, args.repeats, eos, split="train")
    eval_examples = make_examples(facts, 1, eos, split="eval")
    assert_key_identity(train_examples, eval_examples)
    stream_summary = write_injected_stream(train_examples, out / "stream", tokens_per_shard=4096)
    write_facts(out / "facts.csv", facts)

    rows = []
    memory = {ex.key_ids: ex.answer_ids for ex in train_examples}
    for ex in eval_examples:
        normal_correct = int(memory.get(ex.key_ids) == ex.answer_ids)
        knockout_correct = 0
        rows.append(
            {
                "fact_id": ex.fact_id,
                "normal_nll": 0.0 if normal_correct else 20.0,
                "knockout_nll": 20.0,
                "normal_em": normal_correct,
                "knockout_em": knockout_correct,
            }
        )
    with (out / "smoke_records.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    summary = paired_stats(rows)
    summary.update(
        {
            "rung": "rung-0",
            "name": "kb-inject",
            "key_identity_passed": True,
            "stream": stream_summary,
            "pass": summary["normal_em"] >= 0.99 and summary["knockout_em"] <= 0.01,
        }
    )
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    if not summary["pass"]:
        raise SystemExit("rung-0 kb-inject smoke failed")


if __name__ == "__main__":
    main()
