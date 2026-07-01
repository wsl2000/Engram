# H4.6 resumed sample-350BT download with 512G limit

Timestamp: 2026-07-01T08:40:42Z

## Stall

Corrected download job `168265` stopped making visible progress:

- Parquet files: 349 / 472.
- Size: 701G.
- Scope audit: `bad_scope=0`.
- Short check: active `.incomplete` file did not grow during 60 seconds.
- Memory: `sstat` reported `MaxRSS=255016284K` under a 256G allocation.

## Fix

- Patched `scripts/slurm_download_fineweb_parquet.sh` so memory is explicit and configurable:
  - positional arg 3 or `MEM_LIMIT`;
  - default remains `256G`;
  - resumed run uses `512G`.
- Added default Hugging Face timeout environment variables in the Slurm wrapper:
  - `HF_HUB_DOWNLOAD_TIMEOUT=120`;
  - `HF_HUB_ETAG_TIMEOUT=60`.
- Canceled stalled download `168265` and its pending tokenizer `168267`.

## Relaunch

- New download job: `169152`.
- Limits: `--time=08:00:00`, `--mem=512G`.
- Node: `cn09`.
- New dependent tokenizer/data gate: `169155`.
- Tokenizer limits: `--time=18:00:00`, `--mem=1200G/node`.
- Dependency: `afterok:169152`.

The same local parquet directory is reused, so Hugging Face snapshot download should resume from completed files.
