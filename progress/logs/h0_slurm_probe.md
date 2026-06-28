# H0 Slurm/GPU Probe

- Host: `login-01.head.cm.cluster43.local`
- Launcher: Slurm (`srun`, `sbatch`) on `cluster43`
- Partition: `all`
- Probe command shape: `srun -p all -N10 --ntasks-per-node=1 --gres=gpu:h100:8 --time=00:02:00 --mem=64G --immediate=30 ...`
- Result: succeeded
- Nodes: `cn02, cn03, cn04, cn13, cn14, cn15, cn16, cn17, cn34, cn35`
- Per node: `8` visible GPUs
- GPU: `NVIDIA H100 80GB HBM3, 81559 MiB`
- Total confirmed: `80` H100-80GB GPUs

