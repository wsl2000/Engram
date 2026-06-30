# H22.3 - h4 B final complete; final eval running

- Elapsed: H22.3 wall-clock from the resumed run.
- Completed run: h4 B job `167284` completed successfully (`COMPLETED`, exit `0:0`, elapsed `02:15:48`) on `cn[14-15,19,24-26,29-32]`.
- Step/tokens vs target: final rank0 log reached step 5,027 / 5,027, tokens 19,766,968,320 / 19,766,968,320.
- Measured MFU and tok/s: final logged step reports 2,571,946 tok/s and MFU 9.26%; run held about 2.57M tok/s steady throughput.
- Checkpoints: final checkpoint `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step005027.pt` is complete at 28,027,733,867 bytes, along with periodic checkpoints 000952/001907/002863/003820/004777.
- Final eval array: dependency released and `167289_0..8` started automatically. At latest check, tasks 4-8 completed (`0:0`) and tasks 0-3 are still running.
- Completed partial eval: h5-disjoint slices/depth/diagnostics are written. Slice NLLs: A global 2.7372745 vs B 2.7473171; A repeat-ngram 1.0668151 vs B 1.0691550; A entity-proxy 4.2457943 vs B 4.2930119. Depth: A mean earliest layer 17.09375 / median 19, B mean 17.06543 / median 19. B final Engram diagnostics: final hidden delta RMS 0.0649173, last-logit mean abs delta 0.0961437, layer-6 contribution/hidden RMS ratio 0.0121942.
- Interpretation: Engram path remains nonzero and stronger than early h4 quick-gate, but h5 slices do not currently favor B. Do not update the verdict until final TriviaQA/PopQA knockout and EM tasks 0-3 finish.
- Feedback loop: pulled `origin/main`; no new feedback beyond `feedback/review-20260629T1032Z.md`.
- Next: wait for tasks 0-3, aggregate final h4 results, update `REPORT.md`/result tables, push, then pull/check feedback.

# H22.1 - h4 B fifth checkpoint complete

- Elapsed: H22.1 wall-clock from the resumed run.
- Active run: h4 B job `167284` is still `RUNNING` on `cn[14-15,19,24-26,29-32]`; final eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: latest checked monitor state is step 4,828 / 5,027, tokens 18,984,468,480 / 19,766,968,320.
- Measured MFU and tok/s: latest checked step reports 2,569,715 tok/s and MFU 9.25%; steady throughput remains about 2.57M tok/s.
- Checkpoints: `ckpt_step000952.pt`, `ckpt_step001907.pt`, `ckpt_step002863.pt`, `ckpt_step003820.pt`, and `ckpt_step004777.pt` are complete, each 28,027,733,867 bytes. Training continued past the fifth checkpoint barrier.
- Feedback loop: pulled `origin/main`; no new feedback beyond `feedback/review-20260629T1032Z.md`.
- Next: final h4 B checkpoint should be reached in about 5 minutes if current throughput holds; dependent final eval array should start automatically after B exits successfully.

# H21.8 - h4 B fourth checkpoint complete

- Elapsed: H21.8 wall-clock from the resumed run.
- Active run: h4 B job `167284` is still `RUNNING` on `cn[14-15,19,24-26,29-32]`; final eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: latest checked monitor state is step 3,850 / 5,027, tokens 15,138,816,000 / 19,766,968,320.
- Measured MFU and tok/s: latest checked step reports 2,558,234 tok/s and MFU 9.21%; steady throughput remains about 2.57M tok/s.
- Checkpoints: `ckpt_step000952.pt`, `ckpt_step001907.pt`, `ckpt_step002863.pt`, and `ckpt_step003820.pt` are complete, each 28,027,733,867 bytes. Training continued past the fourth checkpoint barrier.
- Feedback loop: pulled `origin/main`; no new feedback beyond `feedback/review-20260629T1032Z.md`.
- Next: keep monitoring B toward final step 5,027. Expected final checkpoint is about 30 minutes from this check if current throughput holds; dependent final eval array should start automatically after B exits successfully.

# H21.4 - h4 B third checkpoint complete

- Elapsed: H21.4 wall-clock from the resumed run.
- Active run: h4 B job `167284` is still `RUNNING` on `cn[14-15,19,24-26,29-32]`; final eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: latest checked monitor state is step 2,872 / 5,027, tokens 11,293,163,520 / 19,766,968,320.
- Measured MFU and tok/s: latest checked step reports 2,560,055 tok/s and MFU 9.22%; steady throughput remains about 2.57M tok/s.
- Checkpoints: `ckpt_step000952.pt`, `ckpt_step001907.pt`, and `ckpt_step002863.pt` are complete, each 28,027,733,867 bytes. Training continued past the third checkpoint barrier.
- Feedback loop: pulled `origin/main`; no new feedback beyond `feedback/review-20260629T1032Z.md`.
- Next: keep monitoring B toward final step 5,027. Expected final checkpoint is about 55 minutes from this check if current throughput holds; dependent final eval array should start automatically after B exits successfully.

