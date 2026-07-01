# H7.5 Tier-1 R-pilot submitter running

Timestamp: 2026-07-01T12:19:06Z

## Job

- Submitter job: `171792`.
- Name: `engram-tier1-rpilot-submit`.
- Node: `cn09`.
- Limits: `TimeLimit=08:00:00`, `MinMemoryNode=512G`, 16 CPUs.
- GPU allocation: 0.

## Inputs

- Facts: `data/injected_facts/facts_5000_seed17.csv`.
- Base token list: `data/fineweb_edu_deepseek_v3_300b/merged/shards.txt`.
- Config: `configs/generated/A_seed1337.json`.

## Settings

- R values: `1,2,4,8,16,32`.
- Target tokens per R stream: 20,000,000,000.
- Steps per A-only train: 3,179.
- Train dependency: `afterok:168251`.

## Next

Wait for stream construction and train/eval job emission. Confirm generated train jobs are dependency-pending on node preflight `168251`.
