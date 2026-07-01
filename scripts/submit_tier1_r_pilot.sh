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

  TRAIN_JOB="$(sbatch --parsable scripts/slurm_tier1_train.sh "${CONFIG_JSON}" "${STREAM_DIR}/shards.txt" "${RUN_DIR}" "${STEPS}")"
  CKPT_STEP="$(printf '%06d' "${STEPS}")"
  EVAL_JOB="$(sbatch --parsable --dependency="afterok:${TRAIN_JOB}" scripts/slurm_tier1_eval.sh "${RUN_DIR}/ckpt_step${CKPT_STEP}.pt" "${FACTS_CSV}" "${OUT_PREFIX}")"
  echo "R=${R} train_job=${TRAIN_JOB} eval_job=${EVAL_JOB}" | tee -a progress/results/tier1_rpilot_jobs.tsv
done