# H21.0 - h4 B second checkpoint complete

- Elapsed: H21.0 wall-clock from the resumed run.
- Active run: h4 B job `167284` is still `RUNNING` on `cn[14-15,19,24-26,29-32]`; final eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: latest checked rank0 log is step 1,944 / 5,027, tokens 7,644,119,040 / 19,766,968,320.
- Measured MFU and tok/s: latest checked step reports 2,581,119 tok/s and MFU 9.30%; recent steady throughput remains about 2.57M tok/s.
- Checkpoints: `ckpt_step000952.pt` and `ckpt_step001907.pt` are complete, each 28,027,733,867 bytes. Training continued past the second checkpoint barrier.
- Quick-gate interpretation remains unchanged: first-checkpoint Engram path is nonzero/exercised, but factual answer-NLL knockout is weak/no-collapse; do not claim verification before final h5-disjoint eval.
- Feedback loop: pulled `origin/main`; no new feedback beyond `feedback/review-20260629T1032Z.md`.
- Next: keep monitoring B toward final step 5,027. Expected final checkpoint is around 78-80 minutes from this check if current throughput holds; dependent final eval array should start automatically after B exits successfully.

# H20.7 - h4 B quick gate complete

- Elapsed: H20.7 wall-clock from the resumed run.
- Active run: h4 B job `167284` is still `RUNNING`; quick gate job `167601` completed successfully (`0:0`, elapsed `00:03:20`); final eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: latest checked rank0 log is step 1,268 / 5,027, tokens 4,985,978,880 / 19,766,968,320.
- Measured MFU and tok/s: latest checked step reports 2,568,808 tok/s and MFU 9.25%.
- Checkpoints: first checkpoint `ckpt_step000952.pt` remains complete.
- Quick-gate result: first-checkpoint answer-NLL knockout is weak/no-collapse. TriviaQA delta knockout-normal = `-0.0039065862`; PopQA delta = `+0.0017110395`. Diagnostics confirm nonzero Engram path: final hidden delta RMS `0.0362668246`, last-logit mean absolute delta `0.0367558546`, layer 6 contribution/hidden RMS ratio `0.0034090547`.
- Interpretation: wiring is exercised/nonzero, but early factual knockout remains weak. Continue to final checkpoint and h5-disjoint final eval; do not claim verification from this early signal.
- Results updated: raw `h4v3_b0952_*` files under `results/knockout/` and `results/diagnostics/`, plus aggregate `results/knockout.csv` and `results/gate_diagnostics.csv`.
- Feedback loop: no new feedback after latest pull.
- Next: keep monitoring B to final. After B success, final eval array `167289` should run automatically.

# H20.6 - h4 B quick gate running

- Elapsed: H20.6 wall-clock from the resumed run.
- Active run: h4 B job `167284` is still `RUNNING`; quick gate job `167601` is `RUNNING` on `cn06`; final eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: latest checked rank0 log is step 1,082 / 5,027, tokens 4,254,597,120 / 19,766,968,320.
- Measured MFU and tok/s: latest checked step reports 2,579,384 tok/s and MFU 9.29%.
- Checkpoints: first checkpoint `ckpt_step000952.pt` is complete and is being evaluated by quick gate job `167601`.
- Bug gate: `167601` runs first-checkpoint TriviaQA/PopQA answer-NLL knockout plus h5-disjoint Engram gate/contribution diagnostics using `scripts/slurm_h4_b0952_quick_gate.sh`.
- Feedback loop: no new feedback after latest pull.
- Next: monitor quick gate `167601` for outputs while B continues toward final checkpoint; final eval array `167289` remains queued after B success.

# H20.5 - h4 B first checkpoint complete

- Elapsed: H20.5 wall-clock from the resumed run.
- Active run: h4 B job `167284` is still `RUNNING` on `cn[14-15,19,24-26,29-32]`; dependent eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: latest checked rank0 log is step 1,014 / 5,027, tokens 3,987,210,240 / 19,766,968,320.
- Measured MFU and tok/s: latest checked step reports 2,563,131 tok/s and MFU 9.23%.
- Checkpoints: first checkpoint completed at `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step000952.pt`, size 28,027,733,867 bytes. Training continued past the checkpoint barrier.
- Bug gate: added `scripts/slurm_h4_b0952_quick_gate.sh` for first-checkpoint TriviaQA/PopQA answer-NLL knockout and h5-disjoint Engram contribution diagnostics.
- Feedback loop: no new feedback after the latest pull.
- Next: submit quick gate job for checkpoint `000952`, then keep monitoring B to final. Final eval array `167289` remains queued for after B success.

# H20.1 - h4 B v3 running

