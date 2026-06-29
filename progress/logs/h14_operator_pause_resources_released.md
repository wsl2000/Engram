# H14.7 operator pause and resource release

Operator requested release of H100 resources to discuss the project.

Actions:

- Stopped local monitoring shell sessions.
- Canceled h4 B training job `165375`.
- Canceled dependent h4 eval jobs `165432`-`165440`.
- Verified `squeue` has no remaining `engram-*` jobs for this user.

State at cancellation:

- h4 A seed 2024 completed successfully and checkpoint is retained:
  `runs/pair_h4_A_seed2024_20B_mbs4_80_v2/ckpt_step005027.pt`
- h4 B seed 2024 had last logged step 4,668 / 5,027, 18,355,322,880 tokens.
- h4 B had no checkpoint because the run used final-only checkpointing and was canceled before step 5,027 checkpoint save.
- h5 eval tranche is complete and available at `data/fineweb_edu_deepseek_h5_eval/shards.txt`.
