# Engram Reproduction & Verification — Handoff

**Target paper:** DeepSeek, *"Conditional Memory via Scalable Lookup: A New Axis of Sparsity for LLMs"* (Engram), arXiv:2601.07372.
**Audience:** a team with a multi-node H100 cluster (≤80× H100-80GB) whose single job is to **reproduce / verify Engram itself**.
**Reproduction target:** the **flat n-gram conditional-memory** value on an **MoE backbone** — the U-shape sparsity-allocation law and the downstream / knockout gains. The structured / VSA ("binding") value extension is **out of scope** (§7).

> This doc was assembled by an upstream team that ran small-scale precursors (and hit the off-regime traps in §6). Every paper number below was transcribed from arXiv:2601.07372 Table 1/2 + the official repo; where the paper does **not** state something it is marked **[ASSUMPTION]** — verify against the paper's Appendix A before committing compute.

---

## 1. Goal and definition of "reproduced"

**What Engram claims.** Add a second axis of sparsity to an MoE LLM: a huge, sparsely-accessed **n-gram → value lookup table** (conditional memory) storing parametric knowledge. At iso-activated-params and iso-FLOP it **barely moves pretraining loss** but materially improves **downstream knowledge / reasoning / long-context** benchmarks, and the knowledge provably lives *in the table* (a knockout test collapses factual recall).

**Success criteria, ordered cheapest / most-diagnostic first.** A reproduction succeeds if it hits these:

| Pri | Criterion | Grounded target |
|---|---|---|
| **1. U-shape allocation law** (cheapest; architecture validation) | Sweep Engram's share of the **sparse** budget; optimum at **20–25% Engram / 75–80% MoE**; pure-MoE strictly worse; curve turns up by ρ≈0.5. | The **portable target is the *shape* + the Δ at the optimum ≈ −0.014** val loss vs pure-MoE in the small/in-regime sweep. (Paper's sweep-point absolutes 1.7248→1.7109 are **token-budget-specific**, not a number to hit.) |
| **2. Loss deltas** (iso-param, iso-FLOP, 262B tok) | Both in-distribution **and** held-out gaps are *small* — this is expected, not a failure. | val loss **1.634 → 1.622 (Δ −0.012)**; held-out **Pile 1.960 → 1.950 (Δ −0.010)**. Engram-40B reaches 1.610. **Both gaps are ~0.01.** (The often-quoted 2.091 Pile number is **Dense-4B**, NOT the iso MoE-27B baseline — do not use it.) |
| **3. Downstream deltas** (Engram-27B vs iso MoE-27B; Table 1, exact) | Reasoning + long-context are the load-bearing, hardest-from-noise gains. | BBH **50.9→55.9 (+5.0)**, CMMLU **57.9→61.9 (+4.0)**, ARC-C **70.1→73.8 (+3.7)**, MMLU **57.4→60.4 (+3.0)**, HumanEval **37.8→40.8 (+3.0)**, MATH **28.3→30.7 (+2.4)**, GSM8K **58.4→60.6 (+2.2)**, TriviaQA **48.8→50.7 (+1.9)**. **Long-context (RULER 32k, after YaRN stage §3.4):** NIAH Multi-Query **84.2→97.0 (+12.8)**, Variable Tracking **77.0→89.0 (+12.0)**. |
| **4. Knockout** (decisive mechanistic verifier) | Disable the Engram read at inference: factual recall must collapse, reading-comprehension must survive. | **Retention ratios** (proxy-robust): TriviaQA retention **≈29%**, factual tasks **29–44%**, RC tasks **81–93%**. (e.g. TriviaQA EM ≈ 50.7 × 0.29 ≈ **14.7** — that absolute is *derived*, gate on the ratio.) If knowledge does **not** collapse → the table isn't storing knowledge → **reproduction FAILED regardless of loss.** |

**The loss axis is weak by design.** The pretraining-loss/BPB gain is ~0.01–0.014 even at 27B; **a near-null BPB neither confirms nor refutes anything.** Do **not** optimize or adjudicate on BPB alone — the durable verdict is **downstream + knockout**.

