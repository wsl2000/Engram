#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
from pathlib import Path

from engram.config import build_experiment_configs, invariant_report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="configs/generated")
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    configs = build_experiment_configs()
    for name, cfg in configs.items():
        (out_dir / f"{name}.json").write_text(json.dumps(cfg, indent=2))
    (out_dir / "invariants.json").write_text(json.dumps(invariant_report(), indent=2))
    print(json.dumps(invariant_report(), indent=2))


if __name__ == "__main__":
    main()

