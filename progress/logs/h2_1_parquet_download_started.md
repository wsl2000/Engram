# H2.1 offline parquet download started

- Submitted correct job: `168254` / `engram-parquet-download`.
- State: running on `cn34`.
- Resources: CPU-only, `cpu=16`, `mem=256G`, no GPU TRES.
- Command path: `scripts/slurm_download_fineweb_parquet.sh data/fineweb_edu_parquet 12:00:00`.
- Destination: `data/fineweb_edu_parquet`.
- First observed output:
  - `data/fineweb_edu_parquet/.cache/huggingface/.gitignore`
  - `data/fineweb_edu_parquet/data/CC-MAIN-2013-20/train-00000-of-00014.parquet`
- Accident corrected: outer wrapper job `168253` was canceled; it would only have submitted another `sbatch` layer.
- Concurrent GPU preflight: `168251` still pending with no GPU allocation.
