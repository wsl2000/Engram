#!/usr/bin/env bash
#SBATCH --job-name=engram-tier1-rpilot-submit
#SBATCH --partition=all
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=512G
#SBATCH --time=08:00:00
#SBATCH --output=progress/logs/tier1_rpilot_submit_%j.out

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: sbatch $0 FACTS_CSV BASE_TOKEN_LIST [R_VALUES] [TARGET_TOKENS] [STEPS]" >&2
  exit 2
fi

cd /mnt/vast/workspaces/JAIF/dy/code/Engram
bash scripts/submit_tier1_r_pilot.sh "$@"
