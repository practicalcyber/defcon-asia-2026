"""Test suite for nric-redactor.

ONE structural test below — keeps pytest green at start.
You write the behavioural tests. Do NOT ask Claude to write them.
"""

import redactor  # noqa: F401


def test_module_imports():
    """Smoke test — module is importable. You write the real tests below."""
    assert redactor is not None


# ---------- YOUR TESTS GO HERE ----------
#
# Suggested coverage (from the brief):
#   1. Valid NRIC formats are detected and redacted
#   2. Invalid checksums are NOT redacted
#   3. Multiline inputs preserve line breaks
#   4. UTF-8 with non-ASCII content survives the round-trip
#   5. Empty file is handled cleanly
#
# def test_valid_nric_is_redacted(tmp_path):
#     ...
