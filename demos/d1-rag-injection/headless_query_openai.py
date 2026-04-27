"""Same as headless_query.py, but routes to OpenAI gpt-4o-mini.

Used to compare cross-provider robustness to RAG injection.
"""
from __future__ import annotations

import os
import sys

from openai import OpenAI
from retriever import search
from llm import SYSTEM_PROMPT


def ask_openai(query: str, chunks: list[dict]) -> str:
    client = OpenAI()
    context_block = "\n\n---\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    )
    user_message = f"<context>\n{context_block}\n</context>\n\nQuestion: {query}"
    resp = client.chat.completions.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        max_tokens=1024,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )
    return resp.choices[0].message.content or ""


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: python headless_query_openai.py <question>")
    query = " ".join(sys.argv[1:])
    chunks = search(query, k=3)
    print(f"--- retrieved {len(chunks)} chunks ---")
    for c in chunks:
        preview = c["text"][:120].replace("\n", " ")
        print(f"  • {c['source']}: {preview}...")
    print()
    print("--- model response ---")
    print(ask_openai(query, chunks))


if __name__ == "__main__":
    main()
