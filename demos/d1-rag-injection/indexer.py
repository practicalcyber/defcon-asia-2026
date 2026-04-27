"""Reindex a directory of markdown docs into Chroma.

Usage:
    python indexer.py docs/         # index benign docs
    python indexer.py docs_evil/    # index poisoned doc + benign filler
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import chromadb

CHROMA_DIR = ".chroma"
COLLECTION = "policy_docs"
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 200


def chunk(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    if len(text) <= size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + size])
        start += size - overlap
    return chunks


def reindex(docs_dir: Path, also_include: Path | None = None) -> None:
    shutil.rmtree(CHROMA_DIR, ignore_errors=True)
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    coll = client.get_or_create_collection(name=COLLECTION)

    sources: list[Path] = sorted(docs_dir.glob("*.md"))

    if also_include:
        for p in sorted(also_include.glob("*.md")):
            if not any(s.name == p.name for s in sources):
                sources.append(p)

    docs, metas, ids = [], [], []
    for path in sources:
        text = path.read_text(encoding="utf-8")
        for i, c in enumerate(chunk(text)):
            docs.append(c)
            metas.append({"source": path.name})
            ids.append(f"{path.name}::{i}")

    coll.add(documents=docs, metadatas=metas, ids=ids)
    print(f"Indexed {len(docs)} chunks from {len(sources)} files into {CHROMA_DIR}/")
    for s in sources:
        print(f"  - {s}")


if __name__ == "__main__":
    primary = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("docs")
    fallback = Path("docs") if primary.name == "docs_evil" else None
    reindex(primary, also_include=fallback)
