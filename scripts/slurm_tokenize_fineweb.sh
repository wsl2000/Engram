#!/usr/bin/env bash
set -euo pipefail

PARQUET_GLOB="${1:?usage: $0 PARQUET_GLOB OUT_DIR [MAX_TOKENS] [NODES] [TIME_LIMIT]}"
OUT_DIR="${2:?usage: $0 PARQUET_GLOB OUT_DIR [MAX_TOKENS] [NODES] [TIME_LIMIT]}"
MAX_TOKENS="${3:-300000000000}"
NODES="${4:-4}"
TIME_LIMIT="${5:-08:00:00}"
CPUS_PER_TASK="${CPUS_PER_TASK:-32}"

mkdir -p "${OUT_DIR}" progress/logs

sbatch -p all \
  --job-name=engram-tokenize-local \
  -N"${NODES}" --ntasks=1 --cpus-per-task="${CPUS_PER_TASK}" \
  --time="${TIME_LIMIT}" --mem=1200G \
  --output="${PWD}/progress/logs/tokenize_%j.out" \
  --wrap="cd '${PWD}' && PYTHONPATH=src python -m engram.tokenize_fineweb --parquet-glob '${PARQUET_GLOB}' --output-dir '${OUT_DIR}' --max-tokens '${MAX_TOKENS}' --tokens-per-shard 100000000 --batch-docs 512"
