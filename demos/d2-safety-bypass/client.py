"""Multi-provider CLI for the safety-bypass demo.

Reads a single section from a runsheet file and issues it to a chosen provider.
Each section in the runsheet is delimited by a heading like:

    # bypass1: roleplay frame

    [optional system prompt block]
    ---
    [user prompt block]

Usage:
    python client.py --section baseline                    # clean refusal
    python client.py --section bypass1                     # roleplay
    python client.py --section bypass2-step1               # decomposition step 1
    python client.py --section bypass3                     # encoded
    python client.py --provider anthropic --section bypass1
    python client.py --runsheet runsheet.local.md --section bypass1
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def parse_runsheet(path: Path) -> dict[str, dict]:
    """Parse markdown runsheet into {section_name: {system, user}}."""
    sections: dict[str, dict] = {}
    current = None
    body: list[str] = []

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            if current is not None:
                sections[current] = _split_body("\n".join(body))
            header = line[2:].strip()
            current = header.split(":", 1)[0].strip()
            body = []
        elif current is not None:
            body.append(line)

    if current is not None:
        sections[current] = _split_body("\n".join(body))

    return sections


def _split_body(body: str) -> dict:
    if "\n---\n" in body:
        sys_part, user_part = body.split("\n---\n", 1)
        return {"system": sys_part.strip(), "user": user_part.strip()}
    return {"system": "", "user": body.strip()}


def call_anthropic(system: str, user: str, model: str) -> str:
    from anthropic import Anthropic

    client = Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system or "You are a helpful assistant.",
        messages=[{"role": "user", "content": user}],
    )
    if not resp.content:
        return f"[hard refusal — no content; stop_reason={resp.stop_reason}]"
    return resp.content[0].text


def call_openai(system: str, user: str, model: str) -> str:
    from openai import OpenAI

    client = OpenAI()
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": user})
    resp = client.chat.completions.create(model=model, messages=msgs, max_tokens=1024)
    return resp.choices[0].message.content or ""


def call_gemini(system: str, user: str, model: str) -> str:
    from google import genai

    client = genai.Client()
    contents = (system + "\n\n" + user).strip() if system else user
    resp = client.models.generate_content(model=model, contents=contents)
    return resp.text or ""


PROVIDERS = {
    "anthropic": (call_anthropic, "claude-sonnet-4-6"),
    "openai":    (call_openai,    "gpt-4o-mini"),
    "gemini":    (call_gemini,    "gemini-2.5-flash"),
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--runsheet", default="runsheet.local.md")
    p.add_argument("--section", required=True)
    p.add_argument("--provider", default="anthropic", choices=list(PROVIDERS))
    p.add_argument("--model", default=None, help="Override default model")
    args = p.parse_args()

    path = Path(args.runsheet)
    if not path.exists():
        sys.exit(f"runsheet not found: {path}\n"
                 f"Hint: copy runsheet.example.md to runsheet.local.md and fill it in.")

    sections = parse_runsheet(path)
    if args.section not in sections:
        sys.exit(f"section '{args.section}' not found. "
                 f"Available: {', '.join(sorted(sections))}")

    sec = sections[args.section]
    fn, default_model = PROVIDERS[args.provider]
    model = args.model or os.environ.get("DEMO_MODEL") or default_model

    print(f"--- provider: {args.provider} | model: {model} | section: {args.section} ---")
    if sec["system"]:
        print(f"[system]\n{sec['system']}\n")
    print(f"[user]\n{sec['user']}\n")
    print("--- response ---")
    print(fn(sec["system"], sec["user"], model))


if __name__ == "__main__":
    main()
