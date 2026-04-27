# REJECTIONS — SSH Classifier

Log every "no" to Claude. Aim for ≥3.

```
HH:MM:SS — Claude proposed: <one line>
           Rejected because: <one line>
           Replaced with:    <one line>
```

## Example (delete before submitting)

```
00:18:05 — Claude proposed: classify on a fixed 60s window starting at the first event
           Rejected because: misses bursts that straddle the window boundary; sliding window is the correct primitive
           Replaced with:    sliding 5-minute window with 1-minute step
```

## Your log

```


```
