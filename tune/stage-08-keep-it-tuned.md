# Stage 8: Keep It Tuned

### What this stage changes

Everything so far tuned the install you have today. Updates change it: new tools land and defaults flip. This stage installs the hermes-tune skill. It adds one row to your skills index, the only change this stage makes to what each call sends, and it brings a weekly audit that measures, compares with your baseline and proposes changes for you to approve. The audit has a running cost of its own: if you schedule it, every run is one agent session on `cron.model`, or on your main model when that is empty, so the weekly audit section below shows how to pin it to an inexpensive model.

### Why budgets drift

The maintainers work on the fixed prefix too, and it moves both ways. Their context-burden campaign ([#95681](https://github.com/NousResearch/hermes-agent/issues/95681)) cut about 15.2K tokens a call on the CLI, and [PR #97979](https://github.com/NousResearch/hermes-agent/pull/97979) in v0.21.1 took the CLI from 10,578 to 7,306 tokens a call by deferring cold tools. Then the prefix grew from 11,595 to 14,962 tokens in five weeks as new tools landed, until [PR #137084](https://github.com/NousResearch/hermes-agent/pull/137084) in v0.22.0 took 2.1K back.

Those are the maintainers' figures from their own issues and pull requests, not this volume's measurements, so read them for direction. The direction is the lesson: a release can undo a stage you finished, or hand you a saving you never asked for, and only a measurement after the update tells you which.

### The version label trap

The first line of `hermes --version` starts with the release, v0.22.5 here, and a date in parentheses, and the rest of the line names the build, such as its channel and a commit. Only the date can mislead. It was not bumped for v0.22.5, which still shows 2026.9.24, and the release tagged v2026.9.24 is v0.21.5. Go by the release and the build, never the date, and quote the whole first line in a bug report: a report that quotes only the date can be a whole release off.

To learn whether an update is waiting and what it would touch, run the update command's two read-only checks yourself, in your own terminal:

*`version-check.sh`*

```bash
hermes update --check   # is an update waiting; installs nothing
hermes update --plan    # what an update would touch; changes nothing
```

`--check` says whether an update is available without installing anything. `--plan` shows the install kind, every running Hermes service across your profiles with the code version it runs, and how each would restart, and it changes nothing. Looking before you update is a habit from [witcheer's Almanac](https://x.com/witcheer/status/2108564754893582428).

Run both yourself. Hermes flags every `hermes update` command as dangerous, `--check` and `--plan` included, so in a session one has to pass your approval mode first and in a cron job it is refused outright. That is why the stage prompt below hands the update check to you instead of running it.

### Install the skill

*`install-hermes-tune.sh`*

```bash
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

*`pin-the-audit.sh`*

```bash
hermes cron list
hermes cron edit <job-id> --model <cheap-model> --provider <provider>
```

Each run makes twelve checks. A1 to A3, and A5 when a skill is new, report a change since your baseline: a new release or build, a budget that grew, a toolset or skill that appeared. A7 reports its values on every run. Everything else reports a standing condition for as long as it holds, so the same line comes back every week until you fix it or decide to keep it. A default install trips A8 and A9 every week, because its side tasks sit on `auto` and its caps are unlimited, and A10 trips on the audit's own job until you pin its model or set `cron.model`.

| Check | What it reads | It reports when |
|---|---|---|
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

Each run saves `tune/audit-YYYY-MM-DD.md` beside config.yaml: a budget table against the baseline, the drift it found, and numbered proposals with the exact command or config.yaml lines for each. Near the top it records the first line of `hermes --version` and the result of the before and after check described below, and its last line says that nothing was changed, which that check lets you confirm. To act on a proposal, open a session, load hermes-tune and name its number.

The skill's never list holds in both modes: change no config, toolsets, skills, memory or cron jobs during a scheduled run; apply nothing before you say yes in the session; never run `hermes doctor`, `hermes status` with `--deep`, or `hermes debug`, which call providers or upload logs; never read or print secrets; never prune, archive or delete sessions, skills, memories or backups; never install, remove or update skills, plugins or Hermes itself; never schedule, edit or remove cron jobs; and never commit a Hermes home or a backup of one to git, since both hold your `.env` and auth files.

Those lines are instructions to the model, and two Hermes guards back them up. Hermes's file tools, write_file and patch, refuse to write the active config.yaml. In a cron job `approvals.cron_mode` defaults to `deny`, so any command Hermes flags as dangerous, `hermes update` among them, is refused instead of waiting for an approval nobody is there to give. Neither guard covers everything, since a plain `hermes config set` passes both, so the skill also checks its own run: at the start and at the end it hashes config.yaml and cron/jobs.json and lists the files in the skills and memories folders with their sizes, never their content, and the report names any difference. Names and sizes catch a file added, removed or resized, though not an edit that keeps the size, and the scheduler rewrites cron/jobs.json whenever a job starts or ends, so a jobs.json line can be its doing when another job ran during the audit.

After every update, run the audit by hand instead of waiting for Monday: open a session, load hermes-tune and ask for the weekly audit in audit mode. An update is exactly when the budget moves.

### The stage prompt

*`prompt-stage-8-keep-tuned.md`*

```markdown
Tune Hermes, stage 8: Keep It Tuned. Work in five steps, one change at a time.
MEASURE: Read the release and the build from the first line of `hermes --version`, never the date in parentheses, the skills that load from `hermes skills list` with `--enabled-only`, and whether a tune folder with a baseline.json sits next to my config.yaml, whose location `hermes config path` prints. Ask me to run `hermes update --check` in my own terminal and tell you whether an update is waiting, and never run any form of hermes update yourself. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: Propose installing the hermes-tune skill and nothing else, as a command for me to run in my own terminal, hermes skills install jasonjeske/hermes-master-class/skills/hermes-tune --yes, and never run it yourself. Tell me that it adds one row to the skills index and offers a weekly audit under /suggestions that I schedule myself and then pin to an inexpensive model, because each run is one agent session. Show the exact command, or the exact lines of config.yaml before and after, and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: Copy config.yaml to a dated backup next to it with `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in its folder, never overwriting an earlier backup, then make only the change I approved.
VERIFY: Confirm that hermes-tune appears in `hermes skills list` and that the skills index in the breakdown grew by one row. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

- [ ] `hermes skills list` shows hermes-tune, and the skills index in the prompt-size report grew by one row
- [ ] `/suggestions` offered the weekly audit, and you scheduled it yourself or chose not to
- [ ] If you scheduled it, `hermes cron list` shows it on `0 9 * * 1`, and you pinned it with `hermes cron edit` or set `cron.model` first
- [ ] The tune folder next to config.yaml holds baseline.json, and after the first run an audit report whose before and after check reads unchanged
- [ ] You read your release and build from the first line of `hermes --version`, not the date, and ran `hermes update --check` yourself

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-TUNING.md)
