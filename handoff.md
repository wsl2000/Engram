# Engram Verification — Handoff v2 (128× H100, sensitivity-first, designed to VERIFY)

**Audience:** an autonomous engineering agent that implements and runs this end-to-end.
**Status:** ready to execute. Read §0 → §1 (what failed last time) → §3 (the verification ladder) → §11 (timeline).
**Design goal (changed from v1):** *be CERTAIN to verify Engram as a load-bearing factual memory — even if the
natural loss/BPB effect is smaller than the paper.* We buy certainty with (a) a real **data regime** (≥200B
**unique** tokens, robustly tokenized as a hard gate), (b) a **controlled, powered injected-fact knockout** that
must fire if the mechanism works, and (c) a **throughput gate** so we actually reach the token target.

---

## ⚠️⚠️⚠️ COLLABORATION RULE — PUSH PROGRESS EVERY 2 HOURS ⚠️⚠️⚠️
**Every 2h and at every milestone, commit & push a progress snapshot to `github.com/wsl2000/Engram`.** Include:
training logs (`progress/logs/`), partial results (`progress/results/`), a `progress/STATUS.md` status line
(wall-clock, active run/seed/arm, step/tokens vs target, measured MFU & tok/s, health, what just finished / next /
ETA), and **any anomaly immediately** (OOM, MFU drop, NaN, knockout-not-collapsing). Commit msg:
`progress: H<elapsed>h — <one-line>`. Author **wsl2000 <wsuli615@gmail.com>**. Partial/ugly is fine — visibility > polish.

## ⚠️⚠️⚠️ TWO-WAY FEEDBACK — `git pull` EVERY ~2 HOURS, CHECK `feedback/` ⚠️⚠️⚠️
A reviewer pushes notes into **`feedback/review-<UTC>.md`** (top line `VERDICT: ON-TRACK | ISSUES | BLOCKER`).
After each progress push, **`git pull` and read `feedback/`**; **acknowledge in `STATUS.md`** (name the file + your
action); apply the fix or reply via `feedback/reply-<UTC>.md`. **Treat `BLOCKER` as stop-and-fix.** An
unacknowledged review file is a process failure.

---

## 0. Objective
**Verify DeepSeek Engram (arXiv:2601.07372):** under a strict **iso-parameter / iso-FLOP** comparison, an MoE that
reallocates ~20–25% of its sparse budget to an Engram N-gram memory (arm **B**) is a **functioning, load-bearing
factual memory** vs the same model as pure MoE (arm **A**). **Verification = the Engram path provably stores and
serves rare factual N-grams**, shown by a **knockout collapse** that is *controlled and statistically powered*,
not left to chance on natural data.

**What "certain" means here.** We do **not** rely on Engram spontaneously winning on natural TriviaQA/PopQA
(it did not, last time — §1). We give Engram the exact job it is designed for — storing **rare** factual N-grams —
via a **controlled injected-fact set** in the rare regime, and test, with enough items to be ~100%-powered,
whether **knockout collapses recall of those facts in B**. Our own small-scale `kb-inject` control already showed
the mechanism does this (knockout → chance); this handoff reproduces that **inside the real pretraining stack at
scale**, which is the faithful, certain verification. Natural-data knockout/slices/loss are reported as the
**paper-level bonus**, not the pass condition.

**Success (one sentence):** in B, **knockout collapses recall of the injected rare facts** (B-normal ≫ B-knockout,
many-σ), while A (no Engram) is knockout-invariant — i.e. Engram is the load-bearing store; natural slices/loss
corroborate in the expected direction.

---

## 1. What FAILED in the v1 run (read — do not repeat)
The H22 run finished **NOT VERIFIED**, but the report is honest it was **below sensitivity**, for three concrete
reasons. v2 fixes each:

| v1 failure (from `REPORT.md` / `progress/`) | Root cause | v2 fix |
|---|---|---|
| Only **4.7B unique tokens** (pair1 repeated to 20B) | **on-the-fly HF tokenization hit repeated 504s** → stream starved | **§5 DATA GATE:** download + tokenize **offline** to ≥**200B unique** tokens, **verify counts before any training**. No streaming-and-hope. |
| **20B tokens/arm** actual vs 70B planned | **MFU 9.26%** (`STATUS`: 2.57M tok/s vs 8.34M target) forced step cut | **§7 MFU GATE:** must reach **≥30% MFU** (diagnose the 9% first) or STOP; 128 GPUs + token-driven schedule (no hard 24h cap). |
| Knockout weak (+0.011 NLL), slices unfavorable | natural facts too sparse at 20B for Engram to become load-bearing; test **underpowered & uncontrolled** | **§3/§4 injected-fact knockout:** controlled rare facts + **F≈5,000** items ⇒ ~100% power; certain to fire if mechanism works. |

