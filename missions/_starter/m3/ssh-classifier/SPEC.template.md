# SPEC — SSH Failed-Login Classifier

Fill in **before** writing any code. Five lines.

1. **Input:** _e.g. iterable of auth.log-style lines, or JSON-lines_
2. **Output:** _e.g. for each event: {timestamp, src_ip, username, classification}_
3. **One rule:** _e.g. classification windows on a 5-minute sliding bucket_
4. **One anti-rule:** _e.g. NEVER return None or raise on a recognised-but-novel pattern; return "unknown"_
5. **One example:** _input "Apr 27 10:01:02 host sshd[123]: Failed password for root from 1.2.3.4 port 22 ssh2" (×120 in 1 min) → output classification "targeted-bruteforce"_

---
_Time on this step: 2 minutes max._
