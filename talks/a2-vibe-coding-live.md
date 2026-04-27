# A2 — Vibe Coding Live: Architecture over Syntax

**Speaker:** Ethan Seow
**Default length:** 20 minutes (scalable: 10-min compressed, 45-min workshop)
**Format:** Live build with Claude Code, audience-driven prompt
**Audience:** Practitioners, builders, curious leaders
**Throughline:** _"Vibe coding is not 'AI writes my code.' It's 'I architect, AI types.' If you cannot tell me which line you'd reject, you're not vibe coding — you're being driven."_

---

## 1. The frame

This session exists because **the most dangerous thing in 2026 is not an AI that writes bad code**. It's a human who can't tell when AI wrote bad code.

My number one concern about this generation of tools is not capability — Claude Code is genuinely great. My concern is that we're producing engineers who never learned to *reject* a suggestion. Architecture is the discipline of rejection. Syntax is the easy part.

This is the **Translator capability** in code form: I'm not faster than the AI at typing. I'm faster than the AI at knowing what *should* be typed. That gap is the entire job.

---

## 2. Cold open (60–90 seconds)

> "I'm going to build a real security tool, in front of you, in the next eighteen minutes. The audience picks the tool. I will not pre-write anything. I will use Claude Code, the same way I use it on a Tuesday at my desk.
>
> But here's the rule of the demo: **at least once, I'm going to reject something Claude writes**, out loud, with my reasoning. That rejection is the whole point. The code that ships is what's left after I say no.
>
> Who has a tool they wish existed? Shout it out."

**If the room is shy** — pull from the pre-staged fallbacks:
- "Scan an S3 bucket for files containing Singapore NRIC numbers, mask them, write a redacted manifest."
- "Tail Suricata alerts and post de-duplicated, enriched summaries to a Slack channel."
- "Classify failed SSH login attempts on a honeypot — bot vs targeted human — using last 24h of logs."

These are in `demos/d3-vibe-coding-fallbacks/` with rough scaffolds I've sanity-checked, so I know they're 18-minute-buildable.

---

## 3. Set the stage (2 min)

Before the build, say out loud what I'm watching for. This is the **architect's eye** — the thing the audience is here to learn, not the syntax.

> "Three things I'm watching as Claude Code writes:
>
> **One — does it make a security decision I should be making?** Things like 'should this be encrypted at rest', 'who can call this endpoint', 'what's the failure mode'. If the AI silently decides those, I have to roll it back.
>
> **Two — does it hide a side effect?** AI loves to confidently `os.remove`, `git push`, `subprocess.run` in the middle of a function called `parse_thing`. The function name should equal the function's blast radius. If it doesn't, I rewrite.
>
> **Three — does it pretend to handle an error it cannot handle?** Try/except blocks that swallow the exception and return None are the new SQL injection. They turn a loud failure into a silent corruption.
>
> Anything else, I let Claude type. That's the 98/2 split, applied to my own keyboard."

**Whiteboard / flipchart:** put those three watch-points up where the audience can see them. They'll pattern-match against my rejections in real-time.

---

## 4. The build (10–12 min)

### Setup beat

- Audience picks tool. (Or I pull the S3 NRIC scanner.)
- I open Claude Code. Audience can see the screen.
- **Spoken aloud:** _"First thing I'm doing — not coding. I'm writing the spec, in plain English, in a `SPEC.md`. If I can't write the spec in five lines, I don't understand the tool yet, and Claude will write something that compiles and is wrong."_

### Build cadence

I'll narrate as I go. The rhythm should be:

1. **Spec it** (1 min) — write the 5-line spec live. Audience sees me think before I type.
2. **Skeleton it** (2 min) — ask Claude for the file layout. Read the layout. **Reject one suggestion** ("no, I don't want a `utils.py` — that's where bugs go to hide. Inline it.").
3. **Tests first** (2–3 min) — write 3 deterministic tests. Claude can suggest them; I gate them. The tests are the spec compiled.
4. **Implement** (4–5 min) — let Claude write. I read every line. I narrate one specific rejection — the **planned moment**, see §5 below.
5. **Run** (1–2 min) — tests go red, then green. If green-on-first-try, suspicious; show how I'd add one more edge-case test.

