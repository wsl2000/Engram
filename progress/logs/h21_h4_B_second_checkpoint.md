# H21.0 h4 B second checkpoint

- UTC check: 2026-06-30 around 20:56-21:00.
- Training job: `167284` / `engram-h4-B2024v3`, still running on `cn[14-15,19,24-26,29-32]`.
- Eval array: `167289_[0-8]`, pending on `afterok:167284`.
- Latest rank0 step at milestone: 1,944 / 5,027.
- Latest tokens: 7,644,119,040 / 19,766,968,320.
- Latest throughput/MFU: 2,581,119 tok/s, MFU 0.09295.
- Complete checkpoints:
  - `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step000952.pt`, 28,027,733,867 bytes.
  - `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step001907.pt`, 28,027,733,867 bytes.
- Barrier status: training log advanced to step 1,944 after `ckpt_step001907.pt`, so the second checkpoint write/barrier did not halt training.
- Current interpretation: the earlier first-checkpoint quick gate showed a nonzero Engram path but weak/no factual knockout collapse. Continue to final checkpoint and h5-disjoint eval before updating the verdict.
