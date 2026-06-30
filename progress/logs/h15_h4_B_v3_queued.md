# H14.9 - h4 B v3 queued

- Submitted Slurm job: `167284` (`engram-h4-B2024v3`).
- Submit UTC: 2026-06-30T14:56:20Z.
- State at submit check: `PENDING (Resources)`.
- Request: 10 nodes, 80 H100, `--mem=1800G` per node, `--time=04:00:00`, `--cpus-per-task=16`, excluded `cn02,cn10,cn17,cn34`.
- Command source: `scripts/slurm_h4_b_seed2024_resume.sh`.
- Output path once started: `progress/logs/pair_h4_B_seed2024_20B_v3_167284.out`.
- Training target: B seed 2024, h4 shard stream, `max_steps=5027`, `micro_batch_size=4`, `grad_accum=6`, grouped MoE backend, bf16, AdamW, 25-minute checkpoints.
- Next: poll until allocation starts; once running, monitor first steps for matching invariants, tok/s, MFU, and checkpoint creation.
