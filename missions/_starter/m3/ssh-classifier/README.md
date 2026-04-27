# SSH Failed-Login Classifier — starter

**Spec (in 1 sentence):** ingest `auth.log`-style lines (or JSON-formatted equivalents), and for each failed-login event, classify it as `bot-scan` / `targeted-bruteforce` / `stuffing` / `unknown` based on rate, source diversity, and username pattern.

## Tests you'll write (suggested)

1. **Burst from one IP at one user → `targeted-bruteforce`.** Many attempts, narrow source, narrow target.
2. **Spread across many users from rotating IPs → `stuffing`.** Wide source, wide target, low per-pair count.
3. **Scan of common usernames (`root`, `admin`, `oracle`, …) from many IPs → `bot-scan`.** Wide source, narrow common-username target.
4. **Anything that doesn't match the heuristics → `unknown`.** Never `null`, never an exception.
5. **Malformed log lines are skipped with a count, not a crash.** Counter is exposed in the result.

## Anti-patterns we'll dock points for

- AI wrote the tests.
- Test rewritten to make a failing case pass.
- Classifier returns `None` for "unknown" instead of the literal string `"unknown"`.
- Hardcoded thresholds that aren't documented in the SPEC. (We'll ask.)
- Silent skip of malformed lines with no counter — we won't know what was lost.

## Sample data

A tiny fixture lives at `tests/fixtures/auth.log.sample` once you create one. Generate your own to drive your tests — that's part of the deliverable.

## Bootstrap

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
```
