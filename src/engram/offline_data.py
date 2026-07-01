from __future__ import annotations

import csv
import glob
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class ShardRecord:
    path: str
    token_count: int
    first_doc_id: str
    last_doc_id: str


def snapshot_download_parquet(
    repo_id: str,
    local_dir: str | Path,
    allow_patterns: tuple[str, ...] = ("*.parquet", "**/*.parquet"),
    repo_type: str = "dataset",
) -> str:
    os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")
    from huggingface_hub import snapshot_download

    return snapshot_download(
        repo_id=repo_id,
        repo_type=repo_type,
        local_dir=str(local_dir),
        allow_patterns=list(allow_patterns),
        resume_download=True,
    )


def iter_parquet_texts(paths: Iterable[str | Path], text_column: str = "text", id_column: str | None = None):
    import pyarrow.parquet as pq

    for parquet_path in paths:
        parquet_path = Path(parquet_path)
        table = pq.read_table(parquet_path, columns=[c for c in (id_column, text_column) if c])
        texts = table[text_column].to_pylist()
        ids = table[id_column].to_pylist() if id_column and id_column in table.column_names else None
        for row_idx, text in enumerate(texts):
            if text is None:
                continue
            doc_id = str(ids[row_idx]) if ids is not None else f"{parquet_path.name}:{row_idx}"
            yield doc_id, str(text), str(parquet_path), row_idx


