from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

import numpy as np

from .injected_facts import InjectedExample, binomial_two_sided_p, make_examples, read_facts


def read_token_file_list(paths: list[str] | None = None, list_file: str | None = None) -> list[str]:
    out: list[str] = []
    if list_file:
        out.extend(x.strip() for x in Path(list_file).read_text().splitlines() if x.strip())
    if paths:
        out.extend(paths)
    return out


class SequentialTokenReader:
    def __init__(self, token_files: list[str]):
        if not token_files:
            self.arrays: list[np.memmap] = []
        else:
            self.arrays = [np.memmap(path, dtype=np.uint32, mode="r") for path in token_files]
        self.file_idx = 0
        self.offset = 0

    def take(self, n: int) -> np.ndarray:
        if n <= 0 or not self.arrays:
            return np.empty(0, dtype=np.uint32)
        chunks: list[np.ndarray] = []
        taken_total = 0
        while taken_total < n:
            arr = self.arrays[self.file_idx]
            remain = len(arr) - self.offset
            take = min(n - taken_total, remain)
            if take:
                chunks.append(np.array(arr[self.offset : self.offset + take], dtype=np.uint32, copy=True))
                self.offset += take
                taken_total += take
            if self.offset >= len(arr):
                self.file_idx = (self.file_idx + 1) % len(self.arrays)
                self.offset = 0
        if len(chunks) == 1:
            return chunks[0]
        return np.concatenate(chunks).astype(np.uint32, copy=False)


