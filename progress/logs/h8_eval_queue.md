# H8.4 preliminary eval queue

Queued the preliminary final-checkpoint evals behind pair-1 B final-only job `165327`.

Dependency policy: `afterany:165327`, not `afterok`, because previous A/B jobs sometimes failed shortly after checkpoint writes. Each eval wrapper checks that the target checkpoint exists and is at least 25GB before loading; if B fails before producing a usable final checkpoint, the dependent B evals exit without producing metrics.

Queued jobs:

- `165333` - B final TriviaQA answer-NLL knockout, 200 records.
- `165334` - B final PopQA answer-NLL knockout, 200 records.
- `165335` - B final TriviaQA 5-shot EM knockout, 100 records.
- `165336` - B final PopQA 5-shot EM knockout, 100 records.
- `165337` - A final held-out h4 token slices, 16 batches, eval seed 424242.
- `165338` - B final held-out h4 token slices, 16 batches, eval seed 424242.
- `165339` - A final held-out h4 depth probe, 8 batches, 256 positions/batch, eval seed 515151.
- `165340` - B final held-out h4 depth probe, 8 batches, 256 positions/batch, eval seed 515151.
- `165342` - B step-959 and step-5027 gate-alpha / contribution-RMS diagnostics, 4 h4 batches, eval seed 616161.

The h4 held-out tranche is `data/fineweb_edu_deepseek_h4/shards.txt`, not the pair-1 training stream.

New reviewer feedback `feedback/review-20260629T0356Z.md` was read after rebasing. It classifies the early weak knockout as concerning but not conclusive: likely repeated-data washout from the 4.69B-unique pair-1 stream. Action taken here: keep the matched endpoint knockout, add gate-alpha and Engram-contribution RMS diagnostics, and avoid turning a weak endpoint knockout into a false negative without the gate/RMS evidence.

Current B final-only monitor snapshot at queue time:

- step 901 / 5,027
- tokens_seen 3,542,876,160 / 19,766,968,320
- tokens/s 2,571,712
- MFU 9.26%
- VAST free space ~99G
