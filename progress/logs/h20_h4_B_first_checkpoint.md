# H20.5 - h4 B v3 first checkpoint

- UTC: 2026-06-30T20:30-20:31Z.
- Slurm job `167284` remains running on 10 nodes / 80 H100.
- First checkpoint: `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step000952.pt`.
- Checkpoint size after write completion: 28,027,733,867 bytes.
- Training passed the checkpoint barrier and continued to step 1,014 / 5,027.
- Latest checked tokens: 3,987,210,240 / 19,766,968,320.
- Latest checked throughput: 2,563,131 tok/s; MFU 9.23%.
- The 25-minute checkpoint cadence is working; this avoids losing the whole B run if interrupted.
- Added `scripts/slurm_h4_b0952_quick_gate.sh` to run first-checkpoint bug-gate checks:
  - TriviaQA answer-NLL normal vs knockout, limit 100.
  - PopQA answer-NLL normal vs knockout, limit 100.
  - h5-disjoint Engram gate/contribution diagnostics.
- Next: submit the quick gate job and keep monitoring B to final.