The v1 **mechanism was active** (gate α≈1.0, contribution grew — not a wiring bug). So the fix is sensitivity, not
re-architecting. Keep v1's faithful model/Engram config and invariants (§6/§8); change data, throughput, and the test.

---

## 2. Budget & philosophy
| Item | Value |
|---|---|
| Hardware | **128× H100-80GB SXM**, multi-node. |
| Philosophy | **Sensitivity-first.** The **token target drives the schedule**, not a wall-clock cap. Better to spend a day on tokenization than to under-fill the table again. |
| Wall-clock | **~3–4 days** expected (tokenization + MFU tuning + runs + eval). No artificial 24h cap (that cap caused the 20B truncation). |
| Tokens/arm | **≥200B unique** (2× the ~100B regime threshold, for margin). Drawn from a ≥300B-unique tokenized pool so seeds use distinct shards. |
| Runs | **2 arms × 3 seeds** `{1337,2024,7}` = 6, **plus** the injected-fact pair (can reuse seed-1337 pair if facts are in its stream). Front-load pair-1 + injected facts. |
| Optimizer | **AdamW** (proven on this stack; Muon only if already vetted — never differ between arms). |

**Compute sanity (128 H100, ~0.475B active, 35% MFU):**
```
FLOP/token = 6·N_active ≈ 6·0.475e9 = 2.85e9
128·990e12·0.35 / 2.85e9 ≈ 15.6e6 tok/s   ⇒  200B tokens/arm ≈ 3.6h
6 arm-runs @200B ≈ 21–22h training ; tokenization (offline, CPU) is the real long pole.
```
Compute is **not** the binding constraint — **data tokenization and MFU are**. Plan accordingly.

---

## 3. The VERIFICATION LADDER (the heart of v2)
Run in order. Each rung has a **pre-registered** pass bar. Rung 1 is the **certain** verdict; 2–3 are paper-level bonus.

- **Rung 0 — mechanism smoke (cheap, must pass before training).** In-stack `kb-inject`: tiny run, inject ~200
  facts, confirm `knockout=True` drops recall to chance and `knockout=False` recalls. *This validates the Engram
  wiring + the knockout harness end-to-end.* If it fails → wiring bug, fix before anything else (this is the
  cheapest place to catch the "knockout doesn't collapse" class). 
- **Rung 1 — injected rare-fact knockout at scale (THE CERTAIN VERDICT).** Inject **F≈5,000** controlled rare
  facts (§4) into the ≥200B stream; train arm B (and A) on it; test closed-book recall **B-normal vs B-knockout vs
  A-normal**. **PASS:** B-normal ≫ B-knockout (knockout collapses, ≥10× the paired SE — trivially many-σ at
  F=5,000) **and** B-normal > A-normal (Engram stores facts the backbone alone did not). This is certain to fire
  if Engram is a functional factual memory. *If it fails with rung 0 passing and the path active → genuine
  negative about load-bearing-ness, recorded honestly.*
- **Rung 2 — natural knockout + targeted slices (paper claim, bonus).** TriviaQA/PopQA on→off; rare-2/3-gram &
  entity-proxy NLL slices, A vs B. Expect direction-correct at 200B; may be small at 0.475B.
- **Rung 3 — paired global loss / BPB (corroboration).** 3 paired seeds, powered per §10. Secondary.

> Why rung 1 is faithful, not a cheat: Engram's *entire* thesis is "an O(1) N-gram table stores rare knowledge the
> backbone would otherwise need depth/params for." Injected rare facts are exactly that, made controllable and
> powered. We are testing Engram's mechanism on its home turf, not inventing an easier task.

---

