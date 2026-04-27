# Mission 2 — Stealth Architect starter kit

> AI architects offensive infrastructure; deterministic validators gate every plan.

## Scope (re-read every time you sit down)

This is a **lab exercise**. The starter ships with safe-by-default config and a teardown script. We will refuse to score anything that violates these:

- All ports bind to `127.0.0.1` only. No `0.0.0.0`. No public exposure.
- All containers run on a private docker network with `internal: true` where appropriate.
- Lure copy is generated for **review and analysis only**. Never sent.
- Targets: only domains/IPs you own or have explicit written authorisation for.
- If your tool can be re-pointed at a real target by flipping one flag, you've built it wrong.

The judging panel will refuse to score anything that breaks the above.

## What's in the kit

```
m2/
├── README.md
├── pyproject.toml
├── SPEC.template.md
├── REJECTIONS.template.md
├── teardown.sh                       # always-safe kill switch
├── sandbox/
│   └── docker-compose.yml            # localhost-only nginx redirector + C2 stub
├── validators/
│   ├── compose_policy.py             # deterministic gate: rejects unsafe compose
│   └── lure_schema.py                # pydantic schema for AI-drafted lures
├── prompts/
│   ├── architect.md                  # system prompt for IaC drafter
│   └── lure_variants.md              # system prompt for lure drafter
└── tests/
    ├── __init__.py
    ├── test_compose_policy.py        # passes on safe compose, fails on unsafe
    └── test_lure_schema.py           # passes on valid lure, fails on one with hardcoded URLs
```

## The 98/2 split, made concrete

| Layer | Owner | What |
|---|---|---|
| **Architect prompt** | `prompts/architect.md` | LLM drafts container/redirector configs. |
| **Plan validator** | `validators/compose_policy.py` | Deterministic policy: no public binds, no privileged containers, no host network. |
| **Apply** | `docker compose up -d` | Only after the validator passes. |
| **Lure drafter** | `prompts/lure_variants.md` | LLM generates lure variants. |
| **Lure reviewer** | `validators/lure_schema.py` | Pydantic schema rejects lures missing required fields, with hardcoded URLs, or with risky claims. |
| **Teardown** | `teardown.sh` | One command, always works, no flags. |

## Bootstrap

```bash
cd missions/_starter/m2
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest                         # all tests should pass
docker compose -f sandbox/docker-compose.yml config   # validate
```

## The build loop

1. **You write the SPEC** (5 lines).
2. **You ask Claude to extend `sandbox/docker-compose.yml`** to add the redirector / payload-factory / C2 backend you want.
3. **You run `validators/compose_policy.py sandbox/docker-compose.yml`** — if it fails, log the rejection in `REJECTIONS.md`, ask Claude to fix, repeat.
4. **You ask Claude to draft 3 lure variants** using `prompts/lure_variants.md`.
5. **You run `validators/lure_schema.py`** against the JSON output — same rejection-loop pattern.
6. **You demo the build + the rejection log** at the booth. The rejection log is the prized artefact.

## Anti-patterns we'll dock points for

- AI-generated config applied without the validator running.
- Hardcoded credentials in the compose file (even fake ones).
- Lure copy that names a real organisation by name without consent.
- A C2 service bound to `0.0.0.0` ("for the demo"). Wrong default.
- "The AI told me this was fine." Not a defence — you're the architect.

## Stretch goals

- **Time-bound infra** — add a sidecar that auto-runs `teardown.sh` after N hours.
- **Canary token in lure copy** — a deliberately implausible claim only an AI would generate; show your reviewer catches it.
- **Policy diff view** — when the validator rejects a plan, output the rejected fragment + the policy rule that fired.
