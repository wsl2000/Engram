#!/usr/bin/env python
from __future__ import annotations

import argparse
import json

from engram.offline_data import snapshot_download_parquet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-id", default="HuggingFaceFW/fineweb-edu")
    parser.add_argument("--local-dir", required=True)
    parser.add_argument("--allow-patterns", nargs="+", default=["sample/350BT/*.parquet"])
    args = parser.parse_args()
    path = snapshot_download_parquet(args.repo_id, args.local_dir, allow_patterns=tuple(args.allow_patterns))
    print(json.dumps({"local_dir": path}, indent=2))


if __name__ == "__main__":
    main()
