# H0.5 — implementation scaffold and local gates pass

- Elapsed: H0.5
- Active run: setup only; no training launched
- Step/tokens vs target: 0 / TBD; tokens/run will be set by 200-step calibration
- Measured MFU and tok/s: TBD after calibration
- Git/progress channel: verified push to `origin/main` after non-destructive rebase onto updated `handoff.md`
- Authoritative plan: re-read updated 24h `handoff.md` in full after rebase; no 27B/U-shape sweep, use 6-run 0.48B activated paired plan
- Launcher: Slurm on `cluster43`, partition `all`, use `srun/sbatch`; commands will carry explicit `--time/--mem` plus shell `timeout` for probes
- Node health: 10-node immediate probe succeeded; 80x H100-80GB reachable (`cn02,cn03,cn04,cn13,cn14,cn15,cn16,cn17,cn34,cn35`, 8 GPUs each, 81559 MiB)
- Feedback loop: no `feedback/` directory present yet
- User note: searched for `43_intro`; no matching repo/workspace task file found, so continuing from `handoff.md`
- Environment: PyTorch 2.9.1+cu128, datasets/transformers/lm-eval present; FlashAttention/Transformer Engine absent
- Judgment call: Muon modules not installed/vetted; fixed optimizer to AdamW for all runs
- Implementation: added pure PyTorch DDP scaffold, MoE full replication, EngramRead, tokenizer script, training entry, Slurm calibration script
- Local gates: `pytest -q` passed 8/8; `py_compile` passed; synthetic paired-loader first 100 batches hash matched exactly
- Invariants: active params `475,136,000` both arms; A non-embed `4,505,600,000`; B non-embed `4,505,598,976`; delta `1,024`; Engram sparse budget fraction `22.47%`; tokens/step on 80 GPUs `4,259,840`; 70B max steps `16,432`
- Next: push implementation snapshot, then prepare real tokenizer/data shard and bounded Slurm smoke/calibration
- ETA: preliminary verdict target remains H12 if infra/training gates pass
