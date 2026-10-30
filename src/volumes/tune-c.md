## Stage 6: Cache, Compression and Side Tasks

### What this stage changes

Stages 0 to 5 cut what Hermes sends before your first word. This stage works on what you pay to send it again and again: whether the provider can read that prefix from its cache or has to write it again, when a long session gets rewritten by compaction, and which model runs the side tasks you never see.

None of these levers moves the fixed budget. The prompt-size numbers stay where Stage 5 left them, and the stage prompt shows that on purpose: the change lands on the cost of each call, not on what each call sends.

[Volume 1 Build 10](https://github.com/jasonjeske/hermes-master-class/blob/main/masterclass/build-10-tuning-and-safety.md) set the basics: approval modes, the compression threshold and a cheaper model for side tasks. This stage goes underneath them, and it corrects one number Build 10 took from the docs.

### The cache lasts one session

Hermes builds the system prompt and the tool list once per session and sends the same bytes on every call after that. That is how it keeps the provider's prefix cache warm, and it is why most of what you change in a running session waits for the next one.

```table
| In a running session | Breaks the cache | What happens |
| A memory write | No | It reaches disk now and the prompt at the next session or compaction |
| A skill install or edit | No | A short note in the next message lists the change; the index itself updates next session |
| An edit to SOUL.md or AGENTS.md | No | Read again at the next session or compaction |
| Midnight | No | The date line stays fixed to the start of the session |
| A model switch with `/model` | Yes | The prompt is rebuilt and the new model starts with a cold cache |
| A toolset change | Yes | The tool list heads every request, so everything is written again |
| A compaction | Yes | The system prompt is rebuilt and the whole prefix is written again |
| Resuming from another folder | Yes | Context files depend on the folder, so the prompt is rebuilt |
```

The habit that falls out of the table: pick the model before you start, and change it between sessions, not inside one. A switch in a long session pays to write the whole conversation again at the new model's price. The habit is [witcheer's](https://x.com/witcheer/status/2074153526222114974): batch your model switches, or start a fresh session, instead of going back and forth in one.

How long a cached prefix lives is `prompt_caching.cache_ttl`, and the default is `5m`. A one hour cache write costs 2x the base input price against 1.25x for five minutes, so the long tier pays off only when you come back to a session after a pause. `auto`, opt-in since v0.21.5, picks per session: one hour for sessions a person types into (CLI, TUI, Desktop and the messaging platforms) and five minutes for subagents, cron, one-shots and the other machine-paced runs. On an install whose sessions are parked and resumed through the day, the docs put the cut in the interactive cache-write bill at roughly 40%; the code's own note, from one install, says 42%.

```code lang=bash file=cache-ttl.sh
hermes config set prompt_caching.cache_ttl auto
```

A value such as `off` or `false` in `prompt_caching.cache_ttl` turns caching off. The docs say no such switch exists, but it does. It earns its place only on plans that bill cache writes and behind proxies that add their own cache markers, so leave caching on otherwise.

Two provider routes need a check of their own. If you run Claude through the Nous Portal, the default chat wire caches only the system prompt inside tool loops: the reports in [#141833](https://github.com/NousResearch/hermes-agent/issues/141833) show 13 to 21% cache hits, and the native wire measured 95% or better. The default stays `chat` because `native` has a cache problem of its own on the OpenRouter-served path, so treat the switch as a test: set it, run one long tool-heavy task, and watch the cache field in the status bar.

On OpenRouter, the response cache is on by default: send the identical request again within 300 seconds, the default of `openrouter.response_cache_ttl`, and you get the stored response back, tool calls included ([#70387](https://github.com/NousResearch/hermes-agent/issues/70387)). In an agent loop a replayed tool call is a stale decision, so turn it off there.

```code lang=bash file=provider-cache.sh
hermes config set nous.anthropic_wire native
hermes config set openrouter.response_cache false
```

### Compression starts later than you think

`compression.threshold` defaults to 0.50, and Volume 1 Build 10 repeats that number from the docs. In v0.22.5 it holds only for models with a context window of 512K or more. For any smaller window Hermes raises the trigger to 0.75, so a 200K model compacts near 150K, not 100K. The floor only ever raises: a threshold above 0.75 makes a small model compact later, and anything below it acts as 0.75.

Each compaction is one call to a summary model. Up to 160,000 characters of history go in, and the summary that comes out is sized at 20% of the turns being compacted, never under 2,000 tokens and never over 5% of the window or 10K tokens, whichever is smaller. Then the whole new prefix is written to the cache again. That call runs on your main model unless you route it, which is the next section. A lower threshold means more compactions and smaller requests; a higher one means fewer compactions and a bigger prefix riding the cache between them.

Two things to know before you touch it. `/compress --preview` shows what a compaction would do, from local estimates, without calling any model; a real `/compress` calls the summary model. And `compression.target_ratio`, which some guides tune, does nothing under the default lean tail: it applies only when `compression.tail_mode` is `legacy`. The lean tail keeps 2.5% of the window word for word, never less than 10K or more than 25K tokens.

### Side tasks run on your main model

Hermes runs a handful of jobs beside your conversation: the compaction summary, vision, the check behind smart approvals, session titles and the background review. Each has its own block under `auxiliary`, and each block's provider defaults to `auto`, which starts with your main model. Chat on a frontier model and every side task runs on it too. Since v0.21.2 a side task never bills a provider you did not select ([#107366](https://github.com/NousResearch/hermes-agent/pull/107366)), so this is a cost problem, not a surprise on some other account.

Community authors got here first, and this stage adopts their fixes. [Azamat Safarov](https://dev.to/azamat_safarov/hermes-agent-burned-603m-tokens-behind-my-back-i-cut-background-costs-by-up-to-125x-43oi) traced runaway background spend to side tasks left on `auto` and pinned every one of them to a provider and model chosen on purpose. [Tonbi's AI Garage](https://www.youtube.com/watch?v=NoF-YajElIM) showed the gotcha that trips most people: the summary model belongs under `auxiliary.compression`, while the top-level `compression` block holds only behavior such as `compression.threshold`. And witcheer added two refinements: a fast, inexpensive model for compaction summaries ([on summaries](https://x.com/witcheer/status/2086745372521591061)), and lower thinking for side tasks, such as `auxiliary.compression.reasoning_effort` at `low` ([on side-task thinking](https://x.com/witcheer/status/2100460797239415168)), which Build 10 already sets. The review fork ignores its own effort setting while it stays on the main model.

Route the two side tasks that read the most history, by provider and model only. The block below is an example, not a drop-in: `<cheap-model>` stands for a smaller model your provider serves, and `openrouter` for whichever provider you use. Merge the lines into config.yaml yourself, or let the stage prompt set them one key at a time with `hermes config set`:

```code lang=yaml file=side-tasks.yaml
auxiliary:
  compression:
    provider: openrouter
    model: <cheap-model>
  background_review:
    provider: openrouter
    model: <cheap-model>
```

Pick a provider you already have a key for. The key stays where Hermes already keeps it, never in this block. What it costs you: the summary is what a long session carries forward after compaction, so try the cheaper model on one long session before you trust it.

### The review fork and smart approvals

After some replies Hermes forks a background review that decides what to save to memory and which skills to write or patch. It fires every 10 user turns for memory and every 10 tool iterations for skills, runs up to 16 iterations, and costs about 30K tokens an event by the code's own note, a figure this volume did not measure. On `auto` it replays your whole conversation on the main model, reading the warm cache. Routed to any other model it replays a shorter digest instead, which the docs and the code put at about 3 to 5x cheaper. Cron runs never fork it.

You have two levers: route it to a cheaper model as in the lines above, or switch the automatic review off. Off, the review no longer runs after turns on its own; the memory tool still works in the conversation, and `/refine` runs a review whenever you ask for one.

```code lang=bash file=review-off.sh
hermes config set auxiliary.background_review.enabled false
```

`approvals.mode` defaults to `smart`, and a smart approval asks a side-task model about every command it flags as dangerous: one small call per flagged command, on your main model unless `auxiliary.approval` is routed. `manual` drops that call and asks you every time instead; [Volume 1 Build 10](https://github.com/jasonjeske/hermes-master-class/blob/main/masterclass/build-10-tuning-and-safety.md) covers what each mode lets through. Session titles are the last small one: `auxiliary.title_generation.model_upgrade_enabled` set to `false` keeps the free title Hermes derives on its own and skips the model call.

### The stage prompt

```code lang=markdown file=prompt-stage-6-runtime.md
Tune Hermes, stage 6: Cache, Compression and Side Tasks. Work in five steps, one change at a time.
MEASURE: Read `hermes config get prompt_caching.cache_ttl`, `hermes config get compression.threshold`, `hermes config get auxiliary.compression.provider`, `hermes config get auxiliary.background_review.enabled`, `hermes config get auxiliary.background_review.provider` and `hermes config get approvals.mode`, then tell me which model and provider you run on, its context window, and which side tasks run on it. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: Propose the one change that fits how I work: `prompt_caching.cache_ttl` set to `auto` if I come back to sessions after breaks, or `auxiliary.compression` and `auxiliary.background_review` routed to a cheaper model on a provider I already use, by provider and model only, each key set with `hermes config set`. Show the exact command, or the exact lines of config.yaml before and after, and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: Copy config.yaml to a dated backup next to it with `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in its folder, never overwriting an earlier backup, then make only the change I approved.
VERIFY: Read the changed key back with `hermes config get` and confirm that the fixed budget did not move, because this stage changes what each call costs, not what it sends. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

```checklist
[ ] `hermes config get prompt_caching.cache_ttl` prints the value you chose, `5m` or `auto`
[ ] You know whether your model's window is under 512K, and so whether your threshold acts as 0.75
[ ] `/compress --preview` in a long session showed the plan without calling a model
[ ] `hermes config get auxiliary.compression.provider` names the provider you routed it to, or you chose to keep `auto`
[ ] The fixed budget from the prompt-size check matches the one from before this stage
```

## Stage 7: Cap the Runaways

### What this stage changes

Every stage so far shrank a cost you pay on every call. This one bounds the costs that have no ceiling at all: a task that keeps calling tools, a fan-out of subagents, a search loop on a weak model, a cron job that wakes a full agent on your best model every morning. Nothing here moves the fixed budget. A cap costs you nothing until a job hits it, and then it is the difference between a stopped turn and a bill.

Turn caps, the budget warning and reasoning effort are in [Volume 1 Build 10](https://github.com/jasonjeske/hermes-master-class/blob/main/masterclass/build-10-tuning-and-safety.md), and Build 10 has the effort key right: `agent.reasoning_effort` is read on every surface even though config ships no default for it, and `/reasoning <level> --global` writes it cleanly. This stage covers what Build 10 does not.

### Open budgets

What v0.22.5 lets run without a ceiling, surface by surface:

```table
| What can run long | The ceiling in v0.22.5 | Where you set one |
| Agent turns in the CLI or a gateway chat | None: `agent.max_turns` is empty, and empty means unlimited | `agent.max_turns` |
| Agent turns in the TUI | 500 when `agent.max_turns` is empty | `agent.max_turns` |
| A one-shot run with `hermes -z` | None: the one-shot path passes no cap | No setting reaches it in v0.22.5 |
| Iterations of one subagent | 250 | `delegation.max_iterations` |
| Subagents running at once | 10 | `delegation.max_concurrent_children` |
| `tool_search` calls in one turn | None | Hard stops, or tool search off on a weak model |
```

The last row is not hypothetical. In [#96247](https://github.com/NousResearch/hermes-agent/issues/96247) one session ran 1,523 `tool_search` calls, and v0.22.5 still has no per-turn cap on them. On a weak local model with a small catalog, the sure fix is to turn tool search off: the loop has nothing left to search, and every deferred schema comes back, 4,859 tokens a call on a fresh install. That is a Stage 1 change, and it moves the fixed budget. On a strong model, keep tool search and use the guardrails below.

Subagents are the other open tap. Each child is a fresh agent that pays your tool schemas and the working folder's AGENTS.md again as a cold prefix (Stage 4), and the defaults allow 250 iterations each with 10 running at once. A cheaper child model, `delegation.model` with `delegation.provider` (empty inherits yours), and a lower `delegation.max_iterations` are the levers.

### Loop guardrails

Hermes already watches for loops. Within a turn it counts repeated failing calls, calls that make no progress and identical replays, and warns in the tool result. Stopping a loop takes more: the detectors' blocks and halts, the halt after five identical replays included, all need `tool_loop_guardrails.hard_stop_enabled`, which is off by default. Hermes switches it on for you only in non-interactive runs, the gateway and cron, through `tool_loop_guardrails.non_interactive_hard_stop_enabled`, so in your own sessions the detectors only warn. Two checks work without it: web searches and subagents are capped at 50 per turn (`tool_loop_guardrails.loop_caps.max_web_searches` and `tool_loop_guardrails.loop_caps.max_subagents`), and after three smart-approval denials in a row the denial tells the model to stop trying and hand the command to you (`approvals.denial_breaker_threshold`).

[witcheer](https://x.com/witcheer/status/2098290534758408306) recommends turning the hard stop on for your own sessions as well:

```code lang=bash file=hard-stops.sh
hermes config set tool_loop_guardrails.hard_stop_enabled true
```

What it does not catch: the guardrails look for identical and failing calls, so a run of different, successful searches like the one in #96247 may not trip them. That case is the tool search switch above.

### Cron jobs are full agents

A cron job is not a script with a model attached. Every fire builds a fresh agent: SOUL.md and memory every time, the whole cron toolset unless the job names its own `enabled_toolsets`, and a cold prompt cache unless fires come less than five minutes apart. Since v0.21.4 a job with no pinned model runs on your main model as it is at fire time, so moving your chat to an expensive model moves every unpinned job with it.

The cron help gives three ways to pin a model. `--model` with `--provider` pins a job to a model you name. `--pin` locks your current main model onto the job so later model changes never touch it (it is ignored when `--model` is given). And `cron.model` with `cron.model_provider` sets a fleet default for every job that names none, a tip from [witcheer](https://x.com/witcheer/status/2095722000907923465), along with pinning heavy jobs one by one. A job's model is yours to set: the cron help says the agent's own cron tool cannot set it, so the stage prompt hands you the `hermes cron edit` command instead of running it.

Three modes can skip the model, which makes them the cheapest jobs you can schedule. A job with `--no-agent` runs a script from the scripts folder of your Hermes home and delivers what it prints, with no model at all; empty output stays silent. Script-only jobs for routine chores are a pattern [witcheer's Almanac](https://x.com/witcheer/status/2108903932797796580) reported from an r/hermesagent post. A job with `--script` alone is different: the script runs first and its output goes into the agent's prompt, and an empty output still wakes the agent. Only a last line of `{"wakeAgent": false}` skips the model for that run. A job with `--monitor-script` (or `--monitor-url`) checks a source every tick and wakes the agent only when the output changed.

The block below is an example to adapt, not to run as it stands: the schedules, the tasks and the folder are placeholders for your own, `<cheap-model>` stands for a smaller model your provider serves, `openrouter` for whichever provider you use, and `<job-id>` for an ID from `hermes cron list`.

```code lang=bash file=cron-pinned.sh
hermes cron create "every day at 7:30" "Summarize the files changed in ~/reports since yesterday, in three lines." --model <cheap-model> --provider openrouter
hermes cron create "0 9 * * 1" "Write the weekly status report." --pin   # keeps today's main model if you change it later
hermes cron edit <job-id> --model <cheap-model> --provider openrouter   # pins a job you already have
hermes cron list
```

The schedule grammar has traps, and the cron docs' own example falls into one:

```table
| Schedule | What v0.22.5 does |
| `every 1d at 07:30` | Rejected, and so is the `every 1d at 09:00` in the cron docs |
| `every day at 7:30` or `30 7 * * *` | Runs at 7:30 every day |
| `every monday at 9am` or `0 9 * * 1` | Runs Mondays at 9:00 |
| `every 1d` | Repeats a day after each run, so the time drifts |
| `30m` | Repeats every 30 minutes; a bare duration is not a one-shot |
| `in 30m` | Runs once, 30 minutes from now |
```

### The session store

Hermes keeps every session in state.db, and on v0.22.5 nothing trims it unless you ask, apart from a one-time question when the disk holding it runs low. Auto-prune was on from v0.21.1 to v0.22.2 and is opt-in again from v0.22.3: `sessions.auto_prune` is `false`, with `sessions.retention_days` at 90 for when you turn it on. `hermes sessions stats` shows the size of the store, and the doctor check warns once it passes 1 GB.

Pruning by hand is a habit [witcheer](https://x.com/witcheer/status/2097201422844436642) and [Shabnam Katoch](https://www.betterclaw.io/blog/hermes-agent-bugs-fixes) both wrote up. A dry run is the safe way in, and the cost and token filters double as an audit of your most expensive sessions:

```code lang=bash file=session-store.sh
hermes sessions stats
hermes sessions prune --dry-run --older-than 30
hermes sessions prune --dry-run --min-cost 1
hermes sessions prune --dry-run --min-tokens 500000
```

`--dry-run` lists what matches and changes nothing. `--older-than` takes days, a duration such as `1w`, or a date. `--min-cost` compares the actual or estimated cost Hermes recorded, in USD, which Stage 0 explains is not audit-grade, and `--min-tokens` counts input plus output. Without `--dry-run`, prune deletes after a confirmation, and pinned and archived sessions are left out unless you add their include flags.

### The stage prompt

```code lang=markdown file=prompt-stage-7-caps.md
Tune Hermes, stage 7: Cap the Runaways. Work in five steps, one change at a time.
MEASURE: Read `hermes config get agent.max_turns`, `hermes config get delegation.max_iterations`, `hermes config get delegation.max_concurrent_children`, `hermes config get tool_loop_guardrails.hard_stop_enabled` and `hermes config get cron.model`, list my cron jobs with `hermes cron list`, show the size of my session store from `hermes sessions stats`, and tell me which of these budgets has no ceiling. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: Propose one cap for the most open budget you found, such as `hermes config set tool_loop_guardrails.hard_stop_enabled true` for hard stops in my own sessions, or a turn limit in `agent.max_turns` or a lower `delegation.max_iterations`, set with `hermes config set`. For a cron job, give me the exact `hermes cron edit` command that pins its model for me to run in my own terminal, and never edit, pin or delete a cron job or delete a session yourself. Show the exact command, or the exact lines of config.yaml before and after, and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: Copy config.yaml to a dated backup next to it with `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in its folder, never overwriting an earlier backup, then make only the change I approved.
VERIFY: Read the changed key back with `hermes config get`, or the changed job's schedule with `hermes cron list` and its model in cron/jobs.json, and confirm that the fixed budget did not move, because a cap bounds the worst case and sends nothing new. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

```checklist
[ ] `hermes config get tool_loop_guardrails.hard_stop_enabled` reads back what you approved
[ ] Any other cap you set reads back with `hermes config get`
[ ] You can say which model each cron job runs on, pinned or following your main model
[ ] Every schedule you wrote reads back in `hermes cron list` at the time you meant
[ ] `hermes sessions stats` reports the store size, and nothing was pruned without a dry run first
```

## Stage 8: Keep It Tuned

### What this stage changes

Everything so far tuned the install you have today. Updates change it: new tools land and defaults flip. This stage installs the hermes-tune skill. It adds one row to your skills index, the only change this stage makes to what each call sends, and it brings a weekly audit that measures, compares with your baseline and proposes changes for you to approve. The audit has a running cost of its own: if you schedule it, every run is one agent session on `cron.model`, or on your main model when that is empty, so the weekly audit section below shows how to pin it to an inexpensive model.

### Why budgets drift

The maintainers work on the fixed prefix too, and it moves both ways. Their context-burden campaign ([#95681](https://github.com/NousResearch/hermes-agent/issues/95681)) cut about 15.2K tokens a call on the CLI, and [PR #97979](https://github.com/NousResearch/hermes-agent/pull/97979) in v0.21.1 took the CLI from 10,578 to 7,306 tokens a call by deferring cold tools. Then the prefix grew from 11,595 to 14,962 tokens in five weeks as new tools landed, until [PR #137084](https://github.com/NousResearch/hermes-agent/pull/137084) in v0.22.0 took 2.1K back.

Those are the maintainers' figures from their own issues and pull requests, not this volume's measurements, so read them for direction. The direction is the lesson: a release can undo a stage you finished, or hand you a saving you never asked for, and only a measurement after the update tells you which.

### The version label trap

The first line of `hermes --version` starts with the release, v0.22.5 here, and a date in parentheses, and the rest of the line names the build, such as its channel and a commit. Only the date can mislead. It was not bumped for v0.22.5, which still shows 2026.9.24, and the release tagged v2026.9.24 is v0.21.5. Go by the release and the build, never the date, and quote the whole first line in a bug report: a report that quotes only the date can be a whole release off.

To learn whether an update is waiting and what it would touch, run the update command's two read-only checks yourself, in your own terminal:

```code lang=bash file=version-check.sh
hermes update --check   # is an update waiting; installs nothing
hermes update --plan    # what an update would touch; changes nothing
```

`--check` says whether an update is available without installing anything. `--plan` shows the install kind, every running Hermes service across your profiles with the code version it runs, and how each would restart, and it changes nothing. Looking before you update is a habit from [witcheer's Almanac](https://x.com/witcheer/status/2108564754893582428).

Run both yourself. Hermes flags every `hermes update` command as dangerous, `--check` and `--plan` included, so in a session one has to pass your approval mode first and in a cron job it is refused outright. That is why the stage prompt below hands the update check to you instead of running it.

### Install the skill

```code lang=bash file=install-hermes-tune.sh
hermes skills install jasonjeske/hermes-master-class/skills/hermes-tune --yes
```

Run it in your own terminal; the stage prompt hands it to you rather than installing anything itself. The command goes through the skills hub. Hermes fetches [the skill folder](https://github.com/jasonjeske/hermes-master-class/tree/main/skills/hermes-tune) from GitHub, runs its install scanner at community trust, where any high finding blocks the install, and then offers the skill's weekly audit under `/suggestions`. Install it this way and not by copying the folder into your skills directory: a copy skips the scanner, and only the hub install offers the audit.

The install takes effect in your next session. It adds one row to the skills index, and the description is 52 characters, inside the 60 the index keeps. Measure before and after, and the skills index line of the prompt-size report grows by that one row.

### Two modes

In guided tuning you load the skill in a session and it walks this ladder one stage at a time with the same five steps as the stage prompts: measure, propose one change, wait for your yes, back up config.yaml, apply, measure again. After you confirm the result, it refreshes `tune/baseline.json`. In audit mode the scheduled job runs it: it measures, compares with the saved baseline, writes a report and proposes changes, and its instructions are to change nothing else, the baseline included. The weekly audit section below says what holds it to that.

Both modes keep their state in a tune folder next to the active profile's config.yaml, which `hermes config path` prints. `baseline.json` holds the prompt-size output with its date and the first line of `hermes --version`, and each audit writes `audit-YYYY-MM-DD.md` beside it.

### The weekly audit

The skill carries a blueprint for one weekly job: schedule `0 9 * * 1`, which is Mondays at 9:00, with only the terminal and file toolsets. Hermes offers it under `/suggestions` after the install and never schedules it for you; you schedule it from there, or you do not. Like every cron job it fires only while a gateway runs for that profile, and each fire is a fresh agent (Stage 7), which is why the job names its two toolsets instead of carrying the whole cron set.

The blueprint names no model, so the job runs on `cron.model`, or on your main model when that is empty, and every run costs one full agent session: it loads the skill, runs the read-only checks below and writes a report. The audit's own check A10 flags exactly that, a job that follows your main model, so pin it right after you schedule it, in your own terminal, or set `cron.model` and `cron.model_provider` before you schedule it. Here `<job-id>` is the ID of the job named blueprint:hermes-tune in the list, and `<cheap-model>` and `<provider>` stand for your own choices:

```code lang=bash file=pin-the-audit.sh
hermes cron list
hermes cron edit <job-id> --model <cheap-model> --provider <provider>
```

Each run makes twelve checks. A1 to A3, and A5 when a skill is new, report a change since your baseline: a new release or build, a budget that grew, a toolset or skill that appeared. A7 reports its values on every run. Everything else reports a standing condition for as long as it holds, so the same line comes back every week until you fix it or decide to keep it. A default install trips A8 and A9 every week, because its side tasks sit on `auto` and its caps are unlimited, and A10 trips on the audit's own job until you pin its model or set `cron.model`.

```table
| Check | What it reads | It reports when |
| A1 Version | The first line of `hermes --version`: the release and the build | That line differs from the baseline's, so a new release or build is in |
| A2 Budget | The prompt-size breakdown | Estimated tokens rose 5 percent or more, or the tool count changed |
| A3 Toolsets | The toolset list | A toolset is on that the baseline did not have |
| A4 Tool search | `tools.tool_search.enabled` and `tools.tool_search.defer` | Tool search is off, or an explicit list dropped a curated default name |
| A5 Skills | The enabled skills and `skills.auto_load` | A new skill, any pinned skill, or a description over 60 characters |
| A6 Memory | The characters in MEMORY.md and USER.md, counted with `wc -m`, against their caps | Either store is at nine tenths of its cap or more |
| A7 Cache and compression | `prompt_caching.cache_ttl` and `compression.threshold` | Every run, with what the values mean for your model |
| A8 Side tasks | The compaction and review providers | A side task is on `auto`, which runs on your main model |
| A9 Caps | `agent.max_turns` and the delegation caps | A cap is unlimited |
| A10 Cron | The cron job list, `cron.model`, and each job's model and toolsets in cron/jobs.json | A job names no toolsets, or has no model while `cron.model` is empty, the audit's own job included until you pin it |
| A11 Session store | The session statistics | The store nears the 1 GB the doctor check warns about |
| A12 MCP | The Tools column of `hermes mcp list` | A server has no tool include list |
```

Each run saves `tune/audit-YYYY-MM-DD.md` beside config.yaml: a budget table against the baseline, the drift it found, and numbered proposals with the exact command or config.yaml lines for each. Near the top it records the first line of `hermes --version` and the result of the before and after check described below, and its last line says that nothing was changed, which that check lets you confirm. To act on a proposal, open a session, load hermes-tune and name its number.

The skill's never list holds in both modes: change no config, toolsets, skills, memory or cron jobs during a scheduled run; apply nothing before you say yes in the session; never run `hermes doctor`, `hermes status` with `--deep`, or `hermes debug`, which call providers or upload logs; never read or print secrets; never prune, archive or delete sessions, skills, memories or backups; never install, remove or update skills, plugins or Hermes itself; never schedule, edit or remove cron jobs; and never commit a Hermes home or a backup of one to git, since both hold your `.env` and auth files.

Those lines are instructions to the model, and two Hermes guards back them up. Hermes's file tools, write_file and patch, refuse to write the active config.yaml. In a cron job `approvals.cron_mode` defaults to `deny`, so any command Hermes flags as dangerous, `hermes update` among them, is refused instead of waiting for an approval nobody is there to give. Neither guard covers everything, since a plain `hermes config set` passes both, so the skill also checks its own run: at the start and at the end it hashes config.yaml and cron/jobs.json and lists the files in the skills and memories folders with their sizes, never their content, and the report names any difference. Names and sizes catch a file added, removed or resized, though not an edit that keeps the size, and the scheduler rewrites cron/jobs.json whenever a job starts or ends, so a jobs.json line can be its doing when another job ran during the audit.

After every update, run the audit by hand instead of waiting for Monday: open a session, load hermes-tune and ask for the weekly audit in audit mode. An update is exactly when the budget moves.

### The stage prompt

```code lang=markdown file=prompt-stage-8-keep-tuned.md
Tune Hermes, stage 8: Keep It Tuned. Work in five steps, one change at a time.
MEASURE: Read the release and the build from the first line of `hermes --version`, never the date in parentheses, the skills that load from `hermes skills list` with `--enabled-only`, and whether a tune folder with a baseline.json sits next to my config.yaml, whose location `hermes config path` prints. Ask me to run `hermes update --check` in my own terminal and tell you whether an update is waiting, and never run any form of hermes update yourself. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: Propose installing the hermes-tune skill and nothing else, as a command for me to run in my own terminal, hermes skills install jasonjeske/hermes-master-class/skills/hermes-tune --yes, and never run it yourself. Tell me that it adds one row to the skills index and offers a weekly audit under /suggestions that I schedule myself and then pin to an inexpensive model, because each run is one agent session. Show the exact command, or the exact lines of config.yaml before and after, and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: Copy config.yaml to a dated backup next to it with `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in its folder, never overwriting an earlier backup, then make only the change I approved.
VERIFY: Confirm that hermes-tune appears in `hermes skills list` and that the skills index in the breakdown grew by one row. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

```checklist
[ ] `hermes skills list` shows hermes-tune, and the skills index in the prompt-size report grew by one row
[ ] `/suggestions` offered the weekly audit, and you scheduled it yourself or chose not to
[ ] If you scheduled it, `hermes cron list` shows it on `0 9 * * 1`, and you pinned it with `hermes cron edit` or set `cron.model` first
[ ] The tune folder next to config.yaml holds baseline.json, and after the first run an audit report whose before and after check reads unchanged
[ ] You read your release and build from the first line of `hermes --version`, not the date, and ran `hermes update --check` yourself
```

## Where the Docs and the Code Disagree

Checked against the official docs as they ship in the v0.22.5 source (commit bf0203a): docs paths are relative to `website/docs/`, while code paths, the seeded SOUL.md and the example config are relative to the root of the checkout, and every stage above follows the code.

```table
| Topic | The docs say | v0.22.5 does | Stage |
| `/context` skills | Its category table includes the skills index (`reference/slash-commands.md:66`) | Shows Skills 0 with 58 skills installed: the index sits in the volatile tier (`agent/system_prompt.py:785`) but the breakdown looks in the stable tier (`agent/context_breakdown.py:152`), so the index counts as System prompt | 0 |
| `/usage` cost | Shows a cost breakdown (`reference/slash-commands.md:136`, `:264`) | Prints tokens, calls and duration, with no cost line on the CLI or a gateway (`hermes_cli/cli_info_mixin.py:764-783`, `gateway/slash_commands_status.py:209-226`) | 0 |
| Status bar cost | `display.show_cost` adds an estimated cost to the CLI status bar (`user-guide/configuration.md:2254`, `user-guide/cli.md:224`, `:232`) | Nothing reads `display.show_cost`, and the status bar has no cost segment (`hermes_cli/config_defaults.py:906`, `hermes_cli/cli_status_bar_mixin.py:1017-1106`) | 0 |
| Dashboard analytics | The dashboard page describes the Analytics tab and its cost cards without saying it starts hidden (`user-guide/features/web-dashboard.md:303-310`) | Hidden until `dashboard.show_token_analytics` is true (`web/src/pages/AnalyticsPage.tsx:412-427`), and the key's own comment calls the totals a lower bound (`hermes_cli/config_defaults.py:1019-1026`) | 0 |
| `hermes doctor` | Has one flag, `--fix` (`reference/cli-commands.md:981`) | Also takes `--live` and `--ack`, and calls every configured provider even without `--live` (`hermes_cli/subcommands/doctor.py:15-24`, `hermes_cli/doctor.py:96-108`) | 0 |
| `hermes tools` | Has `--summary` and otherwise opens the interactive tool menu (`reference/cli-commands.md:1694`, `:1701`) | Also has `list`, `disable`, `enable` and `post-setup` (`hermes_cli/subcommands/tools.py:21-49`) | 2 |
| `/insights` | Takes a number of days (`reference/slash-commands.md:268`) | Also takes `--days` and `--source` (`hermes_cli/cli_info_mixin.py:833-842`) | 2 |
| Skills index tier | Skills are part of the stable tier (`developer-guide/prompt-assembly.md:38`) | The index leads the volatile tier (`agent/system_prompt.py:785`) | 3 |
| Skills at session start | `skills_list()` loads at session start for about 3K tokens (`guides/work-with-skills.md:79`, `user-guide/features/skills.md:177`) | What loads is the prompt index, about 1,720 tokens for the 58 bundled skills (`agent/system_prompt.py:301-314`) | 3 |
| `hermes skills config` | Takes a skill name, as in its gif-search example (`guides/work-with-skills.md:162`) | Takes no argument and opens the enable and disable checklist (`hermes_cli/subcommands/skills.py:174-175`) | 3 |
| Plugin skills | Not listed in the system prompt or in `skills_list` (`guides/work-with-skills.md:136`, `developer-guide/plugins/index.md:1201`) | Listed in the index under a plugin category and appended to `skills_list` (`agent/prompt_builder.py:1200-1229`, `tools/skills_tool.py:296-302`) | 3 |
| The skills prompt | Its sample loads a skill when one clearly matches (`developer-guide/prompt-assembly.md:111-113`) | The shipped text tells the model it must load any skill that is even partially relevant (`agent/prompt_builder.py:1363-1365`) | 3 |
| Where skills live | All skills live in one folder of the Hermes home (`user-guide/features/skills.md:11`) | Four tiers: project, local, a create folder and external folders (`agent/skill_utils.py:398-420`) | 3 |
| `HERMES_IGNORE_RULES` | Skips preloaded skills (`reference/environment-variables.md:827`) | Skips `skills.auto_load` only, and skills preloaded with `-s` still load (`agent/system_prompt.py:317-334`) | 3 |
| Curator | Periodically spawns a short side-task model review (`user-guide/features/curator.md:9`) | The scheduled run is deterministic and spends no tokens; the model pass waits for `curator.consolidate` (`hermes_cli/config_defaults.py:1518-1520`) | 3 |
| Seeded SOUL.md | Its comment says each message reads it fresh, with no restart (`hermes_cli/default_soul.py:24`) | The prompt is built once per session, so an edit lands in the next session (`agent/system_prompt.py:1-8`) | 4 |
| Compression threshold | Compaction at 0.50 of the context limit (`user-guide/configuration.md:1012`), as Volume 1 Build 10 repeats | Raised to 0.75 for every window under 512K; 0.50 holds only at 512K or more (`agent/context_compressor.py:2762-2766`) | 6 |
| Lean compaction | The default config's comment says lean mode adds a few summary calls (`hermes_cli/config_defaults.py:612`) | One summary call per compaction, as the user guide says (`agent/context_compressor.py:66-70`) | 6 |
| Caching off | No switch exists to turn caching off (`user-guide/configuration.md:1428`) | `off`, `false`, `none` and similar values turn it off (`agent/agent_runtime_helpers.py:1620-1625`) | 6 |
| `/compress` preview | Documents `here N` and a focus topic (`reference/slash-commands.md:47`, `:259`) | Also takes `--preview` and `--dry-run`, which show the plan from local estimates and compress nothing (`hermes_cli/commands.py:113-114`) | 6 |
| Web and search side tasks | The example config still shows side-task blocks for `web_extract` and `session_search` (`cli-config.yaml.example:944`, `:965`) | Neither calls a model anymore, and leftover blocks are ignored (`tools/web_tools.py:539`, `tools/session_search_tool.py:1-8`) | 6 |
| Cron example | Schedules a job with `every 1d at 09:00` (`user-guide/features/cron.md:187`, `:196`) | Rejects that string; a cron expression such as `0 9 * * *` works (`cron/jobs.py:783-871`) | 7 |
| Auto-prune | The v0.22.0 upgrade notes say sessions prune automatically ([release notes](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.0)) | `sessions.auto_prune` is false again from v0.22.3 (`hermes_cli/config_defaults.py:2283-2288`) | 7 |
| Session export | Exports to JSONL (`reference/cli-commands.md:1783`) | Also exports Markdown, QMD, HTML and a trace format (`hermes_cli/subcommands/sessions.py:91-94`) | 7 |
```
