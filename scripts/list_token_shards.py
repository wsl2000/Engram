#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("token_dir")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    token_dir = Path(args.token_dir)
    manifests = sorted(token_dir.glob("manifest_w*.json"))
    shards = []
    total = 0
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text())
        for shard in manifest.get("shards", []):
            shards.append(shard["path"])
            total += int(shard["tokens"])
    text = "\n".join(shards) + ("\n" if shards else "")
    if args.output:
        Path(args.output).write_text(text)
    else:
        print(text, end="")
    print(f"manifests={len(manifests)} shards={len(shards)} tokens={total}", flush=True)


if __name__ == "__main__":
    main()

