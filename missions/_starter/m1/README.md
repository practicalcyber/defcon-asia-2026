# Mission 1 — Signal Extractor starter kit

> Build a pipeline that strips 99% noise deterministically and uses AI to narrate what's left.

## What's in the kit

```
m1/
├── README.md                  # this file
├── pyproject.toml             # pytest + coverage + pydantic + anthropic
├── SPEC.template.md           # 5-line spec — fill before coding
├── REJECTIONS.template.md     # rejection log (≥3 entries to win the tiebreaker)
├── filter_engine.py           # rule-based deterministic filter (read this — it's your scaffold)
├── narrator.py                # bounded AI narrator with pydantic output schema
├── data/
│   └── cloudtrail-sample.jsonl  # ~200 synth events, 3 planted anomalies
└── tests/
    ├── __init__.py
    └── test_filter.py         # one passing test, one failing test you fix
```

## The three planted anomalies

The sample dataset contains three anomalies. Your pipeline should surface all three. They are:

1. **Impossible-region login.** A `ConsoleLogin` event from a region the principal has never used before.
2. **Mass S3 enumeration.** A burst of `ListBuckets` / `GetBucketAcl` calls in a tight window from one principal.
3. **Root access-key creation.** The root account creates a new access key — a high-severity event that should never be benign.

A correct pipeline drops the noise (~95% of events are routine reads from CI/CD), keeps the three above, and lets the AI narrate *why* each cluster is suspicious.

## The 98/2 split, made concrete

| Layer | Owner | What |
|---|---|---|
| **Filter** | `filter_engine.py` | Deterministic rules, unit-tested. AI never decides what's suspicious. |
| **Cluster** | _your code_ | Group anomalies by principal + time window. Exact joins, no fuzzy logic. |
| **Narrate** | `narrator.py` | LLM gets a STRUCTURED summary, not raw logs. Returns pydantic-validated output. |
| **Egress** | `narrator.py` | Output schema enforced. If the model returns prose where JSON is required, we reject. |

## Bootstrap

```bash
cd missions/_starter/m1
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest                 # one test passes, one fails — fix the failing one
```

Then write your `SPEC.md`, extend `filter_engine.py` with rules for the other two anomalies, write tests for them, and wire it together with `narrator.py`.

## Anti-patterns we'll dock points for

- **AI in the filter.** The deterministic 98% is the *point*. If your filter calls the model, you've lost the mission.
- **Raw logs in the prompt.** PII, prompt injection, cost. Pass the model `{entity, count, top_actions, time_window, severity_hint}`.
- **Schema not enforced.** If `narrator.py` returns whatever the model wrote, the egress filter is theatre. Use pydantic. Validate. Reject.
- **No "why was this dropped?" view.** The audit trail is the product. We need to see which rule dropped which event.
