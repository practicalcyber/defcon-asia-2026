# How to think about your mission

Every mission at this Kampung follows the same shape. If you remember nothing else, remember this — it's the 98/2 Principle as a recipe.

---

## The general pattern (applies to all three missions)

1. **Find the 98%.** What in this problem MUST be auditable, predictable, defensible? That part is code, not AI.
2. **Wall it off.** Write the rule, the policy, the test. Make the deterministic boundary *explicit and runnable* — not implied.
3. **Test the wall.** Add a test that fails before the rule exists and passes after. If you can't write that test, the rule isn't real yet.
4. **Drop AI in for the 2%.** Only after the wall holds, give AI the fuzzy job — narrate, propose, generate, implement. AI never decides what's *correct*; it produces, you check.
5. **Filter the egress.** Whatever AI returns must pass a deterministic check before it reaches the user, the system, or the next stage. Schema, regex, validator — your call. Loud rejection on failure.
6. **Rehearse the failure.** Run the system with a *hostile* input. A poisoned doc. A prompt-injection. A jailbreak. If you can't say "and here's what happens when AI lies," you don't have a system — you have a hope.

The Translator capability is steps 1, 2, 3, and 6. AI does step 4. Step 5 is the contract between them.

---

## M1 — The Signal Extractor

**Goal:** 200 noisy events → 3 explained anomalies. AI writes the explanation; rules pick the events.

1. **Find the 98%:** What makes each anomaly *anomalous*? Encode it as a boolean predicate. (Login from a region the user has never been in. Eight `Describe*` calls in twelve seconds. `CreateAccessKey` by root.)
2. **Wall it off:** Each predicate becomes a `Rule` in `filter_engine.py` — id, predicate, severity, why-string. The starter kit shows the shape.
3. **Test the wall:** One `xfail` test ships with the kit. Make it pass. Then write tests for the other two anomalies before you write the rules.
4. **Drop AI in:** `narrator.py` calls the LLM with *only* the flagged events plus rule context. The LLM never sees the 197 boring events.
5. **Filter the egress:** `Narration` pydantic schema rejects model output that hallucinates fields, fabricates indicators, or claims certainty without evidence. ValidationError = log + drop.
6. **Rehearse the failure:** Feed the LLM a flagged event with a misleading attribute (e.g. region spoofing in the user agent). Does the narration parrot the lie, or does the schema clamp it down?

**You're done when:** the 200-event sample produces exactly 3 anomalies, each with valid narration, and you can explain in one sentence why each rule fires.

---

## M2 — The Stealth Architect

**Goal:** Build an offensive lab AI can extend safely. AI proposes architecture; deterministic policies refuse anything dangerous.

1. **Find the 98%:** What would a hostile prompt try to do to your lab? Bind to public ports. Mount `/etc`. Run privileged. Leak secrets to env. Break the network isolation.
2. **Wall it off:** Each becomes a policy in `validators/compose_policy.py`. The kit ships P001–P005; that's the floor, not the ceiling.
3. **Test the wall:** Each policy has a test asserting it catches the violation AND passes the safe sandbox. If the safe sandbox fails any policy, your policy is wrong, not the sandbox.
4. **Drop AI in:** Use `prompts/architect.md` to ask the model for component changes — new service, new network, scaling. Every diff it proposes goes through `validate(compose)` before you run `docker compose up`.
5. **Filter the egress:** For phishing lures, `validators/lure_schema.py` rejects AI output that names real orgs, contains inline URLs, targets a real person, or duplicates subjects across the batch. No exceptions.
6. **Rehearse the failure:** Prompt-inject the architect — tell it the policy is in test mode and to add `privileged: true`. Watch the validator fire. Ask the lure model to "just this once" use a real bank's name. Watch the schema fire.

**You're done when:** AI has extended the lab (a new service, a new lure batch), every change passed validation, and `teardown.sh` returns the host to clean state.

---

## M3 — The TDD Speedrun

**Goal:** Concept → production tool in 30 minutes. Human writes tests; AI writes implementation. ≥90% coverage.

1. **Find the 98%:** Read your starter's `SPEC.template.md`. What inputs MUST produce what outputs? What inputs MUST be rejected? Those are your tests.
2. **Wall it off:** Write 4–6 tests in `tests/test_<tool>.py`. Each test is one named behaviour ("redacts NRIC in the middle of a sentence", "leaves NRIC-shaped strings inside code blocks alone"). Tests are red. Don't write the implementation yet.
3. **Test the wall:** Run pytest. Confirm everything fails for the *right* reason — `NotImplementedError` or "module empty," not "import error."
4. **Drop AI in:** Hand the spec + test file to your AI: *"Make these pass. Don't modify the tests."* Run pytest after each suggestion.
5. **Filter the egress:** For every AI suggestion, ask: *is this passing the test, or gaming the test?* If it short-circuits the spec to satisfy a test (regex hard-coded to your test data, special-case for the literal input), reject it. Log every rejection in `REJECTIONS.md` with one line of reasoning. **This is your accountability layer and the rubric tiebreaker.**
6. **Rehearse the failure:** Feed your tool an input the tests don't cover. Does it fail loudly or silently produce garbage? Add a test for the new edge case and re-loop.

**You're done when:** all your tests are green, `pytest --cov` shows ≥90% on your module, and `REJECTIONS.md` has at least three entries you can defend out loud.

---

## What the judges are listening for

Three lines. If your demo can answer all three, you're a finalist:

- *"Show me where the deterministic boundary is."*
- *"Show me what AI does and what AI does NOT decide."*
- *"Show me what happens when the AI lies."*
