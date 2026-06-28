# H0 Tokenization Smoke

- DeepSeek-V3 tokenizer load: succeeded
- Dataset: `HuggingFaceFW/fineweb-edu`, config `sample-350BT`, streaming
- Single-worker smoke: `10,687` tokens written to `data/smoke_fineweb/train_00000.bin`
- Real-shard paired loader hash:
  - A: `f58d12d5bacb8af88f6553e697a26fdf38dab3ae7e7d4a8718aa8409c0b1b2e5`
  - B: `f58d12d5bacb8af88f6553e697a26fdf38dab3ae7e7d4a8718aa8409c0b1b2e5`
  - Result: matched
- Multi-worker smoke finding: shared `manifest.json` would be overwritten by workers
- Fix: per-worker `manifest_wNNN.json` plus `scripts/list_token_shards.py`
- Slurm submit check: `sbatch --test-only` passed for 10 nodes, 80 tasks, 4 CPU/task, 4G/CPU

