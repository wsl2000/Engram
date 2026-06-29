# H5.3 h4 tokenization tranche complete

- Slurm job: `165276`.
- State: `COMPLETED`, exit code `0:0`, elapsed `00:18:44`.
- Output directory: `data/fineweb_edu_deepseek_h4`.
- Manifest build: `PYTHONPATH=src python scripts/list_token_shards.py data/fineweb_edu_deepseek_h4 --output data/fineweb_edu_deepseek_h4/shards.txt`.
- Result: 16 worker manifests, 208 shard files, 20,002,166,023 tokens, 75GB on disk.
- Use: available for held-out/slice eval or later seeds. It is not used for pair-1 B because pair-1 A already trained on `data/fineweb_edu_deepseek/shards.txt`; switching B would violate paired-stream invariance.
