# H7.8 first B checkpoint knockout gate

## Checkpoint

- B job: `165317`
- Checkpoint: `runs/pair1_B_seed1337_matchA5027_mbs4_80/ckpt_step000959.pt`
- Checkpoint size: 28,027,733,867 bytes
- Step/tokens: 959 steps, 3,770,941,440 tokens
- Runtime to checkpoint: about 25 minutes
- Throughput before checkpoint: roughly 2.58-2.62M tok/s, MFU roughly 9.3-9.4%

The B training job failed after the checkpoint, with rank0 logging through step 964. No Python/NCCL/OOM traceback was found in the Slurm stdout. A showed the same post-checkpoint failure pattern after its last checkpoint. After the knockout gate, the checkpoint save/resume path needs repair before continuing to the matched B endpoint.

## Knockout jobs

- NLL job: `165324`, node `cn03`, output `progress/logs/knockout_nll_b0959_165324.out`
- QA-EM job: `165325`, node `cn04`, output `progress/logs/knockout_em_b0959_165325.out`
- Outputs: `results/knockout/b0959_*`
- Tasks: TriviaQA and PopQA

BUG GATE rule: if factual recall does not degrade under knockout, treat Engram wiring as untrusted and debug gate/indices/residual before trusting any other number.

## Storage cleanup

VAST reported no global free space and initially refused `results/knockout` creation. To unblock the mandatory gate, removed self-generated intermediate A checkpoints:

- `ckpt_step001002.pt`
- `ckpt_step002007.pt`
- `ckpt_step003013.pt`
- `ckpt_step004020.pt`

Kept A endpoint `ckpt_step005027.pt` and B first checkpoint `ckpt_step000959.pt`.
