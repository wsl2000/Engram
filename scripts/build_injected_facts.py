#!/usr/bin/env python
from __future__ import annotations

import argparse
import json

from transformers import AutoTokenizer

from engram.injected_facts import build_facts_from_tokens, mine_single_token_strings, write_facts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tokenizer", default="deepseek-ai/DeepSeek-V3")
    parser.add_argument("--count", type=int, default=5000)
    parser.add_argument("--output-csv", default="data/injected_facts/facts.csv")
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--negative-control-frac", type=float, default=0.1)
    args = parser.parse_args()
    tok = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=True)
    # Mine disjoint single-token pools. Over-sample so filtering remains robust.
    pool = mine_single_token_strings(tok, args.count * 2, seed=args.seed)
    subjects = pool[: args.count]
    objects = pool[args.count : args.count * 2]
    relations = [" knows ", " stores ", " maps ", " tags ", " marks ", " pairs ", " cites ", " names ", " keys ", " binds "]
    facts = build_facts_from_tokens(
        subjects=subjects,
        objects=objects,
        relations=relations,
        tokenizer=tok,
        count=args.count,
        seed=args.seed,
        negative_control_frac=args.negative_control_frac,
    )
    write_facts(args.output_csv, facts)
    print(json.dumps({"facts": len(facts), "output_csv": args.output_csv}, indent=2))


if __name__ == "__main__":
    main()
