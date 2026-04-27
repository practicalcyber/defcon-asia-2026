# NRIC Redactor — starter

**Spec (in 1 sentence):** read a directory of `.txt`/`.md`/`.csv`, find Singapore NRIC numbers (S/T/F/G prefix + 7 digits + checksum letter), replace with `[REDACTED-NRIC]`, write redacted versions to an output directory.

## Tests you'll write (suggested — adapt as you see fit)

1. **Valid NRIC formats are detected.** S1234567A and at least 6 other variants (different prefixes, both genders).
2. **Invalid checksums are NOT redacted.** Strings that *look* like NRICs but fail the checksum should pass through untouched. (Critical — false-positive guard.)
3. **Multiline inputs preserve line breaks.** Redaction doesn't collapse newlines or strip surrounding whitespace.
4. **UTF-8 with non-ASCII content survives the round-trip.** Chinese characters, emoji, accented Latin all preserved.
5. **Empty file is handled cleanly.** No crash, no exception, output is also empty.

## Anti-patterns we'll dock points for

- Letting AI write the tests. (Disqualifying.)
- Letting AI rewrite a failing test to make it pass. (Disqualifying.)
- A regex that matches the format but skips the checksum. We'll feed it false positives.
- Silent `try/except: pass` around file I/O. Surface failures.
- `# pragma: no cover` on the checksum logic to hit 90%.

## NRIC checksum rule (Singapore)

Multiplier weights for the 7 digits: `2, 7, 6, 5, 4, 3, 2`. Sum the weighted digits. For prefix `T`/`G`, add 4. Divide by 11; the remainder maps to a checksum letter table. Two tables exist — one for citizens (S/T) and one for foreigners (F/G). Look it up; the algorithm is published.

We will test your tool with both real-shape valid NRICs and lookalike invalid ones.

## Bootstrap

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/pytest                  # one structural test should pass
```

Then: fill `SPEC.template.md`, write your tests in `tests/test_redactor.py`, point Claude at them.
