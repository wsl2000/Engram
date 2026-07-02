# H30.6 - registered Tier-1 11h healthy

- Timestamp: 2026-07-02T11:43:00Z.
- Elapsed: H30.6 for the v3 resumed objective.
- Feedback loop: `git fetch origin --prune` found no new feedback beyond `feedback/review-20260701T2025Z.md`; branch is synchronized with `origin/main`.
- Active H100 usage remains 32: A train `175099` on `cn[08-09]`, B train `175100` on `cn[13-14]`, each 2 nodes / 16 H100 with `TimeLimit=20:00:00`, `MinMemoryNode=1800G`.
- Dependency-held jobs unchanged: A eval `175101` and B eval `175102` with `TimeLimit=01:00:00`, `MinMemoryNode=220G`; decision job `175103` with `TimeLimit=00:10:00`, `MinMemoryNode=16G`.
- Progress: A step 16,558 / 25,432, `tokens_seen=13,021,741,056`, ~340.5k tok/s, MFU ~0.0729. B step 16,176 / 25,432, `tokens_seen=12,721,324,032`, ~332.0k tok/s, MFU ~0.0711.
- Checkpoint rotation healthy: A keeps `ckpt_step015943.pt` and `ckpt_step016581.pt`, both 28,030,761,871 bytes. B keeps `ckpt_step015553.pt` and `ckpt_step016176.pt`, both 28,027,736,107 bytes.
- Disk: `/mnt/vast` has 2.5P free; `/tmp` has 238G free.
- Health: no error keywords in train stdout or rank-0 JSONL logs.
- ETA: roughly 5.2-5.8 hours of registered training remain, plus eval/decision.
- Next: continue monitoring; next required progress push by about 2026-07-02T13:43Z unless an anomaly, feedback update, or milestone lands earlier.

# H28.6 - registered Tier-1 halfway healthy

- Timestamp: 2026-07-02T09:41:00Z.
- Elapsed: H28.6 for the v3 resumed objective.
- Feedback loop: `git fetch origin --prune` found no new feedback beyond `feedback/review-20260701T2025Z.md`; branch is synchronized with `origin/main`.
- Active H100 usage remains 32: A train `175099` on `cn[08-09]`, B train `175100` on `cn[13-14]`, each 2 nodes / 16 H100 with `TimeLimit=20:00:00`, `MinMemoryNode=1800G`.
- Dependency-held jobs unchanged: A eval `175101` and B eval `175102` with `TimeLimit=01:00:00`, `MinMemoryNode=220G`; decision job `175103` with `TimeLimit=00:10:00`, `MinMemoryNode=16G`.
- Progress: A step 13,538 / 25,432, `tokens_seen=10,646,716,416`, ~340.2k tok/s, MFU ~0.0728. B step 13,227 / 25,432, `tokens_seen=10,402,136,064`, ~332.1k tok/s, MFU ~0.0711.
- Checkpoint rotation healthy: A keeps `ckpt_step012753.pt` and `ckpt_step013391.pt`, both 28,030,761,871 bytes. B keeps `ckpt_step012435.pt` and `ckpt_step013058.pt`, both 28,027,736,107 bytes.
- Disk: `/mnt/vast` has 2.5P free; `/tmp` has 238G free.
- Health: no error keywords in train stdout or rank-0 JSONL logs.
- ETA: roughly 7.0-7.7 hours of registered training remain, plus eval/decision.
- Next: continue monitoring; next required progress push by about 2026-07-02T11:41Z unless an anomaly, feedback update, or milestone lands earlier.

# H26.6 - registered Tier-1 7h healthy

- Timestamp: 2026-07-02T07:40:00Z.
- Elapsed: H26.6 for the v3 resumed objective.
- Feedback loop: `git fetch origin --prune` found no new feedback beyond `feedback/review-20260701T2025Z.md`; branch is synchronized with `origin/main`.
- Active H100 usage remains 32: A train `175099` on `cn[08-09]`, B train `175100` on `cn[13-14]`, each 2 nodes / 16 H100 with `TimeLimit=20:00:00`, `MinMemoryNode=1800G`.
- Dependency-held jobs unchanged: A eval `175101` and B eval `175102` with `TimeLimit=01:00:00`, `MinMemoryNode=220G`; decision job `175103` with `TimeLimit=00:10:00`, `MinMemoryNode=16G`.
- Progress: A step 10,533 / 25,432, `tokens_seen=8,283,488,256`, ~340.6k tok/s, MFU ~0.0729. B step 10,286 / 25,432, `tokens_seen=8,089,239,552`, ~331.8k tok/s, MFU ~0.0710.
- Checkpoint rotation healthy: A keeps `ckpt_step009563.pt` and `ckpt_step010201.pt`, both 28,030,761,871 bytes. B keeps `ckpt_step009320.pt` and `ckpt_step009943.pt`, both 28,027,736,107 bytes.
- Disk: `/mnt/vast` has 2.5P free; `/tmp` has 238G free.
- Health: no error keywords in train stdout or rank-0 JSONL logs.
- ETA: roughly 8.7-9.4 hours of registered training remain, plus eval/decision.
- Next: continue monitoring; next required progress push by about 2026-07-02T09:40Z unless an anomaly, feedback update, or milestone lands earlier.

# H24.6 - registered Tier-1 5h healthy

- Timestamp: 2026-07-02T05:38:00Z.
- Elapsed: H24.6 for the v3 resumed objective.
- Feedback loop: `git fetch origin --prune` found no new feedback beyond `feedback/review-20260701T2025Z.md`; branch is synchronized with `origin/main`.
- Active H100 usage remains 32: A train `175099` on `cn[08-09]`, B train `175100` on `cn[13-14]`, each 2 nodes / 16 H100 with `TimeLimit=20:00:00`, `MinMemoryNode=1800G`.
- Dependency-held jobs unchanged: A eval `175101` and B eval `175102` with `TimeLimit=01:00:00`, `MinMemoryNode=220G`; decision job `175103` with `TimeLimit=00:10:00`, `MinMemoryNode=16G`.
- Progress: A step 7,520 / 25,432, `tokens_seen=5,913,968,640`, ~340.2k tok/s, MFU ~0.0728. B step 7,336 / 25,432, `tokens_seen=5,769,265,152`, ~331.8k tok/s, MFU ~0.0710.
- Checkpoint rotation healthy: A keeps `ckpt_step006373.pt` and `ckpt_step007011.pt`, both 28,030,761,871 bytes. B keeps `ckpt_step006204.pt` and `ckpt_step006827.pt`, both 28,027,736,107 bytes.
- Disk: `/mnt/vast` has 2.5P free; `/tmp` has 238G free.
- Health: no error keywords in train stdout or rank-0 JSONL logs.
- ETA: roughly 10.8-11.4 hours of registered training remain, plus eval/decision.
- Next: continue monitoring; next required progress push by about 2026-07-02T07:38Z unless an anomaly, feedback update, or milestone lands earlier.

# H22.6 - registered Tier-1 3h healthy

- Timestamp: 2026-07-02T03:36:00Z.
- Elapsed: H22.6 for the v3 resumed objective.
- Feedback loop: `git fetch origin --prune` found no new feedback beyond `feedback/review-20260701T2025Z.md`; branch is synchronized with `origin/main`.
- Active H100 usage remains 32: A train `175099` on `cn[08-09]`, B train `175100` on `cn[13-14]`, each 2 nodes / 16 H100 with `TimeLimit=20:00:00`, `MinMemoryNode=1800G`.
- Dependency-held jobs unchanged: A eval `175101` and B eval `175102` with `TimeLimit=01:00:00`, `MinMemoryNode=220G`; decision job `175103` with `TimeLimit=00:10:00`, `MinMemoryNode=16G`.
- Progress: A step 4,459 / 25,432, `tokens_seen=3,506,700,288`, ~340.6k tok/s, MFU ~0.0729. B step 4,341 / 25,432, `tokens_seen=3,413,901,312`, ~331.6k tok/s, MFU ~0.0710.
- Checkpoint rotation healthy: A keeps `ckpt_step003821.pt` and complete `ckpt_step004459.pt`, both 28,030,761,871 bytes. B keeps `ckpt_step003712.pt` and `ckpt_step004335.pt`, both 28,027,736,107 bytes.
- Disk: `/mnt/vast` has 2.5P free; `/tmp` has 238G free.
- Health: no error keywords in train stdout or rank-0 JSONL logs.
- ETA: roughly 12.8-13.6 hours of registered training remain, plus eval/decision.
- Next: continue monitoring; next required progress push by about 2026-07-02T05:36Z unless an anomaly, feedback update, or milestone lands earlier.

# H20.6 - registered Tier-1 second checkpoints healthy

- Timestamp: 2026-07-02T01:37:00Z.
- Elapsed: H20.6 for the v3 resumed objective.
- Active H100 usage remains 32: A train `175099` on `cn[08-09]`, B train `175100` on `cn[13-14]`, each 2 nodes / 16 H100 with `TimeLimit=20:00:00` and `MinMemoryNode=1800G`.
- Registered eval/decision jobs remain dependency-held: `175101`/`175102` with `TimeLimit=01:00:00`, `MinMemoryNode=220G`; `175103` with `TimeLimit=00:10:00`, `MinMemoryNode=16G`.
- Progress: A step 1,522 / 25,432, `tokens_seen=1,196,949,504`, ~340.6k tok/s, MFU ~0.0729. B step 1,478 / 25,432, `tokens_seen=1,162,346,496`, ~331.8k tok/s, MFU ~0.0710.
- Checkpoints: A has `ckpt_step000627.pt` and `ckpt_step001265.pt`, both 28,030,761,871 bytes. B has `ckpt_step000602.pt` and `ckpt_step001224.pt`, both 28,027,736,107 bytes.
- Disk: `/mnt/vast` still has 2.5P free; `/tmp` has 238G free. Checkpoint rotation is currently keeping the expected two checkpoints per arm.
- Health: no error keywords in train stdout or rank-0 JSONL logs.
- ETA: roughly 15.0-15.7 hours of training remain, then eval/decision.
- Next: continue registered A/B training; next required progress push by about 2026-07-02T03:37Z unless a checkpoint, anomaly, feedback update, eval, or decision lands earlier.

# H20.1 - registered Tier-1 first checkpoints complete

- Timestamp: 2026-07-02T01:06:00Z.
- Elapsed: H20.1 for the v3 resumed objective.
- Active registered Tier-1 jobs remain healthy. A train `175099` is running on `cn[08-09]`, 2 nodes / 16 H100, `TimeLimit=20:00:00`, `MinMemoryNode=1800G`; B train `175100` is running on `cn[13-14]`, 2 nodes / 16 H100, `TimeLimit=20:00:00`, `MinMemoryNode=1800G`.
- Dependent jobs unchanged: A eval `175101` and B eval `175102` pending with `TimeLimit=01:00:00`, `MinMemoryNode=220G`; decision job `175103` pending with `TimeLimit=00:10:00`, `MinMemoryNode=16G`.
- First checkpoints are complete: A `runs/tier1_A_registered_R16_20b_tps50m/ckpt_step000627.pt` is 28,030,761,871 bytes; B `runs/tier1_B_registered_R16_20b_tps50m/ckpt_step000602.pt` is 28,027,736,107 bytes, matching expected B-size scale.
- Current progress: A step 753 / 25,432, `tokens_seen=592,183,296`, ~340.4k tok/s, MFU ~0.0729. B step 728 / 25,432, `tokens_seen=572,522,496`, ~331.3k tok/s, MFU ~0.0709.
- Health: no error keywords in train stdout or rank-0 JSONL logs; compile/DDP/optimizer already completed for both arms.
- ETA: at current throughput, remaining registered train time is roughly 15.8-16.3 hours plus eval/decision.
- Next: continue monitoring checkpoint rotation and 2-hour feedback/push cycle; no Tier-1 verdict until A/B final eval and `registered_decision_R16_20b_tps50m.json` land.

# H19.6 - registered Tier-1 A+B running