---

## 2. The Engram module (implement faithfully)

Per token, hash the local n-gram context into several large embedding tables, gather + mix the retrieved values, gate them, add to the residual. Tables are sparsely accessed (`K × #orders` rows/token) and can live in host DRAM.

- **N-gram orders:** bigram + trigram (max n = 3).
- **Hash heads:** **K = 8** per order, each into a **prime-sized** table (distinct primes per head to decorrelate collisions); multiplicative-XOR hash.
- **Value dim:** `d_mem` = **[ASSUMPTION ≈1280; verify Appendix A]**.
- **Per-token gate:** `α = sigmoid( RMSNorm(h)·RMSNorm(k) / sqrt(d) )` (scalar, from hidden `h` and retrieved `k`).
- **Depthwise CAUSAL conv:** kernel **w=4**, dilation = max n-gram order, **SiLU**. (Must be causal — no future leakage.)
- **Flow:** `K=8 EmbeddingBag gathers per order → concat → depthwise causal conv(w=4, SiLU) → proj → d_model → scalar gate α → residual add`.
- **Inject layers:** **[2, 15] of 30**.
- **Table optimizer:** Engram embeddings in their **own param group**, **weight-decay 0**, LR **[ASSUMPTION ×5 backbone base LR; verify]**; tables **CPU-resident** (pinned host DRAM, async H2D), **excluded from the GPU distributed optimizer**.

**Official code (and its limit):** `github.com/deepseek-ai/Engram` ships only `engram_demo_v1.py` — a data-flow demo with **MOCKED** Attention/MoE/conv, **no training configs / weights / eval harness**. Use it to confirm tensor shapes only; **budget a full re-implementation.**

---

## 3. Compute plan on ≤80× H100 (80GB)

### 3.1 Stack
**Megatron-Core MoE + Transformer-Engine FP8** (the mature H100 stack with grouped-GEMM experts, EP/TP/PP, DeepSeek-style aux-loss-free balancing, distributed optimizer, and a per-layer `ModuleSpec` hook). NeMo wraps the same core; MaxText/OLMoE not recommended as the engine.

**Insert Engram via the per-layer spec:** give layers **2 and 15** a custom `ModuleSpec` whose `TransformerLayerSubmodules` append an `EngramRead` (the §2 module, host-DRAM EmbeddingBag) after the MLP. Megatron's forward carries `hidden_states`, not `input_ids`, so **compute the bi/tri-gram hash-ids once at the embedding step and pass them as an explicit extra forward arg threaded to layers [2,15]** (passing as a forward arg — not stashing on the module — survives activation-recompute cleanly; add a Step-0 test with recompute ON).

**Optimizer:** use Megatron **distributed-Adam** for the backbone (turnkey). *The paper reports Muon for the backbone; Muon on Megatron is a non-trivial custom dependency (sharded Newton-Schulz must coexist with EP/TP + the separate Adam group for CPU tables). Treat backbone-Adam as an explicit, documented deviation, or budget Muon as custom infra + Step-0 tests.* **[ASSUMPTION/deviation — state your choice.]**

### 3.2 Hard constraints / gotchas (do not skip)
- **EP divisibility (launch blocker):** Megatron asserts `num_routed_experts % EP == 0`. With **EP=8**, routed-expert counts **must be multiples of 8** → use **104 or 112** (sweep model) and **56 (Engram-27B) / 72 (iso MoE-27B)**. Do **not** drop EP to a non-8 divisor (breaks the single-node-NVLink all-to-all plan).
- **MoE MFU:** fine-grained MoE spends **<50% of time in GEMMs** → **budget 30–40% BF16 MFU**, not 50%.
- **FP8 reality:** FP8 only speeds the GEMM fraction; end-to-end ≈ **1.15–1.3×**, *not* the 2× peak, and FP8 grouped-GEMM over many small fine-grained experts can give **<1.15× (occasionally none)**. **Validate the FP8 grouped-GEMM speedup empirically in Step 1 before trusting the sweep schedule; if <1.15×, fall back to BF16 and re-budget.** All FP8 wall-clocks below are padded ~20%.
- **Balancing:** `--moe-router-enable-expert-bias --moe-router-bias-update-rate 1e-3 --moe-router-dtype fp32`, grouped-GEMM on.
- **Keep PP=1** so the [2,15] Engram layers + hash-id side-tensor stay on every rank.
- **Tables CPU-resident & out of the GPU optimizer.** The paper's ~2.8% offload penalty is *their optimized overlapped impl*; a from-scratch CPU-EmbeddingBag + async H2D + CPU-Adam path is the **main perf risk** — **micro-benchmark the overlapped H2D/D2H path in Step 0 and gate the schedule on a measured penalty (<~10%)**.

