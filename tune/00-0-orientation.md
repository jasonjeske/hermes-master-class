# Orientation

![The Hermes Tuning Masterclass](../assets/art/v6-hero.webp)

The first five volumes built the agent, the app, the team and the company, and showed the habits that run them. The bonus class ranked every slash command. This volume is about what all of it costs before you say a word.

Every call a Hermes install makes starts with a fixed budget: the schemas of the tools the model can call, a system prompt with your skills index inside it, and the schema of the subagent tool. On a fresh install of v0.22.5 that is 13,769 tokens before your first word, and a large part of it serves tools you may never call. Stage 0 shows exactly where it goes.

This volume measures each lever that moves that number, in the order you should pull them, and gives you a prompt for each one that makes Hermes do the trimming itself, one approved change at a time. It tunes for the four kinds of work people run Hermes for: running a business, automating a company, research, and agentic coding. Stage 2 turns those into three ready toolset profiles, one of them shared by business and company work, and adds a lean chat profile for the terminal; every other stage applies to all four.

The order is the point. Stage 0 measures and changes nothing. Stage 1 takes the free win, deferring heavy tools so they cost almost nothing until they are used, before Stage 2 asks you to give anything up. Stages 3 to 5 trim the skills, memory, context files and MCP servers. Stages 6 and 7 move from the fixed budget to what each call and each runaway costs. Stage 8 keeps the result from drifting, with a skill that audits your install every week.

This volume does not repeat [Volume 1, Build 10](https://github.com/jasonjeske/hermes-master-class/blob/main/masterclass/build-10-tuning-and-safety.md), which it rests on. Approvals, reasoning effort basics, the side task models, compression threshold basics, turn caps, `agent.verify_on_stop`, `hermes insights`, `hermes sessions prune` and `hermes update` are set up there. Read it first if you have not; this volume goes underneath it.

> 📝 **What this volume rests on**
>
> Every token count here is Hermes's own estimate: the bytes it sends, divided by four, the same arithmetic `/context` shows. Each one was measured in a sealed, throwaway install of Hermes Agent v0.22.5 (commit bf0203a, released October 22, 2026) with the 58 bundled skills seeded, on the cli platform, and every command, flag and config key was checked against the source at that commit and the official documentation. Your numbers will differ, because your model, skills, memory and project files differ, which is why every stage starts by measuring yours. Where the docs and the code disagree, the text follows the code, and [the closing page](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/99-where-the-docs-and-the-code-disagree.md) lists every disagreement found.

### How a stage prompt works

Every stage ends with one prompt. Paste it into a Hermes session on the profile you are tuning, and Hermes works through five steps:

| Step | What Hermes does |
|---|---|
| Measure | Reads what the stage is about, then runs `hermes prompt-size` with `--json` and shows the system prompt bytes, the tool schema bytes and their sum divided by four |
| Propose | Proposes one change, as the exact command or the exact lines of config.yaml before and after, with what it saves and what it costs you |
| Wait | Changes nothing until you reply yes |
| Apply | Copies config.yaml to a new dated backup next to it, `config-YYYY-MM-DD-HHMMSS.yaml`, so no earlier backup is overwritten, then makes only the change you approved |
| Verify | Runs the stage's own check, measures again, and shows before, after and the difference |

Hermes applies a config change with its own commands, never by editing config.yaml: its file tools refuse to write the active config.yaml (`tools/file_tools_write_guards.py:166-173`). So the prompts use `hermes tools` and `hermes config set`, which also takes a list written as JSON with no spaces, as in `hermes config set tools.tool_search.defer '<JSON list>'` (`hermes_cli/config.py:3207-3240`). The YAML blocks in this volume are for you, when you edit config.yaml by hand. A few changes Hermes never makes itself and hands you the exact command instead: removing bundled skills, cutting memory or rule files, editing or pinning cron jobs, installing the hermes-tune skill and updating Hermes.

The prompts measure with `hermes prompt-size` for three reasons. It runs offline, with no API call, so measuring costs nothing. Hermes can run it itself, through its terminal tool. And it reports the budget a fresh session would start with, which is the view that matters after a change: a running session keeps the system prompt and tool list it started with, so `/context` in the session that made a change still shows the old budget. A new session shows the new one.

One prompt makes one change, so every saving is measured on its own and every change can be undone on its own. How you undo it depends on what the stage touched:

| Stage | What a change touches | How you undo it |
|---|---|---|
| 1, 2, 5 and 6 | config.yaml | Copy the dated backup back over config.yaml, then open a new session |
| 3 | config.yaml, or the bundled skills on disk | The backup restores a `skills.disabled` list; `hermes skills opt-in --sync` seeds removed bundled skills again |
| 4 | config.yaml, or your memory and rule files | The backup restores config; a memory or rule file comes back only from a copy you make before you cut it |
| 7 | config.yaml, or a cron job | The backup restores config; cron jobs live in their own store, so `hermes cron edit` sets a job back |
| 8 | A new skill | `hermes skills uninstall hermes-tune`, and `hermes cron remove` with the audit's job ID if you scheduled it |

Some sessions have no terminal tool; the lean chat profile in Stage 2 turns it off, for one. The last line of every prompt covers that case: Hermes gives you each command to run and waits for your output.

Both halves of this design come from witcheer. The [Hermes Autopilot prompts](https://notwitcheer.github.io/hermes-recipes/prompts/) are read-only audits that propose a few one-line changes and stop for a yes. [Hermes Wingtips #31](https://x.com/witcheer/status/2081381590488568218) and [#48](https://x.com/witcheer/status/2089706892993941840) measure the fixed budget offline with `hermes prompt-size` and compare it before and after trimming, at zero token cost. The stage prompts here join the two: each one stays a read-only audit until you say yes, with a measurement before and after its one change.

### The ladder at a glance

| Stage | What it changes | Measured on a fresh install | Moves the fixed budget |
|---|---|---|---|
| [Stage 0](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-00-measure-before-you-change-anything.md) | Nothing yet: you save a baseline next to config.yaml | 13,769 tokens before your first word | No |
| [Stage 1](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-01-defer-what-you-rarely-call.md) | Five heavy tools move behind tool search | 13,769 to 10,555, every tool still reachable | Yes |
| [Stage 2](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-02-pick-a-toolset-profile.md) | The toolsets each platform turns on | 3,931 to 11,529, by profile | Yes |
| [Stage 3](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-03-trim-the-skills.md) | Which skills sit in the index, and what they cost to load | 12,388 with only the essential skill, minus 1,381 | Yes |
| [Stage 4](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-04-memory-and-context-files.md) | Memory, context files and the coding brief | Full memory plus 686; a 2.4 KB AGENTS.md plus 1,401 | Yes |
| [Stage 5](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-05-mcp-servers.md) | MCP servers and the tools each one exposes | A 14-tool server plus 326 in the listing, plus 54 with two tools kept | Yes, if you run MCP servers |
| [Stage 6](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-06-cache-compression-and-side-tasks.md) | Cache lifetime, compression and the side task models | Cost per call, outside the fixed budget | No |
| [Stage 7](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-07-cap-the-runaways.md) | Turn, subagent and cron limits, and the session store | Limits, not tokens: most are open by default | No |
| [Stage 8](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-08-keep-it-tuned.md) | A weekly audit by the hermes-tune skill | One more skill in the index, and a weekly report once you schedule it | Barely: one index row, though the scheduled audit runs a full agent session every week |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-TUNING.md)
