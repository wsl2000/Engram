# H21.8 h4 B fourth checkpoint

- UTC check: 2026-06-30 around 21:47.
- Training job: `167284` / `engram-h4-B2024v3`, still running on `cn[14-15,19,24-26,29-32]`.
- Eval array: `167289_[0-8]`, pending on `afterok:167284`.
- Latest monitor step at milestone: 3,850 / 5,027.
- Latest tokens: 15,138,816,000 / 19,766,968,320.
- Latest throughput/MFU: 2,558,234 tok/s, MFU 0.0921.
- Complete checkpoints:
  - `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step000952.pt`, 28,027,733,867 bytes.
  - `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step001907.pt`, 28,027,733,867 bytes.
  - `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step002863.pt`, 28,027,733,867 bytes.
  - `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step003820.pt`, 28,027,733,867 bytes.
- Barrier status: the file was first observed partial at step 3,820, then complete one minute later; training log advanced to step 3,850, so the fourth checkpoint write/barrier did not halt training.
- Current interpretation: no verdict change. Continue to final h4 B checkpoint, then run the dependent h5-disjoint final eval array.
