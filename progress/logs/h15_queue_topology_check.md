# H15.2 - queue topology check

- UTC: 2026-06-30T15:03:53Z.
- Active jobs remain:
  - `167284` h4 B v3: `PENDING (Resources)`.
  - `167289_[0-8]` h4 eval v3: `PENDING (Dependency)`.
- Checked whether a different 80-GPU topology could improve queue time while preserving world size 80, batch, optimizer, steps, and data seed order.
- `sbatch --test-only` estimates:
  - Current 10 nodes x 8 H100: 2026-07-02T03:52:39 in the test-only snapshot; actual queued job `167284` still has the better backfill estimate 2026-07-01T21:32:39Z.
  - 20 nodes x 4 H100: 2026-07-06T14:39:41, worse.
  - 16 nodes x 5 H100: 2026-07-03T18:01:28, worse.
  - 40 nodes x 2 H100: requested node configuration unavailable.
- Verified test-only job ids `167294`, `167295`, and `167296` are not present in `squeue`.
- Decision: keep the already queued 10x8 job `167284`; do not change topology or world size.
