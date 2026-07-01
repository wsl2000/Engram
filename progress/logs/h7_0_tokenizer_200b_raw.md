# H7.0 tokenizer crossed 200B raw estimate

Timestamp: 2026-07-01T10:59:22Z

## Jobs

- `169155`: tokenizer/data-gate job, running on `cn[13-16]`, CPU-only.
- Limits: `TimeLimit=18:00:00`, `MinMemoryNode=1200G`.
- Runtime at check: `1:41:11`.
- `168251`: 128-H100 node preflight pending; no allocation.

Current H100 allocation: 0.

## Tokenizer output

- Worker directories: 16.
- `.u32` shard files: 2,122.
- Sum of `.u32` file bytes: 848,800,000,000.
- Estimated uint32 tokens: 212,200,000,000.
- Output tree size: about 826G.

This crosses the 200B raw-output estimate, but it is not the official data-gate result. The official gate requires worker summaries, merge, and `assert_data_gate.py --min-tokens 200000000000` on the merged output.

## Next

Continue monitoring until all workers finish and `data/fineweb_edu_deepseek_v3_300b/merged/summary.json` exists. Then inspect the gate result before moving to MFU/Tier-2 work.
