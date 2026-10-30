# Stage 7: Cap the Runaways

### What this stage changes

Every stage so far shrank a cost you pay on every call. This one bounds the costs that have no ceiling at all: a task that keeps calling tools, a fan-out of subagents, a search loop on a weak model, a cron job that wakes a full agent on your best model every morning. Nothing here moves the fixed budget. A cap costs you nothing until a job hits it, and then it is the difference between a stopped turn and a bill.

Turn caps, the budget warning and reasoning effort are in [Volume 1 Build 10](https://github.com/jasonjeske/hermes-master-class/blob/main/masterclass/build-10-tuning-and-safety.md), and Build 10 has the effort key right: `agent.reasoning_effort` is read on every surface even though config ships no default for it, and `/reasoning <level> --global` writes it cleanly. This stage covers what Build 10 does not.

### Open budgets

What v0.22.5 lets run without a ceiling, surface by surface:

| What can run long | The ceiling in v0.22.5 | Where you set one |
|---|---|---|
| Agent turns in the CLI or a gateway chat | None: `agent.max_turns` is empty, and empty means unlimited | `agent.max_turns` |
| Agent turns in the TUI | 500 when `agent.max_turns` is empty | `agent.max_turns` |
| A one-shot run with `hermes -z` | None: the one-shot path passes no cap | No setting reaches it in v0.22.5 |
| Iterations of one subagent | 250 | `delegation.max_iterations` |
| Subagents running at once | 10 | `delegation.max_concurrent_children` |
| `tool_search` calls in one turn | None | Hard stops, or tool search off on a weak model |

The last row is not hypothetical. In [#96247](https://github.com/NousResearch/hermes-agent/issues/96247) one session ran 1,523 `tool_search` calls, and v0.22.5 still has no per-turn cap on them. On a weak local model with a small catalog, the sure fix is to turn tool search off: the loop has nothing left to search, and every deferred schema comes back, 4,859 tokens a call on a fresh install. That is a Stage 1 change, and it moves the fixed budget. On a strong model, keep tool search and use the guardrails below.

Subagents are the other open tap. Each child is a fresh agent that pays your tool schemas and the working folder's AGENTS.md again as a cold prefix (Stage 4), and the defaults allow 250 iterations each with 10 running at once. A cheaper child model, `delegation.model` with `delegation.provider` (empty inherits yours), and a lower `delegation.max_iterations` are the levers.

### Loop guardrails

Hermes already watches for loops. Within a turn it counts repeated failing calls, calls that make no progress and identical replays, and warns in the tool result. Stopping a loop takes more: the detectors' blocks and halts, the halt after five identical replays included, all need `tool_loop_guardrails.hard_stop_enabled`, which is off by default. Hermes switches it on for you only in non-interactive runs, the gateway and cron, through `tool_loop_guardrails.non_interactive_hard_stop_enabled`, so in your own sessions the detectors only warn. Two checks work without it: web searches and subagents are capped at 50 per turn (`tool_loop_guardrails.loop_caps.max_web_searches` and `tool_loop_guardrails.loop_caps.max_subagents`), and after three smart-approval denials in a row the denial tells the model to stop trying and hand the command to you (`approvals.denial_breaker_threshold`).

[witcheer](https://x.com/witcheer/status/2098290534758408306) recommends turning the hard stop on for your own sessions as well:

*`hard-stops.sh`*

```bash
hermes config set tool_loop_guardrails.hard_stop_enabled true
```

What it does not catch: the guardrails look for identical and failing calls, so a run of different, successful searches like the one in #96247 may not trip them. That case is the tool search switch above.

### Cron jobs are full agents

A cron job is not a script with a model attached. Every fire builds a fresh agent: SOUL.md and memory every time, the whole cron toolset unless the job names its own `enabled_toolsets`, and a cold prompt cache unless fires come less than five minutes apart. Since v0.21.4 a job with no pinned model runs on your main model as it is at fire time, so moving your chat to an expensive model moves every unpinned job with it.

The cron help gives three ways to pin a model. `--model` with `--provider` pins a job to a model you name. `--pin` locks your current main model onto the job so later model changes never touch it (it is ignored when `--model` is given). And `cron.model` with `cron.model_provider` sets a fleet default for every job that names none, a tip from [witcheer](https://x.com/witcheer/status/2095722000907923465), along with pinning heavy jobs one by one. A job's model is yours to set: the cron help says the agent's own cron tool cannot set it, so the stage prompt hands you the `hermes cron edit` command instead of running it.

Three modes can skip the model, which makes them the cheapest jobs you can schedule. A job with `--no-agent` runs a script from the scripts folder of your Hermes home and delivers what it prints, with no model at all; empty output stays silent. Script-only jobs for routine chores are a pattern [witcheer's Almanac](https://x.com/witcheer/status/2108903932797796580) reported from an r/hermesagent post. A job with `--script` alone is different: the script runs first and its output goes into the agent's prompt, and an empty output still wakes the agent. Only a last line of `{"wakeAgent": false}` skips the model for that run. A job with `--monitor-script` (or `--monitor-url`) checks a source every tick and wakes the agent only when the output changed.

The block below is an example to adapt, not to run as it stands: the schedules, the tasks and the folder are placeholders for your own, `<cheap-model>` stands for a smaller model your provider serves, `openrouter` for whichever provider you use, and `<job-id>` for an ID from `hermes cron list`.

*`cron-pinned.sh`*

```bash
hermes cron create "every day at 7:30" "Summarize the files changed in ~/reports since yesterday, in three lines." --model <cheap-model> --provider openrouter
hermes cron create "0 9 * * 1" "Write the weekly status report." --pin   # keeps today's main model if you change it later
hermes cron edit <job-id> --model <cheap-model> --provider openrouter   # pins a job you already have
hermes cron list
```

The schedule grammar has traps, and the cron docs' own example falls into one:

| Schedule | What v0.22.5 does |
|---|---|
| `every 1d at 07:30` | Rejected, and so is the `every 1d at 09:00` in the cron docs |
| `every day at 7:30` or `30 7 * * *` | Runs at 7:30 every day |
| `every monday at 9am` or `0 9 * * 1` | Runs Mondays at 9:00 |
| `every 1d` | Repeats a day after each run, so the time drifts |
| `30m` | Repeats every 30 minutes; a bare duration is not a one-shot |
| `in 30m` | Runs once, 30 minutes from now |

### The session store

Hermes keeps every session in state.db, and on v0.22.5 nothing trims it unless you ask, apart from a one-time question when the disk holding it runs low. Auto-prune was on from v0.21.1 to v0.22.2 and is opt-in again from v0.22.3: `sessions.auto_prune` is `false`, with `sessions.retention_days` at 90 for when you turn it on. `hermes sessions stats` shows the size of the store, and the doctor check warns once it passes 1 GB.

Pruning by hand is a habit [witcheer](https://x.com/witcheer/status/2097201422844436642) and [Shabnam Katoch](https://www.betterclaw.io/blog/hermes-agent-bugs-fixes) both wrote up. A dry run is the safe way in, and the cost and token filters double as an audit of your most expensive sessions:

*`session-store.sh`*

```bash
hermes sessions stats
hermes sessions prune --dry-run --older-than 30
hermes sessions prune --dry-run --min-cost 1
hermes sessions prune --dry-run --min-tokens 500000
```

`--dry-run` lists what matches and changes nothing. `--older-than` takes days, a duration such as `1w`, or a date. `--min-cost` compares the actual or estimated cost Hermes recorded, in USD, which Stage 0 explains is not audit-grade, and `--min-tokens` counts input plus output. Without `--dry-run`, prune deletes after a confirmation, and pinned and archived sessions are left out unless you add their include flags.

### The stage prompt

*`prompt-stage-7-caps.md`*

```markdown
Tune Hermes, stage 7: Cap the Runaways. Work in five steps, one change at a time.
MEASURE: Read `hermes config get agent.max_turns`, `hermes config get delegation.max_iterations`, `hermes config get delegation.max_concurrent_children`, `hermes config get tool_loop_guardrails.hard_stop_enabled` and `hermes config get cron.model`, list my cron jobs with `hermes cron list`, show the size of my session store from `hermes sessions stats`, and tell me which of these budgets has no ceiling. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: Propose one cap for the most open budget you found, such as `hermes config set tool_loop_guardrails.hard_stop_enabled true` for hard stops in my own sessions, or a turn limit in `agent.max_turns` or a lower `delegation.max_iterations`, set with `hermes config set`. For a cron job, give me the exact `hermes cron edit` command that pins its model for me to run in my own terminal, and never edit, pin or delete a cron job or delete a session yourself. Show the exact command, or the exact lines of config.yaml before and after, and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: Copy config.yaml to a dated backup next to it with `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in its folder, never overwriting an earlier backup, then make only the change I approved.
VERIFY: Read the changed key back with `hermes config get`, or the changed job's schedule with `hermes cron list` and its model in cron/jobs.json, and confirm that the fixed budget did not move, because a cap bounds the worst case and sends nothing new. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

- [ ] `hermes config get tool_loop_guardrails.hard_stop_enabled` reads back what you approved
- [ ] Any other cap you set reads back with `hermes config get`
- [ ] You can say which model each cron job runs on, pinned or following your main model
- [ ] Every schedule you wrote reads back in `hermes cron list` at the time you meant
- [ ] `hermes sessions stats` reports the store size, and nothing was pruned without a dry run first

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-TUNING.md)
