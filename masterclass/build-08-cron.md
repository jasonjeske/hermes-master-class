# Build 8: Cron

![Build 8](../assets/art/part-06.webp)

### What you are building

Scheduled jobs that carry their whole briefing in the prompt, deliver where you actually read, stay silent when nothing is wrong, and cost zero tokens when no reasoning is needed.

### What the docs say

Checked against the Cron page.

| Fact | Detail |
|---|---|
| The gateway must run | Cron lives inside the gateway process. No gateway, no ticks. `hermes gateway setup` from Build 0 |
| Fresh session, every run | A job runs with no chat history and, unless it carries `--workdir`, no context file. The prompt plus the attached skills are the entire briefing |
| Creating | `hermes cron create "<schedule>" "<prompt>" [--skill <name>]... [--workdir /abs/path] [--model <m> --provider <p>] [--reasoning-effort <level>] [--name <name>] [--paused]`. From a chat, `/cron add ...` takes the same shape, and the agent's own `cronjob` tool creates jobs when you ask it to |
| Delivery | The final response is delivered automatically to the origin chat by default, or to explicit targets like `telegram:<chat_id>`, `discord:#channel`, `local`, `all`, or `origin,all`. Do not have the prompt call a send tool for its main delivery |
| Silence | A successful run whose final response contains `[SILENT]` delivers nothing; the output is still saved under `~/.hermes/cron/output/` for audit. Failed runs always deliver, so a broken monitor cannot go quiet |
| Zero tokens | `--no-agent --script <path>` runs a script with no model call at all. Stdout is the message, empty stdout is a silent tick, a non-zero exit or timeout delivers an error |
| Per-job models | A job can pin its own model, provider and reasoning effort. Unpinned jobs snapshot the model at creation; `hermes cron resnap` refreshes that after you change models |
| Operating | `hermes cron list`, `run <id>` (fire now), `pause`, `resume`, `remove`, `edit`, `runs <id>`, `incidents`, and `hermes cron doctor` for a read-only fleet health check. `hermes pause` is the global stop |

### The prompt discipline

The most common cron mistake follows straight from the fresh-session design. A prompt that would work in a conversation, because the conversation carried the context, fails at three in the morning because nothing carries it.

| Bad | Good |
|---|---|
| "Check on that server issue" | "SSH to 203.0.113.10 as deploy. Run systemctl status nginx. Fetch https://example.com and confirm HTTP 200. If both are healthy reply with only [SILENT]. Otherwise report which check failed and the exact output." |
| "Summarize the news" | "Using the blogwatcher skill, read the feeds it defines, and write five bullets of what changed since yesterday, each with a link. If nothing changed, reply with only [SILENT]." |

### Commands

*`cron-jobs.sh`*

```bash
# 1. A morning brief that knows your project, delivered to Telegram
hermes cron create "every day at 07:30" \
  "Read AGENTS.md in this directory. List open pull requests with gh, summarize CI status, and list any issue labeled urgent. Five lines maximum, links included. If there is nothing open and CI is green, reply with only [SILENT]." \
  --workdir /absolute/path/to/your/repo \
  --name "morning-brief"

# 2. A zero-token watchdog: the script is the job
hermes cron create "every 5m" \
  --no-agent \
  --script /absolute/path/to/disk-watchdog.sh \
  --deliver telegram \
  --name "disk-watchdog"

# 3. The weekly tool-surface canary from Part 12, pinned to a cheap model
hermes cron create "every sunday 08:00" \
  "List every toolset and every tool currently available to you. Compare against the list saved at ~/hermes-tool-baseline.txt. If they match, reply with only [SILENT]. If anything disappeared or appeared, report the difference and overwrite the baseline file with the new list." \
  --model your-inexpensive-model \
  --name "tool-canary"

# Operate
hermes cron list
hermes cron run morning-brief
hermes cron doctor
```

*`disk-watchdog.sh`*

```bash
#!/bin/sh
# Prints nothing when healthy. Anything printed is delivered.
use=$(df -P / | awk 'NR==2 {gsub("%","",$5); print $5}')
if [ "$use" -ge 85 ]; then
  echo "Disk on / is at ${use}%"
fi
```

### Prompts

*`prompt-08-create-job.md`*

```markdown
Create a cron job for me. Do these in order.

1. Read the sections on delivery, [SILENT], and per-job models at
   https://hermes-agent.nousresearch.com/docs/user-guide/features/cron
   and tell me in four lines how a job gets its context, where its output
   goes by default, and what [SILENT] does.
2. Here is the job: <what it should do, when, and where I read the
   result>.
3. Write the job prompt as if for a stranger with no history: every path
   absolute, every check explicit, the silent condition stated, the
   report format stated. Attach the skills it needs. If it needs a
   project, set --workdir.
4. Show me the exact hermes cron create command, or the cronjob tool call,
   before creating it. After I say go, create it, run it once with
   hermes cron run, and show me the output from ~/.hermes/cron/output/.
```

*`prompt-08-audit-jobs.md`*

```markdown
Run hermes cron list and hermes cron doctor. For every job tell me: name,
schedule, whether it is pinned to a model, its last status, and one of
keep, fix, or remove with a reason. Flag any job whose prompt relies on
context it cannot have in a fresh session. Do not change anything.
```

### Verify

- [ ] hermes cron list shows each job with the schedule you intended
- [ ] hermes cron run <name> delivers to the place you read, and the output file exists under ~/.hermes/cron/output/
- [ ] The watchdog delivers nothing when healthy and one line when you force the threshold
- [ ] hermes cron doctor reports every job healthy

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