## 4. Injected-fact protocol (rung 1 — specify exactly)
**Fact set.** `F≈5,000` triples `(subject, relation, object)`. `subject` = a **novel, rare** surface string that
appears **only** in these facts (e.g. a templated pronounceable ID like "Zelphonium" / "agent QX-4471") so its
N-gram is genuinely rare; `relation` from a small fixed set (~10, e.g. *origin, color, founder, capital, element*);
`object` = a single tokenizer token where possible (for clean EM). Canonical phrasing so the **(subject⊕relation)
2/3-gram → object** is a stable N-gram the table can capture, e.g. `"The {relation} of {subject} is {object}."`
Include 2–3 paraphrases per fact so recall isn't pure verbatim memorization but the key N-gram recurs.

**Rarity calibration (do FIRST, short pilot).** Sweep repetition `R ∈ {2,4,8,16,32}` on a ~5B-token pilot. Pick
the `R` band where **B recalls ≫ A** *and* **knockout collapses B** — i.e. the regime where the fact is
*Engram-learnable but backbone-hard*. (Too frequent → backbone memorizes too, A≈B; too rare → neither learns.)
Report the chosen `R` and the pilot curve. This calibration is what *guarantees* rung 1 lands in the sensitive band.

**Injection.** Spread the `F·R` fact occurrences uniformly across the ≥200B stream (track doc IDs); keep a
**probe set** = the `F` query prompts `"The {relation} of {subject} is"` → gold `object`. Decontaminate: these
subjects must not collide with natural corpus tokens (they won't — they're novel) and must be excluded from any
natural-slice eval.

**Test & power.** Closed-book: EM and answer-NLL of `object` given the probe prompt, for **A-normal, B-normal,
B-knockout**. Paired McNemar on the F items. *Power:* at `F=5,000`, paired-proportion SE ≈ `√(p(1-p)/F) ≈ 0.007`,
so even a **3-point** knockout collapse is ~4σ and a 20-point collapse is ~29σ ⇒ **effectively certain to resolve
any real effect.** Pre-register: PASS if `EM(B-normal) − EM(B-knockout) ≥ 0.05` at p<1e-4 **and**
`EM(B-normal) > EM(A-normal)`.

---

## 5. DATA — the hard gate (the #1 thing that broke v1)
**No on-the-fly HF streaming.** Tokenize **offline, to disk, with verification, before training starts.**
1. **Acquire** `HuggingFaceFW/fineweb-edu` (`sample-350BT`, ≥300B unique target) by **downloading parquet shards**
   with `hf_transfer`/`datatrove` + **retry/backoff + mirror fallback** (the v1 504s were transient HF errors —
   downloads of static parquet are retryable; streaming-during-train is not). If HF is flaky, fall back to a local
   mirror or **DCLM-baseline / C4 / RedPajama-v2** — any ≥300B-unique clean English corpus is acceptable (claim is
   relative A-vs-B, corpus-agnostic).
3. **Tokenize** with DeepSeek-V3 128k → packed-2048 **mmap shards with document IDs**, parallel across all node CPUs.
4. **VERIFY before training (gate):** assert **≥200B unique tokens** materialized on disk, shard count & token
   count logged to `progress/results/tokenization.csv`, and a **document-ID manifest** exists (so held-out tranches
   are provably disjoint — v1 could not prove this). Inject the §4 facts during/after tokenization with tracked IDs.
5. **Decontaminate** held-out & eval (TriviaQA/PopQA/Pile-test) by doc-ID and n-gram overlap.

> Do not start training until step 4's assertion passes. A day spent here is the whole ballgame — v1 died here.

---

## 6. Model & Engram (keep v1's faithful, iso-param config)
**Backbone (shared):** 20 layers · `d_model` 1280 · MHA 16×80, FlashAttn-3, RoPE θ=1e4 · `seq_len` 2048 ·
DeepSeek-V3 128k tokenizer · SwiGLU MoE (expert hidden 640, 1 shared + **88 routed (A) / 68 routed (B)**, top-k 6,
aux-LB 0.01) · tied embeddings · bf16 · AdamW (β 0.9/0.95, wd 0.1, peak LR 1.5e-3, cosine→10%, warmup 2%, clip 1.0)
· global batch ~4M tokens.
**Iso-param/iso-FLOP (assert in `config_gen.py`):** A non-embed ≈4.50B, activated ≈**0.475B**; B drops 88→68 routed
(frees ~0.983B) → Engram table ≈0.983B → non-embed ≈4.50B, activated ≈0.475B (top-k still 6). **Engram budget =
22.5% of routed (ρ≈77.5%, the sweet spot).** Active params must match to <1e-3 (v1 matched to 1,024 params — keep that).
**Engram module:** layers 2 & 6; per site `N={2,3}`, hash heads `H=8`, `d_e=256`, causal conv k=4 + SiLU,
context-aware gate `α=sigmoid(RMSNorm(h)·RMSNorm(e)/√d)`; `M≈119,600` rows/head/order (~3.8M slots total — fits the
5k injected facts ×N-grams trivially). **`knockout=True` must return `hidden` unchanged** (verified by rung 0).
*Optional sensitivity upgrade if natural signal is wanted and time allows: scale to the paper's **993M-activated**
regime (re-derive iso-param) — rung 1 already guarantees the floor at 0.475B, so this is bonus, not required.*

