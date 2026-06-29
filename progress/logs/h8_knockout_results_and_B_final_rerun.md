# H8.0 knockout results and B final-only rerun

## Knockout results at B step 959

Checkpoint: `runs/pair1_B_seed1337_matchA5027_mbs4_80/ckpt_step000959.pt`

Answer-NLL:

- TriviaQA, 50 records: normal 4.439720, knockout 4.446280, delta knockout-normal +0.006560, positive-delta fraction 0.64.
- PopQA, 50 records: normal 10.805519, knockout 10.792760, delta knockout-normal -0.012760, positive-delta fraction 0.38.

QA-EM:

- TriviaQA, 25 records, 5-shot: normal EM 0.0, knockout EM 0.0.
- PopQA, 25 records, 5-shot: normal EM 0.0, knockout EM 0.0.

Wiring diagnostic:

- Engram knockout is not a no-op in hidden space: normal-vs-knockout final hidden RMS delta is 0.035269; last-token logit mean absolute delta is 0.044900.
- However, the per-site Engram residual is small at the read points: block2 delta/hidden RMS 0.001071, block6 0.003650.

Interpretation: first-checkpoint knockout did not produce factual collapse. This is a bug-gate warning. Because normal EM is at floor and the diagnostic confirms a nonzero Engram path, continue to the matched B endpoint before drawing any primary conclusion; if the final B checkpoint also lacks knockout degradation, stop and debug Engram scale/wiring before more seeds.

## Training recovery

Observed failures:

- A job `165275` failed shortly after checkpoint step 5,027 while VAST was later observed at zero free space.
- B job `165317` failed shortly after checkpoint step 959, same pattern.

Code fix:

- `src/engram/train.py` now broadcasts the checkpoint decision and runs a DDP barrier after save, so rank0 cannot checkpoint while other ranks race ahead.
- Added `--checkpoint-minutes-override`.

Rerun:

- Submitted B final-only job `165327`.
- Output: `runs/pair1_B_seed1337_final5027_mbs4_80`
- Nodes: `cn03,cn04,cn13,cn14,cn15,cn16,cn25,cn26,cn27,cn29`
- Same pair-1 60-shard stream, same seed, mbs4/ga6, AdamW, bf16, grouped MoE backend.
- Checkpoint policy: `--checkpoint-minutes-override 9999`, so only the final step 5,027 checkpoint should be written.
