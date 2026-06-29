# H3.4 microbatch grouped-mm probe

Scope: A arm, seed 1337, native `torch._grouped_mm` MoE backend, DDP full expert replication, bf16, no expert parallelism. These are calibration probes only; no Engram verdict numbers yet.

Completed probes:

- 64GPU mbs2/ga16 (`runs/calib_grouped_mbs2_64_A_seed1337`): steady steps 3-8 averaged 2.4131s/step, 1,738,402 tok/s, MFU 7.83%.
- 64GPU mbs4/ga8 (`runs/calib_grouped_mbs4_64_A_seed1337`): steady steps 3-8 averaged 2.0543s/step, 2,042,121 tok/s, MFU 9.19%.
- 1GPU mbs8 probe fit after AdamW state allocation and reached about 35k tok/s on step 2, but single-GPU probes are only directional.

Rejected or blocked:

- 64GPU mbs8/ga4 at default CE chunk 256 OOMed in `chunked_cross_entropy` during the logits allocation (~126MB request with ~79GB already used). This is a memory gate, not a model wiring gate.
- mbs4 is the current best accepted setting, but linear 80GPU extrapolation is only ~2.55M tok/s. That implies about 7.6h for one 70B run and does not support the six-run 24h handoff schedule.

Code change for next probe:

- Added `ENGRAM_CE_CHUNK_TOKENS` with default 256. This preserves previous behavior unless explicitly overridden.
- Enabled DDP `gradient_as_bucket_view=True` to reduce gradient bucket memory.

Next probe:

- Retry 64GPU mbs8/ga4 with `ENGRAM_CE_CHUNK_TOKENS=128`.
- If it fits and throughput improves materially, run the required 80GPU 200-step calibration on clean nodes before any training launch.
