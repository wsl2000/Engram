# H2.2 parallel tokenizer pipeline

Timestamp: 2026-07-01T06:14:21Z

## State

- `168251` node preflight: pending resources, requests 16 nodes / 128 H100, no GPU allocation yet.
- `168254` parquet download: running on `cn34`, CPU-only, no GPU TRES.
- `168260` local tokenizer: pending dependency on `afterok:168254`, no GPU TRES.
- Current H100 allocation for this resumed objective: 0.

## Data

- Download directory: `data/fineweb_edu_parquet`.
- Latest size: 56G.
- Latest parquet count: 26.

## Implementation

- `tokenize_local_parquet()` now uses recursive globbing so `**/*.parquet` works.
- Worker sharding is deterministic by sorted parquet path index modulo `num_workers`.
- Empty workers write valid empty manifests and summaries instead of failing.
- `merge_tokenized_outputs()` merges worker manifests and summaries into a single token pool for the data gate.
- `scripts/slurm_tokenize_fineweb.sh` submits parallel CPU tokenizer tasks, supports `SBATCH_DEPENDENCY`, merges worker outputs, and runs the >=200B gate on the merged pool.

## Validation

- `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py`: passed.
- `bash -n scripts/slurm_tokenize_fineweb.sh scripts/slurm_download_fineweb_parquet.sh`: passed.
- `PYTHONPATH=src pytest -q`: 19 passed, 1 skipped.
- Recursive glob smoke: 3 docs / 44 tokens, gate passed with min_tokens=1.
- Parallel tokenizer smoke: worker 0 tokenized the tiny parquet sample; worker 1 produced empty manifests; merged output had 3 docs / 44 tokens and passed gate with min_tokens=1.

## Next

Push progress, pull feedback, and monitor download job `168254`. The dependent tokenizer job `168260` should start automatically after a successful download and will run the >=200B data gate on merged output.
