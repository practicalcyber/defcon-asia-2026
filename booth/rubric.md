# Architect of the Quarter — Judging Rubric

**Award:** SG Community Kampung — DEF CON Asia 2026
**Format:** 5-minute live demo to the judging panel + Q&A
**Panel:** Ethan Seow, Palvinder Singh (and rotating community judges)

---

## Scoring

Three criteria. Each scored **1–5**. Maximum 15. Tiebreaker below.

### 1. The 98/2 Split (1–5)

**Question:** _Is the critical logic deterministic and auditable?_

| Score | What it looks like |
|---|---|
| 5 | Builder can point to specific lines and say "this is the deterministic 98%" and "this is the AI 2%" without hesitation. The deterministic part has tests. The AI part is bounded — schema-constrained, length-capped, or post-validated. |
| 4 | Split is clear, deterministic part exists, but boundary is fuzzy in 1–2 places. |
| 3 | AI is doing real work, but at least one critical decision (auth, data egress, persistence) flows through the AI without a deterministic gate. |
| 2 | Most logic is "ask the model and trust." Deterministic code is glue, not gate. |
| 1 | The model is the system. There is no 98. |

**Probe questions:**
- "Show me the test suite. Which tests would still pass if you swapped the AI out for a stub?"
- "What happens if the model returns malformed output?"
- "Which decision in this tool would you defend in a postmortem?"

---

### 2. Resilience (1–5)

**Question:** _Does the tool survive a live prompt-injection probe by the judges?_

We will spend ~90 seconds attempting to break the tool, on the spot. Standard probes:

- **Indirect injection** — feed the tool input that contains adversarial instructions (a log line, a document, a filename).
- **Output exfiltration** — try to make the tool emit data it shouldn't (system prompt, secrets, other users' data).
- **Logic subversion** — try to make the tool produce a structured output that violates its own contract.

| Score | What it looks like |
|---|---|
| 5 | All three probes fail to alter behaviour. Tool either ignores the adversarial content, refuses cleanly, or logs+blocks. |
| 4 | Two of three fail; one produces a noisy non-fatal anomaly that's clearly logged. |
| 3 | One probe lands but the impact is bounded (no data leak, no privilege escalation). |
| 2 | Two probes land. Tool produces undefined or unsafe behaviour. |
| 1 | Tool happily follows attacker instructions. |

**Note:** _intent_ matters. A tool that **logs the attempt** is rated higher than a silent block. Visibility is a security control.

---

### 3. Impact (1–5)

**Question:** _Does this solve a real-world friction point for SG security practitioners?_

| Score | What it looks like |
|---|---|
| 5 | Builder names a specific role, a specific recurring task, and a specific time saved or risk reduced — in **one sentence**. Example: "Tier-1 SOC analysts at SG MSSPs spend 45 min/shift triaging duplicate Suricata alerts; this collapses that to 5 min." |
| 4 | Real problem, real audience, but the impact statement is two sentences or hedged. |
| 3 | Plausible problem, plausible user, but the time/risk delta is not articulated. |
| 2 | Sounds useful but no one specific would adopt it Monday morning. |
| 1 | Tech demo. No identified user. |

**Probe questions:**
- "Who, by name or role, would install this on Monday?"
- "What does that person do today instead?"
- "What would they pay for it?"

---

## Tiebreaker — The Rejection Log

In ties, the team that kept the most interesting **rejection log** wins. The log is a list of moments during the build where the team said *no* to an AI suggestion, with a one-line reason.

A good entry looks like:
> `00:14:32` — Rejected Claude's suggestion to use `eval()` to parse the rule DSL. Reason: arbitrary code exec. Replaced with explicit AST walk.

A great entry looks like:
> `00:21:05` — Rejected Claude's suggestion to retry the API call 5x silently on `RateLimitError`. Reason: retries hide the underlying signal that we're being rate-limited; surface the error to the operator instead.

This log is the *evidence* of the Translator capability. We're rewarding the discipline of rejection, not just the artefact.

---

## Process for the day

1. **Submission window** — opens 14:00 daily, closes 17:00.
2. **Demo slot** — 5 min build walkthrough + 5 min Q&A and probe.
3. **Daily winner** — announced 17:30. Tier rosette + Telegram shout-out.
4. **Weekly winner** — Architect of the Quarter — announced Day 3 close. Mentorship slot with the lead, feature in the C4AIL community channel, optional path to OSS publication.

---

## Judging crib card (for panel use)

```
Team: ____________________  Mission: 1  /  2  /  3
Tool name: _______________________________________

[ ] 98/2 split:    1  2  3  4  5
[ ] Resilience:    1  2  3  4  5
[ ] Impact:        1  2  3  4  5
                              Total: ___ / 15

Rejection log quality (tiebreaker only):
[ ] none  [ ] thin  [ ] solid  [ ] excellent

One-line memorable moment: _____________________
```

---
_Status: drafted 2026-04-27._
