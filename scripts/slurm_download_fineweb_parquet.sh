#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-data/fineweb_edu_parquet}"
TIME_LIMIT="${2:-08:00:00}"
MEM_LIMIT="${MEM_LIMIT:-${3:-256G}}"
DOWNLOAD_TIMEOUT="${HF_HUB_DOWNLOAD_TIMEOUT:-120}"
ETAG_TIMEOUT="${HF_HUB_ETAG_TIMEOUT:-60}"

mkdir -p "${OUT_DIR}" progress/logs

sbatch -p all \
  --job-name=engram-parquet-download \
  -N1 --ntasks=1 --cpus-per-task=16 \
  --time="${TIME_LIMIT}" --mem="${MEM_LIMIT}" \
  --output="${PWD}/progress/logs/parquet_download_%j.out" \
  --wrap="cd '${PWD}' && HF_HUB_ENABLE_HF_TRANSFER=1 HF_HUB_DOWNLOAD_TIMEOUT='${DOWNLOAD_TIMEOUT}' HF_HUB_ETAG_TIMEOUT='${ETAG_TIMEOUT}' PYTHONPATH=src python scripts/download_fineweb_parquet.py --repo-id HuggingFaceFW/fineweb-edu --local-dir '${OUT_DIR}' --allow-patterns 'sample/350BT/*.parquet'"
