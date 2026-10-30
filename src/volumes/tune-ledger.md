## The Tuning Ledger

Nine stages, one prompt and one proof each. Every prompt measures your install, proposes one change, waits for your yes, backs up config.yaml before it applies anything, and measures again.

### Prompts

Each prompt sits at the end of its stage page, just before the stage's Verify list. The figures were measured on a fresh install of v0.22.5 with the 58 bundled skills unless the row says otherwise; your numbers will differ, which is why every prompt measures yours first.

```table
| Stage | Prompt | What it changes |
| [0 Measure before you change anything](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-00-measure-before-you-change-anything.md) | `prompt-stage-0-measure.md` | Nothing in config: it saves your first measurement as `tune/baseline.json` in the folder that holds config.yaml |
| [1 Defer what you rarely call](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-01-defer-what-you-rarely-call.md) | `prompt-stage-1-defer.md` | An explicit `tools.tool_search.defer` list, the curated default names first and five heavy tools after them: 3,214 fewer tokens, every tool still reachable |
| [2 Pick a toolset profile](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-02-pick-a-toolset-profile.md) | `prompt-stage-2-profile.md` | The toolsets on in `platform_toolsets.cli`, picked for your work: the four profiles measured from 11,529 tokens (operator) down to 3,931 (lean chat), against 13,769 for the default |
| [3 Trim the skills](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-03-trim-the-skills.md) | `prompt-stage-3-skills.md` | A `skills.disabled` list in config.yaml for the skills you never load, which take them out of the index; opting out to the one essential skill saved 1,381 tokens |
| [4 Memory and context files](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-04-memory-and-context-files.md) | `prompt-stage-4-memory.md` | What loads into every session from memory and context files; with memory filled toward its caps, setting `memory.memory_enabled` and `memory.user_profile_enabled` to false saved 1,769 tokens |
| [5 MCP servers](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-05-mcp-servers.md) | `prompt-stage-5-mcp.md` | A tool include list for an MCP server: the filesystem server's 14 tools cost 326 tokens in the listing, and 54 with two of them included |
| [6 Cache, compression and side tasks](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-06-cache-compression-and-side-tasks.md) | `prompt-stage-6-runtime.md` | One runtime setting in config.yaml: the cache lifetime, or the model that runs compression and background review. The fixed budget stays where it was |
| [7 Cap the runaways](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-07-cap-the-runaways.md) | `prompt-stage-7-caps.md` | One open budget capped in config.yaml, such as the turn limit or a delegation limit. The fixed budget stays where it was |
| [8 Keep it tuned](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-08-keep-it-tuned.md) | `prompt-stage-8-keep-tuned.md` | The hermes-tune skill, installed by you with the command the prompt hands you: one more row in the skills index, and a weekly audit offered under `/suggestions` |
```

### The skill

The [hermes-tune skill](https://github.com/jasonjeske/hermes-master-class/tree/main/skills/hermes-tune) carries this ladder into Hermes. In a session it walks the stages with you, one approved change at a time. As a weekly audit it measures your install, compares it with `tune/baseline.json` and saves a dated report with its proposals beside it; it is told to change nothing else, and it checks before and after each run that it did not. Install it in your own terminal through the skills hub, which runs Hermes's own scanner on it before it lands:

```code lang=bash file=install-hermes-tune.sh
hermes skills install jasonjeske/hermes-master-class/skills/hermes-tune --yes
```

After the install, `/suggestions` offers the weekly audit on the schedule `0 9 * * 1`, Mondays at 9:00, with only the terminal and file toolsets. Hermes never schedules it for you, and a scheduled job fires only while a gateway runs. Each run is one agent session on `cron.model`, or on your main model when that is empty, so pin the job to an inexpensive model with `hermes cron edit`, as [Stage 8](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-08-keep-it-tuned.md) shows. After every `hermes update`, ask the skill for an audit by hand.

### Verify

```checklist
[ ] Stage 0: `tune/baseline.json` sits in the folder that holds config.yaml and holds your first `hermes prompt-size --json` reading
[ ] Stage 1: `hermes config get tools.tool_search.defer` prints the curated default names first and the heavy tools you chose after them
[ ] Stage 2: `hermes tools list` shows only your profile's toolsets enabled
[ ] Stage 3: `hermes skills list --enabled-only` no longer lists the skills you turned off
[ ] Stage 4: `wc -m` on MEMORY.md and USER.md in the memories folder of your Hermes home shows each under nine tenths of its cap, `memory.memory_char_limit` and `memory.user_char_limit`
[ ] Stage 5: the Tools column of `hermes mcp list` shows a selected count, not all, for every server you kept
[ ] Stage 6: the setting you changed reads back with `hermes config get`, and `hermes prompt-size --json` shows the budget unchanged
[ ] Stage 7: the cap you set reads back with `hermes config get`, a capped `agent.max_turns` as a number, and the budget did not move
[ ] Stage 8: `hermes skills list` shows hermes-tune, `/suggestions` offers its weekly audit, and if you scheduled it, the job is pinned with `hermes cron edit` or `cron.model` is set
[ ] A dated backup such as `config-YYYY-MM-DD-HHMMSS.yaml` sits next to config.yaml for every change you approved, none of them overwritten, so the first one still holds config.yaml as it was before you started
```

```callout kind=success title="What you have now"
A Hermes install that sends what your work needs, measured before and after every change, with a dated backup behind each one. You know what each toolset, skill, memory store and MCP server costs before your first word, which changes cut what every call sends and which only change what calls cost, and where the open budgets now have caps. And you have a skill that can measure the install every Monday, tell you what drifted since your baseline, and propose changes that wait for your yes.
```
