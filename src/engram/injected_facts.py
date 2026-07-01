from __future__ import annotations

import csv
import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Any, Iterable

import numpy as np


@dataclass(frozen=True)
class InjectedFact:
    fact_id: str
    relation: str
    subject: str
    object: str
    subject_ids: tuple[int, ...]
    relation_ids: tuple[int, ...]
    object_ids: tuple[int, ...]
    fact_class: str = "main"

    @property
    def key_ids(self) -> tuple[int, ...]:
        return self.subject_ids + self.relation_ids

    @property
    def answer_ids(self) -> tuple[int, ...]:
        return self.object_ids


@dataclass(frozen=True)
class InjectedExample:
    fact_id: str
    doc_id: str
    token_ids: tuple[int, ...]
    key_ids: tuple[int, ...]
    answer_ids: tuple[int, ...]
    split: str


def stable_doc_id(prefix: str, *parts: object) -> str:
    h = hashlib.blake2b(digest_size=10)
    for part in parts:
        h.update(str(part).encode())
        h.update(b"\0")
    return f"{prefix}-{h.hexdigest()}"


def token_ids(tokenizer: Any, text: str) -> tuple[int, ...]:
    return tuple(int(x) for x in tokenizer(text, add_special_tokens=False)["input_ids"])


def is_single_token(tokenizer: Any, text: str) -> bool:
    return len(token_ids(tokenizer, text)) == 1


def mine_single_token_strings(
    tokenizer: Any,
    limit: int,
    min_id: int = 256,
    max_id: int | None = None,
    seed: int = 0,
) -> list[str]:
    vocab_size = int(getattr(tokenizer, "vocab_size", 0) or len(tokenizer))
    high = min(vocab_size, max_id or vocab_size)
    rng = random.Random(seed)
    ids = list(range(min_id, high))
    rng.shuffle(ids)
    out: list[str] = []
    seen_text: set[str] = set()
    seen_ids: set[tuple[int, ...]] = set()
    for idx in ids:
        text = tokenizer.decode([idx], clean_up_tokenization_spaces=False)
        if not text or text.isspace():
            continue
        if any(ch in text for ch in "\n\r\t"):
            continue
        if text.strip() != text:
            continue
        ids_for_text = token_ids(tokenizer, text)
        if len(ids_for_text) == 1 and text not in seen_text and ids_for_text not in seen_ids:
            seen_text.add(text)
            seen_ids.add(ids_for_text)
            out.append(text)
        if len(out) >= limit:
            break
    if len(out) < limit:
        raise RuntimeError(f"only mined {len(out)} single-token strings, need {limit}")
    return out


def build_facts_from_tokens(
    subjects: list[str],
    objects: list[str],
    relations: list[str],
    tokenizer: Any,
    count: int,
    seed: int = 0,
    negative_control_frac: float = 0.1,
) -> list[InjectedFact]:
    if len(subjects) < count:
        raise ValueError("need at least count subjects")
    if len(objects) < count:
        raise ValueError("need at least count objects")
    rng = random.Random(seed)
    rng.shuffle(subjects)
    rng.shuffle(objects)
    facts: list[InjectedFact] = []
    neg_count = int(round(count * negative_control_frac))
    for i in range(count):
        relation = relations[i % len(relations)]
        fact_class = "negative_control" if i < neg_count else "main"
        facts.append(
            InjectedFact(
                fact_id=f"fact_{i:06d}",
                relation=relation,
                subject=subjects[i],
                object=objects[i],
                subject_ids=token_ids(tokenizer, subjects[i]),
                relation_ids=token_ids(tokenizer, relation),
                object_ids=token_ids(tokenizer, objects[i]),
                fact_class=fact_class,
            )
        )
    return facts


def canonical_train_text(fact: InjectedFact) -> str:
    return f"{fact.subject}{fact.relation}{fact.object}"


def canonical_probe_text(fact: InjectedFact) -> str:
    return f"{fact.subject}{fact.relation}"


def make_examples(
    facts: Iterable[InjectedFact],
    repeats: int,
    eos_id: int,
    split: str,
) -> list[InjectedExample]:
    examples: list[InjectedExample] = []
    for fact in facts:
        if fact.fact_class == "negative_control":
            # Deliberately remove the clean recurring key N-gram for the control.
            seq = fact.relation_ids + fact.subject_ids + fact.object_ids + (eos_id,)
            key = fact.relation_ids + fact.subject_ids
        else:
            seq = fact.subject_ids + fact.relation_ids + fact.object_ids + (eos_id,)
            key = fact.key_ids
        for r in range(repeats):
            examples.append(
                InjectedExample(
                    fact_id=fact.fact_id,
                    doc_id=stable_doc_id("kb", split, fact.fact_id, r),
                    token_ids=seq,
                    key_ids=key,
                    answer_ids=fact.answer_ids,
                    split=split,
                )
            )
    return examples


def assert_key_identity(train_examples: Iterable[InjectedExample], eval_examples: Iterable[InjectedExample]) -> None:
    train = {}
    for ex in train_examples:
        train.setdefault(ex.fact_id, ex.key_ids)
    for ex in eval_examples:
        expected = train.get(ex.fact_id)
        if expected is None:
            continue
        if tuple(expected) != tuple(ex.key_ids):
            raise AssertionError(f"key token mismatch for {ex.fact_id}: train={expected} eval={ex.key_ids}")


