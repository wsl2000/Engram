# H7.4 Tier-1 submit hardening

Timestamp: 2026-07-01T12:20:00Z

## Purpose

Prepare Tier-1 pre-gate submission without letting GPU training start before the pending node preflight succeeds.

## Changes

- `scripts/submit_tier1_r_pilot.sh` honors `TRAIN_DEPENDENCY`.
- `scripts/submit_tier1_registered.sh` honors `TRAIN_DEPENDENCY`.
- Added `scripts/slurm_submit_tier1_r_pilot.sh`:
  - CPU-only stream-build submitter;
  - `--time=08:00:00`;
  - `--mem=512G`;
  - calls `scripts/submit_tier1_r_pilot.sh`.

## Validation

- `bash -n scripts/*.sh`: passed.
- `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py`: passed.
- Static Slurm time/mem audit: passed.

## Next

Submit the Tier-1 A-only R-pilot stream builder with `TRAIN_DEPENDENCY=afterok:168251` so downstream train jobs wait for node preflight.
