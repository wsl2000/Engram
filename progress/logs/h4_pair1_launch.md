# H4.1 pair-1 launch anomaly

Attempted launch:

- Job: `165273`
- Arm/seed: A / 1337
- Target: 20B tokens, 5,086 steps, mbs4/ga6, 80 GPUs
- Nodelist: `cn13,cn14,cn15,cn16,cn25,cn26,cn27,cn29,cn34,cn35`

Failure:

- The job failed before any training step.
- Root cause in `progress/logs/pair1_A_seed1337_20B_165273.out`: rank67/local_rank3 on `cn34` failed in `torch.cuda.set_device` with CUDA out of memory.
- The residual Slurm allocation was canceled.

Node decision:

- Exclude `cn34` from training nodelists, same as `cn17`.
- `cn02` is mixed but has 8 free H100s and passed a fresh 8-rank CUDA `set_device` probe.
- Relaunch pair-1 A with `cn02,cn13,cn14,cn15,cn16,cn25,cn26,cn27,cn29,cn35` and `--cpus-per-task=16`.
