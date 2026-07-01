#!/usr/bin/env bash
#SBATCH --job-name=engram-tier1-eval
#SBATCH --partition=all
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:h100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=220G
#SBATCH --time=01:00:00
#SBATCH --exclude=cn02,cn10,cn17,cn34
#SBATCH --output=progress/logs/tier1_eval_%j.out

set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "usage: sbatch $0 CHECKPOINT FACTS_CSV OUTPUT_PREFIX [LIMIT]" >&2
  exit 2
fi

CHECKPOINT="$1"
FACTS_CSV="$2"
OUTPUT_PREFIX="$3"
LIMIT="${4:-}"

cd /mnt/vast/workspaces/JAIF/dy/code/Engram
mkdir -p "$(dirname "${OUTPUT_PREFIX}")"
export PYTHONPATH=src
export ENGRAM_MOE_BACKEND=grouped

ARGS=(
  --checkpoint "${CHECKPOINT}"
  --facts-csv "${FACTS_CSV}"
  --output-csv "${OUTPUT_PREFIX}.csv"
  --summary-json "${OUTPUT_PREFIX}.json"
)
if [[ -n "${LIMIT}" ]]; then
  ARGS+=(--limit "${LIMIT}")
fi

python scripts/eval_injected_facts.py "${ARGS[@]}"
