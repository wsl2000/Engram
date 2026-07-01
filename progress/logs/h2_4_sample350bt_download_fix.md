# H2.4 sample-350BT download fix

Timestamp: 2026-07-01T06:21:15Z

## Anomaly

The first static parquet download command allowed both:

- `sample/350BT/*.parquet`
- `**/*.parquet`

The broad pattern matched the full dataset layout and began downloading `data/CC-MAIN-*` parquet shards. This violates the current handoff scope, which requires the FineWeb-Edu `sample-350BT` subset.

At detection:

- Wrong download job: `168254`
- Dependent wrong tokenizer job: `168260`
- Wrong-scope local data: 34 parquet files / 73.40GiB under `data/fineweb_edu_parquet/data/CC-MAIN-*`

## Action

- Canceled `168254` and `168260`.
- Removed generated wrong-scope `data/fineweb_edu_parquet` contents.
- Patched `scripts/download_fineweb_parquet.py` default allow-pattern to `sample/350BT/*.parquet` only.
- Patched `scripts/slurm_download_fineweb_parquet.sh` to pass only `sample/350BT/*.parquet`.

## Relaunch

- Corrected download: `168265`, CPU-only, `--time=12:00:00`, `--mem=256G`, running on `cn09`.
- Corrected dependent tokenizer/data gate: `168266`, CPU-only, dependency `afterok:168265`, `--time=18:00:00`, `--mem=1200G/node`, parquet glob `data/fineweb_edu_parquet/sample/350BT/*.parquet`.

## Validation

- `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py`: passed.
- `bash -n scripts/*.sh`: passed.
- Static Slurm time/mem audit: passed.

Next check must verify downloaded parquet paths are under `sample/350BT/` before trusting the tokenizer dependency.
