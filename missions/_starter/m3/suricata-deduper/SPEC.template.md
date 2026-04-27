# SPEC — Suricata Alert Deduper

Fill in **before** writing any code. Five lines.

1. **Input:** _e.g. JSON-lines stream of Suricata alert events_
2. **Output:** _e.g. JSON-lines stream of cluster summaries: {sid, src, dst, first_seen, last_seen, count}_
3. **One rule:** _e.g. cluster = same SID + same (src, dst) + max gap 60s between consecutive alerts_
4. **One anti-rule:** _e.g. NEVER use arrival time for windowing — use the alert's own `timestamp`_
5. **One example:** _3 alerts at t=0, t=15s, t=45s with same SID and src/dst → one cluster with count=3_

---
_Time on this step: 2 minutes max._
