#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 6 ]]; then
  echo "usage: $0 PARQUET_GLOB OUT_DIR MAX_TOKENS WORKERS CPUS_PER_TASK GATE_MIN_TOKENS" >&2
  exit 2
fi

PARQUET_GLOB="$1"
OUT_DIR="$2"
MAX_TOKENS="$3"
WORKERS="$4"
CPUS_PER_TASK="$5"
GATE_MIN_TOKENS="$6"
TOKENS_PER_WORKER=$(( (MAX_TOKENS + WORKERS - 1) / WORKERS ))

mkdir -p "${OUT_DIR}"

srun --ntasks="${WORKERS}" --cpus-per-task="${CPUS_PER_TASK}" bash -c '
set -euo pipefail
worker="${SLURM_PROCID}"
PYTHONPATH=src python -m engram.tokenize_fineweb \
  --parquet-glob "$1" \
  --output-dir "$2/worker_${worker}" \
  --max-tokens "$3" \
  --tokens-per-shard 100000000 \
  --batch-docs 512 \
  --num-workers "$4" \
  --worker-index "${worker}"
' _ "${PARQUET_GLOB}" "${OUT_DIR}" "${TOKENS_PER_WORKER}" "${WORKERS}"

mapfile -t worker_dirs < <(find "${OUT_DIR}" -maxdepth 1 -type d -name "worker_*" | sort)
if [[ "${#worker_dirs[@]}" -ne "${WORKERS}" ]]; then
  echo "expected ${WORKERS} worker dirs, found ${#worker_dirs[@]}" >&2
  exit 1
fi

PYTHONPATH=src python scripts/merge_tokenized_outputs.py \
  --worker-dirs "${worker_dirs[@]}" \
  --output-dir "${OUT_DIR}/merged"
PYTHONPATH=src python scripts/assert_data_gate.py \
  --output-dir "${OUT_DIR}/merged" \
  --min-tokens "${GATE_MIN_TOKENS}"
