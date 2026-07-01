#!/usr/bin/env bash
set -euo pipefail

PARQUET_GLOB="${1:?usage: $0 PARQUET_GLOB OUT_DIR [MAX_TOKENS] [WORKERS] [NODES] [TIME_LIMIT]}"
OUT_DIR="${2:?usage: $0 PARQUET_GLOB OUT_DIR [MAX_TOKENS] [WORKERS] [NODES] [TIME_LIMIT]}"
MAX_TOKENS="${3:-300000000000}"
WORKERS="${4:-16}"
NODES="${5:-4}"
TIME_LIMIT="${6:-08:00:00}"
CPUS_PER_TASK="${CPUS_PER_TASK:-32}"
TOKENS_PER_WORKER=$(( (MAX_TOKENS + WORKERS - 1) / WORKERS ))

mkdir -p "${OUT_DIR}" progress/logs
SBATCH_DEP_ARGS=()
if [[ -n "${SBATCH_DEPENDENCY:-}" ]]; then
  SBATCH_DEP_ARGS+=(--dependency="${SBATCH_DEPENDENCY}")
fi

sbatch -p all \
  "${SBATCH_DEP_ARGS[@]}" \
  --job-name=engram-tokenize-local \
  -N"${NODES}" --ntasks="${WORKERS}" --cpus-per-task="${CPUS_PER_TASK}" \
  --time="${TIME_LIMIT}" --mem=1200G \
  --output="${PWD}/progress/logs/tokenize_%j.out" \
  --wrap="cd '${PWD}' && srun --ntasks='${WORKERS}' --cpus-per-task='${CPUS_PER_TASK}' bash -lc 'WORKER=\${SLURM_PROCID}; PYTHONPATH=src python -m engram.tokenize_fineweb --parquet-glob \"${PARQUET_GLOB}\" --output-dir \"${OUT_DIR}/worker_\${WORKER}\" --max-tokens \"${TOKENS_PER_WORKER}\" --tokens-per-shard 100000000 --batch-docs 512 --num-workers \"${WORKERS}\" --worker-index \"\${WORKER}\"' && mapfile -t WORKER_DIRS < <(find '${OUT_DIR}' -maxdepth 1 -type d -name 'worker_*' | sort) && PYTHONPATH=src python scripts/merge_tokenized_outputs.py --worker-dirs \"\${WORKER_DIRS[@]}\" --output-dir '${OUT_DIR}/merged' && PYTHONPATH=src python scripts/assert_data_gate.py --output-dir '${OUT_DIR}/merged' --min-tokens 200000000000"
