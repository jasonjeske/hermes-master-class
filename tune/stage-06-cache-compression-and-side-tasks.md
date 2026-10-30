# Stage 6: Cache, Compression and Side Tasks

### What this stage changes

Stages 0 to 5 cut what Hermes sends before your first word. This stage works on what you pay to send it again and again: whether the provider can read that prefix from its cache or has to write it again, when a long session gets rewritten by compaction, and which model runs the side tasks you never see.

None of these levers moves the fixed budget. The prompt-size numbers stay where Stage 5 left them, and the stage prompt shows that on purpose: the change lands on the cost of each call, not on what each call sends.

[Volume 1 Build 10](https://github.com/jasonjeske/hermes-master-class/blob/main/masterclass/build-10-tuning-and-safety.md) set the basics: approval modes, the compression threshold and a cheaper model for side tasks. This stage goes underneath them, and it corrects one number Build 10 took from the docs.

### The cache lasts one session

Hermes builds the system prompt and the tool list once per session and sends the same bytes on every call after that. That is how it keeps the provider's prefix cache warm, and it is why most of what you change in a running session waits for the next one.

| In a running session | Breaks the cache | What happens |
|---|---|---|
| A memory write | No | It reaches disk now and the prompt at the next session or compaction |
| A skill install or edit | No | A short note in the next message lists the change; the index itself updates next session |
| An edit to SOUL.md or AGENTS.md | No | Read again at the next session or compaction |
| Midnight | No | The date line stays fixed to the start of the session |
| A model switch with `/model` | Yes | The prompt is rebuilt and the new model starts with a cold cache |
| A toolset change | Yes | The tool list heads every request, so everything is written again |
| A compaction | Yes | The system prompt is rebuilt and the whole prefix is written again |
| Resuming from another folder | Yes | Context files depend on the folder, so the prompt is rebuilt |

The habit that falls out of the table: pick the model before you start, and change it between sessions, not inside one. A switch in a long session pays to write the whole conversation again at the new model's price. The habit is [witcheer's](https://x.com/witcheer/status/2074153526222114974): batch your model switches, or start a fresh session, instead of going back and forth in one.

How long a cached prefix lives is `prompt_caching.cache_ttl`, and the default is `5m`. A one hour cache write costs 2x the base input price against 1.25x for five minutes, so the long tier pays off only when you come back to a session after a pause. `auto`, opt-in since v0.21.5, picks per session: one hour for sessions a person types into (CLI, TUI, Desktop and the messaging platforms) and five minutes for subagents, cron, one-shots and the other machine-paced runs. On an install whose sessions are parked and resumed through the day, the docs put the cut in the interactive cache-write bill at roughly 40%; the code's own note, from one install, says 42%.

*`cache-ttl.sh`*

```bash
hermes config set prompt_caching.cache_ttl auto
```

A value such as `off` or `false` in `prompt_caching.cache_ttl` turns caching off. The docs say no such switch exists, but it does. It earns its place only on plans that bill cache writes and behind proxies that add their own cache markers, so leave caching on otherwise.

Two provider routes need a check of their own. If you run Claude through the Nous Portal, the default chat wire caches only the system prompt inside tool loops: the reports in [#141833](https://github.com/NousResearch/hermes-agent/issues/141833) show 13 to 21% cache hits, and the native wire measured 95% or better. The default stays `chat` because `native` has a cache problem of its own on the OpenRouter-served path, so treat the switch as a test: set it, run one long tool-heavy task, and watch the cache field in the status bar.

On OpenRouter, the response cache is on by default: send the identical request again within 300 seconds, the default of `openrouter.response_cache_ttl`, and you get the stored response back, tool calls included ([#70387](https://github.com/NousResearch/hermes-agent/issues/70387)). In an agent loop a replayed tool call is a stale decision, so turn it off there.

*`provider-cache.sh`*

```bash
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

*`side-tasks.yaml`*

```yaml
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

*`review-off.sh`*

```bash
hermes config set auxiliary.background_review.enabled false
```

`approvals.mode` defaults to `smart`, and a smart approval asks a side-task model about every command it flags as dangerous: one small call per flagged command, on your main model unless `auxiliary.approval` is routed. `manual` drops that call and asks you every time instead; [Volume 1 Build 10](https://github.com/jasonjeske/hermes-master-class/blob/main/masterclass/build-10-tuning-and-safety.md) covers what each mode lets through. Session titles are the last small one: `auxiliary.title_generation.model_upgrade_enabled` set to `false` keeps the free title Hermes derives on its own and skips the model call.

### The stage prompt

*`prompt-stage-6-runtime.md`*

```markdown
Tune Hermes, stage 6: Cache, Compression and Side Tasks. Work in five steps, one change at a time.
MEASURE: Read `hermes config get prompt_caching.cache_ttl`, `hermes config get compression.threshold`, `hermes config get auxiliary.compression.provider`, `hermes config get auxiliary.background_review.enabled`, `hermes config get auxiliary.background_review.provider` and `hermes config get approvals.mode`, then tell me which model and provider you run on, its context window, and which side tasks run on it. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: Propose the one change that fits how I work: `prompt_caching.cache_ttl` set to `auto` if I come back to sessions after breaks, or `auxiliary.compression` and `auxiliary.background_review` routed to a cheaper model on a provider I already use, by provider and model only, each key set with `hermes config set`. Show the exact command, or the exact lines of config.yaml before and after, and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: Copy config.yaml to a dated backup next to it with `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in its folder, never overwriting an earlier backup, then make only the change I approved.
VERIFY: Read the changed key back with `hermes config get` and confirm that the fixed budget did not move, because this stage changes what each call costs, not what it sends. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

- [ ] `hermes config get prompt_caching.cache_ttl` prints the value you chose, `5m` or `auto`
- [ ] You know whether your model's window is under 512K, and so whether your threshold acts as 0.75
- [ ] `/compress --preview` in a long session showed the plan without calling a model
- [ ] `hermes config get auxiliary.compression.provider` names the provider you routed it to, or you chose to keep `auto`
- [ ] The fixed budget from the prompt-size check matches the one from before this stage

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-TUNING.md)
