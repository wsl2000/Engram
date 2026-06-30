# H15.4 - blocked waiting for H100 allocation

- UTC: 2026-06-30T15:07:29Z.
- Pulled `origin/main`; no new feedback files beyond `feedback/review-20260629T1032Z.md`.
- Active queued jobs:
  - `167284` (`engram-h4-B2024v3`): `PENDING (Resources)`.
  - `167289_[0-8]` (`engram-h4-eval-v3`): `PENDING (Dependency)`.
- Slurm details for `167284`:
  - Submitted: 2026-06-30T14:56:20.
  - Request: 10 nodes / 80 H100, 160 CPUs, 18,000G total memory, 4h walltime.
  - Excludes: `cn02,cn10,cn17,cn34`.
  - Backfill estimate remains `2026-07-01T21:32:39`.
- Artifacts:
  - No `runs/pair_h4_B_seed2024_20B_mbs4_80_v3` output directory exists yet.
  - No B v3 checkpoint or eval output exists yet.
- This is the third consecutive resumed progress check with the same external blocker: Slurm cannot currently allocate the required 80 H100. The queued jobs and dependent evals are in place; no further scientifically meaningful progress is possible until allocation starts or the operator changes cluster/resource policy.
- Next on resume/allocation: inspect `progress/logs/pair_h4_B_seed2024_20B_v3_167284.out`, confirm first-step invariants, monitor first 25-minute checkpoint, then let eval array `167289` run after B success.
