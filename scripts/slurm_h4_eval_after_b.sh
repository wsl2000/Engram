#!/usr/bin/env bash
#SBATCH --job-name=engram-h4-eval-v3
#SBATCH --partition=all
#SBATCH --array=0-8
#SBATCH --gres=gpu:h100:1
#SBATCH --cpus-per-task=12
#SBATCH --mem=220G
#SBATCH --time=03:00:00
#SBATCH --exclude=cn02,cn10,cn17,cn34
#SBATCH --output=progress/logs/h4_eval_v3_%A_%a.out

set -euo pipefail

cd /mnt/vast/workspaces/JAIF/dy/code/Engram

export PYTHONPATH=src
export ENGRAM_MOE_BACKEND=grouped
export ENGRAM_CE_CHUNK_TOKENS=128
export OMP_NUM_THREADS=1

A_CONFIG=configs/generated/A_seed2024.json
B_CONFIG=configs/generated/B_seed2024.json
A_CKPT=runs/pair_h4_A_seed2024_20B_mbs4_80_v2/ckpt_step005027.pt
B_CKPT=runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step005027.pt
H5_TOKENS=data/fineweb_edu_deepseek_h5_eval/shards.txt

mkdir -p results/knockout results/slices results/depth_probe results/diagnostics

case "${SLURM_ARRAY_TASK_ID}" in
  0)
    python scripts/eval_answer_nll.py \
      --config "${B_CONFIG}" \
      --checkpoint "${B_CKPT}" \
      --task triviaqa \
      --limit 200 \
      --moe-backend grouped \
      --output-csv results/knockout/h4v3_b5027_triviaqa_nll.csv \
      --summary-json results/knockout/h4v3_b5027_triviaqa_nll.json
    ;;
  1)
    python scripts/eval_answer_nll.py \
      --config "${B_CONFIG}" \
      --checkpoint "${B_CKPT}" \
      --task popqa \
      --limit 200 \
      --moe-backend grouped \
      --output-csv results/knockout/h4v3_b5027_popqa_nll.csv \
      --summary-json results/knockout/h4v3_b5027_popqa_nll.json
    ;;
  2)
    python scripts/eval_qa_em.py \
      --config "${B_CONFIG}" \
      --checkpoint "${B_CKPT}" \
      --task triviaqa \
      --limit 100 \
      --num-shots 5 \
      --max-new-tokens 16 \
      --moe-backend grouped \
      --output-csv results/knockout/h4v3_b5027_triviaqa_em.csv \
      --summary-json results/knockout/h4v3_b5027_triviaqa_em.json
    ;;
  3)
    python scripts/eval_qa_em.py \
      --config "${B_CONFIG}" \
      --checkpoint "${B_CKPT}" \
      --task popqa \
      --limit 100 \
      --num-shots 5 \
      --max-new-tokens 16 \
      --moe-backend grouped \
      --output-csv results/knockout/h4v3_b5027_popqa_em.csv \
      --summary-json results/knockout/h4v3_b5027_popqa_em.json
    ;;
  4)
    python scripts/eval_token_slices.py \
      --config "${A_CONFIG}" \
      --checkpoint "${A_CKPT}" \
      --token-files-list "${H5_TOKENS}" \
      --num-batches 16 \
      --batch-size 1 \
      --eval-seed 424242 \
      --chunk-tokens 128 \
      --moe-backend grouped \
      --output-csv results/slices/h4v3_a5027_h5_slices.csv \
      --summary-json results/slices/h4v3_a5027_h5_slices.json
    ;;
  5)
    python scripts/eval_token_slices.py \
      --config "${B_CONFIG}" \
      --checkpoint "${B_CKPT}" \
      --token-files-list "${H5_TOKENS}" \
      --num-batches 16 \
      --batch-size 1 \
      --eval-seed 424242 \
      --chunk-tokens 128 \
      --moe-backend grouped \
      --output-csv results/slices/h4v3_b5027_h5_slices.csv \
      --summary-json results/slices/h4v3_b5027_h5_slices.json
    ;;
  6)
    python scripts/eval_depth_probe.py \
      --config "${A_CONFIG}" \
      --checkpoint "${A_CKPT}" \
      --token-files-list "${H5_TOKENS}" \
      --num-batches 8 \
      --positions-per-batch 256 \
      --eval-seed 515151 \
      --moe-backend grouped \
      --output-csv results/depth_probe/h4v3_a5027_h5_depth.csv \
      --summary-json results/depth_probe/h4v3_a5027_h5_depth.json
    ;;
  7)
    python scripts/eval_depth_probe.py \
      --config "${B_CONFIG}" \
      --checkpoint "${B_CKPT}" \
      --token-files-list "${H5_TOKENS}" \
      --num-batches 8 \
      --positions-per-batch 256 \
      --eval-seed 515151 \
      --moe-backend grouped \
      --output-csv results/depth_probe/h4v3_b5027_h5_depth.csv \
      --summary-json results/depth_probe/h4v3_b5027_h5_depth.json
    ;;
  8)
    python scripts/eval_engram_diagnostics.py \
      --config "${B_CONFIG}" \
      --checkpoint "${B_CKPT}" \
      --token-files-list "${H5_TOKENS}" \
      --num-batches 4 \
      --batch-size 1 \
      --eval-seed 616161 \
      --moe-backend grouped \
      --output-csv results/diagnostics/h4v3_b5027_engram_diag.csv \
      --summary-json results/diagnostics/h4v3_b5027_engram_diag.json
    ;;
  *)
    echo "Unknown SLURM_ARRAY_TASK_ID=${SLURM_ARRAY_TASK_ID}" >&2
    exit 2
    ;;
esac
