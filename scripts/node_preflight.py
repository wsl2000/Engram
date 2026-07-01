#!/usr/bin/env python
from __future__ import annotations

import argparse
import json

from engram.ops import cuda_node_preflight, write_preflight


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()
    result = cuda_node_preflight()
    if args.output:
        write_preflight(args.output)
    print(json.dumps(result, indent=2))
    if result["cuda_available"] and result["device_count"] <= 0:
        raise SystemExit("CUDA reported available but no devices passed preflight")


if __name__ == "__main__":
    main()
