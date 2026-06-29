# H10.6 h4 A running and h5 eval tranche started

Corrected h4 A launch:

- Bad job `165367` was canceled before training because it ran `torchrun --nnodes=10` only on the batch host.
- Corrected job `165373` uses one `srun` task per node and is running on 80 GPUs.
- Output: `runs/pair_h4_A_seed2024_20B_mbs4_80_v2`
- Early step sample: step 15 / 5,027, 58,982,400 tokens, ~2.64M tok/s, MFU ~9.5%.

Held-out eval contamination mitigation:

- `feedback/review-20260629T0432Z.md` noted that h4 document-level disjointness cannot be proven from existing manifests.
- Added `--skip-tokens` to `src/engram/tokenize_fineweb.py`; it discards whole encoded documents until the requested per-worker token prefix is skipped.
- Started tokenization job `165374` for `data/fineweb_edu_deepseek_h5_eval`.
- Parameters: 16 workers, skip 1,260,000,000 tokens per worker, output 125,000,000 tokens per worker, 100M-token shards.

This h5 eval tranche is intended for h4-trained pair evaluation, not for training.

Queued matching h4 B:

- Job: `165375`
- Dependency: `afterok:165373`
- Output: `runs/pair_h4_B_seed2024_20B_mbs4_80_v2`
- Same h4 token stream, seed 2024, mbs4/ga6, 80 GPUs, AdamW, bf16, final-only checkpoint.
