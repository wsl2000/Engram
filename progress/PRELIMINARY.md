# Preliminary Verdict - H10.3

## Verdict

**NOT VERIFIED / INCONCLUSIVE for pair 1.** The pair-1 20B-token endpoint does **not** satisfy the handoff PASS criteria: Engram knockout does not degrade TriviaQA/PopQA, and targeted slices are mixed rather than clearly better for the Engram arm.

This is **not** a clean claim that Engram does not work. The Engram path is active and its contribution grew by the endpoint, but the pair-1 training stream used only 4.69B unique tokens sampled with replacement to 19.77B tokens. The current best interpretation is repeated-data washout / below the data threshold where Engram has a distinct job.

## Pair-1 Endpoint

- A checkpoint: `runs/pair1_A_seed1337_20B_mbs4_80_v2/ckpt_step005027.pt`
- B checkpoint: `runs/pair1_B_seed1337_final5027_mbs4_80/ckpt_step005027.pt`
- Tokens per arm: 19,766,968,320
- Optimizer/precision/world size: AdamW, bf16, 80 GPUs, DDP full expert replication, grouped local MoE backend
- Data caveat: pair-1 consumed the 60-shard 4.6908B-token stream with replacement. Eval used a separate h4 tokenization directory, but the current manifests do not include document IDs, so document-level disjointness from pair-1 cannot be proven after the fact.

## Knockout - Primary

Answer-NLL knockout minus normal:

| Task | Records | Normal NLL | Knockout NLL | Delta |
|---|---:|---:|---:|---:|
| TriviaQA | 200 | 3.615770 | 3.609136 | -0.006633 |
| PopQA | 200 | 9.611481 | 9.592465 | -0.019016 |

5-shot EM:

| Task | Records | Normal EM | Knockout EM | Retention |
|---|---:|---:|---:|---:|
| TriviaQA | 100 | 0.000 | 0.000 | n/a |
| PopQA | 100 | 0.000 | 0.000 | n/a |

Interpretation: no factual collapse. EM is still at floor, and answer-NLL moves slightly in the wrong direction on both tasks.

## Targeted Slices - Primary

Held-out h4 FineWeb-Edu, 16 batches, same eval seed for A/B. Positive A-B means B is better.

| Slice | A NLL | B NLL | A-B |
|---|---:|---:|---:|
| Global | 2.972447 | 2.975272 | -0.002825 |
| Repeated 2/3-gram | 1.083465 | 1.107236 | -0.023771 |
| Entity proxy | 4.471435 | 4.455587 | +0.015848 |

Interpretation: entity-proxy tokens favor B, but repeated n-grams and global loss favor A. This does not meet the slice criterion of clear targeted-slice improvement with slice-gap > global-gap.

## Depth Probe

Held-out h4, 2,048 sampled positions. Lower earliest layer means earlier resolution.
For the cumulative resolved columns, negative A-B means B resolved more positions by that layer.

| Arm | Mean earliest layer | Median earliest layer | Resolved by layer 18 | Resolved by layer 19 |
|---|---:|---:|---:|---:|
| A | 16.455078 | 19.0 | 0.495605 | 0.650879 |
| B | 16.454102 | 18.0 | 0.502930 | 0.664551 |
| A-B | +0.000977 | +1.0 | -0.007324 | -0.013672 |

Interpretation: B median is one layer earlier and layer-18/19 cumulative resolution is slightly higher, but mean depth is effectively tied. Supportive at most, not decisive.

## Gate / Contribution Diagnostics

The gate is not suppressed: alpha is saturated near 1.0 at both Engram layers. Contribution is small but grows by the endpoint.

| Checkpoint | Layer | Alpha mean | Contribution/hidden RMS | Final hidden delta RMS | Last-logit abs delta mean |
|---|---:|---:|---:|---:|---:|
| B step 959 | 2 | 1.000000 | 0.001103 | 0.041301 | 0.050603 |
| B step 959 | 6 | 0.999051 | 0.003903 | 0.041301 | 0.050603 |
| B step 5027 | 2 | 1.000000 | 0.001303 | 0.079599 | 0.119674 |
| B step 5027 | 6 | 0.999448 | 0.008297 | 0.079599 | 0.119674 |

Interpretation: this is not a dead-path bug. The path changes hidden/logits and grows during training, but it is not load-bearing for factual recall in the repeated-data pair-1 regime.

## Decision vs Handoff Criteria

- PASS criterion 1, knockout: **fail**. No substantial degradation; answer-NLL improves slightly under knockout.
- PASS criterion 2, targeted slices: **fail/mixed**. Entity proxy favors B, repeated n-gram and global favor A.
- Depth: weakly supportive in median only; not enough to rescue primary failures.
- Global loss: secondary and underpowered; pair-1 h4 global A-B is -0.002825, so B is slightly worse on this sample.

## Next Action

Do not spend phase 2 on repeated-stream seeds. Following the handoff adaptive rule and `feedback/review-20260629T0356Z.md`, pivot to a fresh h4 unique-data paired run. I removed only the obsolete B step-959 checkpoint after saving diagnostics, restored free space, and launched h4 A/seed 2024 as Slurm job `165367`. If it completes, launch h4 B/seed 2024 with the exact same h4 token stream, world size, batch, optimizer, precision, and 5,027-step endpoint. For h4-pair evaluation, do **not** reuse h4 as held-out; create a new document-ID-aware held-out tranche or run token/ngram decontamination first, per `feedback/review-20260629T0432Z.md`.
