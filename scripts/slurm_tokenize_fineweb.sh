#!/usr/bin/env bash
set -euo pipefail

PARQUET_GLOB="${1:?usage: $0 PARQUET_GLOB OUT_DIR [MAX_TOKENS] [WORKERS] [NODES] [TIME_LIMIT]}"
OUT_DIR="${2:?usage: $0 PARQUET_GLOB OUT_DIR [MAX_TOKENS] [WORKERS] [NODES] [TIME_LIMIT]}"
MAX_TOKENS="${3:-300000000000}"
WORKERS="${4:-16}"
NODES="${5:-4}"
TIME_LIMIT="${6:-08:00:00}"
CPUS_PER_TASK="${CPUS_PER_TASK:-32}"
GATE_MIN_TOKENS="${GATE_MIN_TOKENS:-200000000000}"

mkdir -p "${OUT_DIR}" progress/logs
SBATCH_DEP_ARGS=()
if [[ -n "${SBATCH_DEPENDENCY:-}" ]]; then
  SBATCH_DEP_ARGS+=(--dependency="${SBATCH_DEPENDENCY}")
fi
printf -v Q_PWD "%q" "${PWD}"
printf -v Q_PARQUET_GLOB "%q" "${PARQUET_GLOB}"
printf -v Q_OUT_DIR "%q" "${OUT_DIR}"

sbatch -p all \
  "${SBATCH_DEP_ARGS[@]}" \
  --job-name=engram-tokenize-local \
  -N"${NODES}" --ntasks="${WORKERS}" --cpus-per-task="${CPUS_PER_TASK}" \
  --time="${TIME_LIMIT}" --mem=1200G \
  --output="${PWD}/progress/logs/tokenize_%j.out" \
  --wrap="cd ${Q_PWD} && bash scripts/run_tokenize_fineweb_job.sh ${Q_PARQUET_GLOB} ${Q_OUT_DIR} ${MAX_TOKENS} ${WORKERS} ${CPUS_PER_TASK} ${GATE_MIN_TOKENS}"
