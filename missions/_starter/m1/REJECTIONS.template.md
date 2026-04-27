# REJECTIONS — Signal Extractor

Log every "no" to Claude. Aim for ≥3.

```
HH:MM:SS — Claude proposed: <one line>
           Rejected because: <one line>
           Replaced with:    <one line>
```

## Example (delete before submitting)

```
00:22:30 — Claude proposed: pass the raw event JSON into the narrator prompt
           Rejected because: prompt-injection surface; cost; PII; the model only needs the structured summary
           Replaced with:    pass {principal, action_set, count, time_window} only; raw events stay server-side
```

## Your log

```


```
