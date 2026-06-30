# H19.4 - still waiting; backfill slipped

- UTC: 2026-06-30T19:07:59Z.
- Pulled `origin/main`; no new feedback files beyond `feedback/review-20260629T1032Z.md`.
- Active queued jobs:
  - `167284` (`engram-h4-B2024v3`): `PENDING (Resources)`.
  - `167289_[0-8]` (`engram-h4-eval-v3`): `PENDING (Dependency)`.
- Slurm backfill for `167284` has slipped from the prior `2026-07-01T21:32:39Z` estimate to `2026-07-02T04:43:08Z`.
- No `runs/pair_h4_B_seed2024_20B_mbs4_80_v3` output directory or checkpoint exists yet.
- Rechecked 80-GPU topology alternatives with `sbatch --test-only`:
  - New 10x8 test-only estimate: `2026-07-02T09:07:08`, later than the already queued job.
  - 20x4 estimate: `2026-07-03T21:39:40`, worse.
  - 16x5 estimate: `2026-07-03T21:39:40`, worse.
  - 13x7 was probed accidentally for scheduler reference but is invalid for the 80-GPU invariant and was not considered.
- Verified test-only job ids `167545`-`167548` are absent from `squeue`.
- Decision: keep `167284` unchanged; it remains the earliest known valid 80-H100 allocation.
