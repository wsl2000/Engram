# H2.1 80GPU calibration

- Time: 2026-06-28 23:37 UTC
- Run: `runs/calib_A_seed1337`
- Arm/seed: A / 1337
- Launcher: Slurm, 10 nodes x 8 H100, DDP full expert replication
- Nodelist: `cn02,cn04,cn13,cn14,cn15,cn16,cn25,cn26,cn27,cn35`
- Config: `configs/generated/A_seed1337.json`
- Token shards: 60 shards from `data/fineweb_edu_deepseek`, 4.6908B tokens available
- Optimizer: AdamW, as previously fixed because Muon was not installed/vetted
- Checkpointing: disabled for calibration with `--no-checkpoint`

The 200-step calibration was stopped after 12 valid full-model A-arm steps once throughput stabilized far below the handoff target. Steps 8-12 averaged 402,919 tok/s, 10.58s/step, MFU 1.45%.

Throughput implication:

- 70B tokens/run: ~48.26h per run
- Pair 1 A+B: ~96.52h before evaluation
- Six training runs: ~12.06 days before final evaluation

This is an implementation/stack blocker, not a DeepSeek Engram verdict. The likely bottleneck is the current pure-PyTorch MoE expert loop with full expert replication. No Megablocks, Tutel, DeepSpeed MoE, FlashAttention, or Transformer Engine stack is available in the current environment. Continuing the exact H12/H24 handoff timeline on this implementation would not satisfy the requested schedule.