- Timestamp: 2026-07-02T00:38:00Z.
- Elapsed: H19.6 for the v3 resumed objective.
- Registered Tier-1 stream completed after the chunked-writer fix: `data/tier1/registered_R16_tokens20000000000_20b_tps50m`, `token_count=19,999,760,000`, `doc_count=160,000`, `base_docs=80,000`, `injected_docs=80,000`, `shard_count=399`, `tokens_per_shard=50,000,000`, `base_chunk_tokens=249,992`.
- Submitted registered A+B at frozen R=16, 20B tokens/arm, `STEPS=25,432`, `RUN_SUFFIX=_20b_tps50m`. Job table is `progress/results/tier1_registered_R16_20b_tps50m_jobs.txt`.
- A train `175099` is running on `cn[08-09]` with 2 nodes / 16 H100, `TimeLimit=20:00:00`, `ReqMem=3600G` total / `MinMemoryNode=1800G`. A eval `175101` is pending on `afterok:175099` with `TimeLimit=01:00:00`, `ReqMem=220G`.
- B train `175100` is running on `cn[13-14]` with 2 nodes / 16 H100, `TimeLimit=20:00:00`, `ReqMem=3600G` total / `MinMemoryNode=1800G`. B eval `175102` is pending on `afterok:175100` with `TimeLimit=01:00:00`, `ReqMem=220G`.
- Decision job `175103` is pending on both eval jobs with `TimeLimit=00:10:00`, `ReqMem=16G`.
- First metrics: A reached step 49 / 25,432, `tokens_seen=38,535,168`, ~337.8k tok/s, MFU ~0.0723. B reached step 40 / 25,432, `tokens_seen=31,457,280`, ~327.7k tok/s, MFU ~0.0702.
- Invariants seen in rank-0 logs: `world_size=16`, `loader_seed=1337`, `arm=A/B`, `seed=1337`, `moe_backend=grouped`, `ce_impl=memory_efficient`, `micro_batch_size=4`, `grad_accum_steps=6`, AdamW, bf16 compile path.
- Health: `torch_compile_done`, DDP wrap, and optimizer init completed for both arms; no `Traceback`, `RuntimeError`, OOM, stale-cache, no-space, `FAILED`, or `ChildFailed` keywords found in train logs/run dirs.
- Active H100 usage for this objective is 32. ETA at current throughput is roughly 16.5-17.0 hours to final checkpoints, plus eval/decision.
- Next: monitor to first 25-minute checkpoint for each arm, then continue 2-hour progress/pull cycle until registered eval/decision lands.

# H19.1 - registered stream builder stall fixed; retry prepared

- Timestamp: 2026-07-02T00:05:00Z.
- Elapsed: H19.1 for the v3 resumed objective.
- Anomaly: first registered Tier-1 R=16 20B stream build (`scripts/submit_tier1_registered.sh ... R=16 target_tokens=20000000000 steps=25432`) stalled after writing 92 shards / ~35G under `data/tier1/registered_R16_tokens20000000000`. It used CPU only and submitted no Slurm GPU jobs.
- Evidence: builder stayed at 92 shards from 2026-07-01T23:52:22Z to 2026-07-02T00:02:15Z with no `/proc` IO counter movement, while the Python process remained ~97% CPU and ~40G RSS. No H100 was consumed.
- Resource cleanup: canceled obsolete pending 128-H100 preflight job `168251` before the registered submission path; it was no longer part of the 2-node/80-H100-compatible Tier-1 plan and consumed no GPU when canceled.
- Fix committed in code before retry: `src/engram/tier1.py` now buffers stream output as numpy chunks rather than a huge Python `list[int]`; `scripts/submit_tier1_registered.sh` now accepts explicit `TOKENS_PER_SHARD` and `RUN_SUFFIX` so retries can use a new stream/run/result namespace.
- Validation: `PYTHONPATH=src python -m py_compile src/engram/tier1.py scripts/build_tier1_stream.py scripts/decide_tier1.py`, `bash -n scripts/submit_tier1_registered.sh scripts/submit_tier1_r_pilot.sh scripts/slurm_tier1_train.sh scripts/slurm_tier1_eval.sh`, and `git diff --check` all passed.
- Active H100 usage for this objective is 0; Slurm queue for this user is empty after the unrelated `geowam` job ended.
- Retry plan: rebuild and submit registered Tier-1 with `RUN_SUFFIX=_20b_tps50m`, `TOKENS_PER_SHARD=50000000`, `TRAIN_NODES=2`, `TRAIN_TIME=20:00:00`, `TRAIN_MEM=1800G`, `EVAL_TIME=01:00:00`, `EVAL_MEM=220G`, `DECIDE_TIME=00:10:00`, `DECIDE_MEM=16G`, frozen `R=16`, `TARGET_TOKENS=20,000,000,000`, and `STEPS=25,432`.

# H18.6 - R-pilot complete; freeze R=16

- Timestamp: 2026-07-01T23:35:00Z.
- Elapsed: H18.6 for the v3 resumed objective.
- Feedback loop: `git fetch origin` found no new remote feedback beyond `feedback/review-20260701T2025Z.md`; branch was synchronized before this milestone commit.
- R=32 train `173143` completed successfully (`0:0`) in `04:15:47` with 2 nodes / 16 H100, `TimeLimit=08:00:00`, `ReqMem=3600G` total / `MinMemoryNode=1800G`; final checkpoint `runs/tier1_A_rpilot_R32_2node_5b_compile/ckpt_step006358.pt` is complete at 28,030,761,871 bytes.
- R=32 eval `173144` completed successfully (`0:0`) in `00:03:32` with 1 H100, `TimeLimit=01:00:00`, `ReqMem=220G`.
- R=32 result: main `records=4500`, `normal_em=0.1542222222`, `knockout_em=0.1537777778`, `em_collapse=0.0004444444`, `mean_delta_knockout_minus_normal=0.0000570976`, McNemar `b=19/c=17/p=0.8679394004`; negative controls `records=500`, `normal_em=0`, `knockout_em=0`.
- R-pilot recall trend at 5B tokens, A-only: R=1 `0.0002222222`, R=2 `0.0002222222`, R=4 `0.0008888889`, R=8 `0.0064444444`, R=16 `0.0406666667`, R=32 `0.1542222222`.
- Freeze decision: apply the latest feedback rule and freeze registered Tier-1 at R=16. R=16 is the largest tested R below the ~8-10% A-recall backbone-hard bound; R=32 exceeds it at 15.42%.
- New artifact: `results/tier1/rpilot_summary_2node_5b_compile.csv` records the recall-vs-R pilot and the freeze eligibility decision.
- Active H100 usage for this objective is 0. The old 128-H100 preflight job `168251` remains pending only and consumes no GPU; the visible 1-H100 `geowam` job is unrelated and untouched.
- Disk: `/mnt/vast` has 2.5P free; `/tmp` has 238G free.
- Next: submit registered Tier-1 A+B at frozen R=16 with explicit Slurm limits (`TRAIN_TIME=08:00:00`, `TRAIN_MEM=1800G` per node unless the script requires a tighter value; eval `TimeLimit=01:00:00`, `Mem=220G`), then run B-knockout and targeted slices for the mechanism verdict.

# H17.6 - R32 train healthy at 3.89B tokens

- Timestamp: 2026-07-01T22:31:16Z.
- Elapsed: H17.6 for the v3 resumed objective.
- Feedback loop: `git fetch origin` found no new remote feedback beyond `feedback/review-20260701T2025Z.md`; branch is synchronized with `origin/main`.
- Active H100 usage for this objective remains 16 H100: only R=32 train `173143` is running on `cn[13-14]` with `TimeLimit=08:00:00`, `MinMemoryNode=1800G`. Dependent eval `173144` remains pending with `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- R=32 progress: step 4,941 / 6,358, `tokens_seen=3,885,760,512`, ~340.6k tok/s, MFU ~0.0729, `ce_impl=memory_efficient`, `moe_backend=grouped`, `micro_batch_size=4`, `grad_accum_steps=6`.
- Checkpoints: latest complete R=32 checkpoints are `ckpt_step003817.pt` and `ckpt_step004455.pt`, each 28,030,761,871 bytes.
- Health: error scan over R=32 train log/run dir found no `Traceback`, `RuntimeError`, `OOM`, `OSError`, `FAILED`, `ChildFailed`, or stale-cache errors.
- Disk: `/mnt/vast` has 2.5P free; `/tmp` has 238G free.
- ETA: at current throughput R=32 has roughly 1.11B tokens / 1,417 steps remaining, about 55 minutes of training plus final checkpoint and a ~3-4 minute eval.
- Next: monitor R=32 final checkpoint/eval, then choose freeze-R using the updated feedback rule: freeze R=32 if A-recall remains below ~8-10%, otherwise freeze R=16.

# H15.6 - feedback updates freeze-R rule; wait for R32

- Timestamp: 2026-07-01T20:28:05Z.
- Elapsed: H15.6 for the v3 resumed objective.
- Pulled and read `feedback/review-20260701T2025Z.md` (ON-TRACK). Feedback confirms the A-only R-pilot is doing what it should: A recall rises monotonically from R=1 to R=16 but remains below 10%, negative controls are zero, and knockout does not move A.
- Important correction adopted: freeze-R should be the largest tested R with A-recall below the backbone-hard bound, not the smallest. This maximizes the later registered B signal while keeping A non-circular/backbone-hard.
- Current freeze-R rule: if R=32 A-recall stays below roughly 8-10%, freeze at R=32; if R=32 reaches or exceeds ~10%, freeze at R=16.
- R=32 status: train `173143` is running on 2 nodes / 16 H100 with `TimeLimit=08:00:00`, `MinMemoryNode=1800G`; latest check at 2026-07-01T20:27:56Z reached step 1,867 / 6,358, `tokens_seen=1,468,268,544`, ~340k tok/s, MFU ~0.0728. Dependent eval `173144` remains pending with `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- Health: R=32 has complete checkpoints through `ckpt_step001265.pt`; error scan found no `Traceback`, `RuntimeError`, `OOM`, `OSError`, `FAILED`, `ChildFailed`, or stale-cache errors.
- Active H100 usage for this objective remains 16 H100, all from R=32 train.
- Next: continue monitoring R=32 to completion/eval, then choose freeze-R per the updated feedback rule.

# H15.1 - R16 eval succeeded; recall higher but knockout still not collapsing

