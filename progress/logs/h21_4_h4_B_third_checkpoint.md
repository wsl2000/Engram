# H21.4 h4 B third checkpoint

- UTC check: 2026-06-30 around 21:21.
- Training job: `167284` / `engram-h4-B2024v3`, still running on `cn[14-15,19,24-26,29-32]`.
- Eval array: `167289_[0-8]`, pending on `afterok:167284`.
- Latest monitor step at milestone: 2,872 / 5,027.
- Latest tokens: 11,293,163,520 / 19,766,968,320.
- Latest throughput/MFU: 2,560,055 tok/s, MFU 0.0922.
- Complete checkpoints:
  - `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step000952.pt`, 28,027,733,867 bytes.
  - `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step001907.pt`, 28,027,733,867 bytes.
  - `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step002863.pt`, 28,027,733,867 bytes.
- Barrier status: training log advanced to step 2,872 after `ckpt_step002863.pt`, so the third checkpoint write/barrier did not halt training.
- Current interpretation: no verdict change. Early h4 B quick gate showed a nonzero Engram path but weak/no factual knockout collapse; final h5-disjoint eval remains required.
