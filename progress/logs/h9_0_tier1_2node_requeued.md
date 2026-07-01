# H9.0 Tier-1 2-node preflight passed and jobs requeued

Timestamp: 2026-07-01T13:57:45Z

## Small Preflight

- Job: `172706`.
- Nodes: `cn[13-14]`.
- State: `COMPLETED`.
- Exit: `0:0`.
- Elapsed: 11s.
- Artifacts: `progress/results/node_preflight/172706_0.json`, `progress/results/node_preflight/172706_1.json`.
- Result: each node reported 8x H100 80GB, CUDA available, probe value 1.0.

## Requeue Reason

R1/R2 initially started with `TimeLimit=18:00:00`. Early steps ran at about 300k tok/s for 16 GPUs, making 25,432 steps slightly longer than 18h. Slurm denied live time-limit extension, so the jobs were canceled and requeued before meaningful progress/checkpoints.

Canceled:

- `172707/172708`.
- `172709/172710`.
- R4 submitter `172711`.

## Current Jobs

- R1 train/eval: `172713/172714`.
- R2 train/eval: `172715/172716`.
- R4+ submitter: `172717`.

Train settings:

- `TRAIN_NODES=2`.
- `STEPS=25432`.
- `TRAIN_TIME=20:00:00`.
- `TRAIN_MEM=1800G`.

Current H100 allocation at this check: 0. The new train jobs are pending priority, not allocated.