- Timestamp: 2026-07-01T19:55:58Z.
- Elapsed: H15.1 for the v3 resumed objective.
- R=16 train `173049` completed successfully (`0:0`) in `04:16:25`; final checkpoint `runs/tier1_A_rpilot_R16_2node_5b_compile/ckpt_step006358.pt` is present and complete at 28,030,761,871 bytes.
- R=16 eval `173050` completed successfully (`0:0`) in `00:03:24` with `TimeLimit=01:00:00`, `ReqMem=220G`.
- R=16 eval artifacts are present: `results/tier1/rpilot_A_R16_2node_5b_compile.csv` and `results/tier1/rpilot_A_R16_2node_5b_compile.json`.
- R=16 result: main `records=4500`, `normal_em=0.0406666667`, `knockout_em=0.0417777778`, `em_collapse=-0.0011111111`, `mean_delta_knockout_minus_normal=-0.0007286735`, McNemar `b=7/c=12/p=0.3592834473`; negative controls `records=500`, `normal_em=0`, `knockout_em=0`.
- Recall rises by R=16, but knockout still does not collapse recall; it remains slightly higher than normal. This is evidence that the A-only injected-fact memorization is not dependent on Engram, as expected for the A-only R-pilot.
- Active H100 usage for this objective is now 16 H100: only R=32 train `173143` is running. Its dependent eval `173144` remains pending with `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- Next: monitor R=32 completion/eval, then aggregate recall-vs-R from R=1/2/4/8/16/32 and choose the freeze-R point for registered Tier-1 A/B.

# H15.0 - R8 eval succeeded; recall rises but no knockout collapse

- Timestamp: 2026-07-01T19:45:54Z.
- Elapsed: H15.0 for the v3 resumed objective.
- R=8 train `173044` completed successfully (`0:0`) in `04:15:57`; final checkpoint `runs/tier1_A_rpilot_R8_2node_5b_compile/ckpt_step006358.pt` is present and complete at 28,030,761,871 bytes.
- R=8 eval `173045` completed successfully (`0:0`) in `00:03:28` with `TimeLimit=01:00:00`, `ReqMem=220G`.
- R=8 eval artifacts are present: `results/tier1/rpilot_A_R8_2node_5b_compile.csv` and `results/tier1/rpilot_A_R8_2node_5b_compile.json`.
- R=8 result: main `records=4500`, `normal_em=0.0064444444`, `knockout_em=0.0071111111`, `em_collapse=-0.0006666667`, `mean_delta_knockout_minus_normal=-0.0004969736`, McNemar `b=1/c=4/p=0.375`; negative controls `records=500`, `normal_em=0`, `knockout_em=0`.
- Recall is now nonzero at R=8, but knockout does not collapse recall; it is slightly higher than normal at this point. This remains pilot evidence only, not a Tier-1 mechanism verdict.
- Active H100 usage for this objective is now 32 H100: R=16/R=32 trains are running. R=1/2/4/8 are complete.
- Next: monitor R=16 completion/eval `173050`, then R=32; aggregate recall-vs-R after all pilot evals complete.

# H14.8 - R4 eval succeeded; recall still near zero

- Timestamp: 2026-07-01T19:37:10Z.
- Elapsed: H14.8 for the v3 resumed objective.
- R=4 train `173041` completed successfully (`0:0`) in `04:15:55`; final checkpoint `runs/tier1_A_rpilot_R4_2node_5b_compile/ckpt_step006358.pt` is present and complete at 28,030,761,871 bytes.
- R=4 eval `173042` completed successfully (`0:0`) in `00:03:20` with `TimeLimit=01:00:00`, `ReqMem=220G`.
- R=4 eval artifacts are present: `results/tier1/rpilot_A_R4_2node_5b_compile.csv` and `results/tier1/rpilot_A_R4_2node_5b_compile.json`.
- R=4 result: main `records=4500`, `normal_em=0.0008888889`, `knockout_em=0.0011111111`, `em_collapse=-0.0002222222`, `mean_delta_knockout_minus_normal=-0.0000244341`, McNemar `b=0/c=1/p=1.0`; negative controls `records=500`, `normal_em=0`, `knockout_em=0`.
- Current R-pilot trend across R=1/2/4 remains near-zero recall, so knockout remains non-informative at these R values. No Tier-1 mechanism verdict is claimed.
- Active H100 usage for this objective is now 48 H100: R=8/R=16/R=32 trains are running. R=1/2/4 are complete.
- Next: monitor R=8 completion/eval `173045`, then R=16/R=32; aggregate recall-vs-R after all pilot evals complete.

# H14.6 - R2 eval succeeded; low-recall pilot trend continues

- Timestamp: 2026-07-01T19:27:46Z.
- Elapsed: H14.6 for the v3 resumed objective.
- R=2 train `173037` completed successfully (`0:0`) in `04:15:48`; final checkpoint `runs/tier1_A_rpilot_R2_2node_5b_compile/ckpt_step006358.pt` is present and complete at 28,030,761,871 bytes.
- R=2 eval `173038` completed successfully (`0:0`) in `00:03:25` with `TimeLimit=01:00:00`, `ReqMem=220G`.
- R=2 eval artifacts are present: `results/tier1/rpilot_A_R2_2node_5b_compile.csv` and `results/tier1/rpilot_A_R2_2node_5b_compile.json`.
- R=2 result: main `records=4500`, `normal_em=0.0002222222`, `knockout_em=0.0002222222`, `em_collapse=0.0`, `mean_delta_knockout_minus_normal=0.0001220469`, McNemar `b=0/c=0/p=1.0`; negative controls `records=500`, `normal_em=0`, `knockout_em=0`.
- Current R-pilot recall trend: R=1 and R=2 are both essentially zero recall, so knockout is not yet informative at these R values. No Tier-1 mechanism verdict is claimed.
- Active H100 usage for this objective is now 64 H100: R=4/8/16/32 trains are running. R=1/R=2 are complete.
- Next: monitor R=4 completion/eval `173042`, then R=8/R=16/R=32; aggregate recall-vs-R only after all pilot evals complete.

# H14.4 - R1 eval succeeded; R32 train released

- Timestamp: 2026-07-01T19:16:00Z.
- Elapsed: H14.4 for the v3 resumed objective.
- R=1 eval retry `173180` completed successfully (`0:0`) in `00:03:21` with `TimeLimit=01:00:00`, `ReqMem=220G`.
- R=1 eval artifacts are present: `results/tier1/rpilot_A_R1_2node_5b_compile.csv` (5,000 rows) and `results/tier1/rpilot_A_R1_2node_5b_compile.json`.
- R=1 result at R=1/5B: main `records=4500`, `normal_em=0.0002222222`, `knockout_em=0.0002222222`, `em_collapse=0.0`, `mean_delta_knockout_minus_normal=-0.0021243813`, McNemar `b=0/c=0/p=1.0`; negative controls `records=500`, `normal_em=0`, `knockout_em=0`. This is a low-recall R=1 pilot point, not a Tier-1 verdict.
- R=32 train `173143` released after the successful retry eval and is running on `cn[13-14]` with 2 nodes / 16 H100, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`; dependent eval `173144` remains pending on `afterok:173143` with `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- R=32 early metrics: step 71 / 6,358, `tokens_seen=55,836,672`, ~337.5k tok/s, MFU ~0.0722, `ce_impl=memory_efficient`; no error keywords in the R=32 train log/run dir.
- Active H100 usage for this objective is back to 80 H100: R=2/4/8/16/32 trains are running. R=1 is complete.
- Remaining active train progress: R=2 step 6,225 / 6,358 (`tokens_seen=4,895,539,200`), R=4 step 5,983 / 6,358 (`tokens_seen=4,705,222,656`), R=8 step 5,742 / 6,358 (`tokens_seen=4,515,692,544`), R=16 step 5,507 / 6,358 (`tokens_seen=4,330,881,024`).
- Next: monitor R=2 completion/eval `173038`, then R=4/R=8/R=16/R=32 evals; aggregate R-pilot recall-vs-R after all pilot evals complete.

# H14.3 - R1 train complete; eval dtype failure fixed and retried

- Timestamp: 2026-07-01T19:09:43Z.
- Elapsed: H14.3 for the v3 resumed objective.
- R=1 train retry `172916` completed successfully (`0:0`) in `04:15:46` with 2 nodes / 16 H100, `TimeLimit=08:00:00`, `ReqMem=3600G`; final step reached `6,358 / 6,358`, `tokens_seen=5,000,134,656`, final logged tok/s ~340.5k, MFU ~0.0729.
- Final R=1 checkpoint is present and complete: `runs/tier1_A_rpilot_R1_2node_5b_compile/ckpt_step006358.pt`, 28,030,761,871 bytes.
- Anomaly: dependent eval `172919` failed after 50s with `RuntimeError: expected mat1 and mat2 to have the same dtype, but got: float != c10::BFloat16`. Root cause was `scripts/eval_injected_facts.py` not using bf16 autocast while the grouped MoE router path casts activations to fp32 and checkpoint weights are bf16.
- Fix: added CUDA bf16 autocast around the model/logit forward path in `scripts/eval_injected_facts.py`; `PYTHONPATH=src python -m py_compile scripts/eval_injected_facts.py` and `git diff --check` passed.
- Retried R=1 eval as job `173180` with explicit `TimeLimit=01:00:00`, `MinMemoryNode=220G`; it is running on `cn16`.
- R=32 dependency repair: the existing R=32 train job `173143` had become `DependencyNeverSatisfied` because it depended on failed eval `172919`; updated it in-place to `Dependency=afterok:173180(unfulfilled)`. Its train limits remain 2 nodes / 16 H100, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`; eval `173144` remains `afterok:173143`, `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- Active H100 usage for this objective is now 65 H100: R=2/4/8/16 trains use 64 H100 and R=1 eval retry uses 1 H100. R=32 is pending on dependency and inactive.
- Next: monitor eval `173180` to completion, then verify `results/tier1/rpilot_A_R1_2node_5b_compile.{json,csv}` and R32 train release.

# H13.1 - R32 stream built and dependent jobs verified

- Timestamp: 2026-07-01T17:55:52Z.
- Elapsed: H13.1 for the v3 resumed objective.
- R=32 CPU submitter `173134` completed successfully (`0:0`) in `00:09:23` with `TimeLimit=04:00:00`, `ReqMem=512G`.
- R=32 stream is built under `data/tier1/rpilot_R32_tokens5000000000`: `token_count=4,999,520,000`, `doc_count=320,000`, `base_docs=160,000`, `injected_docs=160,000`, `shard_count=50`, size ~19G.
- Job table now includes R=32: train `173143`, eval `173144`, `run_suffix=_2node_5b_compile`, `target_tokens=5,000,000,000`, `steps=6,358`.
- Verified R=32 train `173143`: pending on `Dependency=afterok:172919(unfulfilled)`, requests 2 nodes / 16 H100, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`, and excludes the same bad nodes as the other Tier-1 train jobs.
- Verified R=32 eval `173144`: pending on `Dependency=afterok:173143(unfulfilled)`, requests 1 H100, `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- Active H100 usage remains 80 for this objective: R=1/2/4/8/16 trains are running; R=32 is dependency-held and inactive.
- Train progress: R=1 step 4,583 / 6,358 (`tokens_seen=3,604,217,856`, ~340.6k tok/s, MFU ~0.0729); R=2 step 4,210 / 6,358 (`tokens_seen=3,310,878,720`, ~341.1k tok/s, MFU ~0.0730); R=4 step 3,972 / 6,358 (`tokens_seen=3,123,707,904`, ~340.2k tok/s, MFU ~0.0728); R=8 step 3,745 / 6,358 (`tokens_seen=2,945,187,840`, ~341.0k tok/s, MFU ~0.0730); R=16 step 3,498 / 6,358 (`tokens_seen=2,750,939,136`, ~339.3k tok/s, MFU ~0.0726).
- Health: error scan across active train logs/run dirs and the R32 submitter log found no `Traceback`, `RuntimeError`, `OOM`, `OSError`, `FAILED`, `ChildFailed`, or stale-cache errors.
- Next: monitor R=1 completion and eval `172919`; R=32 train should remain pending until that eval succeeds.

# H12.9 - R32 submitter queued with dependency gate

- Timestamp: 2026-07-01T17:39:15Z.
- Elapsed: H12.9 for the v3 resumed objective.
- Submitted R=32 CPU submitter `173134` with explicit `TimeLimit=04:00:00`, `MinMemoryNode=512G`; it is pending on scheduler priority and consumes no GPU while pending.
- R=32 train is configured to be submitted by that job with `TRAIN_DEPENDENCY=afterok:172919`, so the 2-node / 16-H100 train cannot start until the R=1 eval job `172919` has completed successfully.
- R=32 train/eval limits passed through the submitter: `TRAIN_NODES=2`, `TRAIN_TIME=08:00:00`, `TRAIN_MEM=1800G`, `EVAL_TIME=01:00:00`, `EVAL_MEM=220G`, `RUN_SUFFIX=_2node_5b_compile`, `TARGET_TOKENS=5,000,000,000`, `STEPS=6,358`.
- Active H100 usage remains 80 for this objective: R=1/2/4/8/16 trains are running; R=32 is not active and has no train job id yet.
- Latest train health immediately before this submission remained clean: no error keywords across active train logs/run dirs, and R1/R2/R4/R8/R16 were all progressing at ~339-341k tok/s with MFU ~0.0726-0.0730.
- Next: monitor submitter `173134`; once it appends R=32 train/eval IDs to `progress/results/tier1_rpilot_5b_jobs.tsv`, verify the train job dependency and Slurm limits, then push the updated job table.

# H12.7 - 5B R-pilot stable; checkpoint write verified

- Timestamp: 2026-07-01T17:27:05Z.
- Elapsed: H12.7 for the v3 resumed objective.
- Feedback loop: `git pull --rebase` returned already up to date; latest feedback remains `feedback/review-20260701T1625Z.md` (ON-TRACK).
- Active H100 usage for this objective remains 80 H100: five 2-node / 16-H100 train jobs are running for R=1/2/4/8/16. R=32 remains held until one 2-node train frees resources.
- Explicit Slurm limits currently in force: each train job uses `TimeLimit=08:00:00`, `MinMemoryNode=1800G`; each dependent eval job uses `TimeLimit=01:00:00`, `MinMemoryNode=220G`; the completed R=2/4/8/16 CPU submitter used `TimeLimit=08:00:00`, `MinMemoryNode=512G`.
- Train progress: R=1 step 3,863 / 6,358 (`tokens_seen=3,037,986,816`, ~340k tok/s, MFU ~0.0728); R=2 step 3,489 / 6,358 (`tokens_seen=2,743,861,248`, ~341k tok/s, MFU ~0.0730); R=4 step 3,253 / 6,358 (`tokens_seen=2,558,263,296`, ~339k tok/s, MFU ~0.0726); R=8 step 3,025 / 6,358 (`tokens_seen=2,378,956,800`, ~341k tok/s, MFU ~0.0730); R=16 step 2,778 / 6,358 (`tokens_seen=2,184,708,096`, ~340k tok/s, MFU ~0.0728).
- Health: grep over all five active train logs and run dirs found no `Traceback`, `RuntimeError`, `OOM`, `OSError`, `FAILED`, `ChildFailed`, or stale-cache errors.
- Checkpoint sanity: the previously observed small R=1 `ckpt_step003816.pt` was an in-progress write; it is now complete at 28,030,761,871 bytes.
- Disk: VAST reports 2.5P free on `/mnt/vast`; local `/tmp` has 238G free for per-job compile caches.
- Next: keep monitoring to R=1 completion and dependent eval `172919`; once a 2-node train allocation frees, submit R=32 with explicit `TRAIN_TIME=08:00:00`, `TRAIN_MEM=1800G`, `EVAL_TIME=01:00:00`, `EVAL_MEM=220G`, and submitter `--time=04:00:00 --mem=512G`.

# H12.1 - feedback confirms rung-0 apparatus validity

- Timestamp: 2026-07-01T16:53:12Z.
- Elapsed: H12.1 for the v3 resumed objective.
- Pulled and read `feedback/review-20260701T1625Z.md` (ON-TRACK). It confirms rung-0 `kb-inject` passed cleanly and treats the certain-verdict apparatus as proven/sensitive.
- Local rung-0 summary matches feedback: `records=200`, `normal_em=1.0`, `knockout_em=0.0`, `em_collapse=1.0`, McNemar `b=200/c=0`, `mcnemar_exact_p=1.2446030555722283e-60`, and `key_identity_passed=true`.
- Updated `progress/PRELIMINARY.md` to distinguish positive apparatus validity from the still-pending Tier-1/Tier-2 Engram verdict. No recall-vs-R/frozen-R/registered-B/knockout verdict is claimed yet.
- Feedback also notes Tier-2 MFU risk: current compile+memory-efficient CE path is actually enabled but still only ~7.3% MFU at mbs=4; before Tier-2, test whether memory-efficient/fused CE permits mbs=8 and do not waive the 18-20% gate into a 6-day run.
- Active H100 usage remains 80 H100 for this objective. R=32 remains held until one 2-node train frees resources.
- Next: continue the R=1/2/4/8/16 A-only pilot to eval completion, then freeze R from A-only recall.

# H11.6 - current preliminary status updated

- Timestamp: 2026-07-01T16:21:11Z.
- Elapsed: H11.6 for the v3 resumed objective.
- Updated `progress/PRELIMINARY.md` to supersede the old June 29 pair-1 preliminary with the current v3 honest status: no Engram verdict yet, because the 5B/R A-only R-pilot is still training and no recall-vs-R, frozen R, registered A/B, B-knockout, paired NLL, McNemar, or Tier-2 result exists yet.
- Current operational evidence is positive only for apparatus/runtime health: data gate passed, injected-fact streams exist, compile-cache failure fixed, five R-pilot trains are stable, and logs show no OOM/traceback/stale-cache failure.
- Active H100 usage remains 80 H100 for this objective. R=32 remains held until one 2-node train frees resources.
- Next: continue monitoring to completion/eval, then freeze R from A-only recall and proceed to registered Tier-1.

# H11.5 - 5B R-pilot mid-run healthy

- Timestamp: 2026-07-01T16:19:45Z.
- Elapsed: H11.5 for the v3 resumed objective.
- Active H100 usage now: 80 H100 allocated by this resumed objective. Five train jobs remain running: R=1 `172916`, R=2 `173037`, R=4 `173041`, R=8 `173044`, R=16 `173049`; their eval jobs remain pending on dependencies.
- Train progress: R=1 step 2,184 / 6,358 (`tokens_seen=1,717,567,488`, ~340k tok/s, MFU ~0.0727); R=2 step 1,816 / 6,358 (`tokens_seen=1,428,160,512`, ~340k tok/s, MFU ~0.0728); R=4 step 1,575 / 6,358 (`tokens_seen=1,238,630,400`, ~340k tok/s, MFU ~0.0728); R=8 step 1,332 / 6,358 (`tokens_seen=1,047,527,424`, ~340k tok/s, MFU ~0.0729); R=16 step 1,102 / 6,358 (`tokens_seen=866,648,064`, ~340k tok/s, MFU ~0.0728).
- Health: grep over all five train logs still found no `Traceback`, `RuntimeError`, `OutOfMemory`, stale-cache `OSError`, or `ChildFailed`.
- Checkpoints: all active R values have at least one checkpoint. R=1/R=2/R=4/R=8 have rotated two-checkpoint sets; R=16 has `ckpt_step000624.pt`.
- Disk: VAST free space is 16T. Checkpoint and Tier-1 stream growth remain within budget.
- Feedback loop: `git fetch origin` produced no new remote updates; branch is synchronized with `origin/main`.
- Next: keep monitoring to completion/eval; submit R=32 only after one 2-node train frees resources.

# H11.0 - five-way 5B R-pilot stable

- Timestamp: 2026-07-01T15:48:16Z.
- Elapsed: H11.0 for the v3 resumed objective.
- Active H100 usage now: 80 H100 allocated by this resumed objective across R=1/2/4/8/16 A-only 5B trains. One unrelated same-user 1-H100 job is present and untouched.
- Train progress: R=1 step 1,394 / 6,358 (`tokens_seen=1,096,286,208`, ~340k tok/s, MFU ~0.0728); R=2 step 1,025 / 6,358 (`tokens_seen=806,092,800`, ~341k tok/s, MFU ~0.0730); R=4 step 785 / 6,358 (`tokens_seen=617,349,120`, ~340k tok/s, MFU ~0.0729); R=8 step 557 / 6,358 (`tokens_seen=438,042,624`, ~340k tok/s, MFU ~0.0727); R=16 step 313 / 6,358 (`tokens_seen=246,153,216`, ~340k tok/s, MFU ~0.0728).
- Health: grep over all five train logs found no `Traceback`, `RuntimeError`, `OutOfMemory`, stale-cache `OSError`, or `ChildFailed` after the local-cache fix.
- Checkpoints: R=1 has `ckpt_step000626.pt` and `ckpt_step001264.pt`; R=2 has `ckpt_step000627.pt`; R=4 has `ckpt_step000627.pt`; R=8/R=16 have not reached first checkpoint windows yet.
- Disk: VAST still has 17T free. `data/tier1` and checkpoint growth are within the stated disk budget.
- Feedback loop: `git fetch origin` produced no new remote updates; branch is synchronized with `origin/main`.
- Next: keep monitoring until R=1 completes and triggers eval `172919`; then submit/queue R=32 only after at least one 2-node training allocation frees.

# H10.8 - R16 5B compile train running; capped pilot set launched

- Timestamp: 2026-07-01T15:36:14Z.
- Elapsed: H10.8 for the v3 resumed objective.
- R=16 stream completed: `token_count=4,999,760,000`, `doc_count=160,000`, `shard_count=50`. R=16 train/eval jobs are `173049/173050`; train is running on `cn[18,26]` with 2 nodes / 16 H100, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`; eval is pending on `afterok:173049` with `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- R=16 compile/cache status: reached step 16 / 6,358, `tokens_seen=12,582,912`, `tokens_per_s=337,193`, MFU `0.0722`, `ce_impl=memory_efficient`; no local-cache Triton failure.
- CPU submitter `172988` completed successfully (`0:0`, elapsed `00:37:41`, `TimeLimit=08:00:00`, `MinMemoryNode=512G`) after building and submitting R=2/4/8/16.
- Active H100 usage now: 80 H100 allocated by this resumed objective: R=1 `172916`, R=2 `173037`, R=4 `173041`, R=8 `173044`, R=16 `173049`. There is also one unrelated same-user 1-H100 job `173043_0`, not touched. The 128-H100 preflight `168251` remains pending.
- Disk: `data/tier1` is 317G. Run dirs are ~27G for R=1 and R=2 after first checkpoints; R=4/R=8/R=16 have not reached checkpoint windows yet.
- Next: do not submit R=32 until one 2-node train finishes. Monitor all five trains for checkpoint/finish and allow dependent evals to run; then collect R-pilot recall and freeze R.

# H10.6 - R8 5B compile train running

- Timestamp: 2026-07-01T15:27:38Z.
- Elapsed: H10.6 for the v3 resumed objective.
- R=8 stream completed: `token_count=4,999,880,000`, `doc_count=80,000`, `shard_count=50`. R=8 train/eval jobs are `173044/173045`; train is running on `cn[09,33]` with 2 nodes / 16 H100, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`; eval is pending on `afterok:173044` with `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- R=8 compile/cache status: reached step 36 / 6,358, `tokens_seen=28,311,552`, `tokens_per_s=338,336`, MFU `0.0724`, `ce_impl=memory_efficient`; no local-cache Triton failure.
- Active H100 usage now: 64 H100 allocated by this resumed objective: R=1 `172916`, R=2 `173037`, R=4 `173041`, R=8 `173044`. There is also one unrelated same-user 1-H100 job `173043_0` (`geowam-b64-page4d-clean`), not touched. CPU submitter `172988` is building R=16. The 128-H100 preflight `168251` remains pending.
- Next: monitor `172988` for R=16 job emission. R=32 remains held until one 2-node train finishes so this objective stays at <=80 H100 active training.

# H10.4 - R4 5B compile train running

- Timestamp: 2026-07-01T15:17:51Z.
- Elapsed: H10.4 for the v3 resumed objective.
- R=4 stream completed: `token_count=4,999,940,000`, `doc_count=40,000`, `shard_count=50`. R=4 train/eval jobs are `173041/173042`; train is running on `cn[31-32]` with 2 nodes / 16 H100, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`; eval is pending on `afterok:173041` with `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- R=4 compile/cache status: reached step 29 / 6,358, `tokens_seen=22,806,528`, `tokens_per_s=338,921`, MFU `0.0725`, `ce_impl=memory_efficient`; no local-cache Triton failure.
- Active H100 usage now: 48 H100 allocated by this resumed objective: R=1 `172916`, R=2 `173037`, R=4 `173041`. CPU submitter `172988` is building R=8. The 128-H100 preflight `168251` remains pending.
- Checkpoints: R=1 wrote `runs/tier1_A_rpilot_R1_2node_5b_compile/ckpt_step000626.pt` (~28G). R=2/R=4 have not yet reached their first checkpoint window.
- Next: monitor `172988` for R=8 and R=16 job emission. Keep R=32 held until one 2-node train finishes so total active Tier-1 train use stays <=80 H100.

# H10.2 - R2 5B compile train running; R4 stream building

- Timestamp: 2026-07-01T15:09:07Z.
- Elapsed: H10.2 for the v3 resumed objective.
- Submitted remaining capped pilot set: CPU submitter `172988` is running for R=2,4,8,16 with explicit `TimeLimit=08:00:00`, `MinMemoryNode=512G`; R=32 is intentionally held back until one 2-node train finishes, keeping worst-case Tier-1 train concurrency at <=80 H100.
- R=2 stream completed: `token_count=4,999,970,000`, `doc_count=20,000`, `shard_count=50`. R=2 train/eval jobs are `173037/173038`; train is running on `cn[24-25]` with 2 nodes / 16 H100, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`; eval is pending on `afterok:173037` with `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- R=2 compile/cache status: reached step 44 / 6,358, `tokens_seen=34,603,008`, `tokens_per_s=338,843`, MFU `0.0725`, `ce_impl=memory_efficient`; no local-cache Triton failure.
- R=1 status: train `172916` reached step 428 / 6,358, `tokens_seen=336,592,896`, `tokens_per_s=339,859`, MFU `0.0727`; eval `172919` remains pending on train completion.
- Active H100 usage now: 32 H100 allocated by this resumed objective. The 128-H100 preflight `168251` remains pending.
- Next: monitor `172988` as it builds R=4/8/16 and emits train/eval jobs; verify each emitted train job keeps 2 nodes / 16 H100, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`.