- Elapsed: H20.1 wall-clock from the resumed run.
- Active run: h4 B job `167284` is `RUNNING` on `cn[14-15,19,24-26,29-32]` with 10 nodes / 80 H100. Dependent eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: latest checked rank0 log is step 86 / 5,027, tokens 338,165,760 / 19,766,968,320.
- Measured MFU and tok/s: latest checked step reports 2,574,192 tok/s and MFU 9.27%; steady early steps are around 2.5-2.58M tok/s.
- Invariants: arm B, seed 2024, loader seed rank0 2024, world size 80, AdamW, grouped MoE, bf16 CUDA autocast path, `micro_batch_size=4`, `grad_accum_steps=6`, `ce_chunk_tokens=256`.
- Node health/resources: Slurm allocation TRES is `cpu=160,mem=18000G,node=10,billing=160,gres/gpu:h100=80`; batch host is `cn14`.
- Checkpoints: none yet. First B v3 checkpoint expected after 25 minutes; output directory is `runs/pair_h4_B_seed2024_20B_mbs4_80_v3`.
- Feedback loop: pulled `origin/main`; no new feedback beyond `feedback/review-20260629T1032Z.md`.
- Next: monitor first 25-minute checkpoint, then continue to final step 5,027. After B success, eval array `167289` should run automatically.

# H19.5 - resumed blocked audit, still waiting for 80 H100

- Elapsed: H19.5 wall-clock from the resumed run; no post-resume training tokens have run.
- Active run: h4 B job `167284` remains `PENDING (Resources)`; dependent eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: unchanged. No B v3 output directory or checkpoint exists. Target remains B seed 2024, h4 stream, step 5,027 / 19,766,968,320 tokens.
- Slurm evidence: `167284` still requests 10 nodes / 80 H100, excludes `cn02,cn10,cn17,cn34`, has no nodes assigned, and backfill remains `2026-07-02T04:43:08`. Current node snapshot shows only 6 full H100 nodes idle, below the 10 full-node requirement.
- Feedback loop: pulled `origin/main`; no new feedback beyond `feedback/review-20260629T1032Z.md`.
- Blocked audit: this is the third resumed check with the same external blocker after the previous blocked state. The faithful h4 B job and dependent eval array are queued, topology alternatives were checked, and no safe non-H100 work remains that improves the requested final state without risking the allocation path.
- Next after unblocking: verify B first-step invariants, tok/s/MFU, and 25-minute checkpoint; after B final checkpoint, collect eval array `167289` outputs and update verdict artifacts.

# H19.4 - still pending; backfill slipped

- Elapsed: H19.4 wall-clock from the resumed run; no post-resume training tokens have run.
- Active run: h4 B job `167284` remains `PENDING (Resources)`; dependent eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: unchanged. Target remains B seed 2024, h4 stream, step 5,027 / 19,766,968,320 tokens. No B v3 output directory or checkpoint exists.
- Slurm evidence: `167284` still requests 10 nodes / 80 H100 and excludes `cn02,cn10,cn17,cn34`. Backfill estimate slipped to `2026-07-02T04:43:08Z`.
- Queue alternatives: rechecked valid 80-GPU topologies with `sbatch --test-only`; already queued 10x8 remains earliest. 20x4 and 16x5 are later. An accidental 13x7 probe is invalid for the 80-GPU invariant and was not used.
- Feedback loop: pulled `origin/main`; no new feedback beyond `feedback/review-20260629T1032Z.md`.
- Next: keep `167284` queued; once allocated, verify first-step invariants, tok/s/MFU, and 25-minute checkpoint creation.

# H15.4 - blocked on 80-H100 allocation

- Elapsed: H15.4 experiment runtime.
- Active run: h4 B job `167284` remains `PENDING (Resources)`; dependent eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: unchanged. No post-resume training tokens have run; no `runs/pair_h4_B_seed2024_20B_mbs4_80_v3` directory or checkpoint exists.
- Slurm evidence: `167284` requests 10 nodes / 80 H100, excludes `cn02,cn10,cn17,cn34`, and backfill still estimates start `2026-07-01T21:32:39`.
- Feedback loop: pulled `origin/main`; no new feedback beyond `feedback/review-20260629T1032Z.md`.
- Blocked status: this is the third consecutive resumed progress check with the same external blocker (required 80-H100 allocation unavailable). Queued B and dependent eval jobs are already in place, and no safe non-H100 work remains that improves the requested final state without risking the backfill. Resume when Slurm allocates `167284` or when the operator changes resource policy.
- Next after unblocking: verify B first-step invariants, tok/s/MFU, and 25-minute checkpoint; after B final checkpoint, collect eval array `167289` outputs and update the h4 verdict artifacts.

# H15.3 - waiting on resources; no extra tokenization

