# H12.6 h4 A complete, h4 B running

H4 A seed 2024 completed successfully:

- Job: `165373`
- State: `COMPLETED`, exit `0:0`
- Output: `runs/pair_h4_A_seed2024_20B_mbs4_80_v2`
- Final checkpoint: `ckpt_step005027.pt`, 28,030,759,631 bytes
- Endpoint: step 5,027 / 19,766,968,320 tokens
- Final observed throughput: 2.70M tok/s, MFU 9.73%

H4 B seed 2024 started automatically:

- Job: `165375`
- Output: `runs/pair_h4_B_seed2024_20B_mbs4_80_v2`
- Same h4 token stream, same seed, same 5,027-step endpoint, same AdamW/bf16/80-GPU/full-replication invariants.

Queued h4-pair eval after B:

- `165432` - B final TriviaQA answer-NLL knockout.
- `165433` - B final PopQA answer-NLL knockout.
- `165434` - B final TriviaQA 5-shot EM knockout.
- `165435` - B final PopQA 5-shot EM knockout.
- `165436` - A final h5 token slices.
- `165437` - B final h5 token slices.
- `165438` - A final h5 depth probe.
- `165439` - B final h5 depth probe.
- `165440` - B final h5 gate/contribution diagnostics.

The h4-pair slice/depth evals use `data/fineweb_edu_deepseek_h5_eval/shards.txt`, which was produced by whole-document prefix skipping beyond the h4 training prefix.
