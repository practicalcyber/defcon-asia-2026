# REJECTIONS — Suricata Deduper

Log every "no" to Claude. Aim for ≥3.

```
HH:MM:SS — Claude proposed: <one line>
           Rejected because: <one line>
           Replaced with:    <one line>
```

## Example (delete before submitting)

```
00:14:11 — Claude proposed: cluster on (signature) only, ignoring src/dst
           Rejected because: collapses unrelated incidents that happen to share an SID
           Replaced with:    cluster key = (sid, src_ip, dest_ip)
```

## Your log

```


```
