#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-data/fineweb_edu_deepseek}"
TOTAL_TOKENS="${2:-90000000000}"
WORKERS="${3:-80}"
TIME_LIMIT="${4:-08:00:00}"
CPUS_PER_TASK="${5:-4}"

TOKENS_PER_WORKER=$(( (TOTAL_TOKENS + WORKERS - 1) / WORKERS ))
mkdir -p "${OUT_DIR}" progress/logs

sbatch -p all \
  --job-name=engram-tokenize \
  -N10 --ntasks="${WORKERS}" --cpus-per-task="${CPUS_PER_TASK}" \
  --time="${TIME_LIMIT}" --mem-per-cpu=4G \
  --output="${PWD}/progress/logs/tokenize_%j.out" \
  --wrap="cd '${PWD}' && srun --ntasks='${WORKERS}' --cpus-per-task='${CPUS_PER_TASK}' bash -lc 'WORKER=\${SLURM_PROCID}; PYTHONPATH=src python -m engram.tokenize_fineweb --output-dir \"${OUT_DIR}\" --max-tokens \"${TOKENS_PER_WORKER}\" --tokens-per-shard 1000000000 --num-workers \"${WORKERS}\" --worker-index \${WORKER} --batch-docs 512'"
