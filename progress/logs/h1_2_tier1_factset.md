# H1.2 Tier-1 factset

- Command:
  `PYTHONPATH=src python scripts/build_injected_facts.py --count 5000 --output-csv data/injected_facts/facts_5000_seed17.csv --seed 17 --negative-control-frac 0.1`
- Output:
  - `data/injected_facts/facts_5000_seed17.csv`
  - `progress/results/tier1_factset_5000_seed17_summary.json`
- Validation:
  - facts: 5,000
  - main class: 4,500
  - negative-control class: 500
  - single-token subjects: 5,000
  - single-token objects: 5,000
  - unique subject token IDs: 5,000
  - unique object token IDs: 5,000
  - subject/object token-ID overlap: 0
- Code fix: updated `mine_single_token_strings()` to de-duplicate decoded text and token IDs before splitting subject/object pools.
- Tests:
  - `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py`
  - `PYTHONPATH=src pytest -q` -> 16 passed, 1 skipped
