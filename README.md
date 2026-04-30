# DEF CON Asia 2026 — AI & AI Security Kampung

**Dates:** 28–30 April 2026 (Tue–Thu)
**Lead:** Ethan Seow (with Palvinder Singh)
**Convener:** SG Community / Div0 / DCSG1
**Programme owner:** Practical Cyber × C4AIL

## Operating frame

> **The 98/2 Principle** — 98% hardened deterministic software, 2% intelligent AI edge. The critical logic is auditable code. AI handles the fuzzy surface.

Mapped onto Ethan's voice:
- **Intellectual labour** (what AI does): research, drafting, narration, pattern-matching.
- **Accountability labour** (what humans do): decisions, sign-offs, defending the outcome when something breaks.
- **The Translator capability** — the leader who can commission, interrogate, and challenge AI systems without becoming an ML engineer.

> Do **not** use the word *village*. Use *hands-on activities* or *Kampung*.

## Format

Booth-decide. Whole day, every day. Modular content blocks the lead pulls on demand based on who walks up.

## Three Missions (participants pick one)

1. **The Signal Extractor** — SecOps pipeline. Strip 99% noise deterministically; AI narrates anomaly context. Auditable dashboard.
2. **The Stealth Architect** — Offensive infra (redirector, phishing factory, C2 backend). AI architects, controls stay deterministic.
3. **The TDD Speedrun** — Concept → production tool in 30 minutes. Human writes tests, AI writes implementation. 90%+ coverage.

## Two Sharing Sessions (the lead's stage time)

- **A1 — AI Red Teaming: Breaking the Black Box** → `talks/a1-ai-red-teaming.md` ✅
- **A2 — Vibe Coding Live: Architecture over Syntax** → `talks/a2-vibe-coding-live.md` ✅

## Award

**Architect of the Quarter.** Scored on 98/2 split, AI-red-team resilience, real-world SG impact. Rubric: `booth/rubric.md`.

## Related tools

The kampung includes one tool from the wider Practical Cyber stack as a git submodule:

- [`tools/exploit-tool/`](tools/exploit-tool) — single-console pentest platform built on authorization, scope, and audit. Correlates best-of-breed scanners; AI handles triage and reports. Repo: [github.com/practicalcyber/exploit-tool](https://github.com/practicalcyber/exploit-tool).

To pull the submodule when cloning:
```bash
git clone --recursive https://github.com/practicalcyber/defcon-asia-2026
# or, if you've already cloned without --recursive:
git submodule update --init --recursive
```

## Directory layout

```
defcon-asia/
├── README.md                          # this file
├── talks/
│   ├── a1-ai-red-teaming.md           # ✅ full script
│   └── a2-vibe-coding-live.md         # ✅ full script
├── booth/
│   ├── one-pager.md                   # ✅ printable A4 handout
│   └── rubric.md                      # ✅ Architect of the Quarter scorecard
├── missions/
│   ├── m1-signal-extractor.md         # ✅ brief + starter-kit spec
│   ├── m2-stealth-architect.md        # ✅ brief + ethics + starter-kit spec
│   ├── m3-tdd-speedrun.md             # ✅ brief + starter-kit spec
│   ├── _starter/m1/                   # ✅ Signal Extractor scaffold
│   │   ├── filter_engine.py           # rule registry + 1 example rule
│   │   ├── narrator.py                # bounded LLM with pydantic egress schema
│   │   ├── generate_data.py           # synth CloudTrail generator
│   │   ├── data/cloudtrail-sample.jsonl  # 200 events, 3 planted anomalies
│   │   └── tests/test_filter.py       # 1 passing + 1 xfail (their starter task)
│   └── _starter/m3/                   # ✅ three runnable starter kits
│       ├── README.md
│       ├── nric-redactor/             # SPEC + REJECTIONS templates + pyproject + stub + structural test
│       ├── ssh-classifier/            # same shape
│       └── suricata-deduper/          # same shape
└── demos/
    ├── d1-rag-injection/              # ✅ built — Streamlit + Chroma + Anthropic
    │   ├── README.md
    │   ├── app.py / retriever.py / indexer.py / llm.py
    │   ├── reindex.sh
    │   ├── docs/                      # benign baseline (4 .md files)
    │   └── docs_evil/                 # injected version of remote_work_policy.md
    └── d2-safety-bypass/              # ✅ built — multi-provider CLI + runsheet
        ├── README.md
        ├── client.py
        ├── runsheet.example.md        # template (committed)
        └── runsheet.local.md          # actual prompts (gitignored)
```

## Build status (as of 2026-04-27)

| Deliverable | Status | Owner | Next step |
|---|---|---|---|
| A1 talk script | ✅ done | — | rehearse |
| A2 talk script | ✅ done | — | rehearse |
| Booth one-pager | ✅ done | — | print ~40 copies |
| Judging rubric | ✅ done | — | print panel crib cards |
| M1/M2/M3 mission briefs | ✅ done | — | print or QR-code at booth |
| D1 RAG injection demo (code) | ✅ built + indexer verified | Ethan | one rehearsal vs live model |
| D2 safety bypass runsheet | ✅ built + parser verified | Ethan | live-test each section tonight |
| M3 starter kits (NRIC / SSH / Suricata) | ✅ built + verified | — | hand to participants on Day 1 |
| M1 starter kit (Signal Extractor) | ✅ built + verified | — | hand to participants on Day 1 |
| M2 starter kit (Stealth Architect) | ✅ built + verified (15 tests pass) | — | hand to participants on Day 1 |

## Source material

- `/tmp/defcon-asia/SG Community (Div0) (DCSG1) - Activities at AI ／ AI Security.docx` — official mission brief (Apr 2026)
- `/tmp/defcon-asia/SINCON 2025 <> AI Kampung Writeups.docx` — Ethan's prior AI Kampung run (Jun 2025), reference only — do not recycle voice

---
_Last updated: 2026-04-27_
