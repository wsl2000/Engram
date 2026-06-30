# H19.5 - resumed blocked audit: still waiting for H100 allocation

- UTC: 2026-06-30T19:10:38Z.
- Pulled `origin/main`; no new feedback files beyond `feedback/review-20260629T1032Z.md`.
- Active queued jobs:
  - `167284` (`engram-h4-B2024v3`): `PENDING (Resources)`.
  - `167289_[0-8]` (`engram-h4-eval-v3`): `PENDING (Dependency)`.
- `167284` details:
  - Request: 10 nodes / 80 H100, 160 CPUs, 18,000G memory, 4h walltime.
  - Excludes: `cn02,cn10,cn17,cn34`.
  - Backfill estimate remains `2026-07-02T04:43:08`.
  - No nodes assigned.
- Cluster snapshot: 6 full H100 nodes currently idle (`cn19,cn25,cn26,cn30,cn31,cn32`), below the 10 full-node requirement for the queued faithful 80-GPU run.
- Artifacts:
  - No `runs/pair_h4_B_seed2024_20B_mbs4_80_v3` output directory exists.
  - No B v3 checkpoint or eval output exists.
- This is the third resumed check after the previous blocked state with the same external blocker: Slurm cannot yet allocate the required 80 H100. The correct B job and dependent eval array are already queued, and the earlier topology checks found no valid earlier 80-GPU alternative.
- Next after unblocking: inspect `progress/logs/pair_h4_B_seed2024_20B_v3_167284.out`, verify first-step invariants, monitor 25-minute checkpoint, and then collect `167289` eval outputs.
