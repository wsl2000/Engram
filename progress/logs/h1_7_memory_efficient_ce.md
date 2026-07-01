# H1.7 memory-efficient linear CE

- Added local recompute/autograd linear CE backend:
  - `ENGRAM_CE_IMPL=memory_efficient`
  - `ENGRAM_CE_IMPL=auto` falls back to this backend when cut-cross-entropy / Liger are unavailable.
  - `ENGRAM_CE_IMPL=chunked` preserves the old chunked implementation.
- Motivation: current container lacks `cut_cross_entropy` and `liger_kernel`; the local backend avoids saving full logits for backward and gives calibration a real non-old CE path.
- Training metrics now log `ce_impl`.
- Validation:
  - memory-efficient CE matches chunked CE loss and gradients on a small randomized case.
  - `PYTHONPATH=src python -m py_compile src/engram/*.py scripts/*.py`
  - `PYTHONPATH=src pytest -q` -> 19 passed, 1 skipped
- Slurm state: node preflight job `168251` still `PENDING (Resources)`.