### What the audience experiences

They watch a senior engineer **read** code more than they write it. That is the thing nobody is teaching, and it is the thing that separates the AI-amplified engineer from the AI-driven one.

---

## 5. The planned rejection moment

This is the central pedagogical beat. **At minute ~10**, regardless of what Claude has produced, I'll find an excuse to do this:

> "Hold on. Look at line 34. Claude just wrote `except Exception: pass`. That's the most dangerous line in modern software. It says 'if anything goes wrong I don't care, return success anyway.'
>
> I'm replacing this with `except (BotoCoreError, ClientError) as e: logger.error(...); raise`. The differences are: I named the exceptions I expected, I logged it, I re-raised so the caller can decide.
>
> **This is intellectual vs accountability labour.** Claude did the intellectual labour — it figured out which AWS calls to make. I do the accountability labour — I decide what happens when the call fails, because *I'm the one defending the decision in a postmortem*."

If Claude doesn't generate something rejection-worthy organically (it usually does), I'll force the moment by asking it to "make the error handling more robust" — which reliably produces something I can dunk on.

---

## 6. The synthesis (2–3 min)

> "What did you just watch?
>
> You watched a build that took eighteen minutes — one I would have given an intern a week to do five years ago. That's not the lesson. The lesson is that **most of those eighteen minutes were me reading, not writing.** I read the spec, I read the tests, I read every line Claude generated, I read the diff before I committed. That ratio — read time to write time — is now the entire skill.
>
> If you walk away with one habit: before you accept any AI-generated code, **say out loud what you would have written instead.** If you can't, you don't understand it well enough to ship it. That's the bar. That's the 98/2. That's the Translator capability in your IDE.
>
> AI's value comes from your data — the spec, the tests, the constraints. Its security comes from your framework — your refusal, your logging, your error model. Vibe coding doesn't change the fundamentals. It just makes them visible faster."

---

## 7. Bridge to Mission 3 — TDD Speedrun (1 min)

> "If you want to feel this in your hands today, **Mission 3 — TDD Speedrun** is the one. Same loop: human writes the tests, AI writes the implementation. Thirty minutes. Ninety per cent coverage. The award goes to the team whose **rejected suggestions** were the most interesting — we'll ask you to keep a one-line note every time you said no to Claude. That note is the deliverable."

---

## Production checklist

- [ ] Claude Code installed and authenticated on demo laptop
- [ ] Test the venue Wi-Fi can reach `api.anthropic.com` (some venues firewall it)
- [ ] If blocked: have a hotspot ready as fallback
- [ ] `SPEC.md` template pre-staged at `demos/d3-vibe-coding-fallbacks/_template/SPEC.md` so I'm not formatting under audience eyes
- [ ] Three fallback prompts printed on a card in pocket
- [ ] HDMI for screen mirroring; **font size bumped to 18pt+ before stage**
- [ ] Terminal theme: high-contrast, dark — readable from 5m away
- [ ] If laptop fails: pre-recorded build (`demos/d3-vibe-coding-fallbacks/recording.mp4`) — shows the same pattern, narrate live over it

## Length flex

- **10-min compressed** → skip §3 (state the watch-points in 30s during the cold open), skip the manual rejection planning — just take whatever Claude does. One fallback prompt, S3 NRIC.
- **20-min default** → as written.
- **45-min workshop** → after the build, hand laptops to 3 audience teams; they each pick a tool and build it. I rove, narrate rejections in real time. End with one-minute show-and-tells.

## Voice notes (Ethan-isms to keep in)

- **Translator capability** explicitly named
- **Intellectual vs accountability labour** as the rejection-moment frame
- **"AI's value comes from your data, its security comes from your framework"** as a signature beat
- **"Bolt-on to a weak foundation"** if the spec discussion gets philosophical
- First person throughout: _"my number one concern"_, _"I'm watching for"_
- Define every tool name on first use (Claude Code, vibe coding, TDD)

---
_Status: drafted 2026-04-27. Fallback prompt scaffolds pending — see `demos/d3-vibe-coding-fallbacks/`._
