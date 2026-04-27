"""Pydantic schema for AI-drafted lure variants.

The model fills the slots; this code reviews the slots. Anything outside the
schema, or a free-text URL, or a hardcoded organisation name, gets rejected.
"""
from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

URL_PATTERN = re.compile(r"https?://\S+", re.IGNORECASE)
DISALLOWED_REAL_ORGS = {
    # Add real SG orgs you want explicitly disallowed in lure copy.
    # The point: lures must use placeholder/fictional orgs only.
    "SingHealth", "DBS", "OCBC", "UOB", "Singtel", "StarHub", "M1",
    "GovTech", "CSA", "MAS", "SPF",
}


class LureVariant(BaseModel):
    subject: str = Field(min_length=5, max_length=120)
    sender_persona: str = Field(min_length=3, max_length=80,
        description="e.g. 'IT Compliance Unit, Ministry of Manpower'")
    body: str = Field(min_length=50, max_length=4000)
    cta_label: str = Field(min_length=2, max_length=60,
        description="The clickable text only — never a URL")
    plausibility_flags: list[str] = Field(
        min_length=1, max_length=10,
        description="Self-declared deception cues, e.g. 'fake urgency', 'mismatched domain'",
    )
    target_role: str = Field(min_length=3, max_length=80,
        description="e.g. 'IT Manager at SG mid-sized company'")
    is_fictional_target: Literal[True] = True

    @field_validator("body", "subject", "cta_label")
    @classmethod
    def reject_inline_urls(cls, v: str) -> str:
        if URL_PATTERN.search(v):
            raise ValueError("inline URLs are not allowed in lure copy; URLs belong in a separate `cta_url` slot owned by the operator")
        return v

    @field_validator("body", "subject", "sender_persona")
    @classmethod
    def reject_real_org_names(cls, v: str) -> str:
        for org in DISALLOWED_REAL_ORGS:
            if re.search(rf"\b{re.escape(org)}\b", v, re.IGNORECASE):
                raise ValueError(f"real organisation name {org!r} is disallowed in lure copy")
        return v


class LureBatch(BaseModel):
    variants: list[LureVariant] = Field(min_length=1, max_length=10)

    @field_validator("variants")
    @classmethod
    def require_distinct_subjects(cls, v: list[LureVariant]) -> list[LureVariant]:
        subjects = [x.subject.strip().lower() for x in v]
        if len(subjects) != len(set(subjects)):
            raise ValueError("variants must have distinct subject lines")
        return v
