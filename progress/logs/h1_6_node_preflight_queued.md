# H1.6 node preflight queued

- Submitted Slurm job `168251` with `scripts/slurm_node_preflight_128.sh`.
- Request:
  - 16 nodes
  - 128 H100
  - 15 minutes
  - exclude `cn02,cn10,cn17,cn34`
- Current state:
  - `PENDING (Resources)`
  - backfill start estimate `2026-07-01T16:30:54Z`
  - scheduler candidate nodes `cn[09,14-15,18-20,24-26,28-33,35]`
- No GPUs are currently allocated to this job.
- Next: monitor until it starts; then validate all per-node preflight JSON outputs before launching calibration or Tier-1 training.
