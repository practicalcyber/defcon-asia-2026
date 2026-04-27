# Mission 3 — The TDD Speedrun

> _Prove that AI makes us better engineers, not just faster typists._

**Track:** Software Engineering
**Time budget:** **30 minutes**, hard cap
**Award criteria mapping:** strong on **98/2 Split** and the rejection-log tiebreaker. Impact must be claimed in one sentence.

---

## The challenge

Take a complex security utility idea and go from **"Concept" to "Production-Ready Tool" in 30 minutes**.

**The Rule** — non-negotiable:

1. **You write the tests** (the deterministic 98%).
2. **AI writes the implementation** (the 2% — though here it's more like 70% of the line count, because boilerplate dominates).
3. If the AI hallucinates logic that breaks a test, **you architect the fix** — you do not let the AI rewrite the test to make it pass. That's the failure mode this whole exercise exists to prevent.

Targets:
- **90%+ code coverage**.
- **Full README** (install + usage + 1 example).
- **Working binary or runnable script.**
- **Rejection log** with at least 3 entries.

---

## Why this mission matters

Most engineers using AI today are letting AI write **both** the test and the implementation. That's not engineering — that's autocomplete with a god complex. You can ship a tool that has 100% passing tests and 0% correctness, because the tests were written to match what the AI happened to produce.

The TDD discipline inverts this: **the test is the spec, written by the human, before the AI sees the problem.** When AI writes implementation that fails the test, the failure is informative. When AI writes implementation that passes a test it also wrote, the pass is meaningless.

That is the whole lesson, in 30 minutes.

---

## Suggested ideas (pick or invent)

We've vetted these for 30-minute scope. The starter kit has skeletons for all three.

### A. NRIC redactor
- **Spec:** read a directory of `.txt`/`.md`/`.csv`, find Singapore NRIC numbers (S/T/F/G + 7 digits + checksum), replace with `[REDACTED-NRIC]`, write to output dir.
- **Tests you'll write:**
  1. Valid NRIC formats are detected (S1234567A and 6 other variants).
  2. Invalid checksums are **not** redacted (false-positive guard).
  3. Multiline inputs preserve line breaks.
  4. UTF-8 with non-ASCII content survives the round-trip.
  5. Empty file is handled cleanly.

### B. Failed-SSH classifier
- **Spec:** ingest `auth.log`-style lines, classify each failed login as `bot-scan` / `targeted-bruteforce` / `stuffing` / `unknown` based on rate, source diversity, username pattern.
- **Tests you'll write:**
  1. A burst from one IP at one user is `targeted-bruteforce`.
  2. A spread across many users from rotating IPs is `stuffing`.
  3. A scan of common usernames from many IPs is `bot-scan`.
  4. Anything else is `unknown` (and never `null` or thrown).
  5. Malformed lines are skipped with a count, not crash.

### C. Suricata alert deduper
- **Spec:** read JSON-lines Suricata alerts, collapse alerts that are "the same incident" (same SID + same src/dst pair + within 60s), output one summary per cluster.
- **Tests you'll write:**
  1. Three alerts in 30s collapse to one.
  2. Same SID across different src-dst pairs do **not** collapse.
  3. Window boundary (61s gap) does not collapse.
  4. Schema-invalid JSON is skipped, counted, logged.
  5. Output is stable across runs (sorted by first-seen).

---

## The 30-minute clock

| Phase | Time | What you do |
|---|---|---|
| 0 | 2 min | Pick a tool. Open `SPEC.md`, write 5 lines: input / output / one rule / one anti-rule / one example. |
| 1 | 8 min | Write the tests. **Do not let AI write tests.** This is the bit that's yours. |
| 2 | 15 min | Let AI write the implementation. Run tests. Iterate. **Every rejection goes into the log.** |
| 3 | 3 min | Write the README. AI can draft; you review. |
| 4 | 2 min | Final test run with coverage. Tag and submit. |

If you blow the budget, that's a result too — submit what you have. We'd rather see an honest 22-minute build than a 30-minute build with smuggled help.

---

## Anti-patterns (we will dock points for, hard)

- **AI wrote any of the tests.** Disqualifying. The tests are your spec; outsourcing them is outsourcing your judgement.
- **You let AI rewrite a test to make it pass.** Disqualifying. If a test fails, the implementation is wrong, not the test.
- **Coverage gaming** — `# pragma: no cover` on the interesting bits to inflate the percentage. We read.
- **No rejection log.** You'll be tied with someone who has one, and they'll win.
- **One-shot prompt** that produced everything. Show the iteration. The iteration is the artefact.

---

## What we're really judging

Not the tool. The **rejection log**.

The deliverable is evidence that you said no, with reasoning, at least three times. A great rejection log entry tells me:

> `00:11:42` — Claude proposed using `re.findall(r'[STFG]\d{7}[A-Z]', text)`. Rejected: doesn't validate the checksum, will redact valid-looking but invalid IDs and miss the discrimination value of "this is a real NRIC pattern not a CAPTCHA." Replaced with explicit checksum check.

That entry shows me you understood the *purpose* of the regex, not just the syntax. That's what we're paying you for in 2026.

---

## Submission

1. Repo (public preferred) or tarball.
2. **`SPEC.md`** — the 5-line spec you wrote at minute 0.
3. **`REJECTIONS.md`** — your rejection log, ≥3 entries.
4. Test suite + coverage report.
5. README with install + usage.
6. Be ready to demo: 5-min walkthrough including a live test run.

---

## Starter kit — `_starter/`

```
_starter/
├── nric-redactor/
│   ├── SPEC.template.md
│   ├── tests/                       # one example test, you write the rest
│   ├── pyproject.toml               # pytest + coverage configured
│   └── REJECTIONS.template.md
├── ssh-classifier/
│   └── (same structure)
├── suricata-deduper/
│   └── (same structure)
└── README.md                        # how to use the starters
```

---
_Mission brief — DEF CON Asia AI Kampung — last updated 2026-04-27._
