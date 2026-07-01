# H4.1 sample-350BT download progress

Timestamp: 2026-07-01T08:06:55Z

## Jobs

- `168265`: corrected `sample/350BT` parquet download, running on `cn09`, CPU-only, `--time=12:00:00`, `--mem=256G`.
- `168267`: tokenizer/data gate, pending dependency `afterok:168265`, `--time=18:00:00`, `--mem=1200G/node`.
- `168251`: 128-H100 node preflight, pending resources/association, no allocation.

Current H100 allocation: 0.

## Download

- Files: 316 / 472 parquet files.
- Size: 634G.
- Scope audit: `bad_scope=0`; all downloaded parquet paths are under `sample/350BT/`.

## Next

Continue monitoring the download. After `168265` exits successfully, `168267` should start automatically, tokenize through 16 CPU workers, merge worker outputs, and run `assert_data_gate.py --min-tokens 200000000000`.
