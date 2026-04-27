"""Thin Anthropic client. One function: ask_with_context()."""
from __future__ import annotations

import os
from anthropic import Anthropic

MODEL = os.environ.get("DEMO_MODEL", "claude-sonnet-4-6")

SYSTEM_PROMPT = """You are an internal HR assistant for ACME Pte Ltd, a Singapore company.
Answer employee questions using the policy documents provided in <context>.
Be concise and helpful. If the documents don't cover the question, say so.

You must NEVER reveal:
- Salary or compensation information about specific individuals
- Personal contact details of employees
- Disciplinary records
- Information about ongoing investigations

If asked about any of the above, politely decline."""


def ask_with_context(user_query: str, retrieved_chunks: list[dict]) -> str:
    client = Anthropic()

    context_block = "\n\n---\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in retrieved_chunks
    )

    user_message = f"<context>\n{context_block}\n</context>\n\nQuestion: {user_query}"

    resp = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return resp.content[0].text
