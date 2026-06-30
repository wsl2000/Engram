# H14.8 resume - h4 B relaunch prepared

- Resume UTC: 2026-06-30T14:54:23Z.
- Pulled `origin/main`; new feedback `feedback/review-20260629T1032Z.md` confirms the pause was operator-requested and the correct resume path is h4 B seed 2024 from scratch, same h4 stream / world size / batch / optimizer / precision / 5,027-step endpoint, followed by h5-disjoint knockout, slices, and depth.
- Current Engram jobs before relaunch: none. Existing non-Engram cluster jobs occupy most H100 nodes; only `cn30` is fully idle, so the 80-GPU job may pend until ten full H100 nodes are free.
- Retained checkpoint: h4 A final `runs/pair_h4_A_seed2024_20B_mbs4_80_v2/ckpt_step005027.pt`.
- Missing checkpoint: h4 B final. Prior h4 B job `165375` was canceled at step 4,668 / 5,027 with no final checkpoint because it used final-only checkpointing.
- Relaunch script: `scripts/slurm_h4_b_seed2024_resume.sh`, requesting 10 nodes / 80 H100, bf16, AdamW, grouped MoE backend, `micro_batch_size=4`, `grad_accum=6`, `max_steps=5027`, and 25-minute checkpoint cadence.
- Node policy: exclude `cn17` and `cn34` due prior CUDA failures, exclude `cn02` due prior batch-host signal failure, exclude drained `cn10`.
- Next: push this resume snapshot, submit h4 B v3, then push the Slurm job id and monitor/pull every ~2h.
