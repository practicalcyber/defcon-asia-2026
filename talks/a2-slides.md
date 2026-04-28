---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    background: #0b0f14;
    color: #e6edf3;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    padding: 36px 56px 56px 56px;
  }
  h1 { color: #58a6ff; font-size: 44px; margin: 0 0 6px 0; }
  h2 { color: #8b949e; font-size: 22px; font-weight: 400; margin: 0 0 22px 0; }
  h3 { color: #58a6ff; font-size: 24px; margin: 0 0 6px 0; }
  strong { color: #f0883e; }
  em { color: #7ee787; font-style: normal; }
  table { width: 100%; border-collapse: collapse; font-size: 19px; }
  th { background: #161b22; color: #58a6ff; text-align: left; padding: 10px 14px; border-bottom: 2px solid #58a6ff; }
  td { padding: 10px 14px !important; border-bottom: 1px solid #30363d !important; vertical-align: top !important; color: #e6edf3 !important; background: transparent !important; }
  tbody tr:last-child td { border-bottom: 2px solid #58a6ff !important; }
  ul, ol { font-size: 22px; line-height: 1.5; }
  li { margin-bottom: 8px; }
  p { font-size: 22px; line-height: 1.45; }
  p.lead { color: #8b949e; font-size: 20px; margin-bottom: 18px; }
  blockquote {
    border-left: 4px solid #58a6ff;
    background: #0d1117;
    padding: 14px 20px;
    color: #c9d1d9;
    font-size: 22px;
    line-height: 1.5;
    margin: 14px 0;
  }
  code { background: #161b22; color: #f0883e; padding: 2px 6px; border-radius: 4px; font-size: 18px; }
  pre { background: #161b22; padding: 14px; border-radius: 6px; font-size: 16px; overflow: auto; }
  pre code { background: transparent; color: #e6edf3; padding: 0; }
  .callout {
    border-left: 4px solid #58a6ff;
    background: #0d1117;
    padding: 14px 18px;
    color: #c9d1d9;
    font-size: 20px;
    margin-top: 14px;
  }
  .split { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }
  .watch {
    border: 1px solid #30363d;
    border-left: 4px solid #f0883e;
    background: #0d1117;
    padding: 14px 18px;
    margin: 10px 0;
    font-size: 20px;
  }
  .watch h3 { color: #f0883e; font-size: 19px; margin: 0 0 6px 0; }
  .ratio {
    display: flex;
    height: 60px;
    border-radius: 6px;
    overflow: hidden;
    margin: 18px 0 6px 0;
    border: 1px solid #30363d;
  }
  .ratio .read { flex: 80; background: #1f6feb; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 600; }
  .ratio .write { flex: 20; background: #f0883e; display: flex; align-items: center; justify-content: center; color: #0b0f14; font-weight: 600; }
  footer { color: #6e7681; font-size: 13px; }
  section::after { color: #6e7681; }
---

# Vibe Coding Live
## Architecture over Syntax

**Ethan Seow** · Practical Cyber × C4AIL
DEF CON Asia 2026 — AI & AI Security Kampung

---

# The frame

<p class="lead">The most dangerous thing in 2026 is not an AI that writes bad code. It's a human who can't tell when AI wrote bad code.</p>

- My concern isn't capability — Claude Code is genuinely great.
- My concern is engineers who never learned to **reject** a suggestion.
- **Architecture is the discipline of rejection. Syntax is the easy part.**

<div class="callout">This is the <strong>Translator capability</strong> in code form: I'm not faster than the AI at typing. I'm faster than the AI at knowing what <em>should</em> be typed. That gap is the entire job.</div>

---

# What you're about to see

<p class="lead">A real security tool, built in front of you, in the next eighteen minutes.</p>

- Audience picks the tool. Nothing pre-written.
- Same Claude Code I use on a Tuesday at my desk.
- **At least once, I will reject something Claude writes**, out loud, with reasoning.

<div class="callout">That rejection is the whole point. <strong>The code that ships is what's left after I say no.</strong></div>

**Fallback prompts on the card:**
- S3 bucket → mask Singapore NRICs → write redacted manifest
- Tail Suricata alerts → de-dupe + enrich → post to Slack
- Classify failed SSH attempts on a honeypot — bot vs targeted human

---

# Three things I'm watching for

<div class="watch">
<h3>1 — Did it make a security decision I should be making?</h3>
"Should this be encrypted at rest." "Who can call this endpoint." "What's the failure mode." If AI silently decides those, I roll back.
</div>

<div class="watch">
<h3>2 — Did it hide a side effect?</h3>
AI loves to <code>os.remove</code>, <code>git push</code>, <code>subprocess.run</code> in the middle of a function called <code>parse_thing</code>. The function name should equal the function's blast radius. If it doesn't, I rewrite.
</div>

<div class="watch">
<h3>3 — Did it pretend to handle an error it cannot handle?</h3>
<code>try / except / pass</code> blocks are the new SQL injection. They turn a loud failure into a silent corruption.
</div>

<div class="callout">Anything else, I let Claude type. <strong>That's the 98/2 split, applied to my own keyboard.</strong></div>

---

# The build cadence

| Min | Phase | What I do | What you watch for |
|---|---|---|---|
| 0–1 | **Spec it** | Write 5-line `SPEC.md` in plain English | Can I state the tool in 5 lines? If not, I don't understand it yet |
| 1–3 | **Skeleton it** | Ask Claude for file layout. **Reject one suggestion.** | "No `utils.py` — that's where bugs go to hide" |
| 3–6 | **Tests first** | 3 deterministic tests. Claude can suggest; I gate. | Tests are the spec, compiled |
| 6–11 | **Implement** | Claude writes. I read. I narrate one rejection live. | The planned moment — see next slide |
| 11–13 | **Run** | Tests red → green. If green-on-first, suspicious — add edge case. | Easy green = missing test |

<div class="callout">If <em>any</em> phase finishes faster than expected, I add tests. <strong>Time saved is risk surfaced.</strong></div>

---

# The planned rejection

<p class="lead">~minute 10. Regardless of what Claude writes, I'll find an excuse.</p>

```python
# What Claude wrote:
try:
    result = boto3.client('s3').get_object(...)
except Exception:
    pass

# What I replace it with:
try:
    result = boto3.client('s3').get_object(...)
except (BotoCoreError, ClientError) as e:
    logger.error("S3 fetch failed: %s", e)
    raise
```

**Three differences:**
1. I named the exceptions I expected.
2. I logged it.
3. I re-raised so the caller can decide.

---

# Why that rejection matters

<div class="split">
<div>
<h3>Claude did the intellectual labour</h3>
<ul>
<li>Figured out which AWS calls to make</li>
<li>Wired up the SDK</li>
<li>Generated the boilerplate</li>
</ul>
</div>
<div>
<h3>I do the accountability labour</h3>
<ul>
<li>Decide what happens when the call fails</li>
<li>Decide what gets logged</li>
<li>Defend it in the postmortem</li>
</ul>
</div>
</div>

<div class="callout"><code>except Exception: pass</code> is the most dangerous line in modern software. It says <em>"if anything goes wrong I don't care, return success anyway."</em> That decision belongs to the person whose name is on the on-call rotation — not to a probability machine.</div>

---

# Read &gt; write

<p class="lead">What you'll watch most of these eighteen minutes is me <em>reading</em>, not typing.</p>

<div class="ratio"><div class="read">~80% reading — spec, tests, generated code, diff before commit</div><div class="write">20% writing</div></div>

- Read the spec.
- Read the tests.
- Read every line Claude generated.
- Read the diff before I commit.

<div class="callout"><strong>That ratio — read time to write time — is now the entire skill.</strong> An intern would have taken a week for this five years ago. The reason it now takes eighteen minutes is not that AI types faster than the intern. It's that I read faster than the intern.</div>

---

# This isn't just my framing

<p class="lead">Liu, Zhao, Shang, Shen — <em>Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems</em>. arXiv 2604.14228, 14 Apr 2026.</p>

Independent analysis of Claude Code's TypeScript source:

> *"A simple while-loop that calls the model, runs tools, and repeats… **most of the code, however, lives in the systems around this loop.**"*

The five values they extracted from the source:
1. **Human decision authority** ← that's the rejection moment, peer-reviewed
2. Safety / security
3. Reliable execution
4. Capability amplification
5. Contextual adaptability

<div class="callout">The tool I'm using right now is itself <strong>98% deterministic harness, 2% model call</strong>. Permission system, context compaction, tool dispatch, session storage — all code. The intelligence is the <em>edge</em>. Same architecture I'm asking you to build into your own tools.</div>

---

# The one habit

<p class="lead">If you walk away with one practice from this session:</p>

<blockquote style="font-size:26px; padding:24px;">
Before you accept any AI-generated code,<br>
<strong>say out loud what you would have written instead.</strong><br>
If you can't, you don't understand it well enough to ship it.
</blockquote>

That's the bar. That's the 98/2. That's the Translator capability in your IDE.

<div class="callout">AI's value comes from your data — the spec, the tests, the constraints. Its security comes from your framework — your refusal, your logging, your error model. <strong>Vibe coding doesn't change the fundamentals. It just makes them visible faster.</strong></div>

---

# Bridge to Mission 3

<p class="lead">Want to feel this in your hands today? <strong>Mission 3 — TDD Speedrun</strong> is the one.</p>

- Same loop: human writes the tests, AI writes the implementation.
- Thirty minutes. Ninety per cent coverage.
- The award goes to the team whose **rejected suggestions** were the most interesting.
- Keep a one-line note every time you say no to Claude.
- **That note is the deliverable.** It's the rubric tiebreaker.

---

# Close

<h2 style="color:#58a6ff; font-size:26px; margin-top:14px;">"I architect. AI types. If you cannot tell me which line you'd reject, you're not vibe coding — you're being driven."</h2>

<div style="display:grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 24px; align-items: center;">
  <div style="text-align:center;">
    <img src="../booth/qr/booth-site.png" style="width: 220px; height: 220px; background:#fff; padding: 10px; border-radius: 8px;">
    <p style="margin-top: 8px; font-size: 16px; color:#58a6ff;">defcon.practical-cyber.com</p>
  </div>
  <div style="text-align:center;">
    <img src="../booth/qr/github-repo.png" style="width: 220px; height: 220px; background:#fff; padding: 10px; border-radius: 8px;">
    <p style="margin-top: 8px; font-size: 16px; color:#58a6ff;">github.com/practicalcyber/defcon-asia-2026</p>
  </div>
</div>

<p style="margin-top: 18px; font-size:16px; color:#8b949e; text-align:center;">Ethan Seow · ethan@practical-cyber.com</p>
