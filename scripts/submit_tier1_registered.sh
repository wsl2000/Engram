#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 4 ]]; then
  echo "usage: $0 FACTS_CSV BASE_TOKEN_LIST FROZEN_R TARGET_TOKENS [STEPS]" >&2
  exit 2
fi

FACTS_CSV="$1"
BASE_TOKEN_LIST="$2"
FROZEN_R="$3"
TARGET_TOKENS="$4"
STEPS="${5:-3179}"
EOS_ID="${EOS_ID:-1}"
TRAIN_TIME="${TRAIN_TIME:-04:00:00}"
TRAIN_MEM="${TRAIN_MEM:-1800G}"
TRAIN_NODES="${TRAIN_NODES:-16}"
EVAL_TIME="${EVAL_TIME:-01:00:00}"
EVAL_MEM="${EVAL_MEM:-220G}"
DECIDE_TIME="${DECIDE_TIME:-00:10:00}"
DECIDE_MEM="${DECIDE_MEM:-16G}"
TOKENS_PER_SHARD="${TOKENS_PER_SHARD:-100000000}"
RUN_SUFFIX="${RUN_SUFFIX:-}"
TRAIN_DEP_ARGS=()
if [[ -n "${TRAIN_DEPENDENCY:-}" ]]; then
  TRAIN_DEP_ARGS+=(--dependency="${TRAIN_DEPENDENCY}")
fi

cd /mnt/vast/workspaces/JAIF/dy/code/Engram
mkdir -p progress/logs results/tier1 runs

STREAM_DIR="data/tier1/registered_R${FROZEN_R}_tokens${TARGET_TOKENS}${RUN_SUFFIX}"
PYTHONPATH=src python scripts/build_tier1_stream.py \
  --facts-csv "${FACTS_CSV}" \
  --output-dir "${STREAM_DIR}" \
  --repeats "${FROZEN_R}" \
  --eos-id "${EOS_ID}" \
  --base-token-list "${BASE_TOKEN_LIST}" \
  --auto-base-chunk \
  --target-tokens "${TARGET_TOKENS}" \
  --tokens-per-shard "${TOKENS_PER_SHARD}"

A_RUN="runs/tier1_A_registered_R${FROZEN_R}${RUN_SUFFIX}"
B_RUN="runs/tier1_B_registered_R${FROZEN_R}${RUN_SUFFIX}"
A_JOB="$(sbatch --parsable "${TRAIN_DEP_ARGS[@]}" --nodes="${TRAIN_NODES}" --time="${TRAIN_TIME}" --mem="${TRAIN_MEM}" scripts/slurm_tier1_train.sh configs/generated/A_seed1337.json "${STREAM_DIR}/shards.txt" "${A_RUN}" "${STEPS}")"
B_JOB="$(sbatch --parsable "${TRAIN_DEP_ARGS[@]}" --nodes="${TRAIN_NODES}" --time="${TRAIN_TIME}" --mem="${TRAIN_MEM}" scripts/slurm_tier1_train.sh configs/generated/B_seed1337.json "${STREAM_DIR}/shards.txt" "${B_RUN}" "${STEPS}")"
CKPT_STEP="$(printf '%06d' "${STEPS}")"
A_OUT="results/tier1/registered_A_R${FROZEN_R}${RUN_SUFFIX}"
B_OUT="results/tier1/registered_B_R${FROZEN_R}${RUN_SUFFIX}"
DECISION_OUT="results/tier1/registered_decision_R${FROZEN_R}${RUN_SUFFIX}.json"
A_EVAL="$(sbatch --parsable --dependency="afterok:${A_JOB}" --time="${EVAL_TIME}" --mem="${EVAL_MEM}" scripts/slurm_tier1_eval.sh "${A_RUN}/ckpt_step${CKPT_STEP}.pt" "${FACTS_CSV}" "${A_OUT}")"
B_EVAL="$(sbatch --parsable --dependency="afterok:${B_JOB}" --time="${EVAL_TIME}" --mem="${EVAL_MEM}" scripts/slurm_tier1_eval.sh "${B_RUN}/ckpt_step${CKPT_STEP}.pt" "${FACTS_CSV}" "${B_OUT}")"
DECIDE_JOB="$(sbatch --parsable --dependency="afterok:${A_EVAL}:${B_EVAL}" --job-name=engram-tier1-decide --partition=all --nodes=1 --ntasks=1 --cpus-per-task=2 --mem="${DECIDE_MEM}" --time="${DECIDE_TIME}" --output=progress/logs/tier1_decide_%j.out --wrap="cd '${PWD}' && PYTHONPATH=src python scripts/decide_tier1.py --a-csv ${A_OUT}.csv --b-csv ${B_OUT}.csv --b-summary-json ${B_OUT}.json --output-json ${DECISION_OUT}")"

{
  echo "stream=${STREAM_DIR}"
  echo "A_JOB=${A_JOB}"
  echo "B_JOB=${B_JOB}"
  echo "A_EVAL=${A_EVAL}"
  echo "B_EVAL=${B_EVAL}"
  echo "DECIDE_JOB=${DECIDE_JOB}"
  echo "TRAIN_DEPENDENCY=${TRAIN_DEPENDENCY:-none}"
  echo "TRAIN_NODES=${TRAIN_NODES}"
  echo "TRAIN_LIMIT=${TRAIN_TIME}/${TRAIN_MEM}"
  echo "EVAL_LIMIT=${EVAL_TIME}/${EVAL_MEM}"
  echo "DECIDE_LIMIT=${DECIDE_TIME}/${DECIDE_MEM}"
  echo "TOKENS_PER_SHARD=${TOKENS_PER_SHARD}"
  echo "RUN_SUFFIX=${RUN_SUFFIX:-none}"
} | tee "progress/results/tier1_registered_R${FROZEN_R}${RUN_SUFFIX}_jobs.txt"