def write_shard(path: Path, tokens: list[int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.asarray(tokens, dtype=np.uint32).tofile(path)


def tokenize_local_parquet(
    parquet_glob: str,
    output_dir: str | Path,
    tokenizer_name: str = "deepseek-ai/DeepSeek-V3",
    text_column: str = "text",
    id_column: str | None = None,
    tokens_per_shard: int = 100_000_000,
    max_tokens: int | None = None,
    eos_token_id: int | None = None,
    batch_docs: int = 256,
) -> dict[str, object]:
    from transformers import AutoTokenizer

    paths = sorted(glob.glob(parquet_glob))
    if not paths:
        raise FileNotFoundError(f"no parquet files matched {parquet_glob!r}")
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(tokenizer_name, trust_remote_code=True)
    eos = eos_token_id if eos_token_id is not None else tok.eos_token_id
    if eos is None:
        eos = tok.convert_tokens_to_ids(tok.eos_token or "<｜end▁of▁sentence｜>")

    shard_manifest_path = out / "shards.csv"
    doc_manifest_path = out / "docs.jsonl"
    shard_records: list[ShardRecord] = []
    shard_tokens: list[int] = []
    shard_doc_start: str | None = None
    total_tokens = 0
    doc_count = 0
    shard_idx = 0
    reached_limit = False

    def flush(last_doc_id: str) -> None:
        nonlocal shard_tokens, shard_doc_start, shard_idx
        if not shard_tokens:
            return
        path = out / f"shard_{shard_idx:06d}.u32"
        write_shard(path, shard_tokens)
        shard_records.append(
            ShardRecord(
                path=str(path),
                token_count=len(shard_tokens),
                first_doc_id=shard_doc_start or "",
                last_doc_id=last_doc_id,
            )
        )
        shard_idx += 1
        shard_tokens = []
        shard_doc_start = None

    with doc_manifest_path.open("w") as doc_f:
        batch = []
        for doc_id, text, source_path, row_idx in iter_parquet_texts(paths, text_column=text_column, id_column=id_column):
            if reached_limit:
                break
            batch.append((doc_id, text, source_path, row_idx))
            if len(batch) < batch_docs:
                continue
            encoded = tok([x[1] for x in batch], add_special_tokens=False)["input_ids"]
            for (doc_id, _, source_path, row_idx), ids in zip(batch, encoded):
                if shard_doc_start is None:
                    shard_doc_start = doc_id
                start = total_tokens
                doc_tokens = list(ids) + [int(eos)]
                if max_tokens is not None and total_tokens + len(doc_tokens) > max_tokens:
                    keep = max_tokens - total_tokens
                    if keep <= 0:
                        flush(doc_id)
                        reached_limit = True
                        break
                    doc_tokens = doc_tokens[:keep]
                shard_tokens.extend(doc_tokens)
                total_tokens += len(doc_tokens)
                doc_count += 1
                doc_f.write(
                    json.dumps(
                        {
                            "doc_id": doc_id,
                            "source_path": source_path,
                            "row_idx": row_idx,
                            "start_token": start,
                            "end_token": total_tokens,
                        }
                    )
                    + "\n"
                )
                while len(shard_tokens) >= tokens_per_shard:
                    chunk = shard_tokens[:tokens_per_shard]
                    shard_tokens = shard_tokens[tokens_per_shard:]
                    old_start = shard_doc_start or doc_id
                    path = out / f"shard_{shard_idx:06d}.u32"
                    write_shard(path, chunk)
                    shard_records.append(ShardRecord(str(path), len(chunk), old_start, doc_id))
                    shard_idx += 1
                    shard_doc_start = doc_id if shard_tokens else None
                if max_tokens is not None and total_tokens >= max_tokens:
                    flush(doc_id)
                    reached_limit = True
                    break
            batch = []
        if batch and not reached_limit:
            encoded = tok([x[1] for x in batch], add_special_tokens=False)["input_ids"]
            for (doc_id, _, source_path, row_idx), ids in zip(batch, encoded):
                if shard_doc_start is None:
                    shard_doc_start = doc_id
                start = total_tokens
                doc_tokens = list(ids) + [int(eos)]
                shard_tokens.extend(doc_tokens)
                total_tokens += len(doc_tokens)
                doc_count += 1
                doc_f.write(
                    json.dumps(
                        {
                            "doc_id": doc_id,
                            "source_path": source_path,
                            "row_idx": row_idx,
                            "start_token": start,
                            "end_token": total_tokens,
                        }
                    )
                    + "\n"
                )
        flush(str(doc_count - 1))

    with shard_manifest_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["path", "token_count", "first_doc_id", "last_doc_id"])
        w.writeheader()
        for rec in shard_records:
            w.writerow(rec.__dict__)
    shard_list_path = out / "shards.txt"
    shard_list_path.write_text("\n".join(rec.path for rec in shard_records) + ("\n" if shard_records else ""))
    summary = {
        "parquet_glob": parquet_glob,
        "output_dir": str(out),
        "tokenizer": tokenizer_name,
        "dtype": "uint32",
        "doc_count": doc_count,
        "token_count": total_tokens,
        "shard_count": len(shard_records),
        "shard_manifest": str(shard_manifest_path),
        "token_list": str(shard_list_path),
        "doc_manifest": str(doc_manifest_path),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary


def assert_data_gate(output_dir: str | Path, min_tokens: int = 200_000_000_000) -> dict[str, object]:
    out = Path(output_dir)
    summary_path = out / "summary.json"
    shard_manifest = out / "shards.csv"
    doc_manifest = out / "docs.jsonl"
    if not summary_path.exists():
        raise FileNotFoundError(summary_path)
    if not shard_manifest.exists():
        raise FileNotFoundError(shard_manifest)
    if not doc_manifest.exists():
        raise FileNotFoundError(doc_manifest)
    summary = json.loads(summary_path.read_text())
    token_count = int(summary.get("token_count", 0))
    doc_count = int(summary.get("doc_count", 0))
    shard_token_sum = 0
    shard_count = 0
    with shard_manifest.open(newline="") as f:
        for row in csv.DictReader(f):
            shard_count += 1
            tokens = int(row["token_count"])
            shard_token_sum += tokens
            shard_path = Path(row["path"])
            if not shard_path.exists():
                raise FileNotFoundError(shard_path)
            expected_bytes = tokens * np.dtype(np.uint32).itemsize
            actual_bytes = shard_path.stat().st_size
            if actual_bytes != expected_bytes:
                raise RuntimeError(
                    f"data gate failed: shard size mismatch for {shard_path}: "
                    f"bytes={actual_bytes} expected={expected_bytes}"
                )
    doc_manifest_lines = sum(1 for line in doc_manifest.open() if line.strip())
    if token_count < min_tokens:
        raise RuntimeError(f"data gate failed: token_count={token_count} < min_tokens={min_tokens}")
    if doc_count <= 0:
        raise RuntimeError("data gate failed: doc manifest is empty")
    if shard_count <= 0:
        raise RuntimeError("data gate failed: no shards in manifest")
    if shard_token_sum != token_count:
        raise RuntimeError(f"data gate failed: shard token sum {shard_token_sum} != summary token_count {token_count}")
    if doc_manifest_lines != doc_count:
        raise RuntimeError(f"data gate failed: doc manifest lines {doc_manifest_lines} != summary doc_count {doc_count}")
    summary["gate_min_tokens"] = min_tokens
    summary["gate_passed"] = True
    summary["gate_shard_token_sum"] = shard_token_sum
    summary["gate_doc_manifest_lines"] = doc_manifest_lines
    return summary
