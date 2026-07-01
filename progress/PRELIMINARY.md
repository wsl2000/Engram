# Preliminary Status - H11.6

Timestamp: 2026-07-01T16:21:11Z.

## Verdict

**No current Engram verdict yet.** This is an explicit honest non-verdict, not a pass/fail claim.

The v3 Tier-1 decision requires the A-only rarity pilot to finish, the frozen R to be selected from A recall, and the registered A/B plus B-knockout evaluation to run. At H11.6 the current 5B/R A-only pilot is still training for R=1,2,4,8,16, so no recall-vs-R table, frozen R, knockout result, paired NLL, McNemar test, or Tier-2 natural-data result exists yet.

## Why This Supersedes The Old Preliminary

The prior `progress/PRELIMINARY.md` described an older pair-1 natural-data run from June 29, 2026. That result is preserved in git history but is not the current v3 verdict path. The current plan follows `handoff.md` and later feedback: build the Tier-1 injected-fact apparatus first, shorten the A-only R-pilot to about 5B/R, then freeze R before any registered A/B claim.

## Current Evidence At H11.6

- Data gate passed earlier with 300B DeepSeek-V3-tokenized FineWeb-Edu tokens on disk.
- Rung-0/fact-set apparatus exists: 5,000 single-token facts with negative controls and injected streams.
- The local compile-cache failure was fixed by moving TorchInductor/Triton caches to per-job local `/tmp` paths.
- Current A-only R-pilot is running for R=1,2,4,8,16 at 5B tokens each, 2 nodes / 16 H100 per run, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`.
- All five active R-pilot trains have reached steady training with `ce_impl=memory_efficient`, grouped MoE, about 337k-341k tok/s per 16-H100 run, and MFU about 0.072-0.073.
- No current train log shows `Traceback`, `RuntimeError`, `OutOfMemory`, stale-cache `OSError`, or `ChildFailed`.

## Current Non-Decision

- **Tier-1 mechanism verdict:** pending. A recall-vs-R and frozen R are not available until A-only pilot evals complete.
- **Bug gate:** pending for the registered B run. No B-knockout number exists yet.
- **Tier-2 natural-data verdict:** pending and intentionally not started until Tier-1 and gates justify it.
- **Loss gap:** not reported as verdict evidence at this stage.

## Next Action

Let R=1,2,4,8,16 finish and allow their dependent eval jobs to run. Submit R=32 only after one 2-node training allocation frees, to keep this objective at or below 80 active H100. Then build the recall-vs-R table, freeze R pre-hoc from A-only recall, and proceed to the registered Tier-1 A/B/B-knockout run.
