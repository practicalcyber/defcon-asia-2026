# SPEC — Stealth Architect

Fill in **before** writing any code.

1. **Input:** _e.g. natural-language description of the offensive infra you want_
2. **Output:** _e.g. a validated docker-compose stack + N lure variants in JSON_
3. **One rule:** _e.g. every AI-generated config passes `validators/compose_policy.py` before `docker compose up`_
4. **One anti-rule:** _e.g. NEVER bind any service to 0.0.0.0; NEVER run privileged containers; NEVER include hardcoded credentials_
5. **One example:** _input "build me a 2-tier redirector for SG corporate phishing analysis" → output: validated compose with 127.0.0.1-bound nginx → caddy → C2 stub, plus 3 lure variants reviewed against schema_

---
_Time on this step: 2 minutes max._