---

## 7. THROUGHPUT GATE (the #2 thing that broke v1: 9.26% MFU)
**Before committing full runs, hit ≥30% MFU or STOP and diagnose.** v1's 9% is abnormal — check, in order:
1. **MoE backend / all-to-all:** confirm **DDP with full expert replication, NO Expert Parallelism** (replicate the
   whole model per GPU; 4.5B+0.16B bf16 + AdamW states ≈ fits 80GB). All-to-all is the #1 MFU killer at this scale.
2. **Grouped-MM expert kernel:** verify the grouped/local-MoE backend isn't falling back to a slow path; benchmark
   experts in isolation.
3. **Engram hash/gather:** vectorize hashing; **precompute host-side N-gram indices** if it bottlenecks; confirm B
   throughput within a few % of A.
4. **Micro-batch / grad-accum / activation-checkpointing / sequence packing** tuned for the 80GB budget.
Run a **200-step calibration** on all 128 GPUs at the intended global batch; log tok/s + MFU to
`progress/results/calibration.csv`. **Gate: MFU ≥30%** (≥25% acceptable with a note). Only then launch.

---

## 8. Invariants (non-negotiable, keep from v1)
Iso-param · iso-FLOP (top-k 6 both arms) · **paired data** (within a seed, A & B consume the identical batch
stream, same order) · everything else identical · **only the arm varies**. **Paired-loader hash test:** hash the
first 100 batches of an A-run and B-run at the same seed → **must be bitwise identical** before training.
Single `config_gen.py` asserts iso-param/iso-FLOP at every run start; identical world size across runs.

---

## 9. Evaluation protocol
- **9.1 Rung-1 injected facts (PRIMARY):** §4 — EM + answer-NLL for A-normal / B-normal / B-knockout; paired test +
  power. The verdict.
- **9.2 Rung-0 smoke:** kb-inject knockout sanity (pre-training).
- **9.3 Natural knockout:** TriviaQA (5-shot EM) + PopQA, B normal vs knockout (contribution zeroed at layers 2&6).
- **9.4 Targeted slices:** held-out (doc-ID-disjoint) rare-2/3-gram & named-entity NLL, A vs B; slice-gap vs global-gap.
- **9.5 Depth probe:** LogitLens earliest-resolution layer, A vs B.
- **9.6 Paired loss/BPB:** Pile-test + held-out val, 3 seeds, paired Δ + CI (§10).
- **9.7 Gate diagnostics:** α, contribution/hidden RMS, hidden-delta RMS — confirm path active (rules out dead-path).
- **9.8 Downstream (secondary, report-only):** lm-eval-harness; near-floor at 0.475B.

---

