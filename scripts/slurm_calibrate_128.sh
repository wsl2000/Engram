#!/usr/bin/env bash
#SBATCH --job-name=engram-calib-128
#SBATCH --partition=all
#SBATCH --nodes=16
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:h100:8
#SBATCH --cpus-per-task=16
#SBATCH --mem=1800G
#SBATCH --time=01:00:00
#SBATCH --exclude=cn02,cn10,cn17,cn34
#SBATCH --output=progress/logs/calibrate_128_%j.out

set -euo pipefail

if [[ $# -lt 4 ]]; then
  echo "usage: sbatch $0 CONFIG_JSON TOKEN_LIST OUTPUT_DIR LABEL [STEPS]" >&2
  exit 2
fi

CONFIG_JSON="$1"
TOKEN_LIST="$2"
OUTPUT_DIR="$3"
LABEL="$4"
STEPS="${5:-200}"

cd /mnt/vast/workspaces/JAIF/dy/code/Engram
mkdir -p "${OUTPUT_DIR}" progress/results
mapfile -t TOKEN_FILES < "${TOKEN_LIST}"

export PYTHONPATH=src
export ENGRAM_MOE_BACKEND=grouped
export ENGRAM_CE_IMPL="${ENGRAM_CE_IMPL:-auto}"
export ENGRAM_CE_CHUNK_TOKENS="${ENGRAM_CE_CHUNK_TOKENS:-256}"
export ENGRAM_TORCH_COMPILE=1
export NCCL_DEBUG=WARN
export OMP_NUM_THREADS=1

MASTER_ADDR="$(scontrol show hostnames "$SLURM_NODELIST" | head -n 1)"
export MASTER_ADDR
export MASTER_PORT="$((29500 + SLURM_JOB_ID % 1000))"

srun \
  --ntasks="${SLURM_NNODES}" \
  --ntasks-per-node=1 \
  --cpus-per-task="${SLURM_CPUS_PER_TASK}" \
  bash -c '
    set -euo pipefail
    torchrun \
      --nnodes="${SLURM_NNODES}" \
      --nproc_per_node=8 \
      --node_rank="${SLURM_PROCID}" \
      --master_addr="${MASTER_ADDR}" \
      --master_port="${MASTER_PORT}" \
      -m engram.train \
      --config "'"${CONFIG_JSON}"'" \
      --token-files "$@" \
      --output-dir "'"${OUTPUT_DIR}"'" \
      --max-steps-override "'"${STEPS}"'" \
      --micro-batch-size-override 4 \
      --grad-accum-override 6 \
      --torch-compile \
      --no-checkpoint \
      --calibration
  ' _ "${TOKEN_FILES[@]}"

python scripts/summarize_calibration.py \
  --train-log "${OUTPUT_DIR}/train_rank0.jsonl" \
  --output-csv progress/results/calibration.csv \
  --label "${LABEL}"
