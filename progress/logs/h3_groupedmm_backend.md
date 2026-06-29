# H3.0 torch grouped-mm backend

- Time: 2026-06-29 00:25 UTC
- Goal: recover MoE throughput without changing handoff model invariants.
- Backend found: PyTorch 2.9.1 exposes `torch._grouped_mm(self, mat2, offs=...)`.
- API notes: `offs` is int32 cumulative end offsets, not a leading-zero prefix array. Empty groups work with repeated offsets. Autograd works for BF16 inputs/weights.
- Code change: added optional `ENGRAM_MOE_BACKEND=grouped`; default remains `loop` until 80GPU calibration validates grouped for both arms. Added DDP `no_sync()` for all but the last microbatch during gradient accumulation.
- Tests: `pytest -q` passes on login (`10 passed, 1 skipped`). CUDA grouped-mm forward/backward regression passes on 1xH100.

Calibration probes:

- Isolated 1xH100 MoE layer, A-shape routed experts: loop forward+backward averaged 0.0782s; grouped-mm averaged 0.00304s.
- 1xH100 full model A, grouped backend, mbs1/ga1: step2 0.138s and step3 0.129s.
- 1xH100 full model A, grouped backend, mbs2/ga1: step2 0.173s and step3 0.173s; mbs2 fits on one H100.
- 64GPU A, loop backend + DDP no_sync, mbs1/default ga32: steady steps 7-10 averaged 465,956 tok/s, MFU 2.10%.
- 64GPU A, grouped backend + DDP no_sync, mbs1/default ga32: steady steps 3-6 averaged 1,411,511 tok/s, MFU 6.35%.

Interpretation:

- Native grouped-mm is a real improvement over the Python expert loop, but 64GPU mbs1 throughput is still about 3.4x below the 24h plan's all-run average need and about 5.9x below the handoff's 8.34M tok/s target.
- The next lever is increasing per-rank micro-batch and decreasing grad-accum while keeping global batch at ~4M tokens. The 1GPU mbs2 probe works; the 64GPU mbs2 probe is still pending due node availability/anomaly (`cn34` set_device OOM; retry busy).

No scientific verdict has been produced yet. This remains a throughput/calibration gate.