def write_tier1_mixed_stream(
    examples: Iterable[InjectedExample],
    output_dir: str | Path,
    base_token_files: list[str] | None = None,
    base_chunk_tokens: int = 2048,
    tokens_per_shard: int = 100_000_000,
    target_tokens: int | None = None,
) -> dict[str, object]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    reader = SequentialTokenReader(base_token_files or [])
    shard_chunks: list[np.ndarray] = []
    shard_token_count = 0
    shard_idx = 0
    token_total = 0
    doc_count = 0
    injected_docs = 0
    base_docs = 0
    shard_rows = []

    def flush() -> None:
        nonlocal shard_chunks, shard_token_count, shard_idx
        if shard_token_count <= 0:
            return
        path = out / f"tier1_{shard_idx:06d}.u32"
        if len(shard_chunks) == 1:
            arr = shard_chunks[0]
        else:
            arr = np.concatenate(shard_chunks).astype(np.uint32, copy=False)
        arr.tofile(path)
        shard_rows.append({"path": str(path), "token_count": shard_token_count})
        shard_chunks = []
        shard_token_count = 0
        shard_idx += 1

    def append_doc(ids: list[int] | np.ndarray, doc_id: str, kind: str, docs_f, meta: dict[str, object]) -> bool:
        nonlocal token_total, doc_count, injected_docs, base_docs, shard_chunks, shard_token_count
        if target_tokens is not None and token_total >= target_tokens:
            return False
        arr = np.asarray(ids, dtype=np.uint32)
        if target_tokens is not None and token_total + len(arr) > target_tokens:
            arr = arr[: target_tokens - token_total]
        if len(arr) == 0:
            return False
        start = token_total
        shard_chunks.append(arr)
        shard_token_count += len(arr)
        token_total += len(arr)
        doc_count += 1
        injected_docs += int(kind == "injected")
        base_docs += int(kind == "base")
        row = {"doc_id": doc_id, "kind": kind, "start_token": start, "end_token": token_total, **meta}
        docs_f.write(json.dumps(row) + "\n")
        while shard_token_count >= tokens_per_shard:
            flush()
        return target_tokens is None or token_total < target_tokens

    with (out / "docs.jsonl").open("w") as docs:
        for idx, ex in enumerate(examples):
            if base_chunk_tokens > 0 and reader.arrays:
                keep_going = append_doc(
                    reader.take(base_chunk_tokens),
                    doc_id=f"base-{idx:08d}",
                    kind="base",
                    docs_f=docs,
                    meta={},
                )
                if not keep_going:
                    break
            keep_going = append_doc(
                list(ex.token_ids),
                doc_id=ex.doc_id,
                kind="injected",
                docs_f=docs,
                meta={
                    "fact_id": ex.fact_id,
                    "split": ex.split,
                    "key_ids": list(ex.key_ids),
                    "answer_ids": list(ex.answer_ids),
                },
            )
            if not keep_going:
                break
        flush()

    with (out / "shards.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["path", "token_count"])
        w.writeheader()
        w.writerows(shard_rows)
    (out / "shards.txt").write_text("\n".join(row["path"] for row in shard_rows) + ("\n" if shard_rows else ""))
    summary = {
        "output_dir": str(out),
        "token_count": token_total,
        "doc_count": doc_count,
        "base_docs": base_docs,
        "injected_docs": injected_docs,
        "shard_count": len(shard_rows),
        "base_chunk_tokens": base_chunk_tokens,
        "target_tokens": target_tokens,
        "doc_manifest": str(out / "docs.jsonl"),
        "shard_manifest": str(out / "shards.csv"),
        "token_list": str(out / "shards.txt"),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def build_tier1_stream_from_facts(
    facts_csv: str,
    repeats: int,
    eos_id: int,
    output_dir: str | Path,
    base_token_files: list[str] | None = None,
    base_chunk_tokens: int = 2048,
    tokens_per_shard: int = 100_000_000,
    target_tokens: int | None = None,
    split: str = "train",
) -> dict[str, object]:
    facts = read_facts(facts_csv)
    examples = make_examples(facts, repeats=repeats, eos_id=eos_id, split=split)
    summary = write_tier1_mixed_stream(
        examples,
        output_dir=output_dir,
        base_token_files=base_token_files,
        base_chunk_tokens=base_chunk_tokens,
        tokens_per_shard=tokens_per_shard,
        target_tokens=target_tokens,
    )
    summary.update({"facts_csv": facts_csv, "repeats": repeats, "split": split, "fact_count": len(facts)})
    Path(output_dir, "summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def load_eval_rows(path: str | Path) -> dict[str, dict[str, object]]:
    with Path(path).open(newline="") as f:
        return {row["fact_id"]: row for row in csv.DictReader(f)}


def mcnemar_gap_p(a_rows: dict[str, dict[str, object]], b_rows: dict[str, dict[str, object]], fact_class: str) -> tuple[float, int, int, int]:
    fact_ids = sorted(set(a_rows) & set(b_rows))
    b_only = 0
    a_only = 0
    n = 0
    for fact_id in fact_ids:
        a = a_rows[fact_id]
        b = b_rows[fact_id]
        if a.get("fact_class", "main") != fact_class or b.get("fact_class", "main") != fact_class:
            continue
        a_em = int(float(a["normal_em"]))
        b_em = int(float(b["normal_em"]))
        b_only += int(b_em == 1 and a_em == 0)
        a_only += int(a_em == 1 and b_em == 0)
        n += 1
    return binomial_two_sided_p(min(b_only, a_only), b_only + a_only), b_only, a_only, n


def tier1_decision(a_csv: str | Path, b_csv: str | Path, b_summary_json: str | Path) -> dict[str, object]:
    a_rows = load_eval_rows(a_csv)
    b_rows = load_eval_rows(b_csv)
    b_summary = json.loads(Path(b_summary_json).read_text())
    main = b_summary["main"]
    control = b_summary.get("negative_control") or {
        "normal_em": 0.0,
        "knockout_em": 0.0,
        "em_collapse": 0.0,
        "mean_delta_knockout_minus_normal": 0.0,
        "mcnemar_exact_p": 1.0,
    }

    p_gap_main, b_only_main, a_only_main, n_main = mcnemar_gap_p(a_rows, b_rows, "main")
    p_gap_control, b_only_control, a_only_control, n_control = mcnemar_gap_p(a_rows, b_rows, "negative_control")
    a_main_em = sum(int(float(r["normal_em"])) for r in a_rows.values() if r.get("fact_class", "main") == "main") / max(1, n_main)
    b_main_em = sum(int(float(r["normal_em"])) for r in b_rows.values() if r.get("fact_class", "main") == "main") / max(1, n_main)
    a_control_em = sum(int(float(r["normal_em"])) for r in a_rows.values() if r.get("fact_class") == "negative_control") / max(1, n_control)
    b_control_em = sum(int(float(r["normal_em"])) for r in b_rows.values() if r.get("fact_class") == "negative_control") / max(1, n_control)
    main_gap = b_main_em - a_main_em
    control_gap = b_control_em - a_control_em
    pass_a = (
        float(main["mean_delta_knockout_minus_normal"]) > 0.0
        and float(main["mcnemar_exact_p"]) < 1e-4
        and float(main["em_collapse"]) >= 0.05
    )
    pass_b = main_gap >= 0.20 and p_gap_main < 1e-4
    pass_c = control_gap < 0.5 * main_gap
    return {
        "tier": "Tier-1",
        "scope": "mechanism/param-efficiency positive control, not paper natural-data verification",
        "a_csv": str(a_csv),
        "b_csv": str(b_csv),
        "b_summary_json": str(b_summary_json),
        "main_b_knockout": main,
        "negative_control_b_knockout": control,
        "a_main_em": a_main_em,
        "b_main_em": b_main_em,
        "main_b_minus_a_em": main_gap,
        "main_b_only": b_only_main,
        "main_a_only": a_only_main,
        "main_gap_mcnemar_p": p_gap_main,
        "a_negative_control_em": a_control_em,
        "b_negative_control_em": b_control_em,
        "negative_control_b_minus_a_em": control_gap,
        "negative_control_b_only": b_only_control,
        "negative_control_a_only": a_only_control,
        "negative_control_gap_mcnemar_p": p_gap_control,
        "criterion_a_b_knockout_collapse": pass_a,
        "criterion_b_b_minus_a_margin": pass_b,
        "criterion_c_negative_control_specificity": pass_c,
        "pass": pass_a and pass_b and pass_c,
    }
