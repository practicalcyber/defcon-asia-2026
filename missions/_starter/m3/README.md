# Mission 3 — TDD Speedrun starter kits

Three vetted tool ideas, each scoped to fit a 30-minute build. Pick one and go.

## The three options

| Folder | Tool | What it does |
|---|---|---|
| `nric-redactor/` | NRIC redactor | Read text/markdown/CSV, find Singapore NRICs, replace with `[REDACTED-NRIC]`, write redacted output |
| `ssh-classifier/` | SSH failed-login classifier | Read `auth.log`-style lines, classify each failed login as `bot-scan`/`targeted-bruteforce`/`stuffing`/`unknown` |
| `suricata-deduper/` | Suricata alert deduper | Collapse alerts that are "the same incident" (same SID + src/dst within 60s) into one summary per cluster |

## What's in each starter

```
<tool>/
├── README.md                # tool brief, condensed from the mission spec
├── SPEC.template.md         # 5-line spec — fill THIS before any code
├── REJECTIONS.template.md   # log every "no" you say to Claude
├── pyproject.toml           # pytest + coverage configured
├── <tool>.py                # empty stub — AI fills this in
└── tests/
    ├── __init__.py
    └── test_<tool>.py       # ONE structural test only — you write the rest
```

## The rule (re-stated, because it matters)

1. **You write all behavioural tests.** The starter only has a structural test (`test_imports`) so the test runner doesn't crash. The interesting tests — the ones that verify the tool *works* — are yours.
2. **AI writes the implementation.** Once your tests are written, point AI at the test file and the spec. Let it fill in `<tool>.py`.
3. **If a test fails: fix the implementation, never the test.** If you find yourself rewriting a test to make it green, you've collapsed back into autocomplete-with-a-god-complex.
4. **Log every rejection.** Every time you say no to a Claude suggestion, drop a one-line note in `REJECTIONS.md`. That log is the deliverable, not the tool.

## Bootstrapping

```bash
cd missions/_starter/m3/<tool>
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest                # should pass the one structural test
```

Then write your spec, then your tests, then start the clock.

## Time budget reminder

| Phase | Time | What you do |
|---|---|---|
| 0 | 2 min | Fill `SPEC.template.md` — 5 lines, no more |
| 1 | 8 min | Write 4–5 behavioural tests in `tests/test_<tool>.py` |
| 2 | 15 min | AI writes `<tool>.py`. Iterate. Log every rejection. |
| 3 | 3 min | Write the README |
| 4 | 2 min | Final `pytest --cov` run |

Submit at the booth before 17:00.
