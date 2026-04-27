"""Deterministic rule engine for the Signal Extractor.

Read this whole file before extending it. It's the scaffold for the 98%.

Pattern:
    - A Rule is (id, predicate, severity, why).
    - apply_rules(events, rules) returns kept events plus the rule_ids that fired
      for each, AND the dropped events with the reason they were dropped.
    - That dropped-events log is the audit trail. Don't lose it.

You write the rules for anomalies 2 and 3 (mass enumeration, root key creation).
Rule for anomaly 1 (impossible region) is provided as an example.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class Rule:
    id: str
    predicate: Callable[[dict], bool]
    severity: str  # "low" | "medium" | "high" | "critical"
    why: str       # human-readable reason this rule exists


@dataclass
class FilterResult:
    kept: list[tuple[dict, list[str]]] = field(default_factory=list)   # (event, rule_ids_that_fired)
    dropped: list[tuple[dict, str]] = field(default_factory=list)      # (event, drop_reason)


# ---------------------------------------------------------------------------
# Example rule — anomaly 1: impossible region for the principal
# ---------------------------------------------------------------------------

# Trivially-baselined "known" regions per principal. In a real pipeline this
# would come from a baselining job; here it's hand-coded so the rule is testable
# in isolation.
KNOWN_REGIONS: dict[str, set[str]] = {
    "alice@acme.example": {"ap-southeast-1"},
    "bob@acme.example": {"ap-southeast-1", "us-east-1"},
    "ci-deployer": {"ap-southeast-1"},
    "root": {"ap-southeast-1"},
}


def _is_impossible_region(event: dict) -> bool:
    if event.get("eventName") != "ConsoleLogin":
        return False
    user = event.get("userIdentity", {}).get("userName")
    region = event.get("awsRegion")
    if not user or not region:
        return False
    known = KNOWN_REGIONS.get(user)
    if known is None:
        return False
    return region not in known


RULE_IMPOSSIBLE_REGION = Rule(
    id="R001-impossible-region",
    predicate=_is_impossible_region,
    severity="high",
    why="ConsoleLogin from a region the principal has never used before",
)


# ---------------------------------------------------------------------------
# YOUR RULES GO HERE
# ---------------------------------------------------------------------------
#
# Anomaly 2 — Mass S3 enumeration
#   Hint: this is an aggregate rule. A single ListBuckets call is normal.
#   You will need a windowed predicate, not a per-event predicate.
#   Consider splitting your engine into per-event rules and per-cluster rules.
#
# Anomaly 3 — Root access-key creation
#   Hint: this is a per-event rule. Look at eventName + userIdentity.type.
#   Severity: critical. Should fire even on a single occurrence.
#
# Add your rules to RULES below.

RULES: list[Rule] = [
    RULE_IMPOSSIBLE_REGION,
    # add your rules here
]


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

def apply_rules(events: list[dict], rules: list[Rule] = RULES) -> FilterResult:
    """Apply per-event rules deterministically. Returns kept + dropped audit log."""
    result = FilterResult()
    for ev in events:
        fired = [r.id for r in rules if r.predicate(ev)]
        if fired:
            result.kept.append((ev, fired))
        else:
            result.dropped.append((ev, "no_rule_fired"))
    return result
