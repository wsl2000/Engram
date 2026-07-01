# H2.5 tokenizer bash wrapper fix

Timestamp: 2026-07-01T06:26:01Z

## Issue avoided

The pending tokenizer job `168266` had not started, but its Slurm `--wrap` command contained Bash-only features (`mapfile` and process substitution). To avoid a shell compatibility failure after the long download finishes, `168266` was canceled before execution.

## Fix

- Added `scripts/run_tokenize_fineweb_job.sh`.
- `scripts/slurm_tokenize_fineweb.sh` now uses `--wrap="cd ... && bash scripts/run_tokenize_fineweb_job.sh ..."` instead of embedding merge logic directly in `--wrap`.
- The helper:
  - runs 16 worker tokenizers through `srun`;
  - uses per-worker parquet sharding and token caps;
  - verifies the expected worker directory count;
  - merges worker outputs;
  - runs `scripts/assert_data_gate.py --min-tokens 200000000000`.

## Relaunch

- New tokenizer/data-gate job: `168267`.
- Dependency: `afterok:168265`.
- Limits: `TimeLimit=18:00:00`, `MinMemoryNode=1200G`.
- Scope: `data/fineweb_edu_parquet/sample/350BT/*.parquet`.

## Current data state

- Corrected download `168265` is running on `cn09`.
- Local parquet count: 14.
- Local parquet size: 29G.
- Scope audit: `bad_scope=0`.