## 10. Decision criteria (pre-registered)
**VERIFIED (rung 1 — the certain bar):** `EM(B-normal) − EM(B-knockout) ≥ 0.05` at **p<1e-4** (paired, F≈5,000)
**and** `EM(B-normal) > EM(A-normal)` **and** rung-0 smoke passed **and** gate diagnostics show the path active.
This is the verification; it does not require natural-data wins.
**BONUS (paper-level):** natural knockout shows substantial TriviaQA/PopQA collapse; slice-gap > global-gap; paired
loss Δ>0 across seeds. Report; do not gate on these.
**Power note (loss, secondary):** with seed σ≈0.008, n=3, CI half-width ≈0.020 nats vs expected ~0.012 nat effect
⇒ loss may not reach significance even if real — *expected*, which is why **rung 1 is the verdict**.
**HONEST NEGATIVE (valid):** if rung 0 passes but **rung 1 fails** (knockout doesn't collapse injected facts) with
the path active and data gate satisfied → Engram is *not* becoming load-bearing even on its home-turf controlled
task at this scale → record as a real negative (not a data artifact this time — the data gate removes that excuse).
**BUG SIGNAL:** rung-0 smoke failing = wiring bug (gate saturated / indices wrong / residual not added) — fix first.

---

## 11. Timeline (token-driven; ~3–4 days)
| Phase | Task | Gate |
|---|---|---|
| **P0 setup** | env (PyTorch, FlashAttn-3, AdamW, lm-eval-harness); `config_gen.py` iso-param/iso-FLOP assert; **rung-0 kb-inject smoke** | smoke passes |
| **P1 DATA (long pole)** | offline download + tokenize ≥200B unique → mmap shards + doc-ID manifest; inject §4 facts; decontaminate | **§5 assertion: ≥200B unique on disk** |
| **P2 calibration** | rarity-R pilot (§4) on ~5B; **200-step MFU calibration** (§7); paired-loader hash test (§8) | **MFU ≥30%; R band chosen; hash identical** |
| **P3 pair-1 + facts** | seed-1337 A then B on the fact-injected stream, all 128 GPUs, ckpt every 20–30 min; quick knockout on first B ckpt | path active at first ckpt |
| **P4 RUNG-1 EVAL** | injected-fact knockout (§4/§9.1) → **the verdict** | pre-registered §10 |
| **P5 seeds 2024,7** | 4 runs for loss corroboration + natural knockout/slices/depth | — |
| **P6 report** | aggregate; `REPORT.md` vs §10 (rung-1 verdict first, paper-level bonus second); plots | — |
> Adaptive slack: if rung-1 is weak, first **raise R or tokens** for the fact-injected pair (sensitivity), then
> consider the **993M-activated** upgrade (§6) — before spending time on extra seeds.

## 12. Pitfalls & mitigations
| Pitfall | Mitigation |
|---|---|
| **HF 504 / streaming starvation (killed v1)** | **offline download + retry/mirror + verify on disk (§5)**; never stream-during-train. |
| **MFU collapse (killed v1)** | **§7 gate**; DDP replication no-EP; grouped-MM check; vectorized Engram. |
| Natural knockout too weak/underpowered | **rung-1 injected facts + F=5,000 power** is the verdict, not natural data. |
| Backbone memorizes injected facts (A≈B) | **rarity-R calibration (§4)** picks the Engram-learnable / backbone-hard band. |
| Repeated-data washout | ≥200B **unique**; distinct shards per seed; doc-ID manifest proves disjoint held-out. |
| Config/optimizer drift between arms | single `config_gen.py`; same optimizer all runs; iso-param assert each start. |
| Knockout-not-collapsing = bug not result | rung-0 smoke catches it pre-training. |

## 13. Deliverables & references
**`results/`:** `injected_facts.csv` (A-norm/B-norm/B-knockout EM+NLL+paired stats — **the headline**),
`knockout.csv`, `slices.csv`, `depth_probe.png`, `loss_table.csv` (paired Δ+CI), `downstream.csv`,
`gate_diagnostics.csv`, `loss_curves.png`. **`REPORT.md`** — rung-1 verdict vs §10 first, paper-level bonus second,
with the data-gate confirmation (so a negative can't be blamed on data again).
**Reference (paper, do NOT expect to match absolutes):** sweet spot 20–25% budget→Engram (ρ≈75–80%); U measured at
568M & 993M activated, loss gap ≈0.014 nats; factual knockout retains ~29%; module `N={2,3}`, H=8, early insertion,
context-gate. 27B headline (not our target): MMLU +3, BBH +5, NIAH@32k 84→97. Sources: `arXiv:2601.07372`,
`github.com/deepseek-ai/Engram`, `github.com/AutoArk/TinyEngram`. **Out of scope:** the VSA/structured-value
extension — Engram is flat-value only; that begins only after this flat verification passes.

---
**End of plan.** Start at P0; **do not train until the §5 data gate and §7 MFU gate pass.** The verdict is the
**rung-1 injected-fact knockout** (certain & powered); natural-data wins are bonus. Push progress every 2h; pull
feedback every 2h.
