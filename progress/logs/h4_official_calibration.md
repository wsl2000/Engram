# H4.0 official 80GPU calibration

Configuration:

- Faithful 88/68 expert counts from `handoff.md`.
- Full expert replication, DDP, bf16, no expert parallelism.
- `ENGRAM_MOE_BACKEND=grouped` using native `torch._grouped_mm`.
- 80 GPUs on `cn13,cn14,cn15,cn16,cn25,cn26,cn27,cn29,cn34,cn35`; `cn17` excluded.
- Official batch decomposition: micro-batch 4, grad accumulation 6, `3,932,160` tokens/step (~4M).

Results:

- A seed 1337 (`runs/calib_grouped_mbs4_80_A_seed1337`): 200 steps completed. Steps 5-200 averaged 1.4502s/step, 2,711,455 tok/s, MFU 9.76%.
- B seed 1337 (`runs/calib_grouped_mbs4_80_B_seed1337`): 50-step throughput confirmation completed. Steps 5-50 averaged 1.5067s/step, 2,609,871 tok/s, MFU 9.40%.
- B is 3.75% slower than A.
- Both runs ended with torchrun rendezvous shutdown warnings after rank0 logged the final step, but process exit code was 0 and metrics files are complete.

Schedule consequence:

- 70B/run would take about 7.16h for A and 7.45h for B.
- 60B/run would still take about 6.14h for A and 6.39h for B.
- The original 70B pair-1 preliminary cannot meet H12, and six 60-80B runs cannot fit the 24h wall-clock budget at measured throughput.

Execution decision:

- Use 20B tokens for the first paired A/B run to preserve the H12 primary-verdict path.
- This is a schedule-driven deviation from the 60-80B planning range. It must not be used to claim a powered global-loss conclusion.
- Primary preliminary remains knockout + targeted slices + depth probe; extend pair-1 or add seeds only if time remains.
