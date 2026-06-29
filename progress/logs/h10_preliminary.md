# H10.3 preliminary verdict and h4 pivot

Pair-1 B final-only job `165327` completed successfully with exit `0:0`.

- Final checkpoint: `runs/pair1_B_seed1337_final5027_mbs4_80/ckpt_step005027.pt`
- Checkpoint size: 28,027,733,867 bytes
- Endpoint: step 5,027 / 19,766,968,320 tokens
- Final observed throughput: 2.58M tokens/s, MFU 9.29%

Final pair-1 eval completed:

- `results/knockout.csv`
- `results/slices.csv`
- `results/depth_probe.csv`
- `results/gate_diagnostics.csv`
- `results/loss_table.csv`
- Detailed per-run outputs under `results/knockout/`, `results/slices/`, `results/depth_probe/`, and `results/diagnostics/`

Preliminary verdict is written in `progress/PRELIMINARY.md`: NOT VERIFIED / INCONCLUSIVE for pair 1. Knockout does not degrade TriviaQA/PopQA, targeted slices are mixed, and depth is only weakly supportive. Gate diagnostics show active/growing Engram contribution, so this is not a dead path; likely repeated-data washout from 4.69B unique tokens sampled to 19.77B. Updated caveat after `feedback/review-20260629T0432Z.md`: h4 is a separate tokenization directory, but current manifests do not contain document IDs, so document-level disjointness from pair-1 cannot be proven.

Adaptive action:

- Removed obsolete self-generated `runs/pair1_B_seed1337_matchA5027_mbs4_80/ckpt_step000959.pt` after saving diagnostics.
- Launched fresh h4 unique-data paired run, starting with A seed 2024 as Slurm job `165367`, then canceled it because it used `torchrun --nnodes=10` from only the batch host and hung in rendezvous before training.
- Relaunched h4 A seed 2024 as corrected Slurm job `165373` with one `srun` task per node; it is pending resources until 10 full H100 nodes are available.
- H4 A uses the same invariants: 80 GPUs, DDP full replication, AdamW, bf16, mbs4/ga6, 5,027-step endpoint, final-only checkpoint.
- Do not use h4 itself as held-out eval for the h4 pair. Prepare a new doc-ID-aware eval tranche or decontaminate before evaluating h4-trained checkpoints.
