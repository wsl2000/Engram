# Engram Verification — Handoff v3 (128× H100, two-tier, review-hardened)

**Audience:** an autonomous engineering agent that implements and runs this end-to-end.
**Read order:** §0 (what we can/can't promise) → §1 (v1 + what's still UNBUILT) → §3 (the two-tier logic) → §13
(build checklist — much of this is *not yet code*) → §6/§7 (the two gates that killed v1) → §11 (decision).

> **v3 is a hardened rewrite after 3 independent reviews** (power, validity, systems). It corrects v2's central
> error — calling a *positive control* "the verdict" — and replaces v2's *named-but-unbuilt* data/MFU fixes with
> the actual engineering. **Honest headline: we can make the MECHANISM verification CERTAIN; we cannot guarantee a
> positive on the paper's natural-data net-benefit claim at this scale — but we can make that test FALSIFIABLE
> (real verified-or-negative, never again "inconclusive/below-sensitivity").**

---

## ▶ DEPLOYMENT SCOPE — what you (the remote) build & run (start here)
**Build items 1–5 are not-yet-built (1–3 are net-new code; 4–5 are fixes/ops on partial code) — confirmed by code audit. Budget to build them; do not assume they exist.**
**BUILD (details in the cited sections):**
1. **Tier-1 injected-fact apparatus + rung-0 `kb-inject` smoke** (§3/§4) — single-token opaque subjects mined from the DeepSeek-V3 vocab, large single-token object pool, paraphrases preserving the key n-gram, a negative-control fact class, stream injector with doc-IDs, probe builder, paired answer-NLL + McNemar, **freeze-R logic** (R value from the remote A-only pilot). *This is the certain-verdict apparatus and it does not exist yet (only `write_synthetic_tokens` random tokens).*
2. **Offline data pipeline** (§6) — parquet `snapshot_download`+`hf_transfer` (resumable) → **local-file tokenizer (NOT `streaming=True`)** → packed-2048 **uint32** shards + **doc-ID manifest** → **≥200B-on-disk gate**. *Replaces the current streaming tokenizer that 504'd v1 to death.*
3. **MFU levers** (§7) — **`torch.compile` + fused linear-CE** (Liger/cut-cross-entropy; the 128k-vocab chunked-CE is the OOM/MFU bottleneck). *Neither is in the repo.*
4. **Spec-drift fixes** (§8) — add **RoPE** (model is currently NoPE); compute the iso-FLOP delta (hard-coded 0).
5. **Ops** (§12) — checkpoint rotation + disk pre-write check + node pre-flight + auto-resume (v1 crashed on a full disk).

**RUN (in order):** rung-0 smoke → **Tier-1** (cheap, any MFU — the *certain* verdict) → pass **data gate ≥200B** + **MFU gate ≥18–20%** → **Tier-2** natural NLL, 3 seeds (the *falsifiable paper claim*) → `REPORT.md`.
**VERDICT framing:** Tier-1 = mechanism/param-efficiency (certain). Tier-2 = the paper's natural-data claim *at this scale* (may be small/negative — that's a real result, not "inconclusive", because Tier-1 proves the apparatus is sensitive). **Do NOT call Tier-1 "verifying the paper."** Full build list in §13.

---

## ⚠️ COLLABORATION — PUSH PROGRESS EVERY 2H; PULL `feedback/` EVERY ~2H ⚠️
Every 2h & at each milestone: commit `progress/logs/`, partial `progress/results/`, and a `progress/STATUS.md`
line (elapsed, active run/seed/arm, step/tokens vs target, **measured MFU & tok/s**, health, what finished/next/ETA);
flag any anomaly immediately. Commit `progress: H<elapsed>h — <one-line>`, author **wsl2000 <wsuli615@gmail.com>**.
After each push, `git pull`, read `feedback/review-<UTC>.md` (top line `VERDICT: ON-TRACK|ISSUES|BLOCKER`),
**ack in STATUS.md**, fix or reply (`feedback/reply-<UTC>.md`). `BLOCKER` = stop-and-fix.

---

## 0. Objective & what is / isn't promised (read first)
**Two separate claims, two tiers — do not conflate them:**

