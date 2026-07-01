# H2.3 Slurm mem/time limits

Timestamp: 2026-07-01T06:17:03Z

User reminder: every run should have explicit memory and wall-time limits.

## Current submitted jobs

- `168251` node preflight: `TimeLimit=00:15:00`, `MinMemoryNode=128G`, pending resources, no allocation.
- `168254` parquet download: `TimeLimit=12:00:00`, `MinMemoryNode=256G`, running on `cn34`.
- `168260` local tokenizer: `TimeLimit=18:00:00`, `MinMemoryNode=1200G`, pending dependency on `168254`.

## Script audit

- `bash -n scripts/*.sh`: passed.
- Static audit over every `scripts/*.sh` containing `sbatch` or `#SBATCH`: no missing time/mem limits after update.
- `submit_tier1_r_pilot.sh` now passes `--time` and `--mem` explicitly for train and eval submissions.
- `submit_tier1_registered.sh` now passes `--time` and `--mem` explicitly for A train, B train, A eval, B eval, and decision submissions.

## Defaults

- Tier-1 train: `TRAIN_TIME=04:00:00`, `TRAIN_MEM=1800G`.
- Tier-1 eval: `EVAL_TIME=01:00:00`, `EVAL_MEM=220G`.
- Tier-1 decision: `DECIDE_TIME=00:10:00`, `DECIDE_MEM=16G`.

The defaults can be overridden through environment variables at submission time, but the resulting `sbatch` command still includes explicit limits.
