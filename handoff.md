# Engram Verification — Handoff (≤80× H100, ≤24h total, preliminary signal ≤12h)

**Audience:** an autonomous engineering agent that implements and runs this end-to-end.
**Status:** ready to execute. Read §0, then §8 (timeline). Everything needed is here.

---

## ⚠️⚠️⚠️ COLLABORATION RULE — PUSH PROGRESS EVERY 2 HOURS ⚠️⚠️⚠️

**Every 2 hours (and at every milestone), commit & push a progress snapshot to this repo (`github.com/wsl2000/Engram`) so collaborators can follow live.** Do not wait for the run to finish.

Each snapshot must include, but is not limited to:
- **Training logs** (`progress/logs/` — per-step loss/LR/grad-norm/tokens-seen/router-LB/step-time; tail of each run's stdout).
- **Current results so far** (`progress/results/` — partial `loss_table.csv`, any `knockout.csv`/`slices.csv`/`depth_probe` already computed, `loss_curves.png` updated).
- **Status line** in `progress/STATUS.md`: wall-clock elapsed, which run/seed/arm is active, step/tokens done vs target, measured MFU & tokens/s, GPU/node health, **what just finished, what's next, and the ETA**.
- **Any anomaly** (OOM, MFU drop, NaN, knockout-not-collapsing bug signal §10) — flag immediately, don't wait for the 2h tick.

Commit message format: `progress: H<elapsed>h — <one-line status>`. Author **wsl2000 <wsuli615@gmail.com>**. Keep it cheap and frequent; partial/ugly is fine — visibility > polish.

---

## ⚠️⚠️⚠️ TWO-WAY FEEDBACK — `git pull` EVERY ~2 HOURS, CHECK `feedback/` ⚠️⚠️⚠️

A reviewer is watching your `progress/` and will push review notes into **`feedback/`**. This is a closed loop — pushing is not enough, you must also **listen**.

- **Every ~2h (right after you push progress), `git pull` and check `feedback/` for new files.** Urgent items may arrive between ticks — pull whenever convenient.
- Reviewer files are named **`feedback/review-<UTC-timestamp>.md`**, each starting with a top line **`VERDICT: ON-TRACK | ISSUES | BLOCKER`**.
- **On a new feedback file:** read it, **acknowledge in `progress/STATUS.md`** (name the file + what you'll do), and either apply the fix or reply (push `feedback/reply-<UTC>.md`) explaining why not. **Treat `BLOCKER` as stop-and-fix before continuing.**
- Don't silently ignore feedback; an unacknowledged review file is a process failure.

> **Net loop:** executor pushes `progress/` every 2h → reviewer pulls, pushes `feedback/` if off-track → executor pulls every 2h, acks in `STATUS.md`, fixes. Both sides poll ~every 2h; anything urgent is pushed immediately.

---

## 0. Objective (read first)

**Goal.** Empirically verify that DeepSeek's **Engram** (conditional memory via O(1) N-gram lookup) is *effective*: under a strict **iso-parameter, iso-FLOPs** comparison, a small MoE that reallocates ~20–25% of its sparse budget to an Engram table **beats** the same model as pure MoE, and the Engram module is **functionally doing the work** (stores knowledge, deepens the net).

**Why this fits 24h.** The decisive signals — **knockout** (disable Engram in-model) and **targeted-slice loss** — are *within-model / paired* and **immune to cross-run seed noise**, so they need only **one (MoE, Engram) pair**, not a seed sweep. We front-load that pair and evaluate it early ⇒ **preliminary verdict by ~H11**. The (underpowered) global-loss comparison is corroboration only and gets the back half of the budget.

**Non-goals:** no U-shape *curve* (single ρ in the sweet spot); no 27B headline; no matching the paper's *absolute* loss (different corpus — only the **relative** A-vs-B claim is made).

**Success (one sentence):** Engram-knockout causes a large clean collapse on factual tasks **and** targeted-slice loss is clearly better for the Engram arm; the paired global-loss gap corroborates as a secondary signal.

**Scale rationale:** ~**0.48B activated** matches the paper's small-scale regime (§3.1 used 568M/993M activated) — where the effect was *actually measured*, not a toy.

---

## 1. Constraints & run budget

| Item | Value |
|---|---|
| Hardware | **80× H100-80GB SXM**, multi-node. |
| Wall-clock | **≤24h total.** Preliminary (knockout+slices on pair 1) **≤12h**. |
| Runs | **6** = 2 arms × 3 seeds, **front-loaded** (pair 1 first). If MFU/time slips, 2 seeds is an acceptable fallback (seeds only feed the *secondary* loss criterion). |
| Arms | (A) pure MoE `ρ=100%`; (B) Engram `ρ≈77%` (~23% of routed budget → Engram). |
| Seeds | `{1337, 2024, 7}` (pair 1 = 1337). |
| Tokens/run | **~70B** (calibrate to 60–80B in §9). *Reduced from a 48h plan's 120B to fit 24h; trade-off is a slightly weaker loss signal only — knockout/slices are unaffected, and ~70B still fills the ~3.8M-slot Zipf tail adequately.* |

> **The 12h preliminary does not depend on seeds.** It rests on knockout + slices from pair 1 (noise-immune). Seeds are phase 2, for the loss corroboration only.

---

## 2. Experimental design (the invariants that make this valid)

1. **Iso-parameter:** identical total non-embedding params; Engram table params exactly replace removed routed-expert params (§5).
2. **Iso-FLOPs:** `top_k = 6` in both arms ⇒ identical activated params ⇒ identical FLOPs/token; Engram lookup adds negligible FLOPs.
3. **Paired data:** within a seed, arms A and B consume **the exact same token stream, batch-by-batch, same order** (§7.3) — cancels the dominant noise source.
4. **Everything else identical across all runs:** backbone, optimizer, LR schedule, batch, steps, tokenizer, LB loss, precision.
5. **The only variable is the arm** (88 experts ↔ 68 experts + Engram table).

---

## 3. Model configuration (shared backbone)

| Component | Setting |
|---|---|
| Layers | 20 · `d_model` 1280 · **MHA** 16 heads (head_dim 80), FlashAttention-3, RoPE θ=10000 |
| `seq_len` | 2048 |
| Tokenizer | **DeepSeek-V3, 128k vocab** (public in `deepseek-ai/DeepSeek-V3`) |
| FFN | SwiGLU MoE, expert hidden `h_e` 640, **1 shared** + **88 routed (A) / 68 routed (B)**, router top-`k`=**6**, aux LB-loss 0.01 (identical) |
| Embeddings | tied in/out (`128k·1280 ≈ 164M`) |
| Precision | **bf16** (not FP8 — comparability > the ~1.5× speedup; avoids scaling-factor confounds) |
| Optimizer | **Muon** (peak LR 3e-3) — **fallback AdamW** (β 0.9/0.95, wd 0.1, peak LR 1.5e-3) if Muon integration is risky; **identical across all runs**. *(Muon is custom infra; if not already vetted, use AdamW and note the deviation — do not let optimizer choice differ between arms.)* |
| LR sched | cosine → 10% peak, warmup 2% of steps · grad clip 1.0 |
| Global batch | **~4M tokens** (2048 × 2048 seqs; grad-accum to reach it) · init std 0.02, scaled-residual |

**Param accounting (assert in `config_gen.py`):** attn per layer `4·d_model²=6.55M` ×20 = 131.1M (active). Expert `3·d_model·h_e=2.458M`.
- **A (ρ=100%):** FFN `(1+88)·2.458M·20=4.374B`; non-embed ≈ **4.50B**; activated `131.1M+(1+6)·2.458M·20 ≈ 0.475B`. ✅
- **B (ρ≈77%):** drop 88→68 routed ⇒ freed `20·2.458M·20=0.983B`; routed FFN `(1+68)·2.458M·20=3.391B` + Engram **≈0.983B** ⇒ non-embed ≈ **4.50B** ✅ (iso-param); activated **0.475B** ✅ (iso-FLOPs, top_k still 6). **% routed budget → Engram = 0.983/4.374 ≈ 22.5%** (ρ≈77.5%, in the 20–25% sweet spot).

> **No expert-parallel divisibility constraint** here — we replicate experts (no EP, §8), so 88/68 are fine.

---

## 4. Engram module (§5 of source plan, unchanged)

Insert at **layers 2 and 6**; split the ~0.983B budget evenly (~0.49B/site).
**Per site:** N-gram orders `N={2,3}` (causal suffix), hash heads `H=8`, dim per n-gram `d_e=256`, causal conv kernel 4 + SiLU, context-aware gate. Tokenizer-compression **skipped in v0** (optional later).
**Table rows:** tables dominate `2·8·M·256 = 4096·M ≈ 0.49e9` ⇒ **M ≈ 119,600 rows/head/order**; ~1.91M slots/site, ~3.8M total (within the paper's 2.6e5–1e7 range). `proj` (256→1280 ≈0.33M) + gate negligible.

**Forward (key points):** deterministic `poly_hash(token_ids, n, salt=h) % M` per head → gather `nn.Embedding(M,d_e)` (16 tables/site) → mean over heads → sum over orders → `proj` → context gate `α=sigmoid(RMSNorm(h)·RMSNorm(e)/√d)` → `SiLU(causal_conv1d(e))` → `hidden + α·e`. **`knockout=True` must cleanly return `hidden` unchanged** (eval-time only). Hashing must be vectorized (precompute indices on host if it bottlenecks throughput).

---

## 5. Datasets

**Training:** `HuggingFaceFW/fineweb-edu`, subset **`sample-350BT`** — public, clean, knowledge-dense. Tokenize once (DeepSeek-V3 128k) → **mmap shards** packed to 2048 with doc separators. **Stream tokenization from H0, overlapped with training; it only needs to stay ahead of consumption** (80 nodes of CPU keep up easily at 8.3M tok/s). Prefer distinct shards per seed; 350BT ≫ 3×70B so reuse is fine.
*Why not the paper's data: DeepSeek's 262B corpus is undisclosed ⇒ we cannot match absolute loss; our claim is **relative** (A vs B on identical data), unaffected.*

**Eval (these may reference the paper; NEVER train on them):**
| Tier | Sets | Purpose |
|---|---|---|
| Primary loss | **The Pile** test (held out — we train only on FineWeb-Edu, so no contamination) + **FineWeb-Edu held-out val** | the loss axis |
| **Knockout (primary verdict)** | **TriviaQA** (5-shot EM), **PopQA** | Engram on/off collapse |
| **Targeted slices (primary)** | held-out FineWeb-Edu filtered to (a) repeated-2/3-gram continuations, (b) named-entity tokens | concentrate the effect |
| Depth probe | small held-out set | LogitLens / early-exit per layer |
| Downstream (secondary, noisy @0.5B) | MMLU/CMMLU/ARC/HellaSwag/PIQA/WinoGrande/BBH(subset)/GSM8K via `lm-eval-harness` | report, do not gate |
| Long-context (optional) | **RULER** (Multi-Query NIAH, Variable Tracking) **at 32k** | the 84.2→97 showcase, if time |

**Paired loader (non-negotiable):** identical token batches for both arms at a given seed (same shard order, packing, shuffle); arm must not influence the pipeline. **Verify by hashing the first 100 batches of an A-run and B-run at the same seed — must be bitwise identical.**

---

## 6. Training infrastructure

- **DDP with full expert replication. NO Expert Parallelism.** 4.5B non-embed + 0.16B embed bf16 ≈ 9.3GB weights + Muon/Adam states ≈ ~45GB ⇒ fits one 80GB H100. Replicate the whole model per GPU ⇒ **no all-to-all** (the #1 cause of MoE MFU collapse at small scale). Engram tables (~2GB bf16) **on-GPU, replicated; no DRAM offload** (that's a 100B-table inference trick, irrelevant here).
- Activation checkpointing if needed to fit the micro-batch at seq 2048.
- **Target MFU 28–32% (plan 30%).** Checkpoint every **20–30 min** + end of each run.
- **Determinism:** seed torch/cuda/numpy from the run seed; the **paired loader** (not bitwise GPU determinism) is what guarantees the comparison.
- **Logging:** per-step train loss, LR, grad-norm, tokens-seen, router LB stats, step-time; periodic val loss.

**Throughput / token math (confirm in §9):**
```
FLOP/token = 6·N_active = 6·0.475e9 ≈ 2.85e9
80 GPU · 990 TFLOP/s · 0.30 MFU / 2.85e9 ≈ 8.34e6 tokens/s
per-run @70B = 70e9/8.34e6 ≈ 8,400 s ≈ 2.33h   (60B≈2.0h, 80B≈2.67h)
6 runs ≈ 14h training ; + ~2h setup + ~5h eval (some overlapped) + buffer  ⇒  ≈22–23h ≤ 24h ✅
steps/run @70B, 4M global batch = 70e9/4e6 ≈ 17,500 steps
MFU sensitivity: 24% ⇒ ~17h train (still fits) ; 35% ⇒ ~12h train (more buffer)
```
**Scheduling:** runs **sequential, each on all 80 GPUs** (identical world size ⇒ maximal comparability). Never mix world sizes across runs. Total FLOPs are fixed ⇒ all-80-on-one-run-at-a-time is already optimal makespan.

---

## 7. Throughput calibration (BEFORE committing token counts)

1. Build arm A; run **200 steps** on all 80 GPUs at the intended global batch. Measure tokens/s + MFU.
2. Back-fill **tokens/run** to fit §6 with 20% margin (target ~70B; 60–80B all fit 24h). `max_steps = tokens_per_run / 4e6`.
3. Confirm arm B throughput within a few % of A (vectorized Engram gather/hash).
4. Only then launch.

---

## 8. 24-hour timeline (start here)

| Window | Task |
|---|---|
| **H0–2** | Env (PyTorch, FlashAttn-3, Muon/AdamW, lm-eval-harness). **Start streaming tokenization** (FineWeb-Edu→DeepSeek-V3 shards, parallel, must stay ahead). `config_gen.py`: assert iso-param + iso-FLOPs (1 step/arm). **Paired-loader hash-equality test** (§5). **Throughput calibration** (§7) → fix tokens/run. |
| **H2–~H6.7** | **Pair 1 (seed 1337): arm A (~2.33h) → arm B (~2.33h)**, all 80 GPUs, ckpt every 20–30 min. *During B, run a quick knockout on the first B checkpoint (~H5) for an earliest "is the module load-bearing?" read.* |
| **~H6.7–H11** | **PRELIMINARY EVAL — the 12h deliverable.** On pair-1 final ckpts: **(1) knockout** (TriviaQA/PopQA on→off, B arm), **(2) targeted slices** (entity / repeated-n-gram NLL, A vs B), **(3) depth probe**, **(4) paired loss** (Pile + val). → **preliminary verdict per §11** (primary signals already decisive here). |
| **H11–~H20.5** | **Seeds 2024 & 7: 4 runs × ~2.33h ≈ 9.3h** (sequential, all 80 GPUs) for the loss corroboration (carry pair-1). |
| **H20.5–H24** | Final eval across 3 seeds: paired Δ + 95% CI, per-arm mean±std; batch `lm-eval-harness` (secondary); plots; **REPORT.md** vs §11. Buffer / rerun any failed job. |

> **Adaptive use of any slack (executor's call, in priority order):**
> 1. If the H11 preliminary knockout is **weak/ambiguous**, spend phase 2 on **more tokens for pair 1** (extend the first B run) rather than more seeds — the table tail may be under-filled. (Knockout/slices are the verdict; strengthen them first.)
> 2. Else add the 2 extra seeds (loss corroboration) as scheduled.
> 3. Else (time left over) the optional long-context + RULER@32k (§11.5).
> Do **not** spend slack on extra ρ points or longer single runs beyond ~80B at the expense of the primary signals.

---

## 9. Evaluation protocol (exact)

**9.1 Primary loss.** Per-token NLL on (a) Pile test, (b) FineWeb-Edu held-out val. Per run; per arm mean±std over seeds; **paired** Δ = loss_A(seed) − loss_B(seed).

**9.2 Knockout (primary verdict — zero cross-run noise).** Each **Engram-arm** ckpt: eval TriviaQA (5-shot EM) + PopQA **twice** — normal, and with `knockout=True` (contribution zeroed at layers 2&6). Report on→off degradation as a **retention ratio**. *Paper expectation: factual tasks retain ~29%.* Within-model A/B ⇒ immune to seed noise ⇒ valid from pair 1 alone.

**9.3 Targeted slices (primary, low-noise).** Held-out FineWeb-Edu positions: (a) tokens continuing a 2/3-gram seen earlier in the same doc; (b) tokens inside named-entity spans (fast NER). Mean per-token NLL, both arms. Report **slice-gap (A−B)** vs **global-gap**. *Expectation: slice-gap > global-gap.*

**9.4 Effective-depth probe (low-noise).** LogitLens: per layer, project hidden through the tied output embedding; record earliest layer whose argmax = final prediction (or per-layer KL to final). *Expectation: Engram arm resolves at earlier layers.*

**9.5 Downstream (secondary).** lm-eval-harness on the §5 list. Near-floor and noisy at 0.48B — **report, do not gate.**

**9.6 Optional long-context.** Continue-train best B + its A pair ~1–2B tokens at 8–16k (RoPE scaling); eval **RULER @32k** (Multi-Query NIAH + Variable Tracking).

---

## 10. Decision criteria (what counts as verified)

**PASS — "Engram is effective" (both primary signals, available at H12 from pair 1):**
1. **Knockout:** disabling Engram degrades TriviaQA/PopQA substantially — target **≥40% relative EM drop** (ideally toward the paper's ~29% retained).
2. **Targeted slices:** Engram-arm NLL on entity / repeated-n-gram slices clearly lower than pure-MoE, **and slice-gap > global-gap**.

**CORROBORATING — global loss (secondary, by H24 over 3 seeds):**
3. Paired across all 3 seeds, B's val/Pile loss < A in **all 3** pairs and mean paired Δ exceeds the across-seed std. Stats: `Δ_i=loss_A(i)−loss_B(i)`; report `mean(Δ)`, `std(Δ)`, 95% CI `= mean ± 4.303·std/√3` (t, df=2).

**⚠ Power note (be realistic):** with seed σ≈0.008 and n=3, CI half-width ≈ `4.303·0.008/√3 ≈ 0.020` nats, while the *expected* effect is ~0.010–0.015 nats ⇒ **the loss criterion may not reach significance even if the effect is real.** Expected — which is exactly why **knockout + slices are the primary verdict.**

**HONEST NEGATIVE (a valid result):** if knockout shows Engram clearly stores knowledge and the depth probe shows earlier resolution, but the paired loss Δ is within noise → report *"Engram is functionally active (stores knowledge, deepens the net) but its net loss advantage is not statistically resolved at 0.48B / ~70B tokens."*

**BUG SIGNAL (debug before trusting anything):** if knockout does **not** degrade factual tasks, the Engram path isn't exercised (gate saturated, indices wrong, residual not added) — fix wiring before believing any number. *Catch this at ~H5 on the first B checkpoint.*

---

## 11. Known pitfalls & mitigations

| Pitfall | Mitigation |
|---|---|
| MoE MFU collapse (all-to-all) | DDP + full replication, **no EP** (§6). |
| Engram gather/hash bottleneck | vectorize hashing; precompute indices; confirm in §7. |
| Seed noise swamps loss | 3 seeds + **paired** identical stream; primary verdict = knockout/slices. |
| Reduced 70B under-fills the table | adaptive: if H11 knockout weak, add tokens to pair 1 before adding seeds (§8). |
| Absolute loss ≠ paper | expected (different corpus); only **relative** A-vs-B claimed. |
| Config drift | single `config_gen.py`; assert iso-param/iso-FLOPs at every run start; identical world size. |
| Muon integration risk | fallback AdamW; whichever, use it for **all** runs. |
| Tokenization eats the budget | stream from H0, overlapped; only needs to stay ahead of 8.3M tok/s. |

---

## 12. Deliverables
`results/`: `loss_table.csv` (per-run + paired Δ + CI), `knockout.csv` (on/off, retention ratio), `slices.csv` (slice-gap vs global-gap), `depth_probe.png`, `downstream.csv` (secondary), optional `ruler.csv`, `loss_curves.png` (all runs; B should pull below A from mid-training). **`REPORT.md`** — verdict vs §10, with the honest-negative caveat stated explicitly. Plus a one-line note on the two executor judgment calls: tokens/run (from §7) and Muon-vs-AdamW (§3, fixed once for all runs).

---

## 13. Reference numbers (paper, arXiv:2601.07372 — for sanity; do NOT expect to match absolutes)
- Sweet spot: ~**20–25%** of sparse budget → Engram (ρ≈75–80%); ρ≈40% still matched pure MoE.
- Small-scale regimes where the U was measured: `P_tot≈5.7B/P_act=568M`, `P_tot≈9.9B/P_act=993M`; measured loss gap ≈ **0.014 nats**.
- Knockout: factual tasks (e.g. TriviaQA) retain ~**29%** when Engram disabled.
- Module defaults: `N={2,3}`, H=8 hash heads, early insertion (~layer 2) optimal, context-aware gate, tokenizer-compression (~23% vocab reduction; optional here).
- 27B headline (NOT our target): MMLU +3.0, CMMLU +4.0, BBH +5.0, ARC-C +3.7, MATH +2.4, Multi-Query NIAH@32k 84.2→97.0.
- Sources: paper `arXiv:2601.07372` / official (mocked-demo) `github.com/deepseek-ai/Engram`; independent small-scale impl `github.com/AutoArk/TinyEngram`.

**Out of scope:** the structured / VSA ("binding") value extension — Engram uses a flat value exclusively; that extension is future work and begins only after this flat verification passes.

---

**End of plan.** Start at §8, H0. Two judgment calls left to the executor: (1) exact tokens/run (set by §7 calibration); (2) Muon vs AdamW (§3, fix once for all runs). **The 12h preliminary stands on knockout + slices from pair 1; seeds are corroboration.**
