# H15.0 - h4 v3 eval array queued

- Submitted Slurm job array: `167289_[0-8]` (`engram-h4-eval-v3`).
- Dependency: `afterok:167284`, so evals start only if h4 B v3 completes successfully and writes the final checkpoint.
- State at submit check: `PENDING (Dependency)`.
- Request per array task: 1 H100, 12 CPUs, 220G memory, 3h time limit, excluded `cn02,cn10,cn17,cn34`.
- Eval script: `scripts/slurm_h4_eval_after_b.sh`.
- Planned tasks:
  - 0: B TriviaQA answer-NLL normal vs knockout.
  - 1: B PopQA answer-NLL normal vs knockout.
  - 2: B TriviaQA 5-shot EM normal vs knockout.
  - 3: B PopQA 5-shot EM normal vs knockout.
  - 4: A h5-disjoint token slices.
  - 5: B h5-disjoint token slices.
  - 6: A h5-disjoint depth probe.
  - 7: B h5-disjoint depth probe.
  - 8: B h5-disjoint Engram gate/contribution diagnostics.
- Output prefix: `h4v3_*` under `results/knockout`, `results/slices`, `results/depth_probe`, and `results/diagnostics`.
- Next: wait for h4 B job `167284` allocation; once running, monitor first-step invariants and first checkpoint.
