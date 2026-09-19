# Build 4: Routines

![Build 4](../assets/art/part-06.webp)

### What you are building

Recurring work attached to the bot that owns it: a morning standup from atlas, a health brief and a nightly backup from ops, a source watch from scout. Each one silent when nothing happened, each one landing in that bot's own chat where you would have asked anyway.

### What the docs say

Checked against the Bot Mode page (Routines) and the Cron page.

| Fact | Detail |
|---|---|
| The pane | The Routines pane docks beside the chat while the Bots tab is active; a structured schedule picker builds the schedule, with an Advanced field for the raw Hermes schedule string |
| What a routine is | A plain Hermes cron job namespaced `[bot:<name>] <routine>`. It shows in `hermes cron list` and the core Cron page. Runs land in the Bot's own chat history |
| The CLI twin | `hermes -p <bot> cron create "<schedule>" "<prompt>" --name "<routine>"`, run under that bot's profile so the job belongs to it |
| Fresh session, every run | No chat history, no context file unless the job carries `--workdir`. The prompt plus the attached skills are the whole briefing |
| Silence | A final response containing `[SILENT]` delivers nothing and is still saved for audit. Failed runs always deliver |
| Per-job pins | A routine can pin its own model, provider and reasoning effort |
| Health | `hermes cron doctor` is the read-only check across every job; `hermes cron runs <id>` shows attempts; `hermes pause` is the global stop |

### The routines the kit ships

*`kits/bot-team/ops/routines.sh`*

```bash
#!/bin/sh
# Ops routines: the bot with a terminal gathers, and delivers where the decision gets made.
# Run once: sh kits/bot-team/ops/routines.sh (the -p flag scopes each job to the ops profile).
# Schedules the parser accepts: "every day at 07:30", "every sunday 18:00", "every 2h", or a cron expression.
# Every prompt is self-contained: a routine runs in a fresh session with no chat history and no message_agent;
# --deliver bot-chat:<profile> drops the output into that bot's Bot Chat as a message it answers, and there it can message teammates.

hermes -p ops cron create "every day at 07:30" \
  "Morning brief. Run hermes doctor, hermes cron doctor and hermes memory status and read their output. Then run hermes kanban list --status blocked and hermes kanban list --status running and pick out cards older than 24 hours. Report in four lines: machines, jobs, memory, board. If everything is healthy and nothing is stuck, reply with only [SILENT]." \
  --name "morning-brief"

hermes -p ops cron create "every day at 22:00" \
  "Nightly backup. Run hermes backup --quick --label nightly and report the path and size in one line. On failure report the exact error." \
  --name "nightly-backup"

hermes -p ops cron create "every sunday 18:00" \
  "Weekly numbers. Run hermes insights --days 7 and hermes insights --days 14 and summarize this week's tokens, cost and the three most active profiles in five lines, with last week's figures next to them. Deliver even when unchanged." \
  --name "weekly-numbers" --deliver bot-chat:atlas

hermes -p ops cron create "every 2h" \
  "Board sweep. Run hermes kanban list. List every card in running for more than 2 hours, blocked for more than 24 hours, or in review for more than 4 hours: card id, title, owner, how long. If the list is empty reply with only [SILENT]. Otherwise start the reply with '@atlas these cards look stalled; message each owner for a one-line status or a kanban_block with the reason:' followed by the list." \
  --name "board-sweep" --deliver bot-chat:atlas
```

*`kits/bot-team/atlas/routines.sh`*

```bash
#!/bin/sh
# Atlas routines. Atlas has no terminal: its routines use the kanban tools, the file tools and session_search, never the shell.
# Anything that needs a shell (hermes insights, hermes kanban list, hermes doctor) is gathered by ops and delivered into
# atlas's Bot Chat with --deliver bot-chat:atlas; atlas answers there, where message_agent exists.
# Run once: sh kits/bot-team/atlas/routines.sh

hermes -p atlas cron create "every day at 08:00" \
  "Standup. Use the kanban tools to read the board (every card, its status and owner) and session_search for what each teammate reported since yesterday. Write a standup in the shape done, in progress, blocked, needs you, one line per item, owners named. End with the one decision that is the human's today, or [SILENT] if the board is empty and nothing is blocked." \
  --name "standup" --deliver bot-chat:atlas

hermes -p atlas cron create "every saturday 17:00" \
  "Weekly review. Use the kanban tools to list this week's completed cards and session_search to find the weekly numbers ops delivered. Write five lines: what shipped, what slipped and why, what to stop, what to start, and the one decision that needs the human. Deliver even when short." \
  --name "weekly-review"
```

*`kits/bot-team/scout/routines.sh`*

```bash
#!/bin/sh
# Scout routine: a watch on the sources that matter to the team. Edit the list in the prompt.
# The result is delivered into atlas's Bot Chat; atlas decides who needs to hear it and messages them from there.
# Run once: sh kits/bot-team/scout/routines.sh

hermes -p scout cron create "every day at 06:30" \
  "Source watch. Read the Hermes Agent documentation changelog page, the Hermes GitHub releases page, and the two feeds named in your MEMORY.md under 'watch list'. For anything new since yesterday that changes how the team works (a renamed command, a new setting, a breaking change), write one line with the link and which teammate it affects. If nothing changed, reply with only [SILENT]. Otherwise start the reply with '@atlas source watch found changes that affect the team:' followed by the lines." \
  --name "source-watch" --deliver bot-chat:atlas
```

> ⚠️ **Three things a routine cannot do, and the flag that fixes two of them**
>
> A routine runs in a fresh headless session. It has no chat history, it has no message_agent (that tool exists only in canonical Bot Chat sessions), and @user means nothing to it, because a routine's output goes wherever its delivery target says. So a routine never "messages a teammate"; it gathers and reports. The kit's answer is --deliver bot-chat:<profile>: the output lands in that bot's Bot Chat as a message the bot answers, and in that reply the bot does have message_agent. That is why ops runs the board sweep and delivers it to atlas, and why the schedule strings read every day at 07:30 and every sunday 18:00: the parser accepts those, a cron expression, and plain intervals such as every 2h, and rejects every 1d at 07:30 even though an older docs example shows it.

> ℹ️ **Who gets a routine**
>
> Workers do not, by default. forge, quill and sentinel receive work as cards and messages; a routine on a worker is usually a sign that the planner should be sending it a card instead. The three bots with standing routines are the ones whose job is to look: the operator at the machines, the chief of staff at the board, the researcher at the sources.

### Prompts

*`prompt-b4-add-a-routine.md`*

```markdown
You are <bot>. Add a routine for yourself. Read
https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode section
"Routines" and the "[SILENT]" and "delivery" sections of
https://hermes-agent.nousresearch.com/docs/user-guide/features/cron. The
routine: <what, when, and what counts as nothing to report>. Write the
prompt for a stranger with no history: every path absolute, every check
explicit, the silent condition stated, the report shape stated. Show me the
exact cronjob tool call or hermes cron create command, then create it after
I say go, run it once, and show me the output in this chat.
```

### Verify

- [ ] hermes -p ops cron list, hermes -p atlas cron list and hermes -p scout cron list each show the jobs by name (the Routines pane adds its own [bot:<name>] prefix only to jobs it creates)
- [ ] hermes -p ops cron run board-sweep either ends in [SILENT] or lands in atlas's Bot Chat, where atlas answers it
- [ ] hermes cron doctor reports every routine healthy
- [ ] The Routines pane in the app lists the same jobs the CLI does

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-BOTS.md)
