# Suricata Alert Deduper — starter

**Spec (in 1 sentence):** read a JSON-lines stream of Suricata `alert` events, collapse alerts that are "the same incident" (same `signature_id` + same `(src_ip, dest_ip)` pair, occurring within 60 seconds of each other) into one summary record per cluster.

## Tests you'll write (suggested)

1. **Three alerts with same SID + src/dst within 30s collapse to one cluster** with count=3.
2. **Same SID across different src/dst pairs do NOT collapse.** Three pairs → three clusters.
3. **Window boundary respected.** A 4th alert at +61s starts a new cluster, not the same one.
4. **Schema-invalid JSON lines are skipped, counted, and logged.** Malformed lines never crash the pipeline.
5. **Output is stable across runs.** Sort by `first_seen` ascending. Re-runs produce identical output.

## Anti-patterns we'll dock points for

- AI wrote the tests.
- Test rewritten to make a failing case pass.
- Window logic that uses arrival time instead of the alert's own `timestamp`.
- Silent `try/except: pass` around `json.loads`. Surface the count.
- Output sort key is non-deterministic (e.g. dict iteration). Re-runs must match.

## Sample event shape

```json
{"timestamp":"2026-04-27T10:00:01.234567+0800","event_type":"alert",
 "src_ip":"1.2.3.4","src_port":50001,"dest_ip":"10.0.0.5","dest_port":443,
 "alert":{"signature_id":2025001,"signature":"ET POLICY suspicious UA","severity":2}}
```

## Bootstrap

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest
```
