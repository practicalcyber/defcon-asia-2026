"""Tests for filter_engine.

ONE passing + ONE intentionally failing test below — the failing one is your starter task.

You write the rest of the behavioural tests yourself. Do NOT ask Claude to write them.
"""
import json
from pathlib import Path

import pytest

from filter_engine import RULES, RULE_IMPOSSIBLE_REGION, apply_rules

DATA = Path(__file__).parent.parent / "data" / "cloudtrail-sample.jsonl"


def load_events() -> list[dict]:
    return [json.loads(line) for line in DATA.read_text().splitlines() if line.strip()]


# ---------- PASSING TEST (the example) ----------

def test_impossible_region_rule_fires_exactly_once():
    """The dataset contains exactly one impossible-region ConsoleLogin (alice in ap-northeast-1)."""
    events = load_events()
    matches = [ev for ev in events if RULE_IMPOSSIBLE_REGION.predicate(ev)]
    assert len(matches) == 1
    assert matches[0]["userIdentity"]["userName"] == "alice@acme.example"
    assert matches[0]["awsRegion"] == "ap-northeast-1"


# ---------- FAILING TEST (your first task) ----------

@pytest.mark.xfail(reason="You haven't added the root-key-creation rule yet. Remove xfail when you do.", strict=True)
def test_root_access_key_creation_is_caught():
    """Anomaly 3 — root account creates an access key. CRITICAL severity, single event."""
    events = load_events()
    result = apply_rules(events, RULES)
    fired_ids = {rid for _, ids in result.kept for rid in ids}
    assert any(rid.startswith("R003") for rid in fired_ids), \
        "expected a rule with id starting 'R003' to fire on CreateAccessKey by root"


# ---------- YOUR TESTS GO HERE ----------
#
# Suggested coverage (from the brief):
#   - Mass S3 enumeration: 8 enum-style calls within 12s from bob@ should cluster as one anomaly.
#     (Hint: this is an aggregate rule — write a separate windowed test fixture.)
#   - Drop count: routine events should outnumber kept events ~9:1.
#   - Audit trail: every dropped event has a non-empty drop_reason.
#   - Rule isolation: each rule's predicate is pure and side-effect-free.
