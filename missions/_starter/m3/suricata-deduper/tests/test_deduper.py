"""Test suite for suricata-deduper.

ONE structural test below — keeps pytest green at start.
You write the behavioural tests. Do NOT ask Claude to write them.
"""

import deduper  # noqa: F401


def test_module_imports():
    """Smoke test — module is importable. You write the real tests below."""
    assert deduper is not None


# ---------- YOUR TESTS GO HERE ----------
#
# Suggested coverage (from the brief):
#   1. 3 alerts within 30s, same SID + src/dst         → one cluster, count=3
#   2. Same SID across different src/dst pairs         → separate clusters
#   3. Gap of 61s starts a new cluster
#   4. Malformed JSON lines skipped, counted, logged
#   5. Output stable across runs (sort by first_seen)
