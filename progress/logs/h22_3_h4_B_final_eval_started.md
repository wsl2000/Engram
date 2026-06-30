# H22.3 h4 B final checkpoint and eval start

- UTC check: 2026-06-30 around 22:20.
- Training job: `167284` / `engram-h4-B2024v3`.
- Slurm result: `COMPLETED`, exit `0:0`, elapsed `02:15:48`, nodes `cn[14-15,19,24-26,29-32]`.
- Final step: 5,027 / 5,027.
- Final tokens: 19,766,968,320 / 19,766,968,320.
- Final logged throughput/MFU: 2,571,946 tok/s, MFU 0.0926.
- Final checkpoint: `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step005027.pt`, 28,027,733,867 bytes.
- Complete B checkpoints: 000952, 001907, 002863, 003820, 004777, and 005027.
- Eval array: `167289_0..8` started automatically after `afterok:167284`.
- Current eval state:
  - Running: tasks 0-3, TriviaQA/PopQA knockout answer-NLL and 5-shot EM.
  - Completed: tasks 4-8, A/B h5 slices, A/B h5 depth, B h5 Engram diagnostics.
- Partial eval values:
  - h5 slices: A global 2.7372745, B global 2.7473171; A repeated-ngram 1.0668151, B repeated-ngram 1.0691550; A entity-proxy 4.2457943, B entity-proxy 4.2930119.
  - h5 depth: A mean earliest layer 17.09375 / median 19; B mean earliest layer 17.06543 / median 19.
  - B diagnostics: final hidden delta RMS 0.0649173; last-logit mean absolute delta 0.0961437; layer-6 contribution/hidden RMS ratio 0.0121942.
- Interpretation: final checkpoint is usable and Engram path remains active. Await tasks 0-3 before making the final h4 verdict.
