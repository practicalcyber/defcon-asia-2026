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
  h1 { color: #58a6ff; font-size: 42px; margin: 0 0 6px 0; }
  h2 { color: #8b949e; font-size: 22px; font-weight: 400; margin: 0 0 18px 0; }
  h3 { color: #58a6ff; font-size: 22px; margin: 0 0 6px 0; }
  strong { color: #f0883e; }
  em { color: #7ee787; font-style: normal; }
  table { width: 100%; border-collapse: collapse; font-size: 17px; }
  th { background: #161b22; color: #58a6ff; text-align: left; padding: 9px 12px; border-bottom: 2px solid #58a6ff; font-size: 16px; }
  td { padding: 9px 12px !important; border-bottom: 1px solid #30363d !important; vertical-align: top !important; color: #e6edf3 !important; background: transparent !important; line-height: 1.35 !important; }
  tbody tr { background: transparent !important; }
  tbody tr:nth-child(even) { background: transparent !important; }
  tbody tr:last-child td { border-bottom: 2px solid #58a6ff !important; }
  ul, ol { font-size: 20px; line-height: 1.45; }
  li { margin-bottom: 6px; }
  p { font-size: 20px; line-height: 1.4; }
  p.lead { color: #8b949e; font-size: 19px; margin-bottom: 14px; }
  blockquote { border-left: 4px solid #58a6ff; background: #0d1117; padding: 12px 18px; color: #c9d1d9; font-size: 19px; line-height: 1.45; margin: 12px 0; }
  code { background: #161b22; color: #f0883e; padding: 2px 6px; border-radius: 4px; font-size: 17px; }
  pre { background: #161b22; padding: 12px; border-radius: 6px; font-size: 15px; overflow: auto; }
  pre code { background: transparent; color: #e6edf3; padding: 0; }
  .callout { border-left: 4px solid #58a6ff; background: #0d1117; padding: 12px 16px; color: #c9d1d9; font-size: 18px; margin-top: 12px; }
  .split { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
  .watch { border: 1px solid #30363d; border-left: 4px solid #f0883e; background: #0d1117; padding: 12px 16px; margin: 8px 0; font-size: 18px; }
  .watch h3 { color: #f0883e; font-size: 17px; margin: 0 0 4px 0; }
  .ratio { display: flex; height: 50px; border-radius: 6px; overflow: hidden; margin: 14px 0 4px 0; border: 1px solid #30363d; }
  .ratio .read { flex: 80; background: #1f6feb; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 600; font-size: 16px; }
  .ratio .write { flex: 20; background: #f0883e; display: flex; align-items: center; justify-content: center; color: #0b0f14; font-weight: 600; font-size: 13px; }
  .stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 24px; margin: 14px 0; }
  .stat { border: 1px solid #30363d; background: #0d1117; padding: 10px 14px; border-radius: 6px; }
  .stat .num { font-size: 28px; color: #f0883e; font-weight: 700; line-height: 1.1; }
  .stat .label { font-size: 14px; color: #8b949e; line-height: 1.35; margin-top: 4px; }
  .qr-center { text-align: center; margin-top: 20px; }
  .qr-center img { width: 220px; height: 220px; background: #fff; padding: 10px; border-radius: 8px; }
  .qr-center p { margin-top: 10px; font-size: 18px; color: #58a6ff; }
  footer { color: #6e7681; font-size: 13px; }
  section::after { color: #6e7681; }
---

# Architecture over Vibes
## Agentic Engineering for Security Practitioners

**Ethan Seow** · Practical Cyber × C4AIL
DEF CON Asia 2026 — AI & AI Security Kampung

<p style="margin-top: 18px; font-size:16px; color:#8b949e;">Companion paper: <em>The Architecture of AI-Assisted Development — From Vibe Coding to Sovereign Command</em> · C4AIL, March 2026</p>

---

# The frame

<p class="lead">The most dangerous thing in 2026 is not an AI that writes bad code. It's a human who can't tell when AI wrote bad code.</p>

- My concern isn't capability — Claude Code, Codex, Gemini CLI are genuinely great.
- My concern is engineers who never learned to **reject** a suggestion.
- **Architecture is the discipline of rejection. Syntax is the easy part.**

<div class="callout">This is the <strong>Translator capability</strong> in code form: I'm not faster than the AI at typing. I'm faster than the AI at knowing what <em>should</em> be typed — and at <em>making it run the actual code</em> so the answer is verified, not vibed.</div>

---

# The five ages of AI-assisted code

<p class="lead">A maturity progression, not a timeline. The industry walked through four wrong defaults to arrive at the fifth.</p>

| Age | Year | Default move | Where it broke |
|---|---|---|---|
| **1. Prompt engineering** | 2023-24 | Craft a smarter prompt | Better prompts, same unreliable output |
| **2. Vibe coding** | Feb 2025 (Karpathy) | "Forget the code even exists" | Three-month wall — nobody can debug it |
| **3. The 70% Problem** | Late 2024 (Osmani) | AI gets 70% done fast | The last 30% is **human accountability labour** |
| **4. Context engineering** | Jun 2025 (Lutke) | Design the environment, not the prompt | Still measures tooling, not human judgment |
| **5. Agentic engineering** | **Feb 2026 (Karpathy: vibe coding "passé")** | Human owns architecture & verification; AI implements | This is where we are |

<div class="callout">Spec-Driven Development is its formal methodology. AWS Kiro, GitHub Spec Kit, SPARC, Intent, OpenSpec — all the same shape: <strong>spec is the source of truth, code is the build output</strong>.</div>

---

# The evidence against vibes

<p class="lead">Four numbers from independent research. Internalise these before you accept your next AI suggestion.</p>

<div class="stat-grid">
  <div class="stat"><div class="num">−19%</div><div class="label">Experienced devs <em>slower</em> on their own codebases with AI assistance — while believing they were 20% faster (METR RCT, 2025)</div></div>
  <div class="stat"><div class="num">−17%</div><div class="label">Skill assessment drop for devs using AI coding assistants. Largest gaps in <em>comprehension and debugging</em> — the exact skills needed to verify AI output (Anthropic, 2025)</div></div>
  <div class="stat"><div class="num">45%</div><div class="label">of AI-generated code contains security vulnerabilities without structural verification (Veracode, 2025)</div></div>
  <div class="stat"><div class="num">+98%</div><div class="label">PRs merged · review time grew only +91% — senior devs reviewing 6.5% more code while their own output declined (Faros AI, 10K+ devs)</div></div>
</div>

<div class="callout"><strong>The Eloquence Trap applied to productivity:</strong> the experience of speed is not the reality of speed. The tool degrades the skill the tool requires.</div>

---

# Verification debt

<p class="lead">Werner Vogels (AWS CTO) named the accumulating cost: <em>verification debt</em>.</p>

> *"When you write code yourself, comprehension comes with the act of creation — but when the machine writes it, you must rebuild that comprehension during review. Every line of AI-generated code that ships without genuine understanding is debt that will come due."*

**The honest counterweight:** human-written code didn't always come with built-in comprehension either. Cargo-culted Stack Overflow has existed for two decades.

The real loss is specific: **the cognitive trace** — the memory of why each decision was made — that made a skilled engineer's code maintainable. AI removes the act of creation, and with it the trace.

<div class="callout"><strong>The fix is not to reject AI.</strong> It's to encode the trace into something machine-readable: instruction files, specs, gotchas, verification chains. Architecture beats audit.</div>

---

# What context engineering actually is

<p class="lead">Lutke (Shopify CEO, Jun 2025): "providing all the context needed for a task to be plausibly solvable by an AI system." Practitioners refined this into four components.</p>

| Component | What it is | Example |
|---|---|---|
| **Instructions** | Rules, constraints, anti-patterns. *Architecture, not suggestions.* | "Never create docs unless asked." "Mandatory plan before edits." |
| **Knowledge** | Domain context. Past failures. Edge cases. The ORM behaviour that surprises everyone. | "kerykeion v5 `mean_node` returns None — use `true_node`." |
| **Tools** | Capabilities the AI can invoke — files, APIs, deploys. | MCP servers, CLI tools, custom validators |
| **State** | What's been done, what's in progress, what failed. | Task system, session memory, audit log |

<div class="callout">Prompt engineering asked: <em>"How do I phrase this so the AI gives me what I want?"</em> Context engineering asks: <em>"What architecture do I need so the AI's <strong>default</strong> output meets my standards?"</em></div>

---

# The five knowledge layers

<p class="lead">A senior engineer's judgment is different from a junior's prompt because humans process five layers simultaneously. AI natively processes the bottom two.</p>

| Layer | What it is | Where it lives in your repo |
|---|---|---|
| **Experiential** | Body-level pattern recognition from years of failures | **Gotchas** — "this broke us in production" |
| **Contextual** | This codebase's patterns, this domain's edge cases | Project-specific instructions |
| **Institutional** | How the team works, what the culture permits | Coding conventions, review norms |
| **Deductive** | Formal reasoning, frameworks, rubrics | Sizing heuristics, validators |
| **Syntactic** | Format, naming, surface language | The layer AI already handles |

<div class="callout"><strong>Vibe coding fails for the same reason factory education fails:</strong> it operates on syntactic + deductive only. Context engineering is the discipline of encoding the missing three layers into the AI's environment.</div>

---

# What you're about to see

<p class="lead">A real security tool, built in front of you, in the next eighteen minutes.</p>

- Audience picks the tool. Nothing pre-written.
- Same Claude Code I use on a Tuesday at my desk — running against a CLAUDE.md I have spent six months refining.
- **At least once, I will reject something Claude writes**, out loud, with reasoning.
- **At least once, I will make Claude run the actual code** — because *running it* is how the answer stops being a vibe.

<div class="callout"><strong>That rejection and that test run are the whole point.</strong> The code that ships is what's left after I say no. The code that's <em>verified</em> is what's left after I make it execute.</div>

**Fallback prompts on the card:** S3 → mask SG NRICs → write redacted manifest · tail Suricata alerts → de-dupe + enrich → Slack · classify failed SSH on a honeypot — bot vs targeted human

---

# Three things I'm watching for

<div class="watch">
<h3>1 — Did it make a security decision I should be making?</h3>
"Should this be encrypted at rest." "Who can call this endpoint." "What's the failure mode." Silent decisions there → I roll back.
</div>

<div class="watch">
<h3>2 — Did it hide a side effect?</h3>
AI loves to <code>os.remove</code>, <code>git push</code>, <code>subprocess.run</code> in the middle of a function called <code>parse_thing</code>. <strong>Function name should equal the function's blast radius.</strong>
</div>

<div class="watch">
<h3>3 — Did it pretend to handle an error it cannot handle?</h3>
<code>try / except / pass</code> blocks are the new SQL injection. They turn a loud failure into a silent corruption.
</div>

<div class="callout">Anything else, I let Claude type. Then I make it run pytest. <strong>Running the code is the cheapest form of accountability labour.</strong></div>

---

# The build cadence

| Min | Phase | What I do | What you watch for |
|---|---|---|---|
| 0–1 | **Spec it** | Write 5-line `SPEC.md` in plain English | Can I state the tool in 5 lines? If not, I don't understand it yet |
| 1–3 | **Skeleton it** | Ask Claude for file layout. **Reject one suggestion.** | "No `utils.py` — that's where bugs go to hide" |
| 3–6 | **Tests first** | 3 deterministic tests. Claude can suggest; I gate. | Tests are the spec, compiled |
| 6–11 | **Implement + run** | Claude writes. I read. **Then I make it run pytest after every change.** | The planned moment — see next slide |
| 11–13 | **Verify** | Tests red → green. Green-on-first → suspicious — add edge case. | Easy green = missing test |

<div class="callout">If <em>any</em> phase finishes faster than expected, I add tests or run a hostile input. <strong>Time saved is risk surfaced.</strong></div>

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

**Then I run pytest.** Because *saying* the fix is right is a vibe. *Running it* is verification.

---

# Why that rejection matters — the labour split

<div class="split">
<div>
<h3>Claude does the intellectual labour</h3>
<ul>
<li>Figured out which AWS calls to make</li>
<li>Wired up the SDK</li>
<li>Generated the boilerplate</li>
<li>Suggested the test structure</li>
</ul>
</div>
<div>
<h3>I do the accountability labour</h3>
<ul>
<li>Decide what happens when the call fails</li>
<li>Decide what gets logged</li>
<li><strong>Make it run the actual code</strong></li>
<li>Defend it in the postmortem</li>
</ul>
</div>
</div>

<div class="callout"><code>except Exception: pass</code> is the most dangerous line in modern software. It says <em>"if anything goes wrong I don't care, return success anyway."</em> That decision belongs to the person whose name is on the on-call rotation — not to a probability machine. <strong>Decision Survivability:</strong> can you defend this after it breaks?</div>

---

# Read &gt; write &gt; vibe — the 80/15/5

<p class="lead">What you'll watch most of these eighteen minutes is me <em>reading</em> and <em>running</em>, not typing.</p>

<div class="ratio"><div class="read">~80% reading — spec, tests, generated code, diff before commit, test output</div><div class="write">20% writing</div></div>

- Read the spec.
- Read the tests.
- Read every line Claude generated.
- **Run pytest.** Read the actual output. Not "Claude said it passes" — *run it*.
- Read the diff before I commit.

<div class="callout"><strong>Self-reported metric on my own context-engineering rig: 50–80% first-time-right on bulk deliverable generation.</strong> Took six months and roughly 4,300 lines of structured CLAUDE.md across 29 files to get there. <em>The discipline, not the model, is the compounding asset.</em></div>

---

# This isn't just my framing

<p class="lead">Liu, Zhao, Shang, Shen — <em>Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems</em>. arXiv 2604.14228, 14 Apr 2026.</p>

Independent analysis of Claude Code's TypeScript source:

> *"A simple while-loop that calls the model, runs tools, and repeats… **most of the code, however, lives in the systems around this loop.**"*

The five values they extracted from the source:
1. **Human decision authority** ← the rejection moment, peer-reviewed
2. Safety / security
3. Reliable execution
4. Capability amplification
5. Contextual adaptability

<div class="callout">The tool I'm using right now is itself <strong>98% deterministic harness, 2% model call</strong>. Permission system, context compaction, tool dispatch, session storage — all code. The intelligence is the <em>edge</em>. Same architecture I'm asking you to build into your own tools.</div>

---

# The one habit

<p class="lead">If you walk away with one practice from this session:</p>

<blockquote style="font-size:24px; padding:20px;">
Before you accept any AI-generated code,<br>
<strong>say out loud what you would have written instead — then run the code to check.</strong><br>
If you can do neither, you don't understand it well enough to ship it.
</blockquote>

That's the bar. That's the 98/2. That's agentic engineering in your IDE.

<div class="callout">AI's value comes from your data — the spec, the tests, the constraints. Its security comes from your framework — your refusal, your logging, your error model, your <em>actual test runs</em>. <strong>Vibe coding doesn't change the fundamentals. It just makes them visible faster.</strong></div>

---

# Bridge to Mission 3

<p class="lead">Want to feel this in your hands today? <strong>Mission 3 — TDD Speedrun</strong> is the one.</p>

- Same loop: human writes the tests, AI writes the implementation, **human runs the tests**.
- Thirty minutes. Ninety per cent coverage.
- The award goes to the team whose **rejected suggestions** were the most interesting.
- Keep a one-line note every time you say no to Claude — and every time you caught it by *running* the code.
- **That note is the deliverable.** It's the rubric tiebreaker.

---

# Close

<h2 style="color:#58a6ff; font-size:26px; margin-top:10px;">"I architect. AI types. I make it run.<br>If you can't tell me which line you'd reject — or which test you'd run — you're not vibe coding. You're being driven."</h2>

<div class="qr-center">
  <img src="../booth/qr/booth-site.png">
  <p>defcon.practical-cyber.com — slides · talks · missions · starter kits</p>
</div>

<p style="margin-top: 14px; font-size:16px; color:#8b949e; text-align:center;">Ethan Seow · ethan@practical-cyber.com</p>
