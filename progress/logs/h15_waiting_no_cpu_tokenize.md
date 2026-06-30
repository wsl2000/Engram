# H15.3 - waiting; no CPU tokenization submitted

- Active jobs:
  - `167284` h4 B v3: `PENDING (Resources)`.
  - `167289_[0-8]` h4 eval v3: `PENDING (Dependency)`.
- Pulled `origin/main`; no new feedback files beyond `feedback/review-20260629T1032Z.md`.
- No B v3 output directory or checkpoint exists yet.
- Current `squeue --start` estimate for `167284` remains `2026-07-01T21:32:39Z`.
- Token data already available:
  - pair-1 repeated tranche: 60 shards.
  - h4 train tranche: 208 shards.
  - h5 eval tranche: 32 shards.
- Considered starting additional CPU-only tokenization while waiting, but did not submit it because the `all` partition is H100-backed; CPU/memory-only jobs can still occupy H100-node resources and may worsen the pending 10x8 backfill. Preserving the 80-H100 allocation path for h4 B is higher priority.
- Next: keep `167284` queued unchanged; when allocated, validate first-step logs and 25-minute checkpoint creation.
