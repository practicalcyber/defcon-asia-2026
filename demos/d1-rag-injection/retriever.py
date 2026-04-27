"""Chroma retriever. Default embeddings (all-MiniLM-L6-v2)."""
from __future__ import annotations

import chromadb

CHROMA_DIR = ".chroma"
COLLECTION = "policy_docs"


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_or_create_collection(name=COLLECTION)


def search(query: str, k: int = 3) -> list[dict]:
    coll = get_collection()
    res = coll.query(query_texts=[query], n_results=k)
    if not res["documents"] or not res["documents"][0]:
        return []
    return [
        {"text": doc, "source": meta["source"]}
        for doc, meta in zip(res["documents"][0], res["metadatas"][0])
    ]
