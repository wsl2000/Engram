# H20.7 - h4 B first-checkpoint quick gate results

- UTC: 2026-06-30T20:37Z.
- Quick gate job `167601` completed successfully (`COMPLETED`, exit `0:0`, elapsed `00:03:20`).
- Checkpoint evaluated: `runs/pair_h4_B_seed2024_20B_mbs4_80_v3/ckpt_step000952.pt`.
- Answer-NLL knockout:
  - TriviaQA limit 100: normal NLL `4.5870017707`, knockout NLL `4.5830951846`, delta knockout-normal `-0.0039065862`, positive-delta fraction `0.43`.
  - PopQA limit 100: normal NLL `9.9563346052`, knockout NLL `9.9580456448`, delta knockout-normal `+0.0017110395`, positive-delta fraction `0.60`.
- Diagnostics:
  - Final hidden delta RMS `0.0362668246`.
  - Last-logit mean absolute delta `0.0367558546`.
  - Layer 2 contribution/hidden RMS ratio `0.0010737991`.
  - Layer 6 contribution/hidden RMS ratio `0.0034090547`.
- Interpretation: early h4 B checkpoint has an exercised/nonzero Engram path, but factual knockout is still weak/no-collapse. This matches the prior early-checkpoint warning and must not be treated as a positive verification signal. Continue to final checkpoint and final h5-disjoint eval.
- Aggregates updated:
  - `results/knockout.csv`.
  - `results/gate_diagnostics.csv`.
- Raw outputs added under `results/knockout/` and `results/diagnostics/` with `h4v3_b0952_*` prefixes.
- Main h4 B job `167284` continues running; latest checked step while recording this was 1,268 / 5,027 and 4,985,978,880 tokens.