- Elapsed: H15.3 experiment runtime.
- Active run: h4 B job `167284` remains `PENDING (Resources)`; eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: unchanged; no B v3 output directory or checkpoint exists yet.
- Queue estimate: `squeue --start` still reports tentative start `2026-07-01T21:32:39Z` for `167284`.
- Feedback loop: pulled `origin/main`; no new feedback beyond `feedback/review-20260629T1032Z.md`.
- Data status: h4 train shards and h5 eval shards are available. Additional CPU-only tokenization was considered but not submitted because the available partition is H100-node backed and CPU/memory allocation could interfere with the 80-GPU backfill. Keep the queued 10x8 h4 B path prioritized.
- Next: continue monitoring `167284`; after allocation, verify first-step invariants, tok/s/MFU, and 25-minute checkpoint creation.

# H15.2 - queue topology alternatives rejected

- Elapsed: H15.2 experiment runtime.
- Active run: h4 B job `167284` remains `PENDING (Resources)`; eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: unchanged; no post-resume training tokens yet.
- Queue check: tested alternative 80-GPU topologies with `sbatch --test-only` only. 20x4 estimated `2026-07-06T14:39:41`, 16x5 estimated `2026-07-03T18:01:28`, and 40x2 was unavailable. The current queued 10x8 job has the best real backfill estimate (`2026-07-01T21:32:39Z` from the earlier `squeue --start` check).
- Decision: keep `167284` unchanged. This preserves the successful h4 A launch pattern and avoids changing topology without a queue benefit.
- Feedback loop: no new feedback after pull; test-only job ids were verified absent from `squeue`.
- Next: wait for `167284` allocation, then monitor first-step invariants and checkpoint creation.

# H15.1 - h4 B waiting on Slurm backfill

- Elapsed: H15.1 experiment runtime.
- Active run: h4 B Slurm job `167284` is still `PENDING (Resources)`. Dependent eval array `167289_[0-8]` remains `PENDING (Dependency)`.
- Step/tokens vs target: unchanged; no post-resume training tokens yet. Target remains B seed 2024 step 5,027 / 19,766,968,320 tokens.
- Measured MFU and tok/s: pending allocation.
- Node health/resources: `squeue --start` reports tentative start `2026-07-01T21:32:39Z` for job `167284`; Slurm backfill estimates can move. The request is still 10 full H100 nodes / 80 H100, excluding `cn02,cn10,cn17,cn34`.
- Feedback loop: pushed H15.0 eval queue state and pulled; no new feedback.
- Next: poll before/around the backfill window, or earlier if resources free. When B starts, verify first logs and 25-minute checkpoints; after B success, eval array `167289` should run automatically.

# H15.0 - h4 v3 eval array queued behind B

- Elapsed: H15.0 experiment runtime.
- Active run: h4 B Slurm job `167284` remains `PENDING (Resources)`. Dependent eval array `167289_[0-8]` is queued as `PENDING (Dependency)` with `afterok:167284`.
- Step/tokens vs target: no post-resume training tokens yet. B target remains step 5,027 / 19,766,968,320 tokens on the h4 shard stream. Eval outputs will use h5-disjoint shards.
- Measured MFU and tok/s: pending until `167284` starts.
- Node health/resources: B requests 80 H100 across 10 nodes and is blocked on resources. Eval array requests 1 H100 / 220G / 3h per task and excludes the same known bad/drained nodes.
- Feedback loop: latest feedback remains `feedback/review-20260629T1032Z.md`; no new feedback after the H14.9 push/pull.
- Next: monitor `167284` for allocation. After it starts, verify first logs for arm B, seed 2024, AdamW, bf16, grouped MoE, 80 world size, `micro_batch_size=4`, `grad_accum=6`, tok/s/MFU, and 25-minute checkpoint creation. Eval array `167289` should then run automatically after B success.

# H14.9 - h4 B v3 queued

- Elapsed: H14.9 experiment runtime.
- Active run: Slurm job `167284` (`engram-h4-B2024v3`) submitted and currently `PENDING (Resources)`.
- Step/tokens vs target: job target is h4 B seed 2024 from scratch to step 5,027 / 19,766,968,320 tokens, matching h4 A endpoint and preserving paired seed 2024 comparison. No new training tokens have run yet after resume.
- Measured MFU and tok/s: pending; use prior h4 B observed ~2.57-2.59M tok/s, MFU ~9.25-9.33% as ETA baseline once allocated.
- Node health/resources: request is 10 nodes / 80 H100, `--mem=1800G`, `--time=04:00:00`, excludes `cn02,cn10,cn17,cn34`; Slurm reason is `Resources` because other workloads currently occupy most H100 nodes.
- Feedback loop: latest pulled feedback remains `feedback/review-20260629T1032Z.md`, acknowledged in H14.8. No new feedback after the resume snapshot push.
- Next: monitor job `167284`; when it starts, verify build/optimizer/first-step logs, tok/s, MFU, and first 25-minute checkpoint. After final checkpoint, queue h5-disjoint knockout+slices+depth evals and push/pull.

