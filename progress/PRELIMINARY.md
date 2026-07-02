# Preliminary Status - H37.0

Timestamp: 2026-07-02T18:06:05Z.

## Verdict

**Tier-1 mechanism positive control: FAIL.** This is a real negative under `handoff.md` §4/§11, not a non-verdict.

The rung-0 `kb-inject` smoke passed earlier, so the synthetic injected-fact/knockout evaluation machinery itself is capable of detecting a load-bearing memory path. The registered Tier-1 run at frozen `R=16` did not satisfy the pre-registered Tier-1 criteria.

**Tier-2 natural-data verdict: not launched.** Per handoff ordering, Tier-2 follows a Tier-1 pass plus data/MFU gates. The latest external feedback also imposes a hard gate before any Tier-2 spend: verify fused/memory-efficient CE in the training path, test `micro_batch_size=8`, rerun 200-step calibration toward `>=18%` MFU, and get explicit owner scope approval.

## Evidence

- Rung-0 smoke: `normal_em=1.0`, `knockout_em=0.0`, `em_collapse=1.0`, McNemar `b=200/c=0`, exact `p=1.2446030555722283e-60`, `key_identity_passed=true`.
- R-pilot freeze rule: R=32 reached `normal_em=0.1542222222`, above the ~8-10% A-recall hard bound, so registered Tier-1 froze pre-hoc at `R=16`.
- Registered A at R=16 / 20B tokens: `normal_em=0.0164444444`, `knockout_em=0.0177777778`, `em_collapse=-0.0013333333`.
- Registered B at R=16 / 20B tokens: `normal_em=0.0237777778`, `knockout_em=0.0253333333`, `em_collapse=-0.0015555556`, mean NLL delta knockout-normal `+0.0038076791`, McNemar `b=4/c=11/p=0.1184692383`.
- B-A main EM gap: `0.0073333333`, far below the required `>=0.20`.
- Negative controls: A and B both `normal_em=0.0`; B-A negative-control gap `0.0`.

## Criteria

- Criterion A, B-knockout collapse: **FAIL**. Knockout slightly increased EM instead of collapsing it; paired McNemar is not significant at the pre-registered gate.
- Criterion B, B-A main margin: **FAIL**. The observed B-A gap is approximately 0.7 percentage points, not the required 20 percentage points.
- Criterion C, negative-control specificity: **PASS**. Negative controls stay at zero.

## Scope

This result is only the Tier-1 mechanism/param-efficiency positive control. It does **not** verify or falsify the paper's natural-data Tier-2 claim, because Tier-2 was not started after the failed mechanism gate and unresolved cost/MFU hard gate.

## Operational State

- Active H100 usage for this Engram objective: 0.
- Completed registered jobs used explicit limits: train `TimeLimit=20:00:00`, `MinMemoryNode=1800G` per node; eval `TimeLimit=01:00:00`, `MinMemoryNode=220G`; decision `TimeLimit=00:10:00`, `ReqMem=16G`.
- Next action: update `REPORT.md` with the v3 Tier-1 FAIL and stop before Tier-2 unless the owner explicitly approves a new scoped Tier-2 plan after the requested MFU calibration.