### 3.3 Config math
Train FLOPs ≈ `6 · N_active · D_tokens` (**iso-FLOP only to within this approximation**; the Engram conv + `d_mem→d_model` proj add a small, uncounted overhead — account for it when sizing the MoE arm if you want strict parity). H100 SXM peak 989.5 TF BF16; **40% MFU ⇒ ~396 TF/GPU BF16; realistic FP8 ⇒ ~1.2× ≈ ~475 TF/GPU.**

**Sweep model (paper's smallest in-regime point — do not go smaller; below ~568M-active the effect is noise):** **568M activated / ~5.7B total**, **104 or 112 routed + 2 shared experts** (DeepSeekMoE fine-grained, sparsity ~10×), DeepSeek-V3 128k tokenizer, seq 4096.
**[ASSUMPTION — the paper does NOT publish the sweep model's layers / d_model / shared-routed split (only Pact=568M, Ptot≈5.7B, fine-grained experts).** Do not assume it reuses the 27B's 30L/d2560 geometry — that is internally inconsistent (more experts at the same geometry ⇒ more total params, not ~5× fewer). **Choose layers / d_model / per-expert FFN width so that 568M active + your routed count reconciles to ~5.7B total, and record the choice.**]

### 3.4 The three compute stages (in order)

**Config A — POSITIVE CONTROL / sensitivity (run FIRST; gates everything).**
- Sweep model; **60B tokens**; arms = Engram-frac **{0 (pure MoE), 0.25 (flat)} × ≥5 paired seeds** (see §3.5 — 2 seeds is underpowered).
- Layout/run: 1 node (8×H100), **EP=8, TP=1, PP=1**, FP8.
- ~**16–18h FP8 / ~22h BF16** per run; 10 runs (5 seeds × 2 arms) on 5 nodes (40 H100) ≈ **<1 day**.

**Config B — RECOMMENDED in-regime U-shape sweep.**
- Sweep model; **100B tokens** (or 60B for speed/margin).
- Sweep Engram-frac **{0, 0.1, 0.2, 0.25, 0.4, 0.5}** (brackets the 0.2–0.25 optimum + confirms the up-turn) **× 2 paired seeds = 12 runs** (carry seeds from Config A where possible).
- Layout/run: 1 node = 8×H100: **EP=8, TP=1, PP=1, attention-DP=8**, grouped-GEMM, NVLink all-to-all, FP8, distributed optimizer; tables on host DRAM.
  - **Memory must be sized, not asserted:** with global batch ~1280 seqs over DP=8 ⇒ ~160 seqs/rank/step ⇒ **mbs 1–2 + grad-accum ~80–160**, **selective/full activation recompute**, and **fused/chunked cross-entropy** for the 128k head (the logit spike OOMs otherwise). Confirm <80GB/GPU before launching.
- ~**1.2–1.3 days/run (100B FP8)** / ~14–16h (60B FP8).
- **Parallelize:** 80 H100 = 10 nodes ⇒ run **10 concurrent, hold 2 nodes** for reruns ⇒ the 12-run sweep ≈ **~1.5–2 days** (one wave + a short second wave). Job array, 1 run/node.

**Config C — Main 27B (only after A+B pass; needed for criteria 2/3/4).**
- **Engram-27B** = 3.8B activated / ~26.7B total (**56 routed + shared experts** + ~5.7B table); **iso MoE-27B** = 3.8B activated, **72 routed experts** **[verify 72 vs Appendix A]**; strictly iso-activated-param + iso-FLOP (within §3.3 caveat), paired seeds, **262B tokens**.
- **Layout (must be specified, not skipped):** **EP=8 intra-node (NVLink) × DP=10 inter-node × PP=1**, **TP=1 or 2**, distributed optimizer. GPU-resident backbone ≈ **26.7B − 5.7B(CPU table) ≈ 21B** params + Adam/FP32 master sharded over DP; **verify per-GPU < 80GB** (replicated attention/embeddings/shared-experts at TP=1 + sharded routed experts + optimizer states); raise TP to 2 if tight. Set mbs/grad-accum to hit the 27B global batch.
- **Cost (corrected):** `6 · 3.8e9 · 2.62e11 = 5.97e21 FLOP` ≈ **~17.5× one 100B sweep run** (not "100×"). At ~475 TF/GPU FP8 × 80 GPU ⇒ **~1.7 days/run** (~3 days BF16@30%). **Both arms + ≥2 seeds + the YaRN stage + eval ≈ ~1 week wall** (not "multi-weeks"). *Note: the full Config-B sweep (~3.4e21 FLOP) is ~57% of one 27B run — the sweep's advantage is **wall-clock parallelism + go/no-go value**, not raw FLOP.*

**Long-context extension (REQUIRED for the NIAH/VT criteria; do not skip).** The paper extends context with **YaRN to 32768** for **~5000 steps / ~30B high-quality long-context tokens** *after* the 262B pretrain. Add this as an explicit stage on both 27B arms (small vs the main run) before any long-context eval. **Eval RULER at 32k** (the paper's NIAH +12.8 / VT +12.0 are 32k numbers — not 50k).

### 3.5 Sensitivity gate — calibrated correctly (critical)
**Do NOT gate on a fixed loss delta** (the paper's *largest* loss effect is 0.0139 and the 27B in-dist gap is 0.012 — both **below** a single-run paired-seed noise floor of ~0.015; a 2-seed magnitude gate would reject a *faithful* reproduction). Instead:
- **Drive the noise floor below the effect with seeds:** the SE of the mean falls ~1/√n ⇒ budget **~5–8 paired seeds** for Config A; estimate the floor empirically from the **ρ=0 (pure-MoE) paired-seed spread**.
- **Gate on the *mean* Δ with a CI that excludes 0**, OR (preferred) make the positive control the **U-shape *shape*** (optimum reliably below ρ=1 across paired seeds + up-turn by ρ≈0.5), not any single magnitude.
- If the shape/CI is inconclusive at this scale: **record "below sensitivity; no verdict"**, add tokens/seeds, and **do not** proceed to Config C.

---

## 4. Datasets

DeepSeek's corpus is private; use knowledge-rich public proxies carrying a real long-tail (Engram's benefit is the **rare-n-gram tail**, which exists only at ~100B-token scale).

**Training (target ~100–262B tok):**
- **Recommended:** **FineWeb-Edu** (`HuggingFaceFW/fineweb-edu`, `sample-350BT`) as the primary knowledge-dense source + **DCLM-baseline** (`mlfoundations/dclm-baseline-1.0`) for breadth (MMLU/BBH).
- **Single drop-in:** `cerebras/SlimPajama-627B` (cleaned/deduped), stream ~200B.
- **Avoid** raw RedPajama-v2 unless you run the full filter/dedup.
- **⚠ Hold the eval probe OUT of training:** **do NOT** train on The Pile if you use Pile loss as the held-out probe (contaminates it). If you want a Pile probe, use a split provably disjoint from training and **decontaminate (n-gram overlap filter)**; document the procedure.

**Tokenizer.** **DeepSeek-V3 tokenizer** (public in `deepseek-ai/DeepSeek-V3`, `tokenizer.json`, ~128k BPE) for the exact regime; proxies: Llama-3 (128k, gated) or GPT-NeoX-20B (~50k, license-free). **BPB = bits_per_token / bytes_per_token**, bytes/token measured on **your own held-out split**.

**Eval (EleutherAI lm-evaluation-harness, `pip install lm-eval`):**
- Turnkey: `lm_eval --tasks mmlu,bbh,triviaqa,nq_open,lambada_openai,ruler`.
- **NIAH = the RULER group** (`niah_*`, variable-tracking, etc.); **set RULER length to 32k** to match the paper.
- **BBH:** pick one variant (`bbh_cot_fewshot` recommended) and keep it fixed across arms.
- **Long-tail factual:** add **PopQA** (`akariasai/PopQA`, ~14k long-tail entity Qs) via a small custom YAML (`--include_path`); optionally LAMA cloze.
- **RC for the knockout-survival check:** use an RC task that **is in the suite** (e.g. `race`, or an MMLU humanities subset) for the 81–93% retention band — **do not** rely on `C3` unless you add it (it is not in the default suite).
- **MMLU note:** abstract says +3.4, Table 1 says **57.4→60.4 (+3.0)** — use Table 1.

---

## 5. Step-by-step protocol (each step has a pass/fail gate)

0. **Build & unit-test `EngramRead` (1 node).** Causal conv has no future leakage; K=8 distinct primes; scalar gate; tables on pinned CPU + async H2D, excluded from GPU optimizer; separate param group (wd 0); hash-id side-tensor reaches [2,15] **and survives activation-recompute**; micro-benchmark the offload penalty (<~10%); validate FP8 grouped-GEMM speedup (≥1.15× or fall back to BF16). *Pass:* numerics finite, shapes match the demo, offload + FP8 within budget.
1. **Sensitivity gate (Config A).** *Pass:* U-shape shape / mean-Δ CI per §3.5. *Fail:* "below sensitivity, no verdict" → add tokens/seeds, **stop**.
2. **U-shape sweep (Config B).** Plot val loss vs ρ. *Pass:* optimum at 20–25% Engram, pure-MoE worse, up-turn by ρ≈0.5, Δ≈−0.014 at optimum.
3. **Main 27B pretrain (Config C) + iso baseline.** *Pass:* val ~1.634→1.622 **and** held-out Pile ~1.960→1.950 — **both ~0.01** (small is expected; the *baseline pairing* must be the iso MoE-27B, not Dense-4B).
4. **YaRN long-context extension (32k)** on both arms.
5. **Downstream eval** (lm-eval + PopQA + 32k RULER). *Pass:* §1 pri-3 deltas within noise; **BBH (+5.0) and NIAH Multi-Query (+12.8) are load-bearing.**
6. **Knockout.** Disable the Engram read; re-eval. *Pass:* retention ratios in §1 pri-4 (factual collapses, RC survives). *Fail:* knowledge doesn't collapse ⇒ **reproduction failed.**

---

## 6. Hygiene + what we learned the hard way (read before launching)

**THE SENSITIVITY RULE.** Check the **positive control first** (flat-Engram is the known-good control). If it doesn't clear the noise floor, the assay is *below sensitivity* — **record the number, draw no conclusion.** Separate **observation** (always record) from **claim** (gated on: control fires + run complete + ≥enough seeds + ablations). A null below sensitivity says nothing.

**Mandatory hygiene (omit one ⇒ you redo a known mistake):**
- **Iso-activated-param AND iso-FLOP (within §3.3) AND iso-memory** — pin the sparse budget identical across arms; Engram-27B trades routed experts for the table, so the baseline must spend the same budget (the EP-divisible 56/72 split).
- **Paired seeds** (same seed/data/val order across matched arms); **enough seeds** that the floor < the effect (§3.5).
- **Report BOTH** the no-tax axis (BPB ≈ tie, expected) and the thesis axis (downstream + knockout, must separate). **Never adjudicate on BPB alone.**
- **Knockout** as the mechanistic check — note its co-adaptation confound (it conflates "info removed" with "co-adapted pathway deleted"); corroborate with the loss-gap + downstream, don't rest the verdict on it alone.

**Off-regime traps we already hit — do NOT repeat (this is the compute we wasted):**
- **Dense backbone instead of MoE** → no sparse budget to allocate → no U-shape exists. Engram is an MoE-regime claim.
- **Arbitrary fraction of *total* params (we used 45–73%)** instead of a **20–25% *sparse-budget* split.** The law is about the *sparse* budget.
- **Toy scale** (≤124–150M activated and/or <2.8B tokens): every such run washed into noise (backbone memorizes the small n-gram set itself). Our `moe_engram_v2` (150M-act / 2.8B tok) and a tiny `nanoGPT+Engram` (100M tok) both sat at the noise floor → "recorded, no verdict"; an independent ~100M-token study saw no consistent gain either. **The binding constraint is DATA (~100B tokens for the rare-n-gram tail), not model size.** 8×A100 / dense / toy is positive-control-only at best.
- **Process:** one-page design doc + red-team review before any large (Config C) launch.

---

## 7. Risks & out-of-scope

**Risks:** weak BPB axis (expected near-null; verdict is downstream+knockout) · below-sensitivity false-negative (→ §3.5 + §6) · unfair non-iso baseline false-positive (→ §6) · mocked official repo (full reimpl) · CPU-offload path is the main perf risk (→ Step 0) · FP8 grouped-GEMM may not speed fine-grained MoE (→ Step 0) · proxy-corpus mismatch ⇒ **judge by deltas & signatures (U-shape, knockout collapse), not absolute scores** · knockout co-adaptation confound.

**Out of scope (one line).** The **structured / VSA / role-filler ("binding") value** is NOT part of this reproduction — Engram uses a **flat value exclusively**; the structured value is novel, untested (status OPEN), and only begins *after* the flat U-shape reproduces. Do not carry a structured arm / writable store / multi-hop / resonator into this work.

---

## 8. First-week checklist
- [ ] **D1–2:** Implement `EngramRead` (§2) + unit tests (§5 Step 0): causality, K=8 distinct primes, scalar gate, pinned-CPU tables + async H2D excluded from GPU optimizer, separate param group, side-tensor survives recompute. Cross-check shapes vs `engram_demo_v1.py`.
- [ ] **D1–2 (parallel):** Stand up Megatron-Core MoE + TE FP8; build the **568M/5.7B** sweep config (**EP=8, routed=104/112, +2 shared, TP=1, PP=1**, grouped-GEMM, fp32 router, aux-loss-free bias); splice Engram `ModuleSpec` at [2,15]; **reconcile the small-model geometry to ~5.7B total and record it**. Choose & document the **backbone optimizer (distributed-Adam vs Muon)**.
- [ ] **D2:** Tokenizer (DeepSeek-V3) + data pipeline for FineWeb-Edu/DCLM (**Pile held out**); tokenize ≥60B tokens; verify held-out split + bytes/token.
- [ ] **D2 (gate infra):** micro-benchmark the offload H2D/D2H + CPU-Adam path (<~10%); validate FP8 grouped-GEMM speedup (≥1.15× or fall back to BF16).
- [ ] **D3:** Run **Config A** (≥5 paired seeds, 40 H100, <1 day). Apply the **§3.5 sensitivity gate** (shape / CI, not a fixed Δ).
- [ ] **D3:** One-page design doc + red-team before any larger launch.
- [ ] **D4–5:** If gate passes, launch **Config B** (12 runs, ~1.5–2 days, 100B FP8). Stand up lm-eval (`mmlu,bbh,triviaqa,nq_open,lambada_openai,ruler@32k`) + PopQA YAML + the knockout intervention code path; dry-run on a checkpoint.
- [ ] **D5–6:** Plot U-shape (val vs ρ); confirm optimum 20–25% Engram, up-turn by ρ≈0.5, Δ≈−0.014. **Go/no-go memo** for Config C.
- [ ] **If go:** schedule **Config C** (Engram-27B vs iso MoE-27B, 262B tok, ~1 week incl. **YaRN 32k extension** + eval + knockout) per §3.4 / §5 Steps 3–6.
