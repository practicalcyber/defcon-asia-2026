"""Bounded AI narrator.

The model never sees raw events. It sees a STRUCTURED SUMMARY and produces
a STRUCTURED OUTPUT. Schema enforcement on both sides is the egress filter.

If the model returns prose, malformed JSON, or fields outside the schema,
the call raises. That rejection is the deterministic gate.
"""
from __future__ import annotations

import json
import os
from typing import Literal

from pydantic import BaseModel, Field, ValidationError


# ---------------------------------------------------------------------------
# Input schema — what the deterministic layer hands to the model.
# DO NOT include raw event dicts. Aggregates only.
# ---------------------------------------------------------------------------
class ClusterSummary(BaseModel):
    principal: str
    anomaly_type: str
    rule_ids: list[str]
    event_count: int
    top_actions: list[str] = Field(max_length=10)
    time_window_seconds: int
    severity_hint: Literal["low", "medium", "high", "critical"]


# ---------------------------------------------------------------------------
# Output schema — what we accept back. Anything else: reject.
# ---------------------------------------------------------------------------
class Narration(BaseModel):
    one_line_summary: str = Field(max_length=240)
    suspicion_level: Literal["low", "medium", "high", "critical"]
    indicators: list[str] = Field(max_length=5)
    requires_human_review: bool


SYSTEM_PROMPT = """You are a SOC analyst's assistant. You receive a STRUCTURED summary
of an anomaly cluster (never raw logs). Your job is to write a one-line plain-English
summary, name the suspicion level, list up to 5 indicators that explain WHY this is
suspicious, and decide whether a human should review.

You MUST return valid JSON matching exactly this schema:
{
  "one_line_summary": str (max 240 chars),
  "suspicion_level": "low" | "medium" | "high" | "critical",
  "indicators": [str, ...]  (up to 5),
  "requires_human_review": bool
}

Do not include any text outside the JSON object. No markdown fences. No commentary."""


def narrate(summary: ClusterSummary, model: str | None = None) -> Narration:
    """Send the structured summary, parse + validate the structured response."""
    from anthropic import Anthropic

    model = model or os.environ.get("DEMO_MODEL", "claude-sonnet-4-6")
    client = Anthropic()

    payload = summary.model_dump_json(indent=2)

    resp = client.messages.create(
        model=model,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": payload}],
    )
    raw = resp.content[0].text.strip()

    # Egress filter — strict JSON parse + schema validation
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"narrator returned non-JSON: {raw[:200]!r}") from e

    try:
        return Narration.model_validate(data)
    except ValidationError as e:
        raise ValueError(f"narrator output failed schema validation: {e}") from e
