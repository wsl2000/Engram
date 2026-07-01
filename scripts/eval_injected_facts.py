#!/usr/bin/env python
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import torch

from engram.config import ModelShape
from engram.injected_facts import InjectedFact, paired_stats, read_facts
from engram.model import EngramTransformerLM


def load_model(checkpoint: str, device: torch.device) -> EngramTransformerLM:
    ckpt = torch.load(checkpoint, map_location="cpu")
    shape = ModelShape(**ckpt["config"]["model"]) if "config" in ckpt else ModelShape()
    arm = ckpt.get("config", {}).get("arm", "B")
    routed = shape.routed_experts_b if arm == "B" else shape.routed_experts_a
    rows = ckpt.get("config", {}).get("engram_rows")
    if rows is None:
        from engram.config import exact_engram_rows

        rows = exact_engram_rows(shape)
    model = EngramTransformerLM(shape, routed_experts=int(routed), engram_rows=int(rows), engram_enabled=(arm == "B"))
    model.load_state_dict(ckpt["model"])
    dtype = torch.bfloat16 if device.type == "cuda" else torch.float32
    return model.to(device=device, dtype=dtype).eval()


def fact_nll(model: EngramTransformerLM, fact: InjectedFact, device: torch.device, knockout: bool) -> tuple[float, int]:
    prompt = list(fact.key_ids)
    answer = list(fact.answer_ids)
    context = prompt[:]
    total = 0.0
    first_pred = None
    with torch.inference_mode():
        for idx, target in enumerate(answer):
            ids = torch.tensor([context], device=device, dtype=torch.long)
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16, enabled=device.type == "cuda"):
                hidden = model(ids, knockout=knockout)["hidden"]
                logits = model.logits_for_hidden(hidden[:, -1:])
            logits = logits.float().squeeze(0).squeeze(0)
            if idx == 0:
                first_pred = int(logits.argmax(dim=-1).item())
            target_t = torch.tensor([target], device=device, dtype=torch.long)
            total += float(torch.nn.functional.cross_entropy(logits[None, :], target_t, reduction="sum").cpu())
            context.append(target)
    return total / max(1, len(answer)), int(first_pred == answer[0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--facts-csv", required=True)
    parser.add_argument("--output-csv", default="results/injected_facts.csv")
    parser.add_argument("--summary-json", default="results/injected_facts.json")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    device = torch.device("cuda", 0) if torch.cuda.is_available() else torch.device("cpu")
    model = load_model(args.checkpoint, device)
    facts = read_facts(args.facts_csv)
    if args.limit:
        facts = facts[: args.limit]
    rows = []
    for fact in facts:
        normal_nll, normal_em = fact_nll(model, fact, device, knockout=False)
        knockout_nll, knockout_em = fact_nll(model, fact, device, knockout=True)
        rows.append(
            {
                "fact_id": fact.fact_id,
                "fact_class": fact.fact_class,
                "normal_nll": normal_nll,
                "knockout_nll": knockout_nll,
                "delta_knockout_minus_normal": knockout_nll - normal_nll,
                "normal_em": normal_em,
                "knockout_em": knockout_em,
            }
        )
    out = Path(args.output_csv)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            w.writeheader()
            w.writerows(rows)
    main_rows = [r for r in rows if r["fact_class"] == "main"]
    control_rows = [r for r in rows if r["fact_class"] == "negative_control"]
    summary = {
        "checkpoint": args.checkpoint,
        "facts_csv": args.facts_csv,
        "main": paired_stats(main_rows),
        "negative_control": paired_stats(control_rows) if control_rows else None,
    }
    Path(args.summary_json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary_json).write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
