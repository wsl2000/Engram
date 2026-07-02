# Engram Reproduction Report

Timestamp: 2026-07-02T18:08:05Z.

## Verdict

**Tier-1 mechanism positive control: FAIL.** The registered injected-fact experiment at frozen `R=16` does not satisfy the pre-registered handoff criteria for a load-bearing Engram memory path.

This is a real negative for the Tier-1 mechanism/param-efficiency positive control. It is not a pass, and it is not a "needs more seeds" non-verdict: the handoff explicitly defines Tier-1 as the certain, cheap positive-control gate.

**Tier-2 paper-claim verification was not launched.** The paper's natural-data claim is therefore not verified or falsified by the current v3 run. Tier-2 remained blocked because the Tier-1 prerequisite failed and the latest feedback imposed a cost/efficiency hard gate before any Tier-2 spend.

## Scope

This report supersedes the older `REPORT.md` from the previous natural-data-only attempt. That prior run is preserved in git history, but it is not the current v3 verdict path.

Per `handoff.md`, Tier-1 and Tier-2 have different meanings:

- Tier-1 tests whether the Engram module can provide a load-bearing controlled memory advantage under iso-param/iso-FLOP.
- Tier-2 tests the paper's natural-data claim at this scale, but only after Tier-1 passes and the data/MFU gates pass.

The current result is a Tier-1 FAIL only.

## Apparatus Checks

- Rung-0 `kb-inject` smoke passed before registered training: `normal_em=1.0`, `knockout_em=0.0`, `em_collapse=1.0`, McNemar `b=200/c=0`, exact `p=1.2446030555722283e-60`, `key_identity_passed=true`.
- This confirms the injected-fact/knockout evaluation can detect a deliberately load-bearing memory path.
- The registered Tier-1 failure is therefore not explained by an obviously dead evaluator.

## R-Pilot And Frozen R

The A-only rarity pilot ran 5B tokens at each tested `R` value. The freeze rule was applied pre-hoc from A recall only: choose the largest tested `R` below the approximate 8-10% A-recall hard bound.

| R | A normal EM | A knockout EM |
|---:|---:|---:|
| 1 | 0.000222 | 0.000222 |
| 2 | 0.000222 | 0.000222 |
| 4 | 0.000889 | 0.001111 |
| 8 | 0.006444 | 0.007111 |
| 16 | 0.040667 | 0.041778 |
| 32 | 0.154222 | 0.153778 |

`R=32` exceeded the A-recall bound, so the registered run froze `R=16`.

## Registered Tier-1 Run

Registered Tier-1 used `R=16`, 20B target tokens per arm, 2 nodes / 16 H100 per arm, AdamW, bf16, grouped MoE, `ce_impl=memory_efficient`, `micro_batch_size=4`, and `grad_accum_steps=6`.

Resource limits were explicit:

- A/B train: `TimeLimit=20:00:00`, `MinMemoryNode=1800G` per node.
- A/B eval: `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- Decision: `TimeLimit=00:10:00`, `ReqMem=16G`.

Completed jobs:

| Job | Meaning | Status | Elapsed |
|---:|---|---|---:|
| 175099 | registered A train | completed `0:0` | 17:01:49 |
| 175100 | registered B train | completed `0:0` | 17:24:48 |
| 175101 | registered A eval | completed `0:0` | 00:03:29 |
| 175102 | registered B eval | completed `0:0` | 00:03:40 |
| 175103 | registered decision | completed `0:0` | 00:00:06 |

## Tier-1 Results

| Metric | A | B | Notes |
|---|---:|---:|---|
| Main normal EM | 0.016444 | 0.023778 | B-A = 0.007333 |
| Main knockout EM | 0.017778 | 0.025333 | Knockout does not collapse B |
| Main EM collapse | -0.001333 | -0.001556 | Negative means knockout is slightly higher |
| Negative-control EM | 0.000000 | 0.000000 | Specificity control passes |

B knockout details:

- Main records: 4500.
- Mean NLL delta, knockout minus normal: `+0.0038076791`.
- McNemar: `b=4/c=11/p=0.1184692383`.

B-A margin details:

- Main EM gap: `0.0073333333`, far below the required `>=0.20`.
- Main gap McNemar: `p=0.0099326684`, but the magnitude gate fails.

Negative-control details:

- A negative-control EM: `0.0`.
- B negative-control EM: `0.0`.
- B-A negative-control gap: `0.0`.

## Criteria

| Criterion | Required | Observed | Result |
|---|---|---|---|
| A: B knockout collapse | NLL worsens significantly and EM collapse >= 0.05 | NLL delta small, McNemar `p=0.1185`, EM collapse `-0.0016` | FAIL |
| B: B-A main margin | B-A EM gap >= 0.20 and significant | B-A EM gap `0.0073` | FAIL |
| C: negative-control specificity | Negative-control B-A gap < half main gap | Negative-control gap `0.0` | PASS |

Overall decision: **`pass=false`**.

## Tier-2 Status

Tier-2 was not launched.

Reasons:

- `handoff.md` says Tier-2 should start after Tier-1 passes.
- Registered Tier-1 failed.
- `feedback/review-20260702T1624Z.md` adds a hard gate before any Tier-2 spend: verify the fused/memory-efficient CE path in training, test `micro_batch_size=8`, rerun a 200-step calibration targeting `>=18%` MFU, and get explicit owner scope approval.
- Observed registered Tier-1 MFU was about `0.071-0.073`, well below the requested Tier-2 gate.

## Artifacts

- R-pilot summary: `results/tier1/rpilot_summary_2node_5b_compile.csv`.
- Registered A eval: `results/tier1/registered_A_R16_20b_tps50m.csv` and `.json`.
- Registered B eval: `results/tier1/registered_B_R16_20b_tps50m.csv` and `.json`.
- Registered decision: `results/tier1/registered_decision_R16_20b_tps50m.json`.
- Progress trail: `progress/STATUS.md`, `progress/PRELIMINARY.md`, and `progress/logs/`.

## Final Assessment

The v3 reproduction does **not** verify DeepSeek's Engram mechanism. The controlled positive-control apparatus is sensitive in rung-0, but the registered iso-param Engram arm did not become a load-bearing memory for the injected facts: B recall is only slightly above A, and knockout does not collapse B recall.

The paper's natural-data claim remains untested in this v3 path because Tier-2 was correctly stopped before launch.
