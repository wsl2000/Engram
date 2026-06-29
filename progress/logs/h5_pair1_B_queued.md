# H4.8 pair-1 B queued

- Submitted Slurm job `165281` for pair-1 B seed 1337.
- Dependency: `afterok:165275`, so B starts only if pair-1 A completes cleanly.
- Requested nodelist: `cn02,cn13,cn14,cn15,cn16,cn25,cn26,cn27,cn29,cn35`.
- Shape: 80 GPUs, mbs4/ga6, 5,086 steps, `ENGRAM_MOE_BACKEND=grouped`, bf16, AdamW.
- Config: `configs/generated/B_seed1337.json`.
- Output: `runs/pair1_B_seed1337_20B_mbs4_80`.
- Log: `progress/logs/pair1_B_seed1337_20B_165281.out`.
- Token stream: `data/fineweb_edu_deepseek/shards.txt` (60 shards), intentionally the same pair-1 stream as A. The newer h4 tokenization tranche is not used for pair-1 B because that would violate the paired-loader invariant.
