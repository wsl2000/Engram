#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $0 FACTS_CSV BASE_TOKEN_LIST [R_VALUES] [TARGET_TOKENS] [STEPS]" >&2
  exit 2
fi

FACTS_CSV="$1"
BASE_TOKEN_LIST="$2"
R_VALUES="${3:-1,2,4,8,16,32}"
TARGET_TOKENS="${4:-20000000000}"
STEPS="${5:-3179}"
EOS_ID="${EOS_ID:-1}"
CONFIG_JSON="${CONFIG_JSON:-configs/generated/A_seed1337.json}"
TRAIN_TIME="${TRAIN_TIME:-04:00:00}"
TRAIN_MEM="${TRAIN_MEM:-1800G}"
TRAIN_NODES="${TRAIN_NODES:-16}"
EVAL_TIME="${EVAL_TIME:-01:00:00}"
EVAL_MEM="${EVAL_MEM:-220G}"
TRAIN_DEP_ARGS=()
if [[ -n "${TRAIN_DEPENDENCY:-}" ]]; then
  TRAIN_DEP_ARGS+=(--dependency="${TRAIN_DEPENDENCY}")
fi

cd /mnt/vast/workspaces/JAIF/dy/code/Engram
mkdir -p progress/logs results/tier1 runs

IFS=',' read -r -a R_ARRAY <<< "${R_VALUES}"
for R in "${R_ARRAY[@]}"; do
  STREAM_DIR="data/tier1/rpilot_R${R}_tokens${TARGET_TOKENS}"
  RUN_DIR="runs/tier1_A_rpilot_R${R}"
  OUT_PREFIX="results/tier1/rpilot_A_R${R}"
  echo "preparing R=${R} stream at ${STREAM_DIR}" >&2
  PYTHONPATH=src python scripts/build_tier1_stream.py \
    --facts-csv "${FACTS_CSV}" \
    --output-dir "${STREAM_DIR}" \
    --repeats "${R}" \
    --eos-id "${EOS_ID}" \
    --base-token-list "${BASE_TOKEN_LIST}" \
    --auto-base-chunk \
    --target-tokens "${TARGET_TOKENS}" \
    --tokens-per-shard 100000000

  TRAIN_JOB="$(sbatch --parsable "${TRAIN_DEP_ARGS[@]}" --nodes="${TRAIN_NODES}" --time="${TRAIN_TIME}" --mem="${TRAIN_MEM}" scripts/slurm_tier1_train.sh "${CONFIG_JSON}" "${STREAM_DIR}/shards.txt" "${RUN_DIR}" "${STEPS}")"
  CKPT_STEP="$(printf '%06d' "${STEPS}")"
  EVAL_JOB="$(sbatch --parsable --dependency="afterok:${TRAIN_JOB}" --time="${EVAL_TIME}" --mem="${EVAL_MEM}" scripts/slurm_tier1_eval.sh "${RUN_DIR}/ckpt_step${CKPT_STEP}.pt" "${FACTS_CSV}" "${OUT_PREFIX}")"
  echo "R=${R} train_job=${TRAIN_JOB} train_dependency=${TRAIN_DEPENDENCY:-none} train_nodes=${TRAIN_NODES} train_time=${TRAIN_TIME} train_mem=${TRAIN_MEM} eval_job=${EVAL_JOB} eval_time=${EVAL_TIME} eval_mem=${EVAL_MEM}" | tee -a progress/results/tier1_rpilot_jobs.tsv
done
