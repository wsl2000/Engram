import csv
import json

from engram.injected_facts import smoke_factset
from engram.tier1 import build_tier1_stream_from_facts, tier1_decision


def test_build_tier1_stream_from_facts(tmp_path):
    facts, _ = smoke_factset(4)
    facts_csv = tmp_path / "facts.csv"
    with facts_csv.open("w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["fact_id", "relation", "subject", "object", "subject_ids", "relation_ids", "object_ids", "fact_class"],
        )
        w.writeheader()
        for fact in facts:
            w.writerow(
                {
                    "fact_id": fact.fact_id,
                    "relation": fact.relation,
                    "subject": fact.subject,
                    "object": fact.object,
                    "subject_ids": json.dumps(list(fact.subject_ids)),
                    "relation_ids": json.dumps(list(fact.relation_ids)),
                    "object_ids": json.dumps(list(fact.object_ids)),
                    "fact_class": fact.fact_class,
                }
            )
    summary = build_tier1_stream_from_facts(str(facts_csv), repeats=2, eos_id=999, output_dir=tmp_path / "stream")
    assert summary["fact_count"] == 4
    assert summary["injected_docs"] == 8
    assert (tmp_path / "stream" / "docs.jsonl").exists()
    assert (tmp_path / "stream" / "shards.txt").exists()


def test_tier1_decision_passes_on_controlled_rows(tmp_path):
    a_csv = tmp_path / "a.csv"
    b_csv = tmp_path / "b.csv"
    fields = ["fact_id", "fact_class", "normal_nll", "knockout_nll", "delta_knockout_minus_normal", "normal_em", "knockout_em"]
    with a_csv.open("w", newline="") as fa, b_csv.open("w", newline="") as fb:
        wa = csv.DictWriter(fa, fieldnames=fields)
        wb = csv.DictWriter(fb, fieldnames=fields)
        wa.writeheader()
        wb.writeheader()
        for i in range(100):
            cls = "negative_control" if i < 10 else "main"
            wa.writerow({"fact_id": f"f{i}", "fact_class": cls, "normal_nll": 10, "knockout_nll": 10, "delta_knockout_minus_normal": 0, "normal_em": 0, "knockout_em": 0})
            b_em = 0 if cls == "negative_control" else 1
            wb.writerow({"fact_id": f"f{i}", "fact_class": cls, "normal_nll": 1, "knockout_nll": 10, "delta_knockout_minus_normal": 9, "normal_em": b_em, "knockout_em": 0})
    b_summary = tmp_path / "b.json"
    b_summary.write_text(
        json.dumps(
            {
                "main": {
                    "mean_delta_knockout_minus_normal": 9.0,
                    "em_collapse": 1.0,
                    "mcnemar_exact_p": 1e-9,
                    "normal_em": 1.0,
                    "knockout_em": 0.0,
                },
                "negative_control": {
                    "mean_delta_knockout_minus_normal": 0.0,
                    "em_collapse": 0.0,
                    "mcnemar_exact_p": 1.0,
                    "normal_em": 0.0,
                    "knockout_em": 0.0,
                },
            }
        )
    )
    decision = tier1_decision(a_csv, b_csv, b_summary)
    assert decision["pass"] is True
    assert decision["scope"].startswith("mechanism")