- **Tier-1 — MECHANISM (sensitivity positive control, CERTAIN).** Under iso-param/iso-FLOP, an Engram-augmented
  MoE (B) can be a **load-bearing store of rare factual N-grams** that an identical pure-MoE (A) cannot recall —
  shown by a *controlled, powered, pre-registered* injected-fact test (§4). This is **certain to return a
  definitive PASS or a real negative** (it doesn't need 200B tokens or high MFU). **It is a positive control, NOT
  proof of the paper's claim.** Its job: prove the apparatus is *sensitive enough to detect a load-bearing Engram
  when one exists.*
- **Tier-2 — THE PAPER'S CLAIM (falsifiable verification).** On *natural* data at iso-param/iso-FLOP, does Engram
  help — natural knockout collapse + rare-n-gram/entity **NLL** slices + paired loss (§5)? This is the real test.
  At ~0.475B activated it may be **small or negative** (the paper's effect ≈0.012–0.014 nats sits below seed
  noise, and natural-QA EM is at floor) — that is an acceptable, *informative* outcome.

**The epistemic that finally escapes v1's trap (this is the whole point):** v1 came back "inconclusive — maybe
Engram doesn't help, maybe our setup was too small." **Tier-1 removes that ambiguity:** if the positive control
*fires*, the apparatus is provably sensitive, so **whatever Tier-2 returns is a REAL result** — VERIFIED if Tier-2
is positive, an **honest negative** ("Engram's natural-data benefit is not present/detectable at 0.475B/200B,
*and the setup is demonstrably sensitive*") if not. This matches our standing rule (`insensitive-setup-record-only`):
a passing positive control *licenses* interpreting a natural negative; it does **not** replace the natural test.

**Success:** Tier-1 fires (apparatus sensitive) **AND** Tier-2 is reported as a real verified-or-negative result
with the sensitivity caveat removed. "Verify Engram" = Tier-2 positive; "verify the mechanism" = Tier-1 positive.

---

## 1. v1 failures + what THIS review round found still UNBUILT
v1 = NOT VERIFIED, but *below sensitivity* (honest). Three root causes — and v2 only *named* the fixes; the code
review found them **unbuilt**:

| killer | v1 reality | v2 status | v3 requirement |
|---|---|---|---|
| **Data** | streaming tokenizer 504'd mid-run → **4.7B unique** | `tokenize_fineweb.py` **still `streaming=True`**, retry wraps only the open, not iteration → **will die identically** | **§6: build a real parquet downloader + local tokenize + doc-ID manifest + ≥200B on-disk gate** (unbuilt = the #1 risk). |
| **MFU** | **9.76%** with no-EP DDP + `torch._grouped_mm` already in use | §7 "diagnose & hit 30%" lists fixes v1 **already did**; **no `torch.compile`, no fused-CE anywhere** | **§7: add torch.compile + fused linear-CE; set gate to ~18–20%** (30% is ~3× v1's already-tuned ceiling). |
| **Test** | natural knockout weak, EM at floor, uncontrolled | injected-fact test good idea but **HARKed** (R tuned to pass) & **mislabeled as the verdict**; apparatus **unimplemented** | **§3/§4: reframe to positive control, freeze R pre-hoc, build the apparatus + rung-0 artifact.** |

v1's Engram path was *active* (α≈1.0, contribution grew) — keep the model/Engram/knockout code (it's faithful, §8);
fix data, throughput, the test framing, and **build the missing apparatus (§13).**

---

## 2. Budget, scale, realistic timeline
| Item | Value |
|---|---|
| Hardware | **128× H100-80GB** (16 healthy nodes). **Secure an allocation window** — v1 backfill for 10 nodes slipped ~2 days; 16 is harder. |
| Default scale | **~0.475B activated** MoE (proven on this stack; iso-param to 1,024 params). Certain Tier-1 + falsifiable Tier-2. |
| **Sensitivity upgrade (optional, for Tier-2)** | scale to the paper's **993M-activated** regime (re-derive iso-param) to give the *natural* effect a better chance — ~2× compute, more systems risk. Tier-1 already guarantees the floor at 0.475B, so this is a **Tier-2-only** bet; decide after Tier-1 passes. |
| Tokens/arm | **≥200B unique** for Tier-2 (Tier-1 needs far less — §4). |
| Realistic wall-clock | **6–12 days** (not 3–4): data build + MFU eng + queue waits + 6 runs at ~18–20% MFU (200B/arm ≈ 6–8.5h ⇒ 6 arms ≈ 37–51h) + eval. **No artificial cap** (the 24h cap caused v1's 20B truncation). |
| Optimizer | AdamW, identical across arms (Muon only if already vetted). |

**Corrected compute math (systems review):** FLOP/token ≈ **3.9e9** (includes the 128k-vocab head + attention, not
just 6·N_active=2.85e9). At an attainable **20% MFU**: `128·990e12·0.20 / 3.9e9 ≈ 6.5M tok/s` ⇒ 200B/arm ≈ **8.5h**.
At a stretch 25%: ≈6.8h. **Compute is fine; the binding constraints are the data build, MFU engineering, and the
128-node queue window.**

---

## 3. The two-tier verification (the corrected core)
**Tier-1 — injected-fact POSITIVE CONTROL (certain; §4).** Inject `F≈5,000` controlled rare facts; test recall
A-normal / B-normal / B-knockout. The clean, non-circular evidence is the **triple**: `A-normal ≈ chance`,
`B-normal ≫ chance`, `B-knockout ≈ chance ≈ A-normal` — Engram provides a recall capability the iso-param backbone
lacks, localized to the table. **Runs on a small PRE-GATE budget — ~20B tokens/arm (far below the §6 ≥200B gate),
at whatever MFU** (facts are ~1e-5 of the stream → A stays at chance even at ~20B tokens and 9% MFU), so Tier-1 is
**immune to the throughput/data problems that killed v1.** *(Tier-1 reuses items 1–2's downloader/tokenizer/injector
at this small scale — it does NOT wait on the ≥200B gate or the MFU gate.)* **R is frozen pre-hoc from arm-A difficulty only (§4) — no tuning toward PASS** (kills the HARKing).
- *Rung-0 (pre-train smoke, must pass & be committed):* the in-stack `kb-inject` (replicate the separate
  small-scale control from the `Compositional_Generalization` repo — *which is not in this repo, so build & commit
  the artifact here*): ~200 facts, confirm `knockout=True` → chance, `knockout=False` → recall, and assert
  train/eval key-N-gram **token-IDs are identical** (catch the tokenization-mismatch silent killer).

**Tier-2 — natural VERIFICATION (falsifiable; §5).** Natural rare-n-gram/entity **NLL** slices + natural
answer-**NLL** knockout + paired loss across 3 seeds. **NLL, not EM** (EM floors at 0.475B). Gated on the §6/§7
regime. This is the test that can actually say "Engram helps on natural data" or "it doesn't, at this scale."

**Order:** rung-0 smoke → Tier-1 (cheap, certain) → if Tier-1 passes, run Tier-2 (the regime-dependent verdict).
A Tier-1 *pass* is the green light that makes a Tier-2 negative *interpretable*.

---

## 4. Tier-1 protocol (bulletproofed — power review)
**Subjects:** mine **~5,000 single-token, opaque, rare IDs from the DeepSeek-V3 vocab** (so the key N-gram is one
clean discriminative token, not a BPE-split suffix — the #1 silent killer). **Objects:** arbitrary **single
tokens from a LARGE pool** (so chance ≈ floor, the backbone prior is at chance, and a correct Engram boost flips
argmax → maximal McNemar discordant pairs). **Relations:** ~10 fixed. **Canonical phrasing** keeps
`{subject}…{object}` **adjacency** so the discriminative `(subject⊕relation)` 2/3-gram recurs; **paraphrases must
preserve that key n-gram** (their purpose is to suppress the *backbone's verbatim* memorization while giving the
table R consistent slot-updates — count R as occurrences of the **canonical key n-gram**, not total mentions).

**R is frozen pre-hoc, from arm A only:** run an A-only rarity pilot; **set R = the smallest value such that
A-recall < 10%** (i.e., backbone-hard). **This R is then fixed for the registered B run — no re-tuning toward a
pass; the §11 negative is reachable.** Report the **full A-and-B recall-vs-R sweep**, not the chosen point (the
paper's spirit is param-efficiency *across* rarities).

**Negative-control fact class (validity review):** a second fact class whose key is **not** a clean recurring
n-gram (subject introduced only via paraphrase/coreference). Predict B's advantage **shrinks** there → shows the
effect is **N-gram-memory-specific**, not "B has spare capacity."

**Primary statistic = paired answer-NLL** (Wilcoxon / paired-t over the F facts) — always powered, moves even when
EM is at floor; **EM is the headline**, with a calibration target **B-normal EM ≥ ~0.3** so the EM drop is
clearable. **Power (corrected):** paired design ⇒ **McNemar on discordant pairs**, not the unpaired √(p(1−p)/F);
a 5-pt knockout collapse at F=5,000 ⇒ b≈250,c≈0 ⇒ z≈√250≈**16σ**. F=5,000 is over-powered; the binding
constraints are *effect existence* and *EM off the floor*, both handled above.

**PASS (Tier-1, pre-registered):** (a) `NLL(B-knockout) − NLL(B-normal) > 0` at p<1e-4 (paired) **and** EM collapse
≥0.05; **and** (b) anti-circularity: `EM(B-normal) − EM(A-normal) ≥ 0.20 at p<1e-4` (paired) — **a pre-hoc margin,
not just ">"** (from the B-normal EM ≥0.3 calibration target vs A≈floor; freeze it before the registered run); **and**
(c) the negative-control fact class shows a B−A gap **< half** the main-class B−A gap. **FAIL is a real negative** if
rung-0 passed (apparatus works) — record, do **not** re-tune R.

---

## 5. Tier-2 protocol (natural, NLL-based, honest about scale)
- **Natural knockout:** TriviaQA/PopQA **answer-NLL** B-normal vs B-knockout (EM reported but expected at floor at
  0.475B — *not* the criterion; the paper's "retain ~29% EM" is **unreachable at this scale**, stated as a limit).
- **Targeted slices:** doc-ID-disjoint held-out, rare-2/3-gram & named-entity **NLL**, A vs B; slice-gap vs
  global-gap.
- **Paired loss/BPB:** Pile-test + held-out val, 3 seeds, paired Δ + 95% CI (t, df=2). Power: σ≈0.008, n=3 ⇒
  CI half-width ≈0.020 nats vs ~0.012 effect ⇒ **may not resolve even if real** — reported as corroboration only.
- **Depth probe, gate diagnostics** (α, contribution RMS — confirm path active, rule out dead-path).

---

## 6. DATA — BUILD the offline pipeline (the #1 unbuilt risk)
**The current `tokenize_fineweb.py` streams and will die on a mid-stream 504 exactly like v1. Replace it.**
1. **Download static parquet** of `HuggingFaceFW/fineweb-edu` (`sample-350BT`) via `huggingface_hub.snapshot_download`
   + `HF_HUB_ENABLE_HF_TRANSFER=1`, **resumable & retryable per file** (static files survive retries; streaming
   does not). Fallback corpus: **DCLM-baseline / C4 / RedPajama-v2** (claim is relative A-vs-B, corpus-agnostic).
   ~**1–1.5 TB** of parquet for ≥300B DeepSeek tokens.
2. **Tokenize from LOCAL files** (not `streaming=True`), DeepSeek-V3 128k, **dtype uint32** (128k > uint16; 4
   bytes/token — *real disk = 200B×4 = 800 GB per arm-pool; 300B = 1.2 TB*). Packed-2048 mmap shards **+ per-document
   IDs in the manifest** (v1's manifests lacked doc-IDs → couldn't prove held-out disjointness; build it now).
   Measured tokenize throughput ≈17.8M tok/s on 4 nodes ⇒ 300B ≈ **1.5–4.7h** *if not interrupted* (now it won't be).
3. **GATE (hard):** assert **≥200B unique tokens on disk** + shard/token counts logged + doc-ID manifest present,
   **before any Tier-2 training**. Inject §4 facts with tracked IDs. Decontaminate eval/held-out by doc-ID + n-gram.
4. **Disk:** budget **~2.5–3 TB** for data (pool + tokenized). "Distinct shards per seed" for 3×200B would need a
   600B pool (2.4 TB) — either provision it or **document controlled reuse** (acceptable; note it).

> Do not start **Tier-2** training until step 3 asserts. (Tier-1 §3/§4 trains on a small **pre-gate** build — items
> 1–2's downloader/tokenizer/injector at ~20B tokens, *without* the ≥200B gate — so it runs first regardless.) This
> is where v1 died; it is unbuilt; treat as ~0.5–1 day of real work.

## 7. THROUGHPUT — BUILD the real MFU levers (the #2 killer)
v1 hit **9.76%** with the *entire* v2 §7 list already done (no-EP DDP, `torch._grouped_mm`, mbs maxed at 4). The
real levers are **absent from the code**:
1. **`torch.compile`** the model (none in repo; ~1.5–2.5× on transformers in eager).
2. **Fused linear-cross-entropy** (Liger / cut-cross-entropy) — the 128k-vocab head currently materializes fp32
   logits in a chunked loop (`model.py:260-277`): it's both the **OOM tipping point** (blocks mbs>4) and a ~+35%
   compute sink. Fusing it **frees memory → raises mbs → raises MFU** (the missing link between the memory & MFU
   limits).
3. Accept the **structural floor:** 0.475B-active @ mbs4 ⇒ ~558 tok/expert ⇒ small bandwidth-bound grouped GEMMs;
   small-active MoEs are *intrinsically* low-MFU. (The 993M upgrade in §2 also *helps* MFU.)
4. **Comm:** 4.669B params ⇒ **9.3 GB bf16 grad all-reduce/step**; world=128 at ~4M global batch forces grad-accum≈4
   (vs v1's 6) → less compute to hide the all-reduce. **Grow global batch to ~6M** (re-tune LR) to keep ga≈6.
**GATE: MFU ≥ ~18–20%** (realistic ceiling ≈9.76%×1.8×1.3 ≈ 18–25%; **drop the 30% literal** — at 30% the gate
either halts the project or gets waived into the slow runs that truncated v1). 200-step calibration **with compile
+ fused-CE** on all 128 GPUs; log to `progress/results/calibration.csv`. Confirm B within a few % of A.

## 8. Model & Engram (keep v1's faithful core; fix the spec discrepancies)
Backbone: 20L · d_model 1280 · MHA 16×80 · seq 2048 · DeepSeek-V3 128k · SwiGLU MoE (expert hidden 640, 1 shared +
**88 routed (A)/68 (B)**, top-k 6, aux-LB 0.01) · tied embeds · bf16 · AdamW (β.9/.95, wd .1, peak 1.5e-3,
cosine→10%, warmup 2%, clip 1.0) · global batch **~6M** (§7). Iso-param to <1,024 params; activated ≈**0.475B**;
Engram = 22.5% of routed budget (ρ≈77.5%).
**Engram:** layers 2&6; N={2,3}, H=8, d_e=256, ~119,918 rows/head/order (~3.8M slots), depthwise causal-conv k=4
+SiLU, RMSNorm context-gate, flat value. `knockout=True` returns `hidden` unchanged (verified clean in
`tests/test_engram_read.py`).
**Fix the spec-vs-code discrepancies the review found:** (a) **add RoPE θ=1e4** — the code is currently **NoPE**
(`model.py` applies no positional encoding) though §spec claims RoPE; adding it is faithful and helps the backbone
(relevant to Tier-2 not flooring). (b) **Compute** `iso_active_param_abs_delta` (currently hard-coded 0; it omits
Engram proj+conv ~671K + the 16 per-token gathers) and report **"iso-FLOP to <1%"**, not "=0". (c) "FlashAttn-3" is
actually `F.scaled_dot_product_attention` (flash kernel — fine; correct the wording). (d) Note the **saturated gate**
(α≈0.997 in v1) in the report — the "context-aware" gate behaves as an always-on residual; doesn't bias A/B.

## 9. Invariants (non-negotiable, keep)
Iso-param · iso-FLOP (top-k 6 both) · **paired data** (identical batch stream/order within a seed — bitwise hash of
first 100 batches must match, `scripts/hash_loader_test.py`) · everything else identical · only the arm varies ·
single `config_gen.py` asserts iso-param/FLOP each run · identical world size.

## 10. Evaluation (artifacts)
Tier-1: `results/injected_facts.csv` (A-norm/B-norm/B-knockout EM+NLL, paired stats, **recall-vs-R sweep**,
negative-control gap) — **the Tier-1 headline**. Tier-2: `knockout.csv` (NLL), `slices.csv` (NLL slice-gap vs
global), `loss_table.csv` (paired Δ+CI), `depth_probe.png`, `gate_diagnostics.csv`, `downstream.csv` (report-only).

## 11. Decision criteria (two-tier, falsifiable — no escape hatch)
- **Tier-1 PASS** = §4(a)+(b)+(c) with rung-0 passed → **apparatus is sensitive; mechanism verified.** **FAIL**
  (rung-0 passed, R frozen) = **real negative about load-bearing-ness** — record; *do not re-tune R* (removing v2's
  "raise R until it passes" escape hatch is what makes Tier-1 falsifiable).
- **Tier-2 VERIFIED** = natural NLL knockout collapses for B (not A) **and** slice-gap > global-gap, paired across
  seeds in the expected direction. **Tier-2 NEGATIVE** (given Tier-1 passed) = **honest, real negative**: "Engram's
  natural-data benefit is absent/undetectable at 0.475B/200B, and the apparatus is demonstrably sensitive" — *not*
  inconclusive. **Loss** is corroboration only (underpowered, §5).
- **BUG** = rung-0 fails (wiring) → fix first.
- **Report must label scope:** Tier-1 = mechanism/param-efficiency; Tier-2 = the paper's natural claim **at this
  scale** (NOT the 27B headline). A flat Tier-2 may simply mean 0.475B is below where the paper's effect emerges —
  state it; offer the §2 993M upgrade as the next lever.

## 12. Storage, node health, resume (BUILD — v1 crashed here)
- **Checkpoint rotation:** 28 GB/ckpt, every 20–30 min, 6 runs ⇒ unrotated ~3 TB and **v1 crashed on a full VAST**.
  Keep **last 1–2 + final**; add a **disk-space pre-write check** that pauses/rotates instead of crashing.
- **Node pre-flight + exclude list** (v1 hit CUDA-OOM-on-empty-GPU / `set_device` fails on cn02/10/17/34); one bad
  node kills a 16-node job. **Auto-resume from last checkpoint** on pre-emption/node-fail (the 128-node window will
  not be contiguous).
- **Total disk budget: ~2–5 TB** (data 1.2–2.5 TB + rotated ckpts ~0.5 TB).

## 13. BUILD checklist (what is NOT yet code — do before claiming)
- [ ] **Parquet downloader** (snapshot_download + hf_transfer, resumable) + **local-file tokenizer** (replace
      `streaming=True`) + **doc-ID manifest** + **≥200B on-disk gate**. (§6)
- [ ] **torch.compile** integration + **fused linear-CE**; 200-step calib proving ≥18–20% MFU. (§7)
- [ ] **RoPE** in attention; **computed** iso-FLOP delta. (§8)
- [ ] **Tier-1 apparatus:** fact generator (single-token subjects/objects, paraphrases, negative-control class),
      stream injector with IDs, probe-set builder, **rung-0 kb-inject smoke**, A-only R-pilot, paired
      NLL + McNemar stats, recall-vs-R sweep. (§3/§4) — **none of this exists in the repo yet.**
- [ ] **Checkpoint rotation + disk pre-check + node pre-flight + auto-resume.** (§12)
- [ ] **Tokenization train/eval key-N-gram token-ID identity assert** (rung-0). (§4)

## 14. Pitfalls / references
HF 504 (killed v1) → offline static parquet + retry + on-disk gate. MFU collapse (killed v1) → torch.compile +
fused-CE, gate 18–20%. EM at floor → paired NLL primary. HARKing → R frozen pre-hoc, sweep reported. Disk full
(killed v1) → rotation + pre-check. Queue → secure 16-node window + auto-resume.
**Paper (arXiv:2601.07372, do NOT expect absolutes):** sweet spot 20–25% budget→Engram; U measured at 568M & 993M
activated, gap ≈0.014 nats; factual knockout retains ~29% (their scale, EM — unreachable at 0.475B); N={2,3}, H=8,
early insertion, context-gate. Sources: paper; `github.com/deepseek-ai/Engram`; `github.com/AutoArk/TinyEngram`.
**Out of scope:** the VSA/structured-value extension (flat value only here; that begins after this passes).

---
**End v3.** The verdict is **two-tier**: Tier-1 (injected facts) is the *certain* sensitivity control — build it,
freeze R, run it cheap; Tier-2 (natural NLL) is the *falsifiable* paper-claim test — build the data/MFU stack
first. **Do not start TIER-2 training until §6 data-gate and §7 MFU-gate pass (Tier-1 runs PRE-GATE first, §3/§4); do not call Tier-1 "verification of the paper."**
