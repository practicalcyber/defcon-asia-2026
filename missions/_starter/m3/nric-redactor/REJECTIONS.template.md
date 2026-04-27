# REJECTIONS — NRIC Redactor

Log every time you say "no" to a Claude suggestion. Aim for at least 3 entries.

Format:

```
HH:MM:SS — Claude proposed: <one line>
           Rejected because: <one line>
           Replaced with:    <one line>
```

## Example (delete before submitting)

```
00:11:42 — Claude proposed: re.findall(r'[STFG]\d{7}[A-Z]', text)
           Rejected because: doesn't validate the checksum, will redact valid-looking but invalid IDs
           Replaced with:    explicit per-character checksum check before redaction
```

## Your log

```


```
