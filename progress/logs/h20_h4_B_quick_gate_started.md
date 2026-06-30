# H20.6 - h4 B first-checkpoint quick gate started

- UTC: 2026-06-30T20:33:33Z.
- Submitted and started quick gate job `167601` (`engram-h4-b0952-gate`) on `cn06`.
- Request/allocation: 1 H100, 12 CPUs, 220G memory, 2h limit.
- Script: `scripts/slurm_h4_b0952_quick_gate.sh`.
- Checkpoint under test: `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step000952.pt`.
- Planned outputs:
  - `results/knockout/h4v3_b0952_triviaqa_nll.{csv,json}`.
  - `results/knockout/h4v3_b0952_popqa_nll.{csv,json}`.
  - `results/diagnostics/h4v3_b0952_engram_diag.{csv,json}`.
- Main B job `167284` continues running; latest checked step after quick-gate submit was 1,082 / 5,027 and 4,254,597,120 tokens.
- Dependent final eval array `167289_[0-8]` remains `PENDING (Dependency)`.
