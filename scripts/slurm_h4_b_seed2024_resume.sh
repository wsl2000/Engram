#!/usr/bin/env bash
#SBATCH --job-name=engram-h4-B2024v3
#SBATCH --partition=all
#SBATCH --nodes=10
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:h100:8
#SBATCH --cpus-per-task=16
#SBATCH --mem=1800G
#SBATCH --time=04:00:00
#SBATCH --exclude=cn02,cn10,cn17,cn34
#SBATCH --output=progress/logs/pair_h4_B_seed2024_20B_v3_%j.out

set -euo pipefail

cd /mnt/vast/workspaces/JAIF/dy/code/Engram

mapfile -t TOKEN_FILES < data/fineweb_edu_deepseek_h4/shards.txt

export PYTHONPATH=src
export ENGRAM_MOE_BACKEND=grouped
export ENGRAM_CE_CHUNK_TOKENS=256
export NCCL_DEBUG=WARN
export OMP_NUM_THREADS=1

MASTER_ADDR="$(scontrol show hostnames "$SLURM_NODELIST" | head -n 1)"
export MASTER_ADDR
export MASTER_PORT="$((29500 + SLURM_JOB_ID % 1000))"

srun \
  --ntasks="$SLURM_NNODES" \
  --ntasks-per-node=1 \
  --cpus-per-task="$SLURM_CPUS_PER_TASK" \
  bash -c '
    set -euo pipefail
    NODE_RANK="${SLURM_PROCID}"
    torchrun \
      --nnodes="${SLURM_NNODES}" \
      --nproc_per_node=8 \
      --node_rank="${NODE_RANK}" \
      --master_addr="${MASTER_ADDR}" \
      --master_port="${MASTER_PORT}" \
      -m engram.train \
      --config configs/generated/B_seed2024.json \
      --token-files "$@" \
      --output-dir runs/pair_h4_B_seed2024_20B_mbs4_80_v3 \
      --max-steps-override 5027 \
      --micro-batch-size-override 4 \
      --grad-accum-override 6 \
      --checkpoint-minutes-override 25
  ' _ "${TOKEN_FILES[@]}"
