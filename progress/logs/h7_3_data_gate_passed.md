# H7.3 official data gate passed

Timestamp: 2026-07-01T12:15:01Z

## Job

- Tokenizer/data-gate job: `169155`.
- State: `COMPLETED`.
- Exit: `0:0`.
- Elapsed: `02:49:18`.
- Batch MaxRSS: `109187940K`.
- `srun` MaxRSS: `163127536K`.
- Limits: `TimeLimit=18:00:00`, `MinMemoryNode=1200G`.

Current H100 allocation: 0. The only remaining Slurm job is the pending 128-H100 node preflight `168251`.

## Gate

Artifact: `progress/results/data_gate_sample350bt_300b.json`

- `gate_passed`: true.
- `gate_min_tokens`: 200,000,000,000.
- `token_count`: 300,000,000,000.
- `gate_shard_token_sum`: 300,000,000,000.
- `doc_count`: 301,488,200.
- `gate_doc_manifest_lines`: 301,488,200.
- `parquet_files`: 472.
- `shard_count`: 3,008.

## Data Layout

- Parquet source: `data/fineweb_edu_parquet`, 930G.
- Tokenized workers: `data/fineweb_edu_deepseek_v3_300b`, 1.2T.
- Merged manifests: `data/fineweb_edu_deepseek_v3_300b/merged`, 52G.

The merged directory contains manifests and summary; token shards remain in worker directories and are referenced by `merged/shards.txt`.
