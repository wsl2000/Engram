# H0 Local Gates

- `PYTHONPATH=src pytest -q`: `8 passed`
- `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py`: passed
- Muon probe: `muon` and `muon_optimizer` modules missing, so AdamW is fixed for all runs
- Synthetic paired-loader test:
  - Command shape: `scripts/hash_loader_test.py --seed 1337 --seq-len 128 --batch-size 4 --num-batches 100`
  - A hash: `470d2e582da346ffaedddd4f3c86edfcf9ad4229e7c039a01ba7ed1302a8c57e`
  - B hash: `470d2e582da346ffaedddd4f3c86edfcf9ad4229e7c039a01ba7ed1302a8c57e`
  - Result: bitwise identical