# H14.8 - resume requested, h4 B relaunch prepared

- Elapsed: H14.8 experiment runtime. Operator resumed after the H14.7 resource-release pause; wall-clock calendar is no longer the original uninterrupted 24h schedule.
- Active run: none yet. Preparing to submit h4 B seed 2024 from scratch because prior h4 B job `165375` was canceled at step 4,668 / 5,027 and saved no final checkpoint.
- Step/tokens vs target: h4 A seed 2024 remains complete at step 5,027 / 19,766,968,320 tokens with final checkpoint `runs/pair_h4_A_seed2024_20B_mbs4_80_v2/ckpt_step005027.pt`. h4 B target remains same endpoint: 5,027 steps, 19,766,968,320 tokens, h4 shard stream.
- Measured MFU and tok/s: latest completed comparable h4 A finished at 2.70M tok/s, MFU 9.73%; canceled h4 B was ~2.57-2.59M tok/s, MFU ~9.25-9.33%.
- Node health/resources: no Engram Slurm jobs are running. Current cluster is mostly occupied by other workloads; only `cn30` is fully idle at resume time. Relaunch will request 10 full H100 nodes and may pend. Continue excluding `cn17`, `cn34`, `cn02`, and drained `cn10`.
- Feedback loop: pulled `origin/main` and read new `feedback/review-20260629T1032Z.md`. Acknowledged: resume by relaunching h4 B seed 2024 from scratch with same h4 stream/world size/batch/optimizer/precision/5,027-step endpoint, enable periodic checkpoints, then run h5-disjoint knockout+slices+depth. Also acknowledge reviewer expectation that 20B unique may still be data-limited and inconclusive.
- Relaunch script: added `scripts/slurm_h4_b_seed2024_resume.sh` with 10 nodes / 80 H100, bf16, AdamW, grouped MoE backend, `micro_batch_size=4`, `grad_accum=6`, `max_steps=5027`, and 25-minute checkpoints.
- Next: push this resume snapshot, submit the h4 B v3 Slurm job, record/push the job id, then monitor and pull feedback every ~2h.

# H14.7 - operator pause, H100 resources released

