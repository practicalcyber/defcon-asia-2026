---
marp: true
theme: default
paginate: false
size: 16:9
style: |
  section {
    background: #0b0f14;
    color: #e6edf3;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    padding: 24px 56px 64px 56px;
    overflow: hidden;
  }
  h1 {
    color: #58a6ff;
    font-size: 40px;
    margin: 0 0 4px 0;
  }
  h2 {
    color: #8b949e;
    font-size: 20px;
    font-weight: 400;
    margin: 0 0 22px 0;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 21px;
    table-layout: auto;
  }
  th {
    background: #161b22;
    color: #58a6ff;
    text-align: left;
    padding: 12px 14px;
    border-bottom: 2px solid #58a6ff;
    font-size: 20px;
  }
  td {
    padding: 12px 14px !important;
    border-bottom: 1px solid #30363d !important;
    vertical-align: top !important;
    color: #e6edf3 !important;
    background: transparent !important;
    line-height: 1.35 !important;
  }
  tbody tr:last-child td { border-bottom: 2px solid #58a6ff !important; }
  tbody tr { background: transparent !important; }
  strong { color: #f0883e; }
  em { color: #7ee787; font-style: normal; }
  .footer {
    position: absolute;
    bottom: 18px;
    left: 56px;
    right: 56px;
    display: flex;
    justify-content: space-between;
    color: #6e7681;
    font-size: 13px;
  }
  ol, ul { font-size: 18px; line-height: 1.5; padding-left: 24px; margin: 8px 0; }
  ol li, ul li { margin-bottom: 6px; }
  ol li strong, ul li strong { color: #f0883e; }
  p { font-size: 18px; line-height: 1.45; margin: 6px 0; }
  p.lead { color: #8b949e; font-size: 17px; margin-bottom: 14px; }
  h3 { color: #58a6ff; font-size: 22px; margin: 0 0 4px 0; }
  .judges {
    margin-top: 14px;
    padding: 10px 14px;
    border-left: 3px solid #58a6ff;
    background: #0d1117;
    font-size: 17px;
    color: #c9d1d9;
  }
---

# AI & AI Security Kampung
## DEF CON Asia 2026 · 28–30 April · Practical Cyber × C4AIL

| Day | Slot | What's on |
|---|---|---|
| **Tue 28 Apr** | Morning | Booth open · M1 / M2 / M3 walk-ups |
| | **Afternoon** | **A1 — AI Red Teaming: Breaking the Black Box** *(30 min)* |
| **Wed 29 Apr** | Morning | Booth · deeper mission conversations |
| | **Afternoon** | **A2 — Vibe Coding Live: Architecture over Syntax** *(30 min)* |
| **Thu 30 Apr** | Morning | Booth · final submissions |
| | Afternoon | **Architect of the Quarter** judging + close |

<div class="footer">
  <span>Leads: Ethan Seow · Palvinder Singh</span>
  <span>98% deterministic · 2% intelligent edge</span>
</div>

---

# How to think about your mission
## The 98/2 Principle as a recipe — applies to every mission

1. **Find the 98%.** What MUST be auditable, predictable, defensible? That part is code, not AI.
2. **Wall it off.** Write the rule, the policy, the test. Make the deterministic boundary explicit and runnable.
3. **Test the wall.** Add a test that fails before the rule, passes after. If you can't write that test, the rule isn't real.
4. **Drop AI in for the 2%.** Only after the wall holds, give AI the fuzzy job — narrate, propose, generate, implement.
5. **Filter the egress.** Whatever AI returns must pass a deterministic check. Schema, regex, validator. Loud rejection on failure.
6. **Rehearse the failure.** Run the system with a hostile input — poisoned doc, prompt injection, jailbreak. Show what happens when AI lies.

<div class="footer">
  <span>The Translator capability lives in steps 1, 2, 3, and 6. AI does step 4. Step 5 is the contract.</span>
  <span>defcon.practical-cyber.com</span>
</div>

---

# M1 — The Signal Extractor

<p class="lead">200 noisy events → 3 explained anomalies. Rules pick events. AI writes the explanation.</p>

1. **Find the 98%:** What makes each anomaly anomalous? Boolean predicate per pattern. *(Login from a region the user has never been in. Eight `Describe*` calls in twelve seconds. `CreateAccessKey` by root.)*
2. **Wall it off:** Each predicate becomes a `Rule` in `filter_engine.py` — id, predicate, severity, why-string.
3. **Test the wall:** Make the shipped `xfail` pass. Then write tests for the other two anomalies before writing the rules.
4. **Drop AI in:** `narrator.py` calls the LLM with *only* flagged events plus rule context. The LLM never sees the 197 boring events.
5. **Filter the egress:** `Narration` pydantic schema rejects hallucinated fields, fabricated indicators, false certainty. ValidationError = log + drop.
6. **Rehearse the failure:** Feed a flagged event with a misleading attribute. Does the narration parrot the lie, or does the schema clamp it?

<div class="judges">Done when: the 200-event sample produces exactly 3 anomalies, each with valid narration, and you can explain in one sentence why each rule fires.</div>

<div class="footer">
  <span>M1 — Signal Extractor (SecOps)</span>
  <span>defcon.practical-cyber.com</span>
</div>

---

# M2 — The Stealth Architect

<p class="lead">Build an offensive lab AI can extend safely. AI proposes architecture; deterministic policies refuse anything dangerous.</p>

1. **Find the 98%:** What would a hostile prompt try to do? Bind public ports. Mount `/etc`. Run privileged. Leak secrets. Break network isolation.
2. **Wall it off:** Each becomes a policy in `validators/compose_policy.py`. The kit ships P001–P005; that's the floor, not the ceiling.
3. **Test the wall:** Each policy has a test asserting it catches the violation AND passes the safe sandbox.
4. **Drop AI in:** Use `prompts/architect.md` to ask for component changes. Every diff goes through `validate(compose)` before `docker compose up`.
5. **Filter the egress:** `validators/lure_schema.py` rejects AI lures naming real orgs, with inline URLs, real targets, or duplicate subjects.
6. **Rehearse the failure:** Prompt-inject the architect — tell it the policy is in test mode and to add `privileged: true`. Watch the validator fire.

<div class="judges">Done when: AI has extended the lab (new service, new lure batch), every change passed validation, and `teardown.sh` returns the host to clean state.</div>

<div class="footer">
  <span>M2 — Stealth Architect (Offensive infra)</span>
  <span>defcon.practical-cyber.com</span>
</div>

---

# M3 — The TDD Speedrun

<p class="lead">Concept → production tool in 30 minutes. Human writes tests. AI writes implementation. ≥90% coverage.</p>

1. **Find the 98%:** Read your starter's `SPEC.template.md`. What inputs MUST produce what outputs? What inputs MUST be rejected? Those are your tests.
2. **Wall it off:** Write 4–6 named-behaviour tests. *("redacts NRIC mid-sentence", "leaves NRIC-shaped strings inside code blocks alone".)* Tests stay red. No implementation yet.
3. **Test the wall:** Run pytest. Confirm everything fails for the *right* reason — `NotImplementedError`, not import error.
4. **Drop AI in:** Hand spec + test file to AI: *"Make these pass. Don't modify the tests."* Run pytest after each suggestion.
5. **Filter the egress:** For every AI suggestion, ask: *passing the test, or gaming the test?* Reject hard-coded short-circuits. Log every rejection in `REJECTIONS.md` with one line of reasoning.
6. **Rehearse the failure:** Feed an input the tests don't cover. Loud failure or silent garbage? Add a test for the new edge case and re-loop.

<div class="judges">Done when: all tests green, `pytest --cov` ≥ 90% on your module, and `REJECTIONS.md` has at least three entries you can defend out loud. The rejection log is the rubric tiebreaker.</div>

<div class="footer">
  <span>M3 — TDD Speedrun (Development)</span>
  <span>defcon.practical-cyber.com</span>
</div>

---

# What the judges are listening for

<p class="lead">Three lines. If your demo can answer all three, you're a finalist.</p>

<div class="judges" style="margin-top:30px; font-size: 24px; line-height: 1.7;">
"Show me where the deterministic boundary is."<br><br>
"Show me what AI does and what AI does NOT decide."<br><br>
"Show me what happens when the AI lies."
</div>

<div class="footer">
  <span>Architect of the Quarter — judged Day 3 afternoon</span>
  <span>98% deterministic · 2% intelligent edge</span>
</div>

---

# Take it home

<p class="lead">Everything from this Kampung — talks, missions, demos, starter kits, slides — is open.</p>

<div style="display:grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 30px; align-items: center;">
  <div style="text-align:center;">
    <img src="qr/booth-site.png" style="width: 200px; height: 200px; background:#fff; padding: 10px; border-radius: 8px;">
    <h3 style="margin-top: 14px;">defcon.practical-cyber.com</h3>
    <p style="font-size: 16px; color:#8b949e; margin-top:4px;">This screen — the whole deck</p>
  </div>
  <div style="text-align:center;">
    <img src="qr/github-repo.png" style="width: 200px; height: 200px; background:#fff; padding: 10px; border-radius: 8px;">
    <h3 style="margin-top: 14px;">github.com/practicalcyber/defcon-asia-2026</h3>
    <p style="font-size: 16px; color:#8b949e; margin-top:4px;">All source · talks · starter kits</p>
  </div>
</div>

<div class="footer">
  <span>Ethan Seow · Palvinder Singh · ethan@practical-cyber.com</span>
  <span>Open source · MIT-spirit · clone, fork, run</span>
</div>
