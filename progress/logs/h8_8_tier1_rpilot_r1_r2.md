# H8.8 Tier-1 R-pilot R1/R2 queued

Timestamp: 2026-07-01T13:48:30Z

## Submitter

- Job: `171792`.
- State: running.
- Node: `cn09`.
- Limits: `TimeLimit=08:00:00`, `MinMemoryNode=512G`.
- Current action: building R=4 stream.

## Completed Streams

- R=1:
  - stream: `data/tier1/rpilot_R1_tokens20000000000`;
  - tokens: 19,999,985,000;
  - docs: 10,000;
  - base chunk tokens: 3,999,992;
  - shards: 193.
- R=2:
  - stream: `data/tier1/rpilot_R2_tokens20000000000`;
  - tokens: 19,999,970,000;
  - docs: 20,000;
  - base chunk tokens: 1,999,992;
  - shards: 197.

## Queued Jobs

- R=1 train/eval: `172196` / `172197`.
- R=2 train/eval: `172669` / `172670`.
- Train jobs are pending on `Dependency=afterok:168251(unfulfilled)`.
- Eval jobs are pending on their train jobs.

Current H100 allocation: 0.