def write_injected_stream(
    examples: Iterable[InjectedExample],
    output_dir: str | Path,
    tokens_per_shard: int = 100_000_000,
) -> dict[str, object]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    shard_rows = []
    doc_path = out / "docs.jsonl"
    shard_tokens: list[int] = []
    shard_idx = 0
    token_total = 0
    doc_count = 0

    def flush() -> None:
        nonlocal shard_tokens, shard_idx
        if not shard_tokens:
            return
        path = out / f"inject_{shard_idx:06d}.u32"
        np.asarray(shard_tokens, dtype=np.uint32).tofile(path)
        shard_rows.append({"path": str(path), "token_count": len(shard_tokens)})
        shard_tokens = []
        shard_idx += 1

    with doc_path.open("w") as docs:
        for ex in examples:
            start = token_total
            ids = list(ex.token_ids)
            shard_tokens.extend(ids)
            token_total += len(ids)
            doc_count += 1
            docs.write(
                json.dumps(
                    {
                        "doc_id": ex.doc_id,
                        "fact_id": ex.fact_id,
                        "split": ex.split,
                        "start_token": start,
                        "end_token": token_total,
                        "key_ids": list(ex.key_ids),
                        "answer_ids": list(ex.answer_ids),
                    }
                )
                + "\n"
            )
            while len(shard_tokens) >= tokens_per_shard:
                flush()
        flush()
    with (out / "shards.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["path", "token_count"])
        w.writeheader()
        w.writerows(shard_rows)
    summary = {
        "output_dir": str(out),
        "token_count": token_total,
        "doc_count": doc_count,
        "shard_count": len(shard_rows),
        "doc_manifest": str(doc_path),
        "shard_manifest": str(out / "shards.csv"),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def choose_freeze_r(a_recall_by_r: dict[int, float], max_recall: float = 0.10) -> int:
    for r in sorted(a_recall_by_r):
        if a_recall_by_r[r] < max_recall:
            return r
    raise ValueError(f"no R has A recall < {max_recall}")


def binomial_two_sided_p(k: int, n: int, p: float = 0.5) -> float:
    if n <= 0:
        return 1.0
    cutoff = min(k, n - k)
    prob = sum(math.comb(n, i) * (p**i) * ((1 - p) ** (n - i)) for i in range(cutoff + 1))
    return min(1.0, 2.0 * prob)


def paired_stats(rows: list[dict[str, float | int | str]]) -> dict[str, float | int]:
    deltas = [float(r["knockout_nll"]) - float(r["normal_nll"]) for r in rows]
    normal_em = [int(r["normal_em"]) for r in rows]
    knockout_em = [int(r["knockout_em"]) for r in rows]
    b = sum(1 for n, k in zip(normal_em, knockout_em) if n == 1 and k == 0)
    c = sum(1 for n, k in zip(normal_em, knockout_em) if n == 0 and k == 1)
    return {
        "records": len(rows),
        "mean_delta_knockout_minus_normal": mean(deltas) if deltas else 0.0,
        "normal_em": mean(normal_em) if normal_em else 0.0,
        "knockout_em": mean(knockout_em) if knockout_em else 0.0,
        "em_collapse": (mean(normal_em) - mean(knockout_em)) if normal_em else 0.0,
        "mcnemar_b_normal_only": b,
        "mcnemar_c_knockout_only": c,
        "mcnemar_exact_p": binomial_two_sided_p(min(b, c), b + c),
    }


def write_facts(path: str | Path, facts: Iterable[InjectedFact]) -> None:
    rows = []
    for fact in facts:
        row = asdict(fact)
        row["subject_ids"] = json.dumps(list(fact.subject_ids))
        row["relation_ids"] = json.dumps(list(fact.relation_ids))
        row["object_ids"] = json.dumps(list(fact.object_ids))
        rows.append(row)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        if rows:
            w.writeheader()
            w.writerows(rows)


def read_facts(path: str | Path) -> list[InjectedFact]:
    facts: list[InjectedFact] = []
    with Path(path).open(newline="") as f:
        for row in csv.DictReader(f):
            facts.append(
                InjectedFact(
                    fact_id=row["fact_id"],
                    relation=row["relation"],
                    subject=row["subject"],
                    object=row["object"],
                    subject_ids=tuple(json.loads(row["subject_ids"])),
                    relation_ids=tuple(json.loads(row["relation_ids"])),
                    object_ids=tuple(json.loads(row["object_ids"])),
                    fact_class=row.get("fact_class", "main"),
                )
            )
    return facts


def smoke_factset(num_facts: int = 200, vocab_start: int = 10_000) -> tuple[list[InjectedFact], int]:
    facts = []
    eos = vocab_start - 1
    rel = (vocab_start - 2,)
    for i in range(num_facts):
        facts.append(
            InjectedFact(
                fact_id=f"smoke_{i:04d}",
                relation="<rel>",
                subject=f"<s{i}>",
                object=f"<o{i}>",
                subject_ids=(vocab_start + i,),
                relation_ids=rel,
                object_ids=(vocab_start + num_facts + i,),
                fact_class="main",
            )
        )
    return facts, eos
