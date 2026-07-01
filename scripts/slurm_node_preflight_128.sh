#!/usr/bin/env bash
#SBATCH --job-name=engram-node-preflight-128
#SBATCH --partition=all
#SBATCH --nodes=16
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:h100:8
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=00:15:00
#SBATCH --exclude=cn02,cn10,cn17,cn34
#SBATCH --output=progress/logs/node_preflight_128_%j.out

set -euo pipefail

cd /mnt/vast/workspaces/JAIF/dy/code/Engram
mkdir -p progress/results/node_preflight
export PYTHONPATH=src

srun \
  --ntasks="${SLURM_NNODES}" \
  --ntasks-per-node=1 \
  --cpus-per-task="${SLURM_CPUS_PER_TASK}" \
  bash -lc 'python scripts/node_preflight.py --output "progress/results/node_preflight/${SLURM_JOB_ID}_${SLURM_PROCID}_$(hostname).json"'
