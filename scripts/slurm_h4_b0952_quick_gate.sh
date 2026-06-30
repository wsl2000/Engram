#!/usr/bin/env bash
#SBATCH --job-name=engram-h4-b0952-gate
#SBATCH --partition=all
#SBATCH --gres=gpu:h100:1
#SBATCH --cpus-per-task=12
#SBATCH --mem=220G
#SBATCH --time=02:00:00
#SBATCH --exclude=cn02,cn10,cn17,cn34
#SBATCH --output=progress/logs/h4_b0952_quick_gate_%j.out

set -euo pipefail

cd /mnt/vast/workspaces/JAIF/dy/code/Engram

export PYTHONPATH=src
export ENGRAM_MOE_BACKEND=grouped
export ENGRAM_CE_CHUNK_TOKENS=128
export OMP_NUM_THREADS=1

B_CONFIG=configs/generated/B_seed2024.json
B_CKPT=runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step000952.pt
H5_TOKENS=data/fineweb_edu_deepseek_h5_eval/shards.txt

mkdir -p results/knockout results/diagnostics

python scripts/eval_answer_nll.py \
  --config "${B_CONFIG}" \
  --checkpoint "${B_CKPT}" \
  --task triviaqa \
  --limit 100 \
  --moe-backend grouped \
  --output-csv results/knockout/h4v3_b0952_triviaqa_nll.csv \
  --summary-json results/knockout/h4v3_b0952_triviaqa_nll.json

python scripts/eval_answer_nll.py \
  --config "${B_CONFIG}" \
  --checkpoint "${B_CKPT}" \
  --task popqa \
  --limit 100 \
  --moe-backend grouped \
  --output-csv results/knockout/h4v3_b0952_popqa_nll.csv \
  --summary-json results/knockout/h4v3_b0952_popqa_nll.json

python scripts/eval_engram_diagnostics.py \
  --config "${B_CONFIG}" \
  --checkpoint "${B_CKPT}" \
  --token-files-list "${H5_TOKENS}" \
  --num-batches 4 \
  --batch-size 1 \
  --eval-seed 616161 \
  --moe-backend grouped \
  --output-csv results/diagnostics/h4v3_b0952_engram_diag.csv \
  --summary-json results/diagnostics/h4v3_b0952_engram_diag.json
