# H8.9 Tier-1 pivot to 2-node train path

Timestamp: 2026-07-01T13:51:42Z

## Feedback

Read `feedback/review-20260701T1224Z.md`: ON-TRACK, with an actionable suggestion to decouple Tier-1's certain verdict from the scarce 128-node preflight window.

## Canceled

- R-pilot submitter: `171792`.
- Old R=1 train/eval: `172196` / `172197`.
- Old R=2 train/eval: `172669` / `172670`.

These jobs had no GPU allocation. The old job table was archived as `progress/results/tier1_rpilot_jobs_canceled_128dep.tsv`.

## Kept

- `data/tier1/rpilot_R1_tokens20000000000`.
- `data/tier1/rpilot_R2_tokens20000000000`.

Removed partial R=4 stream before restart.

## Code

- Added `TRAIN_NODES` support to Tier-1 submit scripts.
- Added `scripts/slurm_node_preflight_2node.sh`:
  - 2 nodes / 16 H100;
  - `--time=00:15:00`;
  - `--mem=128G`;
  - same exclude list as 128-node preflight.

## New Tier-1 Plan

- Submit 2-node preflight.
- Queue R1/R2 trains from existing streams with:
  - `TRAIN_NODES=2`;
  - dependency on the 2-node preflight;
  - `STEPS=25432` for ~20B tokens at 16 GPUs, mbs4, ga6, seq2048.
- Resume R-pilot stream builder for R=4,8,16,32 with the same 2-node train settings.
