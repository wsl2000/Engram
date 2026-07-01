#!/usr/bin/env python
from __future__ import annotations

import argparse
import json

from engram.offline_data import merge_tokenized_outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker-dirs", nargs="+", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    print(json.dumps(merge_tokenized_outputs(args.worker_dirs, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
