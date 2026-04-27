# Mission 2 — The Stealth Architect

> _Automate the logistics so the human can focus on the tradecraft._

**Track:** Offensive Security
**Time budget:** half day (max 4h)
**Award criteria mapping:** strong on **Resilience** (your own infra has to survive its own probes) and **98/2 Split**.

---

## The challenge

Use AI agents to architect and deploy a piece of **hardened offensive infrastructure**. Pick one:

- A multi-tier redirector setup (CDN-fronted, geo-restricted, with traffic shaping).
- A localised phishing payload factory (SG-context lures, branded templates, A/B variant generation).
- A custom C2 backend (HTTP/HTTPS comms with jittered beaconing, structured tasking).

The infrastructure must follow **Singapore-specific contextual cues** — spoofing local corporate intranets, MOM/IRAS/ICA-style notifications, MyInfo-adjacent flows, .com.sg domain conventions.

Success metric: **functional, terraformed infrastructure** where the security controls (encryption, IP whitelisting, scoping, kill-switch) are 100% deterministic code. The AI architects, suggests, drafts copy. The AI does **not** decide what the access boundary looks like.

---

## Scope and ethics — non-negotiable

This is a **lab exercise**. Read this twice.

- Targets: only domains/IPs you own or have explicit written authorisation for. No exceptions.
- The redirector must default to a **localhost-only** allow-list. You demo the principle; you do not point it at the internet.
- Phishing copy is generated for **review and analysis only**. We will not score teams who actually send anything.
- C2 beacons run between containers on the same host. Do not bind to public interfaces.
- If your tool can be re-pointed at a real target with a single flag, **you've built it wrong**. Make the safe-by-default the only easy default.

The judging panel will refuse to score any submission that violates the above. We're not playing.

---

## What "98/2" means here

| Layer | Deterministic 98% | AI 2% |
|---|---|---|
| IaC | Terraform + provider versioning, state locking, module boundaries | "Suggest a redirector layout for these constraints" |
| Network controls | Hard-coded allow-lists, security groups, mTLS configs | — |
| Encryption | Pinned ciphers, cert rotation logic, KMS-managed keys | — |
| Lure copy | — | "Draft 3 variants in SG corporate tone, flag risky claims" |
| Infrastructure naming / decoration | — | "Suggest plausible domain names, internal hostname conventions" |
| Kill switch | Hard-coded teardown script with timeout | — |

The model **drafts**; deterministic code **gates**. If the AI suggests opening port 22 to 0.0.0.0/0, your Terraform validator rejects the plan. That rejection is the deliverable.

---

## Recommended architecture

```
┌─────────────────┐
│  AI architect   │  generates IaC drafts, lure variants, naming
│  (Claude/Bolt)  │
└────────┬────────┘
         │ proposed plan (text)
         v
┌─────────────────┐    ┌─────────────────┐    ┌──────────────────┐
│  Plan validator │ -> │  Terraform      │ -> │  Localhost-only  │
│  (deterministic │    │  apply          │    │  redirector +    │
│  policy checks) │    │  (with locks)   │    │  C2 sandbox      │
└─────────────────┘    └─────────────────┘    └──────────────────┘
         │
         v (rejected plans)
┌─────────────────┐
│  Rejection log  │  ← THIS is the artefact we judge
└─────────────────┘
```

Three rules from me (the lead):

1. **Validators run before Terraform.** Use OPA, Checkov, tfsec, or hand-rolled — but the gate is deterministic policy, not "trust the model."
2. **Lures are generated to a schema.** `{subject, body, sender_persona, plausibility_flags}`. The model fills the slots; your code reviews the slots.
3. **Everything in containers.** No host-level binding. No public DNS. The judging panel needs to see the containment.

---

## Anti-patterns (we will dock points for)

- AI-generated Terraform applied directly without `terraform plan` review on screen.
- Hardcoded credentials in the IaC. (Even fake ones — that's how real ones leak.)
- Lure copy that targets a real organisation by name without consent.
- A C2 server bound to `0.0.0.0`. Demo or not, that's the wrong default.
- "The AI told me this was fine." Not a defence. **You** are the architect.

---

## Stretch goals

- Add a **canary token** to your phishing lure copy — a deliberately implausible claim that only an AI would generate. Show me where your deterministic check catches it.
- Add a **policy diff view**: when the AI proposes a plan that would have opened a hole, show the rejected diff and the policy rule that fired.
- Add **time-bound infra** — Terraform variable that auto-destroys after N hours. Default: 4 hours. The blast radius is bounded by code, not promise.

---

## Submission

1. Source on GitHub (public) — IaC, validators, lure schema, README.
2. Live demo: you propose a tool change, AI drafts, validator runs, Terraform plans, you teardown — all on screen.
3. **Rejection log** of policy violations the validator caught (this is the prized artefact).
4. Statement of authorisation: one paragraph confirming you own / have permission for any domain or IP touched.

---

## Starter kit — `_starter/`

```
_starter/
├── terraform/
│   ├── redirector/                 # localhost-only nginx + Caddy front
│   ├── c2-sandbox/                 # docker-compose, two containers
│   └── modules/                    # reusable bits, version-pinned
├── validators/
│   ├── opa-policies/               # rego rules — public CIDR, port 22, etc.
│   └── lure_schema.py              # pydantic schema for lure variants
├── prompts/
│   ├── architect.md                # system prompt for the IaC drafter
│   └── lure_variants.md            # system prompt for lure generation
├── teardown.sh                     # always-safe kill-switch
├── SPEC.template.md
└── README.md
```

---
_Mission brief — DEF CON Asia AI Kampung — last updated 2026-04-27._
