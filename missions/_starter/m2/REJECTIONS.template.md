# REJECTIONS — Stealth Architect

Log every "no" to Claude. Aim for ≥3.

```
HH:MM:SS — Claude proposed: <one line>
           Rejected because: <one line>
           Replaced with:    <one line>
```

## Example (delete before submitting)

```
00:09:14 — Claude proposed: ports: ["8080:8080"] on the redirector service
           Rejected because: defaults to binding 0.0.0.0:8080 — exposes redirector to the host network
           Replaced with:    ports: ["127.0.0.1:8080:8080"] — explicit loopback bind
```

## Your log

```


```
