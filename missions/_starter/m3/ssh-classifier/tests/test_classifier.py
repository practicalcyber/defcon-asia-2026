"""Test suite for ssh-classifier.

ONE structural test below — keeps pytest green at start.
You write the behavioural tests. Do NOT ask Claude to write them.
"""

import classifier  # noqa: F401


def test_module_imports():
    """Smoke test — module is importable. You write the real tests below."""
    assert classifier is not None


# ---------- YOUR TESTS GO HERE ----------
#
# Suggested coverage (from the brief):
#   1. Burst from one IP at one user                  → "targeted-bruteforce"
#   2. Spread across many users from rotating IPs     → "stuffing"
#   3. Scan of common usernames from many IPs         → "bot-scan"
#   4. Pattern that matches none of the above         → "unknown" (never None)
#   5. Malformed lines are skipped, counter exposed
