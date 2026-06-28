# H1 Smoke Tests And Anomalies

## Passed

- 1xH100 tiny training smoke:
  - Config: `configs/smoke_tiny.json`
  - Steps: 2
  - Output: `runs/smoke_tiny/train_rank0.jsonl`
  - Result: pass
- 80xH100 tiny DDP smoke:
  - Nodelist: `cn03,cn04,cn13,cn14,cn15,cn16,cn25,cn26,cn27,cn34`
  - Steps: 2
  - Job: `165130`
  - Result: `COMPLETED 0:0`
  - Rank0 step 2: loss `7.6021`, tokens/s `1.041e6` on tiny config

## Anomalies

- `cn17` CUDA context anomaly:
  - Symptom: `torch.cuda.set_device(local_rank)` raises CUDA OOM in 8-rank torchrun despite empty `nvidia-smi`
  - Reproduced with a standalone 8-rank CUDA probe
  - Action: exclude `cn17` from training nodelists
- Tokenization job `165112`:
  - Target: 90B tokens, 80 workers
  - Problem: transient Hugging Face 504 killed workers; 1B shard threshold meant no partial files flushed
  - Action: canceled job, added `finally` flush, disabled non-tty tqdm, reduced shard size to 100M

