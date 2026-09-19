# Build 8: Learn While You Run

### What you are building

The mechanism that makes the company better every week without you rewriting prompts: corrections become dated rules in POLICIES.md, repeated corrections become changes to a bot's own instructions, and repeated workflows become skills. This is the single most repeated pattern in the case file, and it is the one that separates operators who are still running from operators who quit.

### What the sources say

| Source | The loop |
|---|---|
| Gumroad | "When Gumclaw makes a mistake, the correction becomes a dated policy rule that every future session must read." |
| HolmeBengt | "Every time I correct something Hermes wrote, the before-and-after gets saved to Notion with notes on what was wrong and why my version was better. On Saturdays, Hermes analyzes the full collection looking for patterns in my corrections. Then it updates its own system prompt to fix those patterns permanently." |
| riceinmybelly | MEMORY.md capped at 2,200 characters, his own convention rather than a Hermes limit, for behavioral rules only; lessons too detailed for it go to Meta/hermes-learnings/ in the vault. His own caveat on the whole setup: "nowhere near an example to follow" |
| aakashgupta | "it writes its own skills. My competitive briefing went from 20 min to 8 min over 6 weeks. Same prompt." |
| Yashica Jain | "Every time you do something, for example, using Hermes to write a LinkedIn post, it uses that experience to create a new skill." |
| Better Stack | "Brand new session test: it recalled everything, including preferred emojis." |
| Wanderloots | refine at the end of a session "will review the conversation and save what it needs to its own skills and memories"; @all plus an explicit memory instruction does it for a room. The orchestrator learned where raw reports go and never had to be told again |
| HolmeBengt, the warning | "Thirty-plus skills means thirty-plus things that can break when APIs or Hermes itself updates." |

> 📝 **What the kit gives Build 8**
>
> Three templates: kits/company/POLICIES.md for the fast loop, kits/company/corrections/README.md for the format of a saved correction, and kits/company/SKILLS-LEDGER.md for the skills you build and must retest after every update.

> 📝 **Three files, three speeds**
>
> POLICIES.md is the fast loop: one dated line the day something goes wrong, read by every bot before work. A bot's SOUL.md or MEMORY.md is the weekly loop: only after the same correction shows up three times does a rule move into the bot's own instructions, and MEMORY.md stays small on purpose. A skill is the slow loop: a workflow you have run five times the same way becomes a file with a name, and gets a line in the ledger of things that can break on the next update.

### Prompts

*`prompt-c8-correction-to-rule.md`*

```markdown
You are @atlas. I just corrected <bot> on <what happened>. Write the
POLICIES.md line in the kit's format, dated today, naming the bot, the
rule and the why in one sentence each. Show me the line. When I approve,
append it, then message <bot> with message_agent: quote the new rule and
ask it to confirm in one line how its next similar task changes.
```

*`prompt-c8-saturday-patterns.md`*

```markdown
You are @quill. Read every file in <company folder>/corrections/ (each
one holds a before, an after, and my note on why mine was better). Find
the patterns: filler words, wrong register for the channel, over-
explaining, invented specifics, anything that appears three times or
more. For each pattern propose the exact line to add to your SOUL.md
under Voice. Show me the proposals with the three examples behind each.
Change your SOUL only when I say which ones.
```

*`prompt-c8-workflow-to-skill.md`*

```markdown
You are @<bot>. We have done <the workflow> the same way at least five
times; find the sessions with session_search and read how it actually
went. Write a skill with skill_manage: a name, when to use it, the steps
as we really run them, the checks that caught mistakes, and the output
format. Keep it to one job with no dependencies. Then run it once on
<a real input> and show me the result next to the last manual run. Add
the skill's name to <company folder>/SKILLS-LEDGER.md with today's date
and the Hermes version, so we know what to retest after an update.
```

*`prompt-c8-end-of-session.md`*

```markdown
@all Before we close: each of you, update your own memory with anything
you learned in this session that will save a step next time. Say in one
line what you saved, or say nothing if there was nothing. atlas, check
that no two of you saved contradicting rules.
```

### Verify

- [ ] POLICIES.md has a rule dated this week that came from a real mistake, and the bot that made it confirmed the change
- [ ] A Saturday pass over your corrections produced at least one SOUL.md line you accepted
- [ ] One repeated workflow is now a skill, ran once on real input, and is listed in SKILLS-LEDGER.md with a version
- [ ] MEMORY.md on every bot is still short after a month (riceinmybelly caps his at 2,200 characters; pick your line and hold it)

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-COMPANY.md)
