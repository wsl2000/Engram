# Engram Reproduction Report

## Verdict

**NOT VERIFIED.** The completed runs do not satisfy the handoff §10 PASS criteria. The Engram path is active and changes hidden states/logits, but the primary evidence does not show a load-bearing factual memory:

- Knockout: final h4 seed-2024 checkpoint shows only tiny answer-NLL degradation under knockout, and 5-shot EM remains at floor on TriviaQA/PopQA.
- Targeted slices: h5-disjoint repeated-ngram and entity-proxy slices do not favor the Engram arm; B is slightly worse than A on all three h5 slice metrics measured here.
- Depth: B has a tiny mean-earliest-layer improvement, but median is tied and cumulative resolution is mixed.
- Global loss: secondary and underpowered; observed paired deltas are negative (B worse), and the planned 3-seed CI was not available after the weak primary verdict and resource pause.

Honest-negative caveat from handoff §10: *"Engram is functionally active (stores knowledge, deepens the net) but its net loss advantage is not statistically resolved at 0.48B / ~70B tokens."* This run supports only the **functionally active / nonzero path** part. It does **not** verify the "stores knowledge" clause because knockout did not collapse TriviaQA/PopQA.

## Executor Judgment Calls

- Tokens/run: due measured throughput around 2.57M tok/s on 80 H100, far below the handoff planning target of 8.34M tok/s, the faithful resumed h4 pair used 5,027 steps = 19,766,968,320 tokens per arm. This was a schedule-driven deviation from the 60-80B planning range.
- Optimizer: AdamW for all runs. Muon was not installed/vetted on this stack.

## Invariants Checked

- Arm A: pure MoE, 88 routed experts.
- Arm B: 68 routed experts + flat Engram value memory.
- Active params matched at 475,136,000; non-embed params differed by only 1,024.
- DDP with full expert replication, no expert parallelism.
- World size 80, bf16, grouped local MoE backend, AdamW, micro-batch 4, grad accumulation 6.
- Paired loader hash test passed for first 100 batches before training.

## Runs

| Pair | Seed | Arm | Tokens | Final checkpoint | Status |
|---|---:|---|---:|---|---|
| pair1 | 1337 | A | 19,766,968,320 | `runs/pair1_A_seed1337_20B_mbs4_80_v2/ckpt_step005027.pt` | complete |
| pair1 | 1337 | B | 19,766,968,320 | `runs/pair1_B_seed1337_final5027_mbs4_80/ckpt_step005027.pt` | complete |
| h4v3 | 2024 | A | 19,766,968,320 | `runs/pair_h4_A_seed2024_20B_mbs4_80_v2/ckpt_step005027.pt` | complete |
| h4v3 | 2024 | B | 19,766,968,320 | `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step005027.pt` | complete |

Pair1 used a 4.69B-token repeated stream; h4v3 used the 20.002B-token h4 tranche. h4v3 eval used the h5-disjoint tranche generated after skipping the h4 prefix by whole documents.

## Knockout

Final h4v3 B checkpoint, answer-NLL knockout minus normal:

| Task | Records | Normal NLL | Knockout NLL | Delta | Positive-delta frac |
|---|---:|---:|---:|---:|---:|
| TriviaQA | 200 | 3.362420 | 3.373400 | +0.010981 | 0.53 |
| PopQA | 200 | 9.733437 | 9.768375 | +0.034938 | 0.58 |

5-shot EM:

| Task | Records | Normal EM | Knockout EM | Retention |
|---|---:|---:|---:|---:|
| TriviaQA | 100 | 0.000 | 0.000 | n/a |
| PopQA | 100 | 0.000 | 0.000 | n/a |

Interpretation: answer-NLL moves in the expected direction at final h4v3, but the effect is small and nowhere near the handoff target of substantial factual collapse. EM is non-informative at floor. This fails the primary knockout PASS criterion.

## Targeted Slices

h4v3 held-out h5, 16 batches. Positive A-B means B is lower NLL.

| Slice | A NLL | B NLL | A-B |
|---|---:|---:|---:|
| Global | 2.737275 | 2.747317 | -0.010043 |
| Repeated 2/3-gram | 1.066815 | 1.069155 | -0.002340 |
| Entity proxy | 4.245794 | 4.293012 | -0.047218 |

Interpretation: B is worse on global, repeated-ngram, and entity-proxy slices. This fails the primary targeted-slice PASS criterion.

## Depth Probe

h4v3 held-out h5, 2,048 positions. Lower earliest layer is better.

| Arm | Mean earliest layer | Median earliest layer | Resolved by layer 18 | Resolved by layer 19 |
|---|---:|---:|---:|---:|
| A | 17.093750 | 19.0 | 0.461914 | 0.614258 |
| B | 17.065430 | 19.0 | 0.456543 | 0.615723 |
| A-B | +0.028320 | 0.0 | +0.005371 | -0.001465 |

Interpretation: B's mean earliest layer is slightly earlier, median is tied, and cumulative resolution is mixed. This is not decisive.

## Gate Diagnostics

Final h4v3 B Engram diagnostics on h5:

| Layer | Alpha mean | Contribution/hidden RMS | Final hidden delta RMS | Last-logit abs delta mean |
|---:|---:|---:|---:|---:|
| 2 | 0.997041 | 0.003611 | 0.064917 | 0.096144 |
| 6 | 0.997382 | 0.012194 | 0.064917 | 0.096144 |

Interpretation: the Engram path is exercised and nonzero. This rules out a dead-path-only failure, but it does not rescue the failed primary criteria.

## Global Loss

Paired FineWeb held-out global loss:

| Seed | Eval split | A | B | A-B |
|---:|---|---:|---:|---:|
| 1337 | h4 global | 2.972447 | 2.975272 | -0.002825 |
| 2024 | h5 global | 2.737275 | 2.747317 | -0.010043 |

The planned 3-seed paired 95% CI is not available. The two completed paired deltas are both negative, so the secondary global-loss signal also does not support Engram here.

## Artifacts

- Raw and aggregate knockout: `results/knockout/`, `results/knockout.csv`
- Slices: `results/slices/`, `results/slices.csv`
- Depth: `results/depth_probe/`, `results/depth_probe.csv`, `results/depth_probe.png`
- Diagnostics: `results/diagnostics/`, `results/gate_diagnostics.csv`
- Loss: `results/loss_table.csv`, `results/loss_curves.csv`, `results/loss_curves.png`
- Downstream/EM summary: `results/downstream.csv`
- Progress trail: `progress/`

## Final Assessment

This reproduction does not verify DeepSeek's Engram claim under the repo plan and current 0.48B-active / 20B-token faithful runs. The most defensible conclusion is:

**Engram is wired and functionally nonzero, but it did not become a load-bearing factual N-gram memory in these runs. Knockout is weak, targeted slices do not improve, and the secondary loss signal is unfavorable/underpowered. Record as NOT VERIFIED rather than PASS.**
