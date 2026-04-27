"""Headless single-shot runner for D1 — used for rehearsal logging.

Streamlit is for live demos at the booth. This script makes it cheap to run
the same retrieval + LLM call without the UI, so we can capture verdicts.

    python headless_query.py "What are the salaries of the executive team?"
"""
from __future__ import annotations

import sys

from retriever import search
from llm import ask_with_context


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: python headless_query.py <question>")
    query = " ".join(sys.argv[1:])

    chunks = search(query, k=3)
    print(f"--- retrieved {len(chunks)} chunks ---")
    for c in chunks:
        preview = c["text"][:120].replace("\n", " ")
        print(f"  • {c['source']}: {preview}...")
    print()

    print("--- model response ---")
    print(ask_with_context(query, chunks))


if __name__ == "__main__":
    main()
