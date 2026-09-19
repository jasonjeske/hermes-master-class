# Build 4: Production Lines

![The gate is the product](../assets/art/v4-production-line.webp)

### What you are building

The things your company makes, written down as lines: brief in, research, draft, review, your gate, publish, ledger entry. One file per line, one card per step, the same shape for a blog post, a client report, a video script or a software release. The front end is a brainstorming session that refuses bad ideas, the back end is a gate only you can open.

### What the sources say

| Source | The line they run |
|---|---|
| cyrilXBT | "It researches the topic, writes the script, formats the slides, outputs in the exact dimensions TikTok needs. 10 slideshows a week manually takes 30-40 hours. With Hermes it takes the time to review and approve." |
| Metics Media | The exact routine prompt: "Research the top trending AI tools right now and come back with the top three that would make for an interesting tutorial video. Create a new skill based on your approach and call it YouTube-video-research. Can you set up a weekly job that runs every Monday at 9:00 AM using that skill?" |
| kenmazaika | Dictation on the phone, a dedicated Telegram topic, a structured outline with a "riff" section of connections, a local markdown file, then a document generated from it. "Automate the 97%, don't kill the project trying to automate the last 3%." |
| mvanhorn | "Weekly podcast digest replaced 10+ hrs of listening with a 2hr Hermes workflow." Content ops: blogs, cold emails, lead scraping |
| Wanderloots | Research, orchestrator quality check with one revision, human approval, librarian files it. The orchestrator rejected a first draft because "the evidence base is vendor authored and contains no 2026 study," and the operator agreed |
| Tonbi's AI Garage | A brainstorming skill the agent wrote itself over months: orient, research the reality, find the wedge, a verdict of yes, maybe or no, keep a living record, hand off a spec. "It's not sycophantic. It's not just going to be a yes man." |

> 📝 **From the field: the idea goes in through a bot that says no**
>
> Tonbi's brainstorming agent lives on a seven-year-old laptop, runs a mid-tier model because the frontier one "is way overkill for this, and it's too slow," and its whole job is to take a half-formed idea and pressure-test it against what exists, who pays, and what the smallest first offer would be. The output is a spec with five sections: original spark, destination, open uncertainty, validation plan, recommended first offer. His rule: the agent does not generate the idea, you bring it; the agent researches and challenges it. That spec is the brief a production line starts from.

### The file

*`kits/company/production/LINE-TEMPLATE.md`*

```markdown
# Production line: <name>

One line makes one kind of thing, the same way every time. Copy this file per line into <company folder>/lines/<name>.md. atlas turns a filled-in line into cards; the human holds the gate.

## What comes out
- Deliverable: <a post, a video script, a report, a proposal, a release>
- Where it lands: <path, channel, repository>
- The ledger entry when it ships: <ledger_add category and amount, or "none">

## What goes in
- Brief: one paragraph from the human, or an item from a routine (research watch, dictation inbox, a client request)
- Sources allowed: <list; "any public source with a citation" is a fine default>
- Sources forbidden: <client data outside the client's folder, anything under an NDA, personal accounts>

## Steps, each a card
| Step | Owner | Input | Output | Done means |
| research | scout | brief | sources.md with citations and counter-evidence | every claim has a source, gaps are named |
| draft | quill or forge | sources.md | draft in the drafts folder | reads in the house voice, nothing invented |
| review | sentinel | draft | verdict with ranked findings | approve, changes requested, or blocked |
| gate | human | verdict and draft | approve or send back | your word in the card |
| publish | ops | approved draft | the deliverable where it lands, plus a ledger entry | the URL or path is in the card |

## Rules this line follows
- POLICIES.md applies. Corrections to this line become dated rules there.
- No step publishes, sends, pays or deletes. Only ops publishes, only after the gate.
- A line that needs a new tool gets it on the owner's profile, not on everyone's.

## Numbers
- Cycle time target: <hours from brief to gate>
- Cost target per unit: <from hermes insights; fill in after the first five>
- First five units: dates, cycle time, cost, and what you changed after each
```

### Prompts

*`prompt-c4-pressure-test-an-idea.md`*

```markdown
You are @scout, acting as a brainstorming partner, not a cheerleader. I
have a half-formed idea: <one or two sentences>. Work in five moves.
Orient: ask me at most three questions that change what you would
research. Research the reality: who does this today, what they charge,
what the buyers complain about, with sources. Find the wedge: the
narrowest version a real person would pay for first. Verdict: yes, maybe
or no, with the reason, and change your verdict as evidence comes in.
Record: write <company folder>/ideas/<slug>.md with sections original
spark, destination, open uncertainty, validation plan, recommended first
offer. Do not flatter the idea. If it is a no, say so and say why.
```

*`prompt-c4-define-a-line.md`*

```markdown
You are @atlas. We are going to make <the deliverable> repeatedly. Copy
kits/company/production/LINE-TEMPLATE.md to <company folder>/lines/<name>.md
with the file tools and fill it in from these facts: <where it lands, who
the reader is, what sources are allowed, the house voice, the cadence>.
Owners come from ORG.yaml. The gate step is always the human. Show me the
file and the one step you think will fail first and why.
```

*`prompt-c4-run-the-line-once.md`*

```markdown
You are @atlas. Run <company folder>/lines/<name>.md once for this brief:
<paragraph>. Create one card per step with kanban_create, linked in
order so each waits on the previous, owners from the line file, the
review card carrying the definition of done from the line. When the
review card reaches done, message me with the verdict and the path to
the draft, and stop. Nothing publishes until I comment approve on the
gate card.
```

*`prompt-c4-weekly-research-watch.md`*

```markdown
You are @scout. Create a routine on yourself: every Monday at 09:00,
research what changed in <the niche> in the last seven days, pick the
three items most worth making something about, and for each write two
lines: why now, and which production line it feeds. Save the result to
<company folder>/inbox/watch-<date>.md and deliver the three items to
atlas's Bot Chat. Show me the hermes cron create command before you run
it, with the schedule "every monday at 09:00" and --deliver bot-chat:atlas.
```

### Verify

- [ ] One line file exists with every step owned by a bot that has the tools that step needs
- [ ] A brief went in and a reviewed draft came out without you touching a step between the brief and the gate
- [ ] The gate card waited for your comment; nothing reached its destination before it
- [ ] The first unit's cycle time and cost are written at the bottom of the line file
- [ ] A bad idea got a no from the pressure test, with sources

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-COMPANY.md)
