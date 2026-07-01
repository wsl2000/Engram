# H5.3 tokenizer running

Timestamp: 2026-07-01T09:22:48Z

## Download

- FineWeb-Edu subset: `sample/350BT`.
- Parquet files: 472 / 472.
- Size: 930G.
- Scope audit: `bad_scope=0`.

## Tokenizer job

- Job: `169155`.
- State: running.
- Nodes: `cn[13-16]`.
- Limits: `TimeLimit=18:00:00`, `MinMemoryNode=1200G`.
- CPU-only; current H100 allocation remains 0.

## Tokenizer progress

- Worker dirs: 16.
- `.u32` shards: 86.
- Token output size: 34G.
- Runtime at check: about 4.5 minutes.

## Log notes

The log contains `TRANSFORMERS_CACHE` deprecation warnings and several tokenizer warnings for individual documents longer than 131072 tokens. There is no stack trace or worker failure at this check.

## Next

Wait for all 16 workers to finish. The helper will assert exact worker count, merge worker manifests into `data/fineweb_edu_deepseek_v3_300b/merged`, and run the >=200B data gate.