# H10.0 - R1 5B compile retry running

- Timestamp: 2026-07-01T14:55:37Z.
- Elapsed: H10.0 for the v3 resumed objective.
- R=1 retry jobs: train `172916`, eval `172919`. Train is running on `cn[13-14]` with 2 nodes / 16 H100, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`; eval is pending on `afterok:172916` with 1 H100, `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- Compile-cache fix status: effective. The retry passed the previous compile failure point, emitted `torch_compile_done`, and reached step 85 / 6,358 without Triton stale-cache errors.
- Latest R=1 metric: `tokens_seen=66,846,720`, `tokens_per_s=338,270`, MFU `0.0724`, `ce_impl=memory_efficient`, `moe_backend=grouped`, `micro_batch_size=4`, `grad_accum_steps=6`.
- Active H100 usage now: 16 H100 allocated by this resumed objective. The 128-H100 preflight `168251` remains pending (`AssocGrpGRES`).
- Job table: appended the retry line to `progress/results/tier1_rpilot_5b_jobs.tsv`; the first failed attempt remains recorded for audit.
- Next: push this R=1 retry status, then submit R=2,4,8,16,32 with `TARGET_TOKENS=5000000000`, `STEPS=6358`, `RUN_SUFFIX=_2node_5b_compile`, train `TimeLimit=08:00:00`/`MinMemoryNode=1800G`, and eval `TimeLimit=01:00:00`/`MinMemoryNode=220G`.

