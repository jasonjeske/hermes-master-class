# Build 7: The Cadence

![The company runs on routines you can read](../assets/art/v4-cadence-wheel.webp)

### What you are building

The clock the company runs on: a standup that reads the board, a supervisor sweep that catches stalls, a Sunday page, a month end, a nightly dreaming pass and a health check that stays silent. All of it as routines you can list, read, pause and edit, owned by the bot that should own each. Plus the two places you look: the board and the standup room.

### What the sources say

| Source | Their clock |
|---|---|
| HolmeBengt | 03:00 Dreaming, 06:30 Daily Status Report ("This is not the news. This is the tactical dashboard."), 12:00 Health Coach, 21:00 Study Audit, Saturdays writing analysis, Sunday 18:00 Finance Review, the 28th at 20:00 monthly P&L, every four hours infrastructure monitoring, every morning a compressed config backup |
| Gumroad | "cron jobs wake it up to check support tickets, watch X mentions, work on engineering tasks, update finance docs, and follow up on previous work" |
| Hermes Swarm | A supervisor that "periodically reviews each agent's transcripts" and nudges the stalled, the looping and the idle; a dashboard with a network graph of who is talking to whom |
| Tonbi's AI Garage | The orchestrator checks the room every twenty minutes and pushes anyone who has not started; the operator's own note is that with no tool calls visible in a room he kept doubting work was happening, and threads fixed it |
| stan_frbd | Daily lesson, daily backup "no LLM involved", daily wiki lint, daily dream, daily articles |
| Hermes docs and hermes cron create --help | A routine's --deliver can be bot-chat:<profile> (Cron page), which drops the output into that bot's Bot Chat as a message it answers; --monitor-script (in the command's own help, not yet on the docs page) runs a cheap script first and only wakes the model when its output changed byte for byte |

> 📝 **Two tricks newer than every operator write-up**
>
> Delivering a routine to bot-chat:atlas means the standup is not a report you read, it is a message atlas answers, in its own chat, with the board in front of it; it is also the only way a scheduled job reaches message_agent, which exists in Bot Chat sessions and nowhere else, so every kit routine that needs a teammate nudged is delivered to atlas rather than told to message anyone. And --monitor-script turns a noisy watch into a quiet one: a script prints the state, the model runs only when the bytes changed. The first is used throughout the kit's routines; the second is added by the quiet-watch prompt below.

### The routines the kit ships

*`kits/company/cadence/routines.sh`*

```bash
#!/bin/sh
# Company cadence. ops owns everything that needs a shell (hermes insights, hermes kanban list, ledger_report) and
# delivers into atlas's Bot Chat with --deliver bot-chat:atlas; atlas owns what needs judgment and the kanban, file
# and session_search tools it has. A routine runs in a fresh session with no chat history and no message_agent;
# the Bot Chat reply that a delivery triggers does have message_agent, which is how atlas nudges owners.
# Schedules: "every day at 08:00", "every sunday 18:00", "every 2h", or a cron expression like "0 20 28 * *".
# Replace <company folder> with the absolute path before running. Run once: sh kits/company/cadence/routines.sh

# Daily standup: atlas reads the board with the kanban tools and the company files with the file tools.
hermes -p atlas cron create "every day at 08:00" \
  "Standup. Read <company folder>/ORG.yaml and <company folder>/POLICIES.md with the file tools, then list the board with the kanban tools. Post one line per bot: what is running, what is blocked and why, what finished since yesterday. End with the one decision that is the human's today, or [SILENT] if there is none and nothing is blocked." \
  --name "standup" --deliver bot-chat:atlas

# Supervisor sweep: the Hermes Swarm pattern. ops finds the stalled cards; atlas, in its Bot Chat, nudges the owners.
hermes -p ops cron create "every 2h" \
  "Supervisor sweep. Run hermes kanban list. List every card in running for more than 2 hours, blocked for more than 24 hours, or in review for more than 4 hours: card id, title, owner, how long. If the list is empty reply with only [SILENT]. Otherwise start the reply with '@atlas these cards look stalled. Message each owner with message_agent: name the card and ask for a one-line status or a kanban_block with the reason. Do not create or close cards.' followed by the list." \
  --name "supervisor-sweep" --deliver bot-chat:atlas

# Sunday numbers: ops gathers the figures, atlas writes the page and the one decision.
hermes -p ops cron create "every sunday 18:00" \
  "Sunday numbers, data pass. Call ledger_report for this month. Run hermes insights --days 7 and hermes insights --days 14 for tokens and cost per profile. Run hermes kanban stats. Reply with the raw figures grouped as money, fleet cost this week versus last, board, and then the line '@atlas write this week's Sunday page from these figures: money in, money out, net; fleet cost this week versus last; cards shipped, cards blocked, the oldest open card; the one number from <company folder>/COMPANY.md and its trend; end with exactly one recommended decision for the human.' Deliver even when unchanged." \
  --name "sunday-numbers" --deliver bot-chat:atlas

# Month end: same split. ops gathers, atlas writes the P and L, the retro and the proposed rules.
hermes -p ops cron create "0 20 28 * *" \
  "Month end, data pass. Call ledger_report for this month and for last month. Run hermes insights --days 30. Run hermes kanban stats. Reply with the raw figures, then the line '@atlas write the month end: P and L, month over month variance by category, the fleet's model spend; a retro of three things that worked and three that did not, each tied to a card id or routine name; then read <company folder>/POLICIES.md and propose new dated rules for anything that went wrong twice. Propose only; the human edits POLICIES.md.'" \
  --name "month-end" --deliver bot-chat:atlas

# Nightly dreaming: the HolmeBengt pattern, owned by atlas with session_search, the file tools and the memory tool.
hermes -p atlas cron create "every day at 03:00" \
  "Dreaming. Using session_search over the last 24 hours across the team, extract decisions made, cards moved, mistakes that must not repeat, and open questions. Write a dated summary to <company folder>/journal/<date>.md with the file tools and update MEMORY.md with the memory tool with at most two behavioral rules if a mistake repeated. Reply with the file path and three lines." \
  --name "dreaming"

# Health every four hours, silent when fine. ops owns machines.
hermes -p ops cron create "every 4h" \
  "Health. Run hermes doctor and hermes gateway status. Check that the always-on box answers (ping the host named in <company folder>/ORG.yaml if any). Check free disk. If everything is healthy reply with only [SILENT]; otherwise three lines: what, since when, what you recommend." \
  --name "health-4h"
```

### The two places you look

| Place | What it shows | When |
|---|---|---|
| The Kanban page in the Desktop, or hermes kanban list and stats | every card, its owner, its status, its thread | any time, and at the standup |
| The standup room from Volume 3 (atlas, forge, scout, quill, sentinel) | the one conversation where the day gets settled, threads for side questions | 08:00, after atlas posts the standup line in its Bot Chat |

### Prompts

*`prompt-c7-install-the-clock.md`*

```markdown
You are @ops. Read kits/company/cadence/routines.sh. For each routine
tell me: owner, schedule, what it reads, what it delivers, and its
silent condition. Flag any two routines that would collide (same hour,
same board reads) and any routine whose owner lacks a tool it needs.
Then show me the exact commands with <company folder> replaced by the
real path, and run them only when I say go. Afterward read back
hermes -p atlas cron list and hermes -p ops cron list and prove each job
exists by name.
```

*`prompt-c7-quiet-watch.md`*

```markdown
You are @ops. Turn the health routine into a monitor: write
~/.hermes/scripts/health-state.sh that prints, one per line, gateway
status as a word, disk as ok or low against a 20 GB line (never the raw
number, the output must be byte-stable), and the reachability of the
always-on box from ORG.yaml as up or down. Then recreate the health routine with --monitor-script
health-state.sh so the model runs only when a line changes. Show me the
command first. Test by stopping nothing; just confirm two consecutive
ticks stayed silent.
```

*`prompt-c7-first-standup.md`*

```markdown
@atlas @forge @scout @quill @sentinel Standup. atlas has posted the
board summary in its Bot Chat; each of you, one line: what you finished
since yesterday, what you are on, what you are blocked on, by card id.
Questions go in threads, not in the room. atlas closes with the one
decision that is mine today, or says there is none.
```

### Verify

- [ ] hermes -p atlas cron list and hermes -p ops cron list show every routine from the kit by name
- [ ] The 08:00 standup arrived in atlas's Bot Chat and atlas answered it with the board open
- [ ] The supervisor sweep nudged a card you had deliberately left running, and nothing else
- [ ] The health routine stayed silent for a whole day on a healthy machine
- [ ] The Sunday page and the month end both delivered even when nothing changed

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-COMPANY.md)
