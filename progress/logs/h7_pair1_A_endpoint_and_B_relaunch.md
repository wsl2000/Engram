# H7.2 pair-1 A endpoint and B relaunch

## A endpoint

- A job: `165275`
- Final state: `FAILED`, `ExitCode=1:0`, elapsed `02:08:40`
- Last rank0 JSON step: 5,034 / 5,086
- Last complete checkpoint: `runs/pair1_A_seed1337_20B_mbs4_80_v2/ckpt_step005027.pt`
- Checkpoint size: 28,030,759,631 bytes
- Endpoint decision: fix pair-1 endpoint to step 5,027 for both A and B, because this is the last complete A checkpoint. This preserves matched step count, seed, data stream, world size, batch, optimizer, and precision.

No Python/NCCL/OOM traceback was found in `progress/logs/pair1_A_seed1337_20B_v2_165275.out`; the Slurm stdout stops at the checkpoint step while `train_rank0.jsonl` continues to step 5,034.

## B relaunch

- Old B job `165281`: canceled after its `afterok:165275` dependency became `DependencyNeverSatisfied`.
- Relaunch `165313`: failed immediately with `RaisedSignal:53`; a same-nodelist debug job `165314` also failed before stdout. Avoid `cn02` for new batch-host launches.
- Debug job `165315`: passed on `cn03,cn04,cn13,cn14,cn15,cn16,cn25,cn26,cn27,cn29`.
- Relaunch `165316`: reached model/optimizer init but failed because `shards.txt` itself was passed to `--token-files`; the train loader expects expanded `.bin` paths.
- Corrected B job `165317`: running on `cn03,cn04,cn13,cn14,cn15,cn16,cn25,cn26,cn27,cn29` with `TOKEN_FILES=$(tr '\n' ' ' < data/fineweb_edu_deepseek/shards.txt)`, target step 5,027, `ENGRAM_MOE_BACKEND=grouped`, bf16, AdamW, mbs4/ga6.

Next gate: run TriviaQA/PopQA answer-NLL and QA-EM knockout immediately at the first B checkpoint. If factual recall does not collapse under knockout, stop and debug Engram wiring before trusting other metrics.