- Elapsed: H14.7
- Active run: none. Operator requested release of H100 resources; canceled h4 B job `165375` and dependent eval jobs `165432`-`165440`.
- Step/tokens vs target: h4 A completed step 5,027 / 19,766,968,320 tokens with exit `0:0` and final checkpoint `runs/pair_h4_A_seed2024_20B_mbs4_80_v2/ckpt_step005027.pt`. h4 B was canceled before final checkpoint at last logged step 4,668 / 5,027, 18,355,322,880 tokens.
- Measured MFU and tok/s: h4 A finished at 2.70M tok/s, MFU 9.73%. h4 B near cancellation was ~2.57-2.59M tok/s, MFU ~9.25-9.33%; official calibration baseline remains A 2,711,455 tok/s and B 2,609,871 tok/s.
- Preliminary verdict: `progress/PRELIMINARY.md` says NOT VERIFIED / INCONCLUSIVE for pair 1. Knockout did not degrade TriviaQA/PopQA; targeted slices are mixed. Engram path is active and grew, so this is not a dead-path bug, but the repeated 4.69B-unique training stream likely washed out the memory signal. Caveat from `feedback/review-20260629T0432Z.md`: h4 was a separate tokenization directory, but current manifests lack document IDs, so doc-level disjointness from pair-1 cannot be proven.
- Pair-1 final evals: B endpoint TriviaQA answer-NLL delta knockout-normal = -0.00663; PopQA = -0.01902. 5-shot EM is 0.0 normal and 0.0 knockout for both. h4 slices: global A-B = -0.00283, repeated-ngram A-B = -0.02377, entity-proxy A-B = +0.01585. Depth: B median resolves one layer earlier, but mean earliest layer is tied.
- Gate diagnostics: B step 959 -> 5027 final hidden delta RMS rose 0.0413 -> 0.0796; last-logit mean abs delta rose 0.0506 -> 0.1197; layer-6 contribution/hidden RMS ratio rose 0.00390 -> 0.00830. Alpha is saturated near 1.0, not suppressed.
- Storage: pair-1 checkpoints removed after saving/pushing diagnostics and preliminary results. Current retained large checkpoint is h4 A final only; VAST reports ~20T free.
- Knockout gate result: weak/no factual-collapse at B step 959. TriviaQA answer-NLL delta knockout-normal = +0.00656; PopQA delta = -0.01276. TriviaQA and PopQA QA-EM are both 0.0 normal and 0.0 knockout, so EM is floor/non-informative at this early checkpoint. Wiring diagnostic shows Engram is nonzero but small: block2 delta/hidden RMS 0.00107, block6 0.00365, final hidden delta RMS 0.0353, last-logit mean abs delta 0.0449.
- Held-out eval rule: targeted slices, depth, and loss eval must use disjoint data, not the repeated pair-1 training stream. Use `data/fineweb_edu_deepseek_h4/shards.txt` (20.002B-token h4 tranche) or another clean split for those evals.
- Git/progress channel: verified push to `origin/main` after non-destructive rebase onto updated `handoff.md`
- Authoritative plan: re-read updated 24h `handoff.md` in full after rebase; no 27B/U-shape sweep, use 6-run 0.48B activated paired plan
- Launcher: Slurm on `cluster43`, partition `all`, use `srun/sbatch`; commands carry explicit `--time/--mem` plus shell `timeout` for probes
- Node health: 80x H100-80GB reachable. Exclude `cn17` (confirmed CUDA context OOM on empty GPUs). Exclude `cn34` for training: despite passing calibration and a quick probe, pair-1 A job `165273` failed at `torch.cuda.set_device` on `cn34` rank67/local_rank3. Also avoid `cn02` for new batch-host launches: immediately after A, debug job `165314` on the A nodelist failed before stdout with `RaisedSignal:53`; the same debug script passed on `cn03,cn04,cn13,cn14,cn15,cn16,cn25,cn26,cn27,cn29`.
- Current 80GPU training nodelist: `cn03,cn04,cn13,cn14,cn15,cn16,cn25,cn26,cn27,cn29`; use `--cpus-per-task=16`, preserving world size, batch, optimizer, precision, and paired data order.
- Feedback loop: read `origin/main:feedback/review-20260629T0033Z.md` (VERDICT: ISSUES), `feedback/review-20260629T0234Z.md` (VERDICT: ON-TRACK), `feedback/review-20260629T0356Z.md` (VERDICT: ISSUES), `feedback/review-20260629T0432Z.md` (VERDICT: ON-TRACK), `feedback/review-20260629T0633Z.md` (VERDICT: ON-TRACK), correction `feedback/review-20260629T0644Z.md` (VERDICT: ON-TRACK), and new `feedback/review-20260629T0831Z.md` (VERDICT: ON-TRACK). Acknowledged the H7.5 knockout bug gate, held-out-slice contamination risk, and instruction not to coarsen experts for the secondary loss signal. Not applying expert coarsening because current `handoff.md` §2/§3 explicitly fixes the only arm difference as `88 routed` vs `68 routed + Engram`; wrote `feedback/reply-20260629T0036Z.md` for the first review. For the H8.0 review, endpoint answer-NLL knockout and gate-alpha / contribution-RMS diagnostics are complete. For the H8.4 review, current manifests cannot prove h4 document disjointness; h5 eval tranche now fixes this by whole-doc prefix skipping. For the H10.7 review, agreed with the unique-data pivot and 100B-token expectation; replied in `feedback/reply-20260629T0642Z.md` to clarify the slice CSV sign convention. The H10.7 correction agrees that `PRELIMINARY.md` was already correct; no result change needed. The H12.6 review says if the h4-pair verdict stays knockout-flat and slice-mixed, stop and write the honest final verdict rather than adding more seeds/tokens.
- User note: found and read `/mnt/vast/workspaces/JAIF/dy/code/symbolicLLM/DOC/43_intro.pdf` with `timeout`; it is 43 cluster usage guidance (Slurm, VAST, Apptainer, Spack) and does not conflict with `handoff.md`
- Environment: PyTorch 2.9.1+cu128, datasets/transformers/lm-eval present; FlashAttention/Transformer Engine absent; example PyTorch 2.7 Apptainer image also lacks Megablocks/Tutel/DeepSpeed/FlashAttention
- Judgment call: Muon modules not installed/vetted; fixed optimizer to AdamW for all runs
- Implementation: added pure PyTorch DDP scaffold, MoE full replication, EngramRead, tokenizer script, training entry, Slurm calibration script; fixed DDP loader seed to split ranks while preserving A/B pairing; added direct GPU/bf16 model build and `--no-checkpoint`; added DDP `no_sync()` during accumulation; added optional `ENGRAM_MOE_BACKEND=grouped` using `torch._grouped_mm`; added configurable `ENGRAM_CE_CHUNK_TOKENS` and DDP `gradient_as_bucket_view=True`; added tokenizer `load_dataset` retry/backoff for the next CPU tranche
- Local gates: `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py` passed; `PYTHONPATH=src pytest -q` passed 10/10 with 1 CUDA grouped-mm test skipped on login; `scripts/eval_token_slices.py --help`, `scripts/eval_depth_probe.py --help`, and `scripts/eval_qa_em.py --help` passed; synthetic small-checkpoint smokes for `eval_token_slices.py`, `eval_depth_probe.py`, and `eval_qa_em.py` passed on CPU; CUDA grouped-mm regression passed on 1xH100; synthetic and real-shard paired-loader first 100 batches hash matched exactly
- Tokenization: DeepSeek-V3 tokenizer + FineWeb-Edu `sample-350BT` smoke succeeded; real smoke paired-loader hash matched; tokenization script now batches docs and writes per-worker manifests
- Tokenization anomaly/fix: 80-worker job 165112 hit HF 504 and was canceled before 1B shard flush; fixed `finally` flush, disabled non-tty tqdm, and reduced shard size to 100M. Robust tranche 165134 failed on HF 504 but flushed partial output: 60 shards / 4.6908B tokens. Current pair-1 loader samples with replacement over those 60 shards, so training can proceed but repeated sampling is a data-quality caveat. CPU-only retry tranche `165276` completed successfully on cn05-08; generated `data/fineweb_edu_deepseek_h4/shards.txt` from manifests: 208 shards / 20,002,166,023 tokens / 75GB. This h4 tranche is available for held-out/slice eval or later seeds, not pair-1 B.
- Slurm smoke: 1xH100 tiny training passed; 80xH100 tiny DDP passed on clean nodelist after excluding `cn17`
- Full-model probes: A/B zero-step build pass on 1xH100 with ~74.9GB free after weights; A/B 1-step probes pass with AdamW state allocation; A accidental checkpoint removed (`27GB`)
- Invariants: active params `475,136,000` both arms; A non-embed `4,505,600,000`; B non-embed `4,505,598,976`; delta `1,024`; Engram sparse budget fraction `22.47%`; official 80GPU batch decomposition is mbs4/ga6 = `3,932,160` tokens/step (~4M)
- Calibration anomaly: full-model pure-PyTorch MoE uses Python expert dispatch; no Megablocks/Tutel/DeepSpeed/FlashAttention stack is installed. Current throughput is ~20.7x below the handoff planning target (~8.34M tok/s for 70B/run within ~2.33h)
- Optimization attempts: earlier padded batched PyTorch paths were rejected; native `torch._grouped_mm` is viable. Isolated 1xH100 MoE forward+backward improved from 78ms to 3ms; 1xH100 full-model grouped mbs1 steps 2-3 were ~0.13s/step; 64GPU grouped mbs1 steady steps 3-6 averaged 1.41M tok/s; mbs2 improved to 1.74M tok/s; mbs4 improved to 2.04M tok/s. Loop/no_sync 64GPU steady was only 0.466M tok/s
- Code status: default MoE backend remains `loop`; grouped backend must be enabled explicitly with `ENGRAM_MOE_BACKEND=grouped` until 80GPU calibration verifies it for both arms. `ENGRAM_CE_CHUNK_TOKENS` defaults to 256, preserving old behavior unless overridden. Added `scripts/eval_answer_nll.py` for first-B-checkpoint answer-NLL knockout gating on TriviaQA/PopQA/JSONL, plus `scripts/eval_qa_em.py` for the handoff's TriviaQA/PopQA on/off EM retention protocol. Added `scripts/eval_token_slices.py` for global/repeated-ngram/entity-proxy NLL slices and `scripts/eval_depth_probe.py` for LogitLens-style earliest-layer resolution. Eval scripts instantiate bf16 on CUDA and fp32 on CPU. Entity slice currently records `capitalized_token_proxy`; replace/augment with fast NER if time permits.
- Schedule impact: official measured throughput is far below the 8.34M tok/s handoff target. 70B/run would take ~7.16h for A and ~7.45h for B; 60B/run would still take ~6.14h/6.39h. The original 70B pair-1 preliminary cannot meet H12, and six 60-80B runs cannot fit 24h.
- Open anomaly: 64GPU `micro_batch_size=8, grad_accum=4` remains rejected. Default CE chunk 256 OOMed on first step; CE chunk 128 + DDP bucket-view completed step 1 at 1,270,903 tok/s but OOMed on step 2 after AdamW state allocation in `chunked_cross_entropy` (`64MiB` logits request, only `9-41MiB` free on failing ranks). `micro_batch_size=6, grad_accum=5` also OOMed on step 2: CE256 requested `126MiB`; CE128+expandable requested `64MiB` and was slower on step 1. These are hard memory gates under faithful 88/68 config.
- Tokens/run judgment call: for the H12 primary-verdict path, use a reduced 20B-token pair-1 run (5,086 steps at 3,932,160 tokens/step) and state this as a schedule-driven deviation from the 60-80B planning range. This is only for knockout/slices/depth preliminary evidence; do not claim a powered global-loss verdict from it. Extend pair-1 or add seeds only if time remains.
- Pair-1 A endpoint anomaly: job `165275` failed with Slurm `ExitCode=1:0` after rank0 logged step 5,034 and after a full 28.0GB checkpoint at step 5,027. No Python/NCCL/OOM stack was present in Slurm stdout. To preserve paired invariants, pair-1 endpoint is fixed to step 5,027 for both A and B.
- Pair-1 B relaunch: old dependency job `165281` was canceled after A failed; first relaunch `165313` hit `cn02` batch-host `RaisedSignal:53`; second relaunch `165316` used a valid node set but incorrectly passed `shards.txt` itself to `--token-files`, causing the expected loader "too short" error. Corrected job `165317` expanded the same 60 shard paths from `data/fineweb_edu_deepseek/shards.txt`, wrote first checkpoint at step 959, then failed after rank0 step 964 with no traceback in Slurm stdout.
- Checkpoint/save/storage anomaly: both A and B failed soon after large checkpoint saves while VAST was at/near full. Added synchronized checkpoint decision + DDP barrier and a `--checkpoint-minutes-override` knob; B final-only rerun uses `--checkpoint-minutes-override 9999` to save only the final checkpoint.
- Storage anomaly: VAST reported `0` global free space and refused `results/knockout` creation. Deleted old self-generated A intermediate checkpoints `ckpt_step001002.pt`, `ckpt_step002007.pt`, `ckpt_step003013.pt`, and `ckpt_step004020.pt`; kept A endpoint `ckpt_step005027.pt` and B first checkpoint `ckpt_step000959.pt`.
- Queued/active next run: none. To resume the h4 pair, relaunch B seed 2024 from scratch or implement/resume from an intermediate checkpoint policy; the canceled B run has no final checkpoint because it was configured final-only.
- H10.4 launch anomaly: initial h4 A job `165367` launched `torchrun --nnodes=10` only on the batch host, so it hung in rendezvous waiting for missing node agents. Canceled it before any rank-0 training step or checkpoint. Relaunched as `165373` with `srun --ntasks=$SLURM_NNODES --ntasks-per-node=1` so each node starts one torchrun agent, matching the successful multi-node pattern.
- H10.6 eval-tranche fix: added `--skip-tokens` to `src/engram/tokenize_fineweb.py` so future eval tokenization can skip a deterministic worker-stream prefix by whole documents. Started h5 eval-tokenization job `165374` to skip 1.26B tokens per worker (beyond h4 train prefix) and write 125M tokens per worker (~2B total) into `data/fineweb_edu_deepseek_h5_eval`.
- H10.7 h4 B queue: queued matching h4 B seed 2024 as Slurm job `165375` with `afterok:165373`, same h4 token stream and 5,027-step endpoint.
- H10.9 h5 eval tranche complete: tokenization job `165374` completed; `data/fineweb_edu_deepseek_h5_eval/shards.txt` has 32 shards / 2,004,168,518 tokens after skipping 20,160,030,489 prefix tokens by whole docs. Use h5, not h4, for h4-pair eval.
- H12.6 h4 eval queue: queued B final TriviaQA/PopQA answer-NLL + 5-shot EM knockout, A/B h5 slices, A/B h5 depth, and B gate diagnostics as jobs `165432`-`165440`.
- H14.7 operator pause: stopped local monitor sessions, canceled h4 B `165375` and dependent eval jobs `165432`-`165440`; verified no `engram-*` jobs remain in `squeue`.
- Milestone: A first checkpoint complete at `runs/pair1_A_seed1337_20B_mbs4_80_v2/ckpt_step001002.pt` (28.0GB); see `progress/logs/h5_pair1_A_first_checkpoint.md`.
- Milestone: A second checkpoint complete at `runs/pair1_A_seed1337_20B_mbs4_80_v2/ckpt_step002007.pt` (28.0GB); see `progress/logs/h6_pair1_A_second_checkpoint.md`.
- Milestone: A third checkpoint complete at `runs/pair1_A_seed1337_20B_mbs4_80_v2/ckpt_step003013.pt` (28.0GB); see `progress/logs/h6_pair1_A_third_checkpoint.md`.
- Milestone: A fourth checkpoint complete at `runs/pair1_A_seed1337_20B_mbs4_80_v2/ckpt_step004020.pt` (28.0GB); see `progress/logs/h7_pair1_A_fourth_checkpoint.md`.
- Milestone: h4 tokenization tranche complete; see `progress/logs/h5_tokenization_h4_complete.md`.
- Knockout eval preflight: `load_records()` loaded TriviaQA validation and PopQA test samples successfully, so the first-B-checkpoint knockout jobs should not block on initial dataset generation.
- Next: monitor B final-only to step 5,027. Treat first-checkpoint numbers as a weak/bug-gate warning and do not trust downstream/slice/loss conclusions yet. If final B checkpoint still shows no factual degradation under knockout, stop and debug Engram scale/wiring before additional seeds.
- ETA: B final-only endpoint around H10.1-H10.3 if throughput holds; then rerun knockout plus held-out h4 slices/depth for the preliminary verdict.
