#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "usage: $0 CONFIG_JSON TOKEN_BIN OUTPUT_DIR [STEPS]" >&2
  exit 2
fi

CONFIG_JSON="$1"
TOKEN_BIN="$2"
OUTPUT_DIR="$3"
STEPS="${4:-200}"

mkdir -p "${OUTPUT_DIR}"

srun -p all \
  -N10 --ntasks-per-node=1 --gres=gpu:h100:8 --cpus-per-task=64 \
  --time=00:45:00 --mem=1500G \
  bash -lc "cd '${PWD}' && MASTER_ADDR=\$(scontrol show hostnames \"\${SLURM_JOB_NODELIST}\" | head -n1) && PYTHONPATH=src torchrun --nnodes=\${SLURM_NNODES} --nproc_per_node=8 --rdzv_backend=c10d --rdzv_id=\${SLURM_JOB_ID} --rdzv_endpoint=\${MASTER_ADDR}:29500 -m engram.train --config '${CONFIG_JSON}' --token-files '${TOKEN_BIN}' --output-dir '${OUTPUT_DIR}' --max-steps-override '${STEPS}' --calibration"
