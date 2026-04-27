# SPEC — Signal Extractor

Fill in **before** writing any code.

1. **Input:** _e.g. JSON-lines stream of CloudTrail-shaped events_
2. **Output:** _e.g. for each surfaced cluster: {principal, anomaly_type, count, time_window, narration, supporting_events_ids}_
3. **One rule:** _e.g. an event survives the filter only if at least one named rule fires; rule IDs are recorded with the event_
4. **One anti-rule:** _e.g. the AI NEVER decides whether an event is suspicious — only whether the deterministic rule's output deserves a 1-sentence narration_
5. **One example:** _input includes 3 ListBuckets calls within 10s from principal X → output: {principal: X, anomaly: "mass_enumeration", count: 3, narration: "..."} _

---
_Time on this step: 2 minutes max._
