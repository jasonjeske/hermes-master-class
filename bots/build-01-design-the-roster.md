# Build 1: Design the Roster

![The roster, and who talks to whom](../assets/art/v3-message-paths.webp)

### What you are building

A roster written down before any bot exists: roles drawn from work you actually do every week, names that resolve as tags without colliding, a size the machine can keep warm, and a section layout that will still make sense in a month.

### What the docs say

Checked against the Bot Mode page: Creating a Bot, renamed Bots keep their tags in sync, Organize bots into sections, Warm Bot Backends, and the Kanban page's cost strategy.

| Rule | Why |
|---|---|
| Roles come from repeated work | The docs' own examples are specialists: a researcher, a reviewer, a scribe. A Bot earns its place by owning a kind of work that recurs, because it accumulates memory and skills only for what it does repeatedly |
| Names are tags | A Bot titled Research Buddy answers to `@research-buddy` and `@researchbuddy`; the profile name is matched first and can never be hijacked by a friendly name; a friendly name shared by two Bots is refused. Pick short, distinct, pronounceable names |
| The primary stays `@hermes` | Rename it Maia and prompts introduce it as `@maia`, but `@hermes` keeps working as an alias for the primary |
| Start at the warm limit | Warm Bot Backends defaults to 3. A fourth open Bot waits up to 30 seconds for a slot. Start with three bots doing real work, raise the setting and the machine's memory together when you add more |
| Sections are yours | Folders like Clients or Team, stored in each Bot's profile metadata, so a section follows the Bot to every desktop connected to that backend |
| Planner and workers | The Kanban page's cost strategy applies to rosters: decomposing work needs frontier-level judgment, executing a well-specified card usually does not, and workers are where the tokens go. Restrict the planner's toolsets so it cannot do the implementation work itself |

### The roster this volume ships

| Bot | Title | Owns | Talks to |
|---|---|---|---|
| atlas | Chief of staff | planning, routing, the standup, escalation to you | everyone; @user for decisions |
| scout | Researcher | finding out what is true, with sources | atlas, quill, forge on request |
| forge | Engineer | implementing well-specified changes, proving them | atlas for design questions, sentinel for review |
| quill | Writer | briefs, posts, docs, messages for a named reader | scout for missing facts, sentinel for review |
| sentinel | Reviewer | the last check before you: code, copy, plans, numbers | forge and quill with findings, atlas with blocks |
| ops | Operator | routines: briefs, sweeps, health, backups, weekly numbers | you, silently unless something is wrong |

Six is the full team. Three is the day-one team: atlas, forge and ops cover planning, doing and keeping the lights on. Add scout when research becomes a bottleneck, quill when you publish, sentinel when a mistake would cost you.

> 📝 **From the field: let a bot design the roster**
>
> Tonbi's most reusable idea is a meta-bot he calls bot HR, whose only job is to read a project brief and create the other bots for it, choosing their roles and models. His description for it was one sentence: "you are a bot who makes other bots based on project requirements and tells them their role." Handed a game spec, it split the work into render, gameplay, technical art and browser QA, created four profiles with a shared working directory, wrote each SOUL with a mission, and picked a different model for each with a stated reason. The gateway RPC the desktop uses for that, `profiles.create`, is documented on the Desktop Plugin SDK page, and the CLI twin is `hermes profile create`. Build 9 turns this into a prompt you can paste.

### Prompts

*`prompt-b1-design-my-roster.md`*

```markdown
Design my bot roster from evidence, not from imagination. Do these in order.

1. Read https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode
   sections "Creating a Bot", "Organize bots into sections" and "Warm Bot
   Backends", and the "Cost strategy" section of
   https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban.
2. Use session_search over my last four weeks and list the kinds of work I
   asked for repeatedly, with a count each. Ignore one-offs.
3. Propose a roster of at most five bots. For each: a one-word lowercase
   name that will read well as an @tag, a title, one sentence of what it
   owns, who it will talk to, and whether it is a planner (no terminal) or
   a worker.
4. Tell me which three to create first and why, given that my desktop keeps
   three backends warm.
5. Stop. Do not create anything.
```

### Verify

- [ ] Your roster document names at most five bots, each tied to work you did more than once this month
- [ ] Every name is lowercase, one word, and unlike every other name when spoken aloud
- [ ] Exactly one bot is the planner and its toolsets exclude the terminal
- [ ] You know which three you are creating first

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-BOTS.md)
