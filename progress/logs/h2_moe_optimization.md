# H2.5 MoE optimization attempts

- Time: 2026-06-29 00:00 UTC
- Goal: recover enough throughput to make the H12/H24 handoff schedule plausible without changing ISO-PARAM/ISO-FLOPS, DDP full expert replication, bf16, optimizer, data order, or arm definitions.
- Available libraries: Triton exists, but Megablocks, Tutel, DeepSpeed MoE, grouped_gemm, FlashAttention, and Transformer Engine are not installed. Spack/module checks found only CUDA relevant to this problem. The example PyTorch 2.7 Apptainer image also lacks those MoE backends.

Attempts:

1. Full padded batched experts via `torch.bmm`
   - Semantics: same router/top-k/expert weights; sort token-expert pairs by expert, pad per expert, run one batched MLP.
   - 1xH100 probe: A 0.781s/step; B 0.747s/step, much faster than original ~4.3s/step.
   - 64GPU DDP+AdamW probe: OOM during routed MLP, with ranks at ~79GB used.
   - Decision: rejected as default path.

2. Grouped padded batched experts
   - Semantics: same as above, but process experts in groups of 8 to reduce peak activation memory.
   - 1xH100 probe: A 1.729s/step; B 1.688s/step.
   - 64GPU probe: fit but step1 took 120.97s, 34.7k tok/s, MFU 0.16%.
   - Decision: rejected; worse than original 80GPU calibration.

3. Full padded batched experts plus block activation checkpointing
   - 1xH100 probe: A 0.961s/step; B 0.854s/step.
   - 64GPU probe: fit but step1/2 took 121.39s and 115.95s, 34.6k-36.2k tok/s.
   - Decision: rejected; checkpointing avoids OOM but makes multi-node throughput unusable.

Current code state:

- Default training path is restored to the safe Python expert loop.
- Only retained implementation change is equivalent router-stat computation using `bincount` instead of materializing a large one-hot tensor.
- `pytest -q` passes 10/10.

Conclusion:

The 24h handoff schedule remains blocked by MoE kernel/runtime performance. Continuing long A/B training with the current pure-PyTorch stack would burn cluster time without reaching the mandatory H12/H24 deliverables. A real grouped-GEMM MoE backend is required before training.
