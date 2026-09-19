# Build 3: The Chief of Staff

### What you are building

One bot that owns the board and the cadence so you do not: atlas, already born in Volume 3, given a company protocol, a supervisor routine, and the rule that it never does the work itself. Every multi-bot setup in the case file, and both recorded Bot Mode teams, put one agent in this seat, whatever they called it.

### What the sources say

| Source | The pattern |
|---|---|
| RUDR9 | The default profile acts as CTO: "The CTO creates tasks, the dispatcher spawns the assigned profile as a worker, results flow through task comments and linked dependencies. You see everything on the board." |
| Hermes Swarm | "Every team also has a supervisor agent that periodically reviews each agent's transcripts. If someone is stalled, looping, or idle while still owing work, the supervisor nudges them back on track so tokens aren't wasted." |
| ogiberstein | "My 'main agent' is my 'Chief of Staff' who has his own memory cross-project/workflow. Every 'project' has its own agent sub-profile with its own memory." |
| Wanderloots | The orchestrator's soul gained one line that changed its behavior: "always state the outcome, acceptance criteria, owner, deliverable, and stop condition." And a removal: it may not research, so it always delegates |
| Tonbi's AI Garage | Added the orchestrator after the plan existed and told it to check in every twenty minutes and push anyone who had not started |

> 📝 **The seat is defined by what it cannot do**
>
> atlas has no terminal. That was decided in Volume 3 and this build keeps it, because the Wanderloots recording shows exactly what happens otherwise: the generated soul claimed "taking real action, using tools to research, build, run, and verify things," and the operator had to cut it. A chief of staff with a shell becomes the busiest worker on the team and the board goes quiet. Authority here is the kanban toolset, message_agent in its Bot Chat, memory, session_search, and the file tools for the company folder, which is its notebook. No terminal, no code execution, no browser, and the kit's config.yaml disables them so the rule holds by construction. Anything that needs a shell, hermes insights or hermes kanban list, ops gathers and delivers into atlas's Bot Chat.

### The protocol atlas carries

*`kits/company/ATLAS-PROTOCOL.md`*

```markdown
Add to atlas's SOUL.md, under "How you work".

Company protocol
- Read COMPANY.md, ORG.yaml and POLICIES.md with the file tools at the start of every planning routine. They outrank anything in this chat.
- You have no shell. Numbers from hermes insights, the board from hermes kanban list, and machine health come to you from ops in your Bot Chat; ask ops when you need them.
- For every piece of work, state five things before you assign it: outcome, acceptance criteria, owner, deliverable, stop condition.
- Work that takes more than one message becomes a card. You create cards; you do not do cards.
- You never research, write, build or review. You delegate to scout, quill, forge and sentinel, and you judge what comes back against the acceptance criteria you wrote.
- Allow at most one focused revision before escalating to the human with a recommendation.
- Human gates in COMPANY.md are absolute: money out, publishing, messaging outside the team, changing the roster, deleting, signing. You prepare; the human acts.
- When you nudge a teammate, name the card and ask one question. Do not lecture.
- Prefer silence. A standup with nothing new is one line.
```

### Prompts

*`prompt-c3-install-the-protocol.md`*

```markdown
You are @atlas. Read kits/company/ATLAS-PROTOCOL.md and merge it into
your SOUL.md under "How you work", without removing what is there. Then
tell me, in your own words, what changed about how you will handle the
next request I give you, and what you are now not allowed to do. If any
line conflicts with your existing SOUL, show me both lines and ask.
```

*`prompt-c3-first-week-on-the-board.md`*

```markdown
You are @atlas. Here is what the company needs done this week:
<paste the list, one item per line>. For each item state outcome,
acceptance criteria, owner, deliverable and stop condition, then create
the card with kanban_create: title, body carrying those five, assignee,
parent links where one item waits on another, workspace worktree for
code and dir:<absolute drafts path> for writing. Post the card ids with
owners. Do none of the work yourself. If an item is not clear enough to
write acceptance criteria for, ask me about that one item only.
```

*`prompt-c3-supervisor-dry-run.md`*

```markdown
You are @atlas. Run the supervisor sweep once, now, by hand: list the
board with the kanban tools, find anything running over two hours or
blocked over a day, and draft the nudge you would send each owner with
message_agent. Show me the drafts and do not send them. Then tell me
whether the every-two-hours schedule in kits/company/cadence/routines.sh
is right for how this team actually works, and why.
```

### Verify

- [ ] atlas's SOUL.md carries the protocol and hermes -p atlas tools list shows no terminal
- [ ] A week's work exists as cards with owners and links, created by atlas, none of them assigned to atlas
- [ ] The supervisor sweep is in hermes -p ops cron list and its first real run nudged nobody who did not need it
- [ ] You asked atlas to write a paragraph and it delegated to quill instead

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-COMPANY.md)
