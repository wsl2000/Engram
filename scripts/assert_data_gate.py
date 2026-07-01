#!/usr/bin/env python
from __future__ import annotations

import argparse
import json

from engram.offline_data import assert_data_gate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--min-tokens", type=int, default=200_000_000_000)
    args = parser.parse_args()
    print(json.dumps(assert_data_gate(args.output_dir, args.min_tokens), indent=2))


if __name__ == "__main__":
    main()