# H9.9 - compile cache failure fixed before R1 retry

- Timestamp: 2026-07-01T14:50:22Z.
- Elapsed: H9.9 for the v3 resumed objective.
- R=1 5B stream completed under `data/tier1/rpilot_R1_tokens5000000000`: `token_count=4,999,985,000`, `doc_count=10,000`, `base_docs=5,000`, `injected_docs=5,000`, `shard_count=50`.
- First R=1 compile train attempt `172863` had correct Slurm limits and allocation (`2 nodes / 16 H100`, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`) but failed after 79s before step 1. Dependent eval `172864` was canceled after `DependencyNeverSatisfied`.
- Root cause: `torch.compile`/Triton failed while reading/writing the shared VAST-backed compile cache (`/mnt/vast/workspaces/JAIF/dy/cache/triton` and `/mnt/vast/workspaces/JAIF/dy/tmp/torchinductor_*`), with `OSError: [Errno 116] Stale file handle` and `OSError: [Errno 521]`. This was an infrastructure/cache-location failure, not a model OOM or data failure.
- Fix: `scripts/slurm_tier1_train.sh` now creates per-job/per-node-task local cache dirs under `/tmp` and exports `TORCHINDUCTOR_CACHE_DIR`, `TRITON_CACHE_DIR`, and `XDG_CACHE_HOME` inside each `srun` task before `torchrun`.
- Current queue: only 128-H100 preflight `168251` is pending. Active H100 usage now: 0 H100 allocated by this resumed objective.
- Validation: `bash -n scripts/slurm_tier1_train.sh` and `git diff --check` passed.
- Next: push this anomaly/fix, then resubmit R=1 5B compile train directly against the completed stream with the same explicit train/eval limits. If local cache compile reaches first metrics, submit R=2,4,8,16,32.

# H9.7 - feedback adopted: switch R-pilot to 5B/R with compile

- Timestamp: 2026-07-01T14:36:23Z.
- Elapsed: H9.7 for the v3 resumed objective.
- Feedback read: `feedback/review-20260701T1425Z.md` is ON-TRACK and recommended shortening the A-only R-pilot to ~5B/R plus applying Tier-1 compile/memory-efficient CE now. Adopted because R1/R2 had only reached ~0.57B of the old 20B target.
- Canceled old 20B pilot jobs: R=1 train/eval `172713/172714`, R=2 train/eval `172715/172716`, and R4+ CPU submitter `172750`. This released the active 32 H100 allocation. Old R1/R2 run dirs are retained as canceled evidence and will not be resumed.
- Code changes: Tier-1 train wrapper now defaults to `ENGRAM_TORCH_COMPILE=1`, `ENGRAM_TORCH_COMPILE_MODE=default`, and `ENGRAM_CE_IMPL=memory_efficient`; the train entry can also read `ENGRAM_TORCH_COMPILE_MODE`. R-pilot submitter now supports `JOB_TABLE` and logs `target_tokens`, `steps`, and `run_suffix`.
- Job manifest hygiene: renamed the old 20B R1/R2 table to `progress/results/tier1_rpilot_2node_20b_canceled.tsv`. New 5B jobs will write `progress/results/tier1_rpilot_5b_jobs.tsv`.
- Submitted first 5B compile pilot: CPU submitter `172758` for R=1 only, `TARGET_TOKENS=5000000000`, `STEPS=6358` (~5.000B tokens at 786,432 tokens/step), `RUN_SUFFIX=_2node_5b_compile`, `JOB_TABLE=progress/results/tier1_rpilot_5b_jobs.tsv`, no stale train dependency. Submitter limit is `TimeLimit=04:00:00`, `MinMemoryNode=512G`.
- Planned train/eval limits for emitted R=1 job: train uses 2 nodes / 16 H100, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`; eval uses 1 H100, `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- Current queue: only 128-H100 preflight `168251` and CPU submitter `172758` are pending. Active H100 usage now: 0 H100 allocated by this resumed objective.
- Validation: `bash -n` passed for the touched shell scripts; `PYTHONPATH=src python -m py_compile src/engram/train.py src/engram/losses.py` passed; `git diff --check` passed.
- Next: wait for `172758` to emit the R=1 train job, verify the train job carries 2 nodes / 16 H100, `TimeLimit=08:00:00`, `MinMemoryNode=1800G`, and compile/CE log events. Once R=1 reaches first metrics, submit R=2,4,8,16,32 with the same 5B/compile settings.

# H9.6 - R4+ submitter repaired; R1/R2 running

- Timestamp: 2026-07-01T14:32:07Z.
- Elapsed: H9.6 for the v3 resumed objective.
- Active H100 usage now: 32 H100 allocated by this resumed objective. R=1 train `172713` is running on `cn[13-14]` and R=2 train `172715` is running on `cn[31-32]`; each uses 2 nodes / 16 H100 with `TimeLimit=20:00:00`, `MinMemoryNode=1800G`, `STEPS=25432`, `micro_batch_size=4`, and `grad_accum=6`.
- Training progress: R=1 reached step 723 / 25,432, `tokens_seen=568,590,336`, ~304k tok/s, MFU ~0.065; R=2 reached step 725 / 25,432, `tokens_seen=570,163,200`, ~304k tok/s, MFU ~0.065. First checkpoints exist: `runs/tier1_A_rpilot_R1_2node/ckpt_step000570.pt` and `runs/tier1_A_rpilot_R2_2node/ckpt_step000571.pt`.
- Anomaly: CPU submitter `172717` failed while submitting R=4 train with `sbatch: ... Job dependency problem`; it was carrying the now-stale `afterok:172706` dependency even though the 2-node preflight had already passed. No training job was emitted from that failed submitter.
- Correction: added `RUN_SUFFIX` support to `scripts/submit_tier1_r_pilot.sh` so R=4/8/16/32 use `_2node` run/result paths. Submitted replacement CPU submitter `172750` with no train dependency, `RUN_SUFFIX=_2node`, `TRAIN_NODES=2`, `TRAIN_TIME=20:00:00`, `TRAIN_MEM=1800G`, `EVAL_TIME=01:00:00`, and `EVAL_MEM=220G`; the submitter itself has `TimeLimit=08:00:00` and `MinMemoryNode=512G`.
- Queue: 128-H100 node preflight `168251` remains pending for Tier-2/MFU work. Eval jobs `172714` and `172716` are pending on their corresponding train dependencies.
- Disk: `data/tier1` is 224G; R1 and R2 run dirs are 27G each; VAST has 17T free.
- Next: monitor `172750` until it emits R=4/8/16/32 train/eval job IDs, verify each emitted train job has 2 nodes / 16 H100, `TimeLimit=20:00:00`, and `MinMemoryNode=1800G`, then push the updated job table.

# H9.0 - 2-node preflight passed; Tier-1 requeued with 20h limit

- Timestamp: 2026-07-01T13:57:45Z.
- Elapsed: H9.0 for the v3 resumed objective.
- Feedback response completed: 2-node preflight `172706` ran on `cn[13-14]` and completed `0:0` in 11s. Both nodes reported 8x NVIDIA H100 80GB HBM3, `cuda_available=true`, and `probe_value=1.0`; JSON artifacts are under `progress/results/node_preflight/172706_*.json`.
- Correction: initial 2-node R1/R2 train jobs `172707` and `172709` started and reached early steps at ~300k tok/s, implying 25,432 steps would slightly exceed the original 18h limit. Slurm denied live `TimeLimit` extension, so canceled `172707/172708/172709/172710` and R4 submitter `172711`, removed partial run/R4 outputs, and requeued with `TRAIN_TIME=20:00:00`.
- Current Tier-1 queue: R=1 train/eval `172713/172714`, R=2 train/eval `172715/172716`, all using 2 nodes / 16 H100, `STEPS=25432`, `TimeLimit=20:00:00`, `MinMemoryNode=1800G`; eval jobs depend on their corresponding train jobs. R=4,8,16,32 CPU submitter is `172717`, `TimeLimit=08:00:00`, `MinMemoryNode=512G`.
- Current state: `172713`, `172715`, and `172717` are `PENDING (Priority)`; the 128-H100 preflight `168251` remains pending. No active H100 allocation at this check.
- H100 usage now: 0 H100 allocated by this resumed objective.
- Job table: saved `progress/results/tier1_rpilot_2node_jobs.tsv` for the current 2-node R1/R2 jobs.
- Next: monitor pending 2-node train jobs and R4+ submitter; once R4+ streams emit jobs, verify they also use 2 nodes and 20h train time.

# H8.9 - pivot Tier-1 train path to 2-node preflight

- Timestamp: 2026-07-01T13:51:42Z.
- Elapsed: H8.9 for the v3 resumed objective.
- Feedback response: read `feedback/review-20260701T1224Z.md` (ON-TRACK) and accepted the actionable suggestion not to couple Tier-1's certain verdict to the scarce 128-H100 preflight window.
- Canceled jobs: canceled old Tier-1 R-pilot submitter `171792` and old 128-node-bound R1/R2 train/eval jobs `172196/172197` and `172669/172670`. These had not allocated GPUs. Archived their job table to `progress/results/tier1_rpilot_jobs_canceled_128dep.tsv`.
- Kept artifacts: completed R=1 and R=2 streams remain usable: `data/tier1/rpilot_R1_tokens20000000000` and `data/tier1/rpilot_R2_tokens20000000000`. Removed partial `data/tier1/rpilot_R4_tokens20000000000` before restart.
- Code changes: added `TRAIN_NODES` support to Tier-1 submit scripts and added `scripts/slurm_node_preflight_2node.sh` for a small 2-node / 16-H100 preflight (`--time=00:15:00 --mem=128G`). Future Tier-1 train submissions can use `TRAIN_NODES=2`, `TRAIN_DEPENDENCY=afterok:<2node_preflight>`, and `STEPS=25432` to cover ~20B tokens at 16 GPUs with mbs4/ga6.
- Validation: `bash -n scripts/*.sh`, `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py`, and static time/mem audit passed.
- Active jobs: 128-H100 node preflight `168251` remains pending. No active H100 allocation.
- H100 usage now: 0 H100 allocated by this resumed objective.
- Next: after pushing/rebasing this update, submit the 2-node preflight and queue R1/R2 2-node trains plus a resumed R=4,8,16,32 R-pilot submitter behind that small preflight.

# H8.8 - Tier-1 R-pilot R1/R2 queued behind preflight

- Timestamp: 2026-07-01T13:48:30Z.
- Elapsed: H8.8 for the v3 resumed objective.
- Active jobs: `171792` Tier-1 R-pilot submitter is still `RUNNING` on `cn09`, CPU-only, elapsed `1:29:19` at latest check, explicit `TimeLimit=08:00:00`, `MinMemoryNode=512G`. It is currently building `R=4`.
- Completed R-pilot streams: `R=1` wrote `data/tier1/rpilot_R1_tokens20000000000` with `token_count=19999985000`, `doc_count=10000`, `base_chunk_tokens=3999992`, `shard_count=193`. `R=2` wrote `data/tier1/rpilot_R2_tokens20000000000` with `token_count=19999970000`, `doc_count=20000`, `base_chunk_tokens=1999992`, `shard_count=197`.
- Queued train/eval jobs: R=1 train/eval `172196/172197`; R=2 train/eval `172669/172670`. Both train jobs are `PENDING (Dependency)` with `Dependency=afterok:168251(unfulfilled)`, `TimeLimit=04:00:00`, `MinMemoryNode=1800G`, and 16 nodes / 128 H100 requested. Eval jobs depend on their corresponding train jobs and have `TimeLimit=01:00:00`, `MinMemoryNode=220G`.
- Active H100 usage now: 0 H100 allocated by this resumed objective. Pending GPU jobs do not have allocations.
- Node preflight: `168251` remains pending for 16 nodes / 128 H100.
- Feedback loop: latest feedback remains ON-TRACK.
- Next: monitor `171792` through R=4/8/16/32 stream builds and verify each emitted train job keeps `afterok:168251`.

# H7.5 - Tier-1 R-pilot submitter running

- Timestamp: 2026-07-01T12:19:06Z.
- Elapsed: H7.5 for the v3 resumed objective.
- Submitted job: `171792` (`engram-tier1-rpilot-submit`) is `RUNNING` on `cn09`, CPU-only, explicit `TimeLimit=08:00:00`, `MinMemoryNode=512G`, 16 CPUs. It is building Tier-1 A-only R-pilot streams from `data/injected_facts/facts_5000_seed17.csv` and `data/fineweb_edu_deepseek_v3_300b/merged/shards.txt`.
- R-pilot settings: `R_VALUES=1,2,4,8,16,32`, `TARGET_TOKENS=20000000000`, `STEPS=3179`, config `configs/generated/A_seed1337.json`. This is Tier-1 pre-gate work and does not wait for MFU/Tier-2 gates.
- Dependency discipline: `TRAIN_DEPENDENCY=afterok:168251` was exported at submission, so the train jobs emitted by the submitter should wait for the 128-H100 node preflight to pass before starting. Eval jobs remain dependent on their corresponding train jobs.
- Active jobs: `171792` CPU submitter running; `168251` node preflight pending with no allocation.
- H100 usage now: 0 H100 allocated by this resumed objective.
- Next: monitor `171792` for stream summaries and emitted train/eval job IDs in `progress/results/tier1_rpilot_jobs.tsv`; verify queued train jobs carry the `afterok:168251` dependency.

# H7.4 - Tier-1 submit path hardened before launch

- Timestamp: 2026-07-01T12:20:00Z.
- Elapsed: H7.4 for the v3 resumed objective.
- Change: added `TRAIN_DEPENDENCY` support to `scripts/submit_tier1_r_pilot.sh` and `scripts/submit_tier1_registered.sh`, so Tier-1 train jobs can be queued with `--dependency=afterok:168251` and cannot start before node preflight succeeds.
- Change: added `scripts/slurm_submit_tier1_r_pilot.sh`, a CPU Slurm wrapper for Tier-1 R-pilot stream construction and train/eval submission. It runs with explicit `--time=08:00:00 --mem=512G`, so large stream construction does not run unbounded on the login node.
- Validation: `bash -n scripts/*.sh`, `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py`, and static time/mem audit passed.
- Active jobs: only `168251` 128-H100 node preflight remains pending; no H100 allocation.
- H100 usage now: 0 H100 allocated by this resumed objective.
- Next: push this hardening, then submit Tier-1 A-only R-pilot stream builder under Slurm with `TRAIN_DEPENDENCY=afterok:168251`.

# H7.3 - official 300B data gate passed

- Timestamp: 2026-07-01T12:15:01Z.
- Elapsed: H7.3 for the v3 resumed objective.
- Completed jobs: `169155` tokenizer/data-gate job completed successfully (`COMPLETED`, exit `0:0`, elapsed `02:49:18`). Batch max RSS was `109187940K`; `srun` step max RSS was `163127536K`, within the explicit `1200G/node` limit.
- Active jobs: only `168251` 128-H100 node preflight remains `PENDING (AssocGrpGRES/Resources)` with no allocation.
- H100 usage now: 0 H100 allocated by this resumed objective.
- Official data gate: saved `progress/results/data_gate_sample350bt_300b.json`. Gate passed with `gate_passed=true`, `gate_min_tokens=200000000000`, `token_count=300000000000`, `gate_shard_token_sum=300000000000`, `doc_count=301488200`, `gate_doc_manifest_lines=301488200`, `parquet_files=472`, and `shard_count=3008`.
- Data layout: static parquet cache is 930G under `data/fineweb_edu_parquet`; tokenized output tree is 1.2T under `data/fineweb_edu_deepseek_v3_300b`; merged manifest directory is 52G and references the worker shard files rather than duplicating token shards.
- Feedback loop: latest feedback remains ON-TRACK (`feedback/review-20260701T0834Z.md`).
- Next: with the official >=200B data gate passed, proceed to Tier-1 pre-gate discipline and MFU gate work. The 128-H100 preflight is still queued; while waiting, prepare or run Tier-1 pre-gate only as allowed by feedback, without waiting for MFU/Tier-2 gates.

# H7.0 - tokenizer crossed 200B raw-output estimate

- Timestamp: 2026-07-01T10:59:22Z.
- Elapsed: H7.0 for the v3 resumed objective.
- Active jobs: `169155` tokenizer/data-gate job is still `RUNNING` on `cn[13-16]`, CPU-only, elapsed `1:41:11`, explicit `TimeLimit=18:00:00`, `MinMemoryNode=1200G`. `168251` 128-H100 node preflight remains `PENDING (AssocGrpGRES/Resources)` with no allocation.
- H100 usage now: 0 H100 allocated by this resumed objective.
- Tokenization progress: 16 worker dirs, 2,122 `.u32` shard files. Sum of `.u32` file bytes is 848,800,000,000, which is an estimated 212,200,000,000 uint32 tokens. Disk usage for the token output tree is about 826G.
- Gate status: this is only a raw-output estimate, not an official data-gate pass. The official >=200B data gate still waits for all workers to finish, `summary.json` files to be written, worker outputs to merge, and `scripts/assert_data_gate.py --min-tokens 200000000000` to pass on `data/fineweb_edu_deepseek_v3_300b/merged`.
- Log notes: tokenizer warnings remain limited to `TRANSFORMERS_CACHE` deprecation and long-document sequence-length warnings; no worker stack trace seen.
- Feedback loop: latest feedback remains ON-TRACK (`feedback/review-20260701T0834Z.md`).
- Next: continue monitoring `169155` for worker summaries and the merged gate result; do not start Tier-2 until the official data gate and MFU gate pass. Tier-1 pre-gate remains allowed per feedback, after tokenizer/gate housekeeping is stable.

# H5.3 - sample-350BT download complete; tokenizer running

- Timestamp: 2026-07-01T09:22:48Z.
- Elapsed: H5.3 for the v3 resumed objective.
- Completed gate input: corrected FineWeb-Edu `sample/350BT` parquet download completed at 472 / 472 files, 930G on disk, `bad_scope=0`.
- Active jobs: `169155` tokenizer/data-gate job is `RUNNING` on `cn[13-16]`, CPU-only, 4 nodes / 16 tasks / 256 CPUs, explicit `TimeLimit=18:00:00`, `MinMemoryNode=1200G`. `168251` 128-H100 node preflight remains `PENDING (AssocGrpGRES/Resources)` with no allocation.
- H100 usage now: 0 H100 allocated by this resumed objective.
- Tokenization progress: `data/fineweb_edu_deepseek_v3_300b` has 16 worker dirs, 86 `.u32` shards, and 34G written after about 4.5 minutes of tokenizer runtime. Merge and >=200B gate have not run yet; they run after all workers finish.
- Log notes: tokenizer log shows repeated `TRANSFORMERS_CACHE` deprecation warnings and several "sequence length longer than max" tokenizer warnings for long documents. These are tokenization-time warnings; no stack trace or worker failure is present.
- Feedback loop: latest feedback `feedback/review-20260701T0834Z.md` is ON-TRACK. Watch-items acknowledged: Tier-1 pre-gate discipline, MFU gate 18-20% via compile+fused CE, and queue/disk resilience.
- Next: monitor `169155` until worker summaries appear, then verify merge output and `assert_data_gate.py --min-tokens 200000000000` result.

# H4.6 - resumed stalled sample-350BT download with larger mem limit

- Timestamp: 2026-07-01T08:40:42Z.
- Elapsed: H4.6 for the v3 resumed objective.
- Anomaly: corrected download `168265` stopped making visible progress at 349 / 472 parquet files and 701G on disk; its active `.incomplete` cache file did not grow during a 60s short check, while `sstat` showed `MaxRSS=255016284K` against a 256G allocation. No wrong-scope data was present (`bad_scope=0`), but the process looked stalled and close to memory limit.
- Fix: patched `scripts/slurm_download_fineweb_parquet.sh` to accept an explicit memory limit as arg 3 / `MEM_LIMIT` and to set `HF_HUB_DOWNLOAD_TIMEOUT=120` plus `HF_HUB_ETAG_TIMEOUT=60` by default. Canceled `168265` and dependent tokenizer `168267` before tokenizer started.
- Relaunch: submitted resumable download `169152` using the same `data/fineweb_edu_parquet` directory with explicit `--time=08:00:00 --mem=512G`; it is `RUNNING` on `cn09`. Submitted dependent tokenizer/data-gate `169155` with `afterok:169152`, explicit `--time=18:00:00 --mem=1200G/node`, and parquet glob `data/fineweb_edu_parquet/sample/350BT/*.parquet`.
- Active jobs: `169152` running CPU-only; `169155` dependency-pending CPU-only; `168251` H100 node preflight still pending with no allocation.
- H100 usage now: 0 H100 allocated by this resumed objective.
- Data state at restart: 349 / 472 sample-350BT parquet files, 701G, `bad_scope=0`.
- Validation: `bash -n scripts/*.sh`, `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py`, and static time/mem audit passed before relaunch.
- Feedback loop: about to push this status and pull feedback.
- Next: monitor `169152` for resumed growth. If it stalls again, inspect the active incomplete file and consider disabling `hf_transfer` for the remaining files.

# H4.1 - sample-350BT download 67pct

- Timestamp: 2026-07-01T08:06:55Z.
- Elapsed: H4.1 for the v3 resumed objective.
- Active jobs: `168265` corrected FineWeb-Edu `sample/350BT` parquet download is `RUNNING` on `cn09`, CPU-only, elapsed `1:45:41`, explicit limit `--time=12:00:00 --mem=256G`. `168267` tokenizer/data-gate job remains `PENDING (Dependency)` on `afterok:168265`, explicit limit `--time=18:00:00 --mem=1200G/node`. `168251` 128-H100 node preflight remains `PENDING (AssocGrpGRES/Resources)` with no allocation.
- H100 usage now: 0 H100 allocated by this resumed objective.
- Data progress: sample-350BT download is at 316 / 472 parquet files (about 67%), 634G on disk, and `bad_scope=0` (all parquet paths under `sample/350BT/`).
- ETA: at the observed rate, corrected download should finish in roughly 45-60 minutes, then `168267` should start automatically and run merge plus the >=200B data gate.
- Validation since last push: no code changes after `5c95a10`; local scope audit remains clean.
- Feedback loop: about to push this status and pull feedback.
- Next: monitor `168265` to completion, then watch `168267` for tokenizer worker startup, worker-count assertion, merge, and data-gate result.

# H2.5 - tokenizer wrapper made bash-explicit

- Timestamp: 2026-07-01T06:26:01Z.
- Elapsed: H2.5 for the v3 resumed objective.
- Anomaly avoided: pending tokenizer job `168266` used a Slurm `--wrap` command containing Bash-only `mapfile`/process substitution. Since Slurm `--wrap` shell behavior is not a good place to rely on those features, canceled `168266` before it started.
- Fix: added `scripts/run_tokenize_fineweb_job.sh` and changed `scripts/slurm_tokenize_fineweb.sh` so `--wrap` only runs `bash scripts/run_tokenize_fineweb_job.sh ...`. The helper runs the 16-way `srun`, merges worker outputs, asserts exact worker count, and runs the >=200B data gate.
- Relaunch: submitted corrected tokenizer/data-gate job `168267` with dependency `afterok:168265`, parquet glob `data/fineweb_edu_parquet/sample/350BT/*.parquet`, explicit `TimeLimit=18:00:00`, and `MinMemoryNode=1200G`. It is `PENDING (Dependency)`.
- Active jobs: `168265` corrected sample-350BT download is still `RUNNING` on `cn09`, CPU-only, and has reached 14 parquet files / 29G with `bad_scope=0`. `168251` node preflight is still pending resources with no allocation.
- H100 usage now: 0 H100 allocated by this resumed objective.
- Validation: `bash -n scripts/*.sh`, `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py`, and static time/mem audit passed.
- Feedback loop: no new feedback after the H2.4 push/pull.
- Next: push wrapper fix, pull feedback, continue monitoring `168265` and verify sample-only paths until `168267` starts.

# H2.4 - corrected parquet scope to sample-350BT only

- Timestamp: 2026-07-01T06:21:15Z.
- Elapsed: H2.4 for the v3 resumed objective.
- Anomaly: the first static parquet download used both `sample/350BT/*.parquet` and broad `**/*.parquet`, so Hugging Face began downloading `data/CC-MAIN-*` shards instead of the handoff-required FineWeb-Edu `sample/350BT` subset. At detection it had written 34 parquet files / 73.40GiB under `data/fineweb_edu_parquet/data/CC-MAIN-*`.
- Fix: canceled wrong download `168254` and dependent tokenizer `168260`, removed the generated wrong-scope `data/fineweb_edu_parquet` contents, and patched `scripts/download_fineweb_parquet.py` plus `scripts/slurm_download_fineweb_parquet.sh` so the only default/Slurm allow-pattern is `sample/350BT/*.parquet`.
- Relaunch: submitted corrected sample-350BT-only parquet download `168265` with explicit limits `--time=12:00:00 --mem=256G`; it is `RUNNING` on `cn09`, CPU-only. Submitted dependent tokenizer/data-gate job `168266` with `SBATCH_DEPENDENCY=afterok:168265`, parquet glob `data/fineweb_edu_parquet/sample/350BT/*.parquet`, and explicit limits `--time=18:00:00 --mem=1200G/node`; it is `PENDING (Dependency)`.
- Active jobs: `168251` 128-H100 node preflight remains `PENDING (Resources)` and has no allocation. `168265` download is running CPU-only. `168266` tokenizer is dependency-pending CPU-only.
- H100 usage now: 0 H100 allocated by this resumed objective.
- Validation: `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py` passed; `bash -n scripts/*.sh` passed; static time/mem audit remains clean.
- Feedback loop: no new feedback after the H2.3 push/pull.
- Next: push this anomaly/fix, pull feedback, monitor `168265`, and verify the first downloaded parquet paths are under `sample/350BT/` before allowing `168266` to run.

# H2.3 - explicit Slurm mem/time limits audited

- Timestamp: 2026-07-01T06:17:03Z.
- Elapsed: H2.3 for the v3 resumed objective.
- Active jobs: `168254` parquet download is `RUNNING` on `cn34`, elapsed 10m30s, with actual Slurm limit `TimeLimit=12:00:00` and `MinMemoryNode=256G`. `168260` local tokenizer is `PENDING (Dependency)`, with actual limit `TimeLimit=18:00:00` and `MinMemoryNode=1200G` across 4 nodes. `168251` node preflight is `PENDING (Resources)`, with actual limit `TimeLimit=00:15:00`, `MinMemoryNode=128G`, and no GPU allocation yet.
- H100 usage now: 0 H100 allocated by this resumed objective. The only GPU job is pending preflight `168251`.
- Limit hygiene: audited all `scripts/*.sh` containing `sbatch`/`#SBATCH`; every submission path now carries explicit `--time` and `--mem`/`#SBATCH --time` and `#SBATCH --mem`. `submit_tier1_r_pilot.sh` and `submit_tier1_registered.sh` now pass explicit train/eval/decision limits on the `sbatch` command line and log them in job manifests.
- Data progress: static FineWeb-Edu parquet download remains at 28 parquet files / 61G at this check.
- Validation: `bash -n scripts/*.sh` passed; static time/mem audit produced no missing scripts.
- Feedback loop: no new feedback after the H2.2 push/pull.
- Next: push this limit-hygiene update, pull feedback, then continue monitoring download `168254` and dependent tokenizer/gate `168260`.

# H2.2 - parallel tokenizer pipeline queued behind download

- Timestamp: 2026-07-01T06:14:21Z.
- Elapsed: H2.2 for the v3 resumed objective.
- Active jobs: `168254` (`engram-parquet-download`) is `RUNNING` on `cn34`, CPU-only (`cpu=16,mem=256G`, no GPU TRES), elapsed 7m at latest check. `168260` (`engram-tokenize-local`) is `PENDING (Dependency)` on `afterok:168254`, 4 nodes / 16 CPU workers / no GPU TRES. `168251` 128-H100 node preflight remains `PENDING (Resources)`.
- H100 usage now: 0 H100 allocated by the current resumed objective. The only H100 request is pending node preflight `168251`; it has not started.
- Data progress: static FineWeb-Edu parquet download has reached 26 parquet files / 56G under `data/fineweb_edu_parquet`.
- Tokenizer progress: local parquet tokenizer now supports recursive `**/*.parquet` globs and deterministic multi-worker parquet sharding (`i % num_workers == worker_index`), writes valid empty manifests for empty workers, and has a merge step that reconstructs root `docs.jsonl`, `shards.csv`, `shards.txt`, and `summary.json` before the >=200B data gate.
- Slurm orchestration: `scripts/slurm_tokenize_fineweb.sh` now submits 16 CPU tokenizer tasks by default, supports `SBATCH_DEPENDENCY`, merges worker outputs, and immediately runs `scripts/assert_data_gate.py --min-tokens 200000000000` on the merged token pool.
- Validation: recursive glob smoke passed with 3 docs / 44 tokens; two-worker tokenizer smoke including one empty worker merged correctly and passed the data gate with `--min-tokens 1`. `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py`, `bash -n scripts/slurm_tokenize_fineweb.sh scripts/slurm_download_fineweb_parquet.sh`, and `PYTHONPATH=src pytest -q` passed (19 passed, 1 skipped).
- Feedback loop: no new feedback files beyond `feedback/review-20260629T1032Z.md`.
- Next: push this progress bundle, pull feedback, then monitor `168254`. If download completes successfully, allow `168260` to start automatically and watch merge/data-gate output. Do not start Tier-2 until the >=200B data gate and MFU gate pass.

# H2.1 - offline parquet download started

- Elapsed: H2.1 for the v3 resumed objective.
- Active jobs: `168251` node preflight remains `PENDING (Resources)` with no GPU allocation. `168254` (`engram-parquet-download`) is `RUNNING` on `cn34`, CPU-only (`cpu=16,mem=256G`, no GPU TRES), time limit 12h.
- Data progress: started static parquet download to `data/fineweb_edu_parquet` via `scripts/slurm_download_fineweb_parquet.sh`, using `HF_HUB_ENABLE_HF_TRANSFER=1` and `scripts/download_fineweb_parquet.py`. Initial file appeared under `data/fineweb_edu_parquet/data/.../*.parquet`, confirming the job is doing real download work.
- Correction: an accidental outer `sbatch` job `168253` was canceled immediately; correct download job is `168254`.
- Disk: VAST free before starting was about 19T at the workspace mount, enough for the expected 1-1.5T parquet plus tokenized data.
- Feedback loop: no new feedback after latest pull.
- Next: monitor `168254` download progress and `168251` preflight. After download completes, run local parquet tokenization and the ≥200B data gate. Tier-2 remains blocked until both data and MFU gates pass.

# H2.0 - streaming tokenizer replaced; data gate hardened

- Elapsed: H2.0 for the v3 resumed objective.
- Active run: node preflight job `168251` remains `PENDING (Resources)`, no GPUs allocated.
- Tokenizer replacement: replaced `src/engram/tokenize_fineweb.py` with a local-parquet-only compatibility entrypoint. The old HF streaming path is removed from tokenizer code. `scripts/slurm_tokenize_fineweb.sh` now requires a parquet glob and local-tokenizes parquet; added `scripts/slurm_download_fineweb_parquet.sh` for resumable static parquet download.
- Compatibility smoke: `PYTHONPATH=src python -m engram.tokenize_fineweb --parquet-glob 'progress/results/local_parquet_smoke/source/*.parquet' --output-dir progress/results/tokenize_fineweb_compat_smoke --id-column id --tokens-per-shard 128 --max-tokens 512 --batch-docs 2` passed with 3 docs, 44 uint32 tokens, `shards.csv`, `shards.txt`, and `docs.jsonl`.
- Data gate hardening: `assert_data_gate()` now validates shard manifest token sums, actual uint32 file byte sizes, and doc manifest line count, not just `summary.json`. Compat smoke gate passed with `gate_shard_token_sum=44` and `gate_doc_manifest_lines=3`.
- Validation: `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py` passed; `PYTHONPATH=src pytest -q` passed 19 tests with 1 CUDA grouped-mm test skipped on login.
- Feedback loop: no new feedback after latest pull.
- Next: keep monitoring `168251`; if it starts and passes node preflight, run 128-H100 calibration. If it stays pending, continue CPU-side data-download orchestration and Tier-1 report templates.

# H1.8 - Tier-1 submit wrappers ready; preflight still pending

- Elapsed: H1.8 for the v3 resumed objective.
- Active run: node preflight job `168251` remains pending. `squeue` briefly reported `AssocGrpGRES`; `scontrol show job` reports `PENDING (Resources)` with updated estimated start `2026-07-01T21:08:46Z`. No GPUs allocated.
- Tier-1 orchestration: added `scripts/submit_tier1_r_pilot.sh` for A-only R sweep submission and `scripts/submit_tier1_registered.sh` for frozen-R registered A/B train + eval + decision submission.
- Stream dilution: `scripts/build_tier1_stream.py` now supports `--auto-base-chunk`, estimating base tokens per injected example from target tokens / (F*R). DeepSeek-V3 EOS default for submit scripts is corrected to token id 1.
- Auto-chunk smoke: `progress/results/tier1_auto_chunk_smoke/` was generated from the registered 5,000-fact set plus local parquet smoke base tokens; target 20,000 tokens, repeats 2, 6,668 docs, 3,334 base docs, 3,334 injected docs, 5 shards.
- Validation: `bash -n` passed for submit wrappers; `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py` passed; `PYTHONPATH=src pytest -q` passed 19 tests with 1 CUDA grouped-mm test skipped on login.
- Feedback loop: no new feedback after latest push/pull.
- Next: monitor `168251`; after node preflight passes, run 128-H100 calibration. Do not start Tier-2 before data/MFU gates.

# H1.7 - local memory-efficient linear CE backend added

- Elapsed: H1.7 for the v3 resumed objective.
- Active run: node preflight job `168251` remains `PENDING (Resources)`, no GPUs allocated.
- CE progress: added a local recompute/autograd `memory_efficient` linear-CE backend in `src/engram/losses.py`. `ENGRAM_CE_IMPL=auto` now tries external cut-cross-entropy/Liger first and then uses the local memory-efficient backend instead of the old logits-saving chunked CE. The old chunked CE remains available via `ENGRAM_CE_IMPL=chunked`.
- Logging: training metrics now include `ce_impl`.
- Validation: memory-efficient CE matches chunked CE loss and gradients in tests; `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py` passed; `PYTHONPATH=src pytest -q` passed 19 tests with 1 CUDA grouped-mm test skipped on login.
- Feedback loop: no new feedback after latest push/pull.
- Next: wait for node preflight allocation; if clean, run compile+CE calibration and check MFU gate before any Tier-2 work. Tier-1 can run pre-gate once R pilot streams/jobs are submitted.

# H1.6 - 128-H100 node preflight queued

- Elapsed: H1.6 for the v3 resumed objective.
- Active run: Slurm job `168251` (`engram-node-preflight-128`) submitted for 16 nodes / 128 H100, 15-minute node preflight.
- Job state: `PENDING (Resources)` at latest check. Backfill estimate: start `2026-07-01T16:30:54Z`, end `2026-07-01T16:45:54Z`.
- Requested/excluded nodes: request is `gres/gpu:h100=128`, `--nodes=16`, excluding `cn02,cn10,cn17,cn34`. Scheduler candidate list is `cn[09,14-15,18-20,24-26,28-33,35]`.
- Resource note: current cluster snapshot had only 15 fully idle H100 nodes after exclusions, so pending is expected; job is short and should not consume GPUs until all 16 nodes are available.
- Feedback loop: no new feedback after latest push/pull.
- Next after allocation: inspect per-node JSON under `progress/results/node_preflight/`; if clean, run 128-H100 compile/fused-CE calibration before Tier-1 train jobs.

# H1.5 - Tier-1 mixed-stream builder and decision aggregator passed

- Elapsed: H1.5 for the v3 resumed objective.
- Active run: none.
- Added Tier-1 registered-run support: `src/engram/tier1.py`, `scripts/build_tier1_stream.py`, and `scripts/decide_tier1.py`.
- Mixed stream smoke: `scripts/build_tier1_stream.py` combined the local parquet token smoke shard with `data/injected_facts/facts_5000_seed17.csv` and wrote `progress/results/tier1_mixed_stream_smoke/`: 10,000 tokens, 953 docs, 477 base docs, 476 injected docs, 3 uint32 shards, `docs.jsonl`, `shards.csv`, and `shards.txt`.
- Data interface fix: local parquet tokenizer now writes `shards.txt` in addition to `shards.csv`, so training/stream builders can consume it directly.
- Tier-1 decision smoke: `scripts/decide_tier1.py` joined synthetic A/B eval rows and correctly reported Tier-1 PASS with scope `mechanism/param-efficiency positive control, not paper natural-data verification`.
- Validation: `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py` passed; `PYTHONPATH=src pytest -q` passed 18 tests with 1 CUDA grouped-mm test skipped on login.
- Feedback loop: no new feedback after latest push/pull.
- Next: submit 16-node H100 node preflight when an allocation window is acceptable; then run 128-GPU calibration and registered Tier-1 A-only R pilot / A-B runs.

# H1.2 - registered Tier-1 factset generated

- Elapsed: H1.2 for the v3 resumed objective.
- Active run: none.
- Factset: generated `data/injected_facts/facts_5000_seed17.csv` with DeepSeek-V3 tokenizer using `scripts/build_injected_facts.py --count 5000 --seed 17 --negative-control-frac 0.1`.
- Validation: 5,000 facts total; 4,500 main and 500 negative-control; all 5,000 subjects are single-token and unique; all 5,000 objects are single-token and unique; subject/object token-ID overlap is 0. Summary written to `progress/results/tier1_factset_5000_seed17_summary.json`.
- Local validation: `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py` passed; `PYTHONPATH=src pytest -q` passed 16 tests with 1 CUDA grouped-mm test skipped on login.
- Feedback loop: no new feedback after latest push/pull.
- Next: produce injected stream variants after the A-only pilot freezes R; then submit node preflight before any 128-H100 calibration/training.

# H1.0 - 128-H100 wrappers and calibration summarizer added

- Elapsed: H1.0 for the v3 resumed objective.
- Active run: none; no 128-H100 allocation requested yet.
- Added Slurm wrappers: `scripts/slurm_node_preflight_128.sh`, `scripts/slurm_calibrate_128.sh`, `scripts/slurm_tier1_train.sh`, and `scripts/slurm_tier1_eval.sh`.
- Calibration logging: added `scripts/summarize_calibration.py`, which appends tail tok/s/MFU summaries to `progress/results/calibration.csv`. Smoke against the existing h4v3 B log wrote `progress/results/calibration_smoke.csv` with tail tok/s `2,577,662` and MFU `0.09283` for the old 80-GPU run.
- Validation: `bash -n` passed for all new Slurm scripts; `PYTHONPATH=src python -m py_compile scripts/summarize_calibration.py` passed; `PYTHONPATH=src pytest -q` passed 16 tests with 1 CUDA grouped-mm test skipped on login.
- Feedback loop: no new feedback after latest push/pull.
- Next: request or wait for a 16-node window only after a real Tier-1 fact set and injected token stream are generated; first run should be 128-H100 node preflight, then compile/fused-CE calibration, then registered Tier-1 A-only R pilot / A-B run.

# H0.8 - Tier-1 CLIs and local parquet smoke passed

- Elapsed: H0.8 for the v3 resumed objective.
- Active run: none; no Tier-2 training launched.
- Tier-1 CLI progress: added `scripts/freeze_injected_r.py` and `scripts/inject_facts_stream.py`. Smoke output under `progress/results/tier1_cli_smoke/` confirms A-only sweep freeze logic selected R=3 from `a_recall=0.09` and the facts+R injector wrote a doc-ID manifest and uint32 stream.
- Offline data smoke: created a tiny local parquet sample and ran `scripts/tokenize_local_parquet.py` with DeepSeek-V3 tokenizer from local files, not `streaming=True`. Output under `progress/results/local_parquet_smoke/tokens/` has 3 docs, 44 uint32 tokens, shard manifest, and per-doc JSONL manifest; `scripts/assert_data_gate.py --min-tokens 1` passed.
- Validation: `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py` passed; `PYTHONPATH=src pytest -q` passed 16 tests with 1 CUDA grouped-mm test skipped on login.
- Feedback loop: no new feedback after latest push/pull; latest remains `feedback/review-20260629T1032Z.md`.
- Next: convert these smoke CLIs into Slurm-ready Tier-1 registered jobs: A-only R pilot, A/B train on injected stream, B-normal/B-knockout eval, and 128-H100 node preflight/calibration scripts.

# H0.6 - handoff v3 pulled; rung-0 apparatus smoke passed

- Elapsed: H0.6 for the v3 resumed objective.
- Active run: none; no Tier-2 training launched. This is build/gate work only, following handoff v3 order.
- Source of truth: pulled `origin/main` to `9a8e777` and read updated `handoff.md` from `DEPLOYMENT SCOPE` through the end.
- Build progress: added Tier-1 injected-fact apparatus scaffolding (`src/engram/injected_facts.py`) with single-token fact schema, stream injector with doc IDs, key-ngram token-ID identity assert, freeze-R helper, paired NLL/EM McNemar stats, rung-0 smoke, fact builder, and injected-fact evaluator.
- Data/MFU/spec/ops progress: added offline parquet downloader/local tokenizer/doc-ID manifest/data gate, RoPE in attention, optional CE backend dispatch for Liger/cut-cross-entropy with chunked fallback, `torch.compile` training flag, corrected arm-specific FLOP/token MFU logging, checkpoint rotation/disk pre-write checks, latest-checkpoint resume, and node preflight.
- Rung-0 result: `PYTHONPATH=src python scripts/run_kb_inject_smoke.py --num-facts 200 --repeats 3 --output-dir progress/results/rung0_kb_inject` passed. Normal EM 1.0, knockout EM 0.0, mean NLL delta knockout-normal 20.0, McNemar exact p `1.2446030555722283e-60`, key identity passed.
- Local validation: `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py` passed; `PYTHONPATH=src pytest -q` passed 16 tests with 1 CUDA grouped-mm test skipped on login; new CLI help checks passed.
- Node health: login-node preflight wrote `progress/results/node_preflight_login.json`; CUDA is not available on the login context, so full H100 node preflight remains pending for Slurm allocation.
- Feedback loop: pulled latest remote; no new feedback beyond `feedback/review-20260629T1032Z.md`.
- Next: tighten Tier-1 registered run scripts/A-only R pilot, then build a small pre-gate local parquet/tokenization smoke before requesting 128-H100 calibration for compile+fused CE.

# H22.4 - final eval complete; report drafted

- Elapsed: H22.4 wall-clock from the resumed run.
- Completed jobs: h4 B job `167284` completed `0:0`; eval array `167289_0..8` completed `0:0`.
- Step/tokens vs target: B final rank0 log reached step 5,027 / 5,027, tokens 19,766,968,320 / 19,766,968,320.
- Measured MFU and tok/s: B final step reported 2,571,946 tok/s and MFU 9.26%; run held about 2.57M tok/s.
- Final checkpoint: `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step005027.pt`, size 28,027,733,867 bytes.
- Primary knockout final: TriviaQA answer-NLL delta knockout-normal `+0.0109805815`, positive-delta frac 0.53; PopQA answer-NLL delta `+0.0349384117`, positive-delta frac 0.58. TriviaQA/PopQA 5-shot EM remains 0.0 normal and 0.0 knockout.
- Primary slices final: h5 A-B global `-0.0100426078`, repeated-ngram `-0.0023399625`, entity-proxy `-0.0472175935`; B is worse on all three measured slices.
- Depth/diagnostics final: B mean earliest layer is 0.0283 layer earlier but median is tied at 19; Engram path remains nonzero with final hidden delta RMS 0.0649173 and layer-6 contribution/hidden RMS ratio 0.0121942.
- Verdict drafted in `REPORT.md`: NOT VERIFIED. Engram is wired/nonzero, but knockout is weak, targeted slices fail, and secondary loss does not support B. This is not a PASS; report as an honest negative/data-limited result rather than manufacturing a conclusion.
- Results updated: aggregate tables, raw h4v3 final knockout files, `results/downstream.csv`, `results/loss_curves.csv`, `results/loss_curves.png`, and `results/depth_probe.png`.
- Feedback loop: latest pull had no new feedback beyond `feedback/review-20260629T1032Z.md`.
- Next: final commit/push this report and result bundle, then pull/check feedback and verify no Engram Slurm jobs remain.

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
