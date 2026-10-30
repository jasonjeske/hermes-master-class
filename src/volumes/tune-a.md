---
title: The Hermes Tuning Masterclass
subtitle: Volume 6 of the Hermes Agent Masterclass. Measure what Hermes sends before you type, cut it with stage prompts that ask before they change anything, pick a toolset profile for the work you do, and keep it tuned with a skill that audits your install every week
why: Every call a default Hermes install makes carries thousands of tokens of tool definitions, skill listings and guidance before your first word, and a large part of it serves tools you may never call. This volume measures each lever on Hermes Agent v0.22.5 in a sealed install and gives you prompts that make Hermes trim its own budget, one approved change at a time.
date: 2026-10-30
eyebrow: HERMES TUNING MASTERCLASS · VOLUME 6
---

![The Hermes Tuning Masterclass](assets/art/v6-hero.webp)

## Orientation

The first five volumes built the agent, the app, the team and the company, and showed the habits that run them. The bonus class ranked every slash command. This volume is about what all of it costs before you say a word.

Every call a Hermes install makes starts with a fixed budget: the schemas of the tools the model can call, a system prompt with your skills index inside it, and the schema of the subagent tool. On a fresh install of v0.22.5 that is 13,769 tokens before your first word, and a large part of it serves tools you may never call. Stage 0 shows exactly where it goes.

This volume measures each lever that moves that number, in the order you should pull them, and gives you a prompt for each one that makes Hermes do the trimming itself, one approved change at a time. It tunes for the four kinds of work people run Hermes for: running a business, automating a company, research, and agentic coding. Stage 2 turns those into three ready toolset profiles, one of them shared by business and company work, and adds a lean chat profile for the terminal; every other stage applies to all four.

The order is the point. Stage 0 measures and changes nothing. Stage 1 takes the free win, deferring heavy tools so they cost almost nothing until they are used, before Stage 2 asks you to give anything up. Stages 3 to 5 trim the skills, memory, context files and MCP servers. Stages 6 and 7 move from the fixed budget to what each call and each runaway costs. Stage 8 keeps the result from drifting, with a skill that audits your install every week.

This volume does not repeat [Volume 1, Build 10](https://github.com/jasonjeske/hermes-master-class/blob/main/masterclass/build-10-tuning-and-safety.md), which it rests on. Approvals, reasoning effort basics, the side task models, compression threshold basics, turn caps, `agent.verify_on_stop`, `hermes insights`, `hermes sessions prune` and `hermes update` are set up there. Read it first if you have not; this volume goes underneath it.

```callout kind=note title="What this volume rests on"
Every token count here is Hermes's own estimate: the bytes it sends, divided by four, the same arithmetic `/context` shows. Each one was measured in a sealed, throwaway install of Hermes Agent v0.22.5 (commit bf0203a, released October 22, 2026) with the 58 bundled skills seeded, on the cli platform, and every command, flag and config key was checked against the source at that commit and the official documentation. Your numbers will differ, because your model, skills, memory and project files differ, which is why every stage starts by measuring yours. Where the docs and the code disagree, the text follows the code, and [the closing page](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/99-where-the-docs-and-the-code-disagree.md) lists every disagreement found.
```

### How a stage prompt works

Every stage ends with one prompt. Paste it into a Hermes session on the profile you are tuning, and Hermes works through five steps:

```table
| Step | What Hermes does |
| Measure | Reads what the stage is about, then runs `hermes prompt-size` with `--json` and shows the system prompt bytes, the tool schema bytes and their sum divided by four |
| Propose | Proposes one change, as the exact command or the exact lines of config.yaml before and after, with what it saves and what it costs you |
| Wait | Changes nothing until you reply yes |
| Apply | Copies config.yaml to a new dated backup next to it, `config-YYYY-MM-DD-HHMMSS.yaml`, so no earlier backup is overwritten, then makes only the change you approved |
| Verify | Runs the stage's own check, measures again, and shows before, after and the difference |
```

Hermes applies a config change with its own commands, never by editing config.yaml: its file tools refuse to write the active config.yaml (`tools/file_tools_write_guards.py:166-173`). So the prompts use `hermes tools` and `hermes config set`, which also takes a list written as JSON with no spaces, as in `hermes config set tools.tool_search.defer '<JSON list>'` (`hermes_cli/config.py:3207-3240`). The YAML blocks in this volume are for you, when you edit config.yaml by hand. A few changes Hermes never makes itself and hands you the exact command instead: removing bundled skills, cutting memory or rule files, editing or pinning cron jobs, installing the hermes-tune skill and updating Hermes.

The prompts measure with `hermes prompt-size` for three reasons. It runs offline, with no API call, so measuring costs nothing. Hermes can run it itself, through its terminal tool. And it reports the budget a fresh session would start with, which is the view that matters after a change: a running session keeps the system prompt and tool list it started with, so `/context` in the session that made a change still shows the old budget. A new session shows the new one.

One prompt makes one change, so every saving is measured on its own and every change can be undone on its own. How you undo it depends on what the stage touched:

```table
| Stage | What a change touches | How you undo it |
| 1, 2, 5 and 6 | config.yaml | Copy the dated backup back over config.yaml, then open a new session |
| 3 | config.yaml, or the bundled skills on disk | The backup restores a `skills.disabled` list; `hermes skills opt-in --sync` seeds removed bundled skills again |
| 4 | config.yaml, or your memory and rule files | The backup restores config; a memory or rule file comes back only from a copy you make before you cut it |
| 7 | config.yaml, or a cron job | The backup restores config; cron jobs live in their own store, so `hermes cron edit` sets a job back |
| 8 | A new skill | `hermes skills uninstall hermes-tune`, and `hermes cron remove` with the audit's job ID if you scheduled it |
```

Some sessions have no terminal tool; the lean chat profile in Stage 2 turns it off, for one. The last line of every prompt covers that case: Hermes gives you each command to run and waits for your output.

Both halves of this design come from witcheer. The [Hermes Autopilot prompts](https://notwitcheer.github.io/hermes-recipes/prompts/) are read-only audits that propose a few one-line changes and stop for a yes. [Hermes Wingtips #31](https://x.com/witcheer/status/2081381590488568218) and [#48](https://x.com/witcheer/status/2089706892993941840) measure the fixed budget offline with `hermes prompt-size` and compare it before and after trimming, at zero token cost. The stage prompts here join the two: each one stays a read-only audit until you say yes, with a measurement before and after its one change.

### The ladder at a glance

```table
| Stage | What it changes | Measured on a fresh install | Moves the fixed budget |
| [Stage 0](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-00-measure-before-you-change-anything.md) | Nothing yet: you save a baseline next to config.yaml | 13,769 tokens before your first word | No |
| [Stage 1](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-01-defer-what-you-rarely-call.md) | Five heavy tools move behind tool search | 13,769 to 10,555, every tool still reachable | Yes |
| [Stage 2](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-02-pick-a-toolset-profile.md) | The toolsets each platform turns on | 3,931 to 11,529, by profile | Yes |
| [Stage 3](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-03-trim-the-skills.md) | Which skills sit in the index, and what they cost to load | 12,388 with only the essential skill, minus 1,381 | Yes |
| [Stage 4](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-04-memory-and-context-files.md) | Memory, context files and the coding brief | Full memory plus 686; a 2.4 KB AGENTS.md plus 1,401 | Yes |
| [Stage 5](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-05-mcp-servers.md) | MCP servers and the tools each one exposes | A 14-tool server plus 326 in the listing, plus 54 with two tools kept | Yes, if you run MCP servers |
| [Stage 6](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-06-cache-compression-and-side-tasks.md) | Cache lifetime, compression and the side task models | Cost per call, outside the fixed budget | No |
| [Stage 7](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-07-cap-the-runaways.md) | Turn, subagent and cron limits, and the session store | Limits, not tokens: most are open by default | No |
| [Stage 8](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-08-keep-it-tuned.md) | A weekly audit by the hermes-tune skill | One more skill in the index, and a weekly report once you schedule it | Barely: one index row, though the scheduled audit runs a full agent session every week |
```

## Stage 0: Measure Before You Change Anything

![What Hermes sends before you type: tool definitions, the system prompt with the skills index, and subagent definitions](assets/art/v6-budget.webp)

### What this stage changes

Nothing in your config. You find out what your install sends before your first word, read it with the tools Hermes already has, and save the numbers as a baseline. Every later stage measures against it, and so does the weekly audit in Stage 8.

### What a fresh install sends

Three parts ride on every call before you type. Here is a fresh install of v0.22.5 with the 58 bundled skills, by Hermes's own breakdown:

```table
| Part | Tokens | What it is |
| Tool definitions | 9,170 | The JSON schemas of the tools the model can call directly |
| System prompt | 3,433 | Hermes's instructions to the model, with the skills index inside it, about 1,720 tokens on its own |
| Subagent definitions | 1,166 | The schema of delegate_task, the tool that starts subagents |
| Total | 13,769 | Before your first word |
```

Turn every toolset off and the same install sends 778 tokens. Most of the difference is tool schemas, which is why Stages 1 and 2 come first.

### Three ways to read the budget

```table
| Tool | Where you run it | What it shows | Cost |
| `/context` | Inside a session | The window by category: system prompt, tool definitions, rules, skills, MCP, subagent definitions, memory and conversation, then free space | Local, no provider call |
| `/context all` | Inside a session | All of that, plus the schema cost of every toolset and the index and load cost of every skill | Local, no provider call |
| `hermes prompt-size` | Your terminal, or Hermes's terminal tool | The fixed budget of a fresh session in bytes: system prompt, skills index, memory, user profile, and tool schemas by toolset; `--json` prints it as JSON, `--platform` simulates a chat platform | Offline, no API call |
```

All three start from bytes. `/context` divides them by four and rounds up; `hermes prompt-size` prints the bytes, so divide by four yourself. Expect the two to sit about 70 tokens apart on the same config: `hermes prompt-size` builds its tool list without the desktop_project listing line that every live session adds (Stage 1 explains that line).

### The Skills 0 trap

Run `/context` on a fresh install and there is no Skills row, although 58 skills are installed. The category comes out at 0, and a row at 0 is not printed. The index is there; it is billed as System prompt. It sits in the volatile tier of the prompt (`agent/system_prompt.py:785`), while the breakdown looks for it in the stable tier (`agent/context_breakdown.py:152`) and finds nothing. Read skill costs from `/context all` or `hermes prompt-size`, which show the index by itself.

### Reading the sample

This is `/context all` on that fresh install, exactly as Hermes printed it in the sealed run:

```code lang=text file=sample-context-all.txt
Conversation is empty (no messages yet).
  user: 0, assistant: 0, tool: 0, system: 0
Model: claude-sonnet-5-5
Provider: auto

Estimated usage by category
■ System prompt        ~    3,433 tokens ~  0.3%
▣ Tool definitions     ~    9,170 tokens ~  0.9%
▦ Subagent definitions ~    1,166 tokens ~  0.1%
▨ Conversation         ~        0 tokens ~  0.0%
· Free space           ~  986,231 tokens ~ 98.6%

Context window: ~13,769 / 1,000,000 tokens (~1%)
Source: local estimate; category counts are local estimates.

Toolsets by schema cost (largest first)
  file                       4 tools ~   1,419 tokens
  skills                     3 tools ~   1,241 tokens
  delegation                 1 tools ~   1,165 tokens
  connections                1 tools ~   1,130 tokens
  browser-use                1 tools ~     831 tokens
  memory                     1 tools ~     821 tokens
  code_execution             1 tools ~     770 tokens
  (unknown)                  3 tools ~     745 tokens
  terminal                   1 tools ~     686 tokens
  web                        2 tools ~     478 tokens
  clarify                    1 tools ~     454 tokens
  tts                        1 tools ~     380 tokens
  vision                     1 tools ~     212 tokens
```

Read three things in it. The Context window line holds the total that every stage moves, 13,769 here. The toolset table is the price list Stage 2 works from, largest first. And the (unknown) row is not an error: it is the tool search bridge from Stage 1, three tools that carry the listing of every deferred tool.

### Money is a different measurement

Tokens before your first word are one number. What a session costs is another, and on v0.22.5 none of Hermes's own displays is audit grade:

```table
| Where | What it gives you | Watch out |
| `/usage` | Session tokens and your provider's account limits | It makes a provider call, and it prints no cost line on the CLI or a chat platform, although the docs promise one |
| `/insights`, `hermes insights` | Tokens, estimated cost, models, platforms and top tools, from the local session database | A lower bound, not a bill: totals fold in cache reads and writes, and custom providers price at zero |
| The status bar | Context use, a cache hit percentage, latency | No cost: `display.show_cost` exists in config and nothing reads it |
| The dashboard's analytics | Token and cost charts | Hidden unless `dashboard.show_token_analytics` is true, and its own comment says the totals can be 10x to 100x under the bill |
```

For money, go to the source: your provider's bill, and the line Hermes writes to agent.log for every API call, which carries that call's cache read and cache write counts.

```callout kind=warn title="The request dump holds everything"
`HERMES_DUMP_REQUESTS=1` writes full prompts to the sessions folder in your Hermes home, your memory and project context files included. If you use it to see exactly what goes out, delete the dumps when you are done and never share them.
```

### Diagnostics that spend

Two commands look like the same checkup and are not. `hermes doctor` calls your providers even without `--live`. `hermes status` reads local state only, unless you add `--deep`, which calls out. To check an install without touching a provider, use `hermes status` and the three tools above.

### The stage prompt

Paste this into a session on the profile you are tuning. It measures, proposes saving a baseline, and changes nothing else.

```code lang=markdown file=prompt-stage-0-measure.md
Tune Hermes, stage 0: Measure Before You Change Anything. Work in five steps, one change at a time.
MEASURE: Run `hermes config path` to find my config.yaml and `hermes tools list` to see which toolsets are on. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: Propose saving this measurement as `tune/baseline.json` in the folder that holds config.yaml: the `hermes prompt-size --json` output with two more top-level keys, `date` for today's date as YYYY-MM-DD and `version_label` for the first line of `hermes --version`. Show the exact command, or the exact lines of config.yaml before and after, and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: Copy config.yaml to a dated backup next to it with `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in its folder, never overwriting an earlier backup, then make only the change I approved.
VERIFY: Read `tune/baseline.json` back and confirm it holds the bytes you showed me, today's `date` and the `version_label`. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

```checklist
[ ] `hermes prompt-size` ran offline and showed the system prompt bytes and the tool schema bytes
[ ] tune/baseline.json sits in the folder with config.yaml, with `date` set to today and `version_label` set to the first line of `hermes --version`
[ ] A new session's `/context all` shows your own toolset table, and you can name your three most expensive toolsets
[ ] You know why `/context` shows no Skills row, and where the index is billed instead
[ ] No request dump is left in your sessions folder
```

## Stage 1: Defer What You Rarely Call

![The tool search lever: four ways to defer tools, measured](assets/art/v6-tool-search.webp)

### What this stage changes

One list in config.yaml, `tools.tool_search.defer`. Five heavy tools move behind tool search, which takes a fresh install from 13,769 tokens to 10,555, 23 percent less, and every tool stays one search away. It is the largest cut in this volume that takes nothing away, so it comes before anything that does.

### How tool search works

Tool search is on by default: `tools.tool_search.enabled` is `auto`, which means on. A deferred tool leaves the tool array the model sees. In its place, three bridge tools, tool_search, tool_describe and tool_call, carry a compact listing: each deferred tool's name and the first sentence of its description, cut at 60 characters. When the model needs a deferred tool, it finds it in the listing and calls it through the bridge.

Out of the box, the curated list defers computer_use, session_search, image_generate, todo_list, process_manage, cronjob_manage, browser_vault and twelve desktop app tools. MCP and plugin tools always defer while the bridge is on. A core tool defers only when the list names it.

That is the (unknown) row in `/context all`: 3 tools, 745 tokens. The bridge tools belong to no toolset, so Hermes has no name for the row. It is also why any session with a toolset on pays a floor of about 568 tokens: the bridge costs 498 tokens bare, and every live session adds a listing line for desktop_project, which is on the curated list.

```table
| Setting | Default | What it does |
| `tools.tool_search.enabled` | `auto` | `auto` and `on` run the bridge; `off` sends every schema on every call |
| `tools.tool_search.defer` | The curated list | The core tools that sit behind the bridge |
| `tools.tool_search.listing_max_tokens` | `4000` | The listing's ceiling in tokens |
| `tools.tool_search.threshold_pct` | `5` | The listing's ceiling as a percent of the context window; the smaller ceiling wins |
| `tools.tool_search.search_default_limit` | `5` | Results per search when the model does not ask for a number |
| `tools.tool_search.max_search_limit` | `25` | The most results one search can return |
```

### What we measured

Four settings on the same fresh install, every tool reachable in all four:

```table
| Setting | Tokens before your first word | Against the default |
| `defer: []`, every tool eager | 19,158 | plus 5,389 |
| Tool search off | 18,628 | plus 4,859 |
| The default install | 13,769 | |
| Five heavy tools deferred as well | 10,555 | minus 3,214, 23 percent less |
```

Turning tool search off to keep things simple costs 4,859 tokens on every call. An empty defer list costs even more.

### The replace rule

An explicit defer list replaces the curated one; it does not add to it (`hermes_cli/config_defaults.py:2032-2039`). Write `defer: [delegate_task]`, or set that one-name list with `hermes config set`, and the curated tools all go eager again. So copy the curated list first and append, and write `defer: []` only if you mean every tool eager.

### The ready list

This is the curated list, in order, with the five heavy tools appended: the setting measured above at 10,555. To set it by hand, merge it into config.yaml; if you already have a tools section, put the defer line under its tool_search part.

```code lang=yaml file=defer-heavy.yaml
TUNE_DEFER_HEAVY_YAML
```

Or set the same list with one command, the way the stage prompt applies it. The list replaces whatever list is there, which is why it starts with every curated name:

```code lang=bash file=defer-heavy.sh
hermes config set tools.tool_search.defer '["computer_use","session_search","image_generate","todo_list","process_manage","cronjob_manage","browser_vault","drive_preview","gui_tour","desktop_preview","annotate_preview","manage_catalog","show_tip","desktop_project","close_terminal","set_theme","read_terminal","read_window_below","focus_pane","manage_connections","browser_exec","text_to_speech","vision_analyze","execute_code"]'
```

Deferring a tool does not turn it off. Its toolset stays on, and the tool is one search away:

```table
| Deferred tool | Its toolset | Its schema in /context all |
| manage_connections | connections | 1,130 |
| browser_exec | browser, shown as browser-use | 831 |
| execute_code | code_execution | 770 |
| text_to_speech | tts | 380 |
| vision_analyze | vision | 212 |
```

### The trade-off

A deferred tool still costs its listing line, about 25 tokens, and each use costs the model a search round trip. The first time a session needs it, the bridge takes 3 to 5 calls to find and run it. So defer what is heavy and occasional, and keep eager what runs every session. If you write code every session, take execute_code off the list: you would pay that round trip every time.

### The stage prompt

It reads your defer list and your recent tool use, proposes one list, and waits for your yes.

```code lang=markdown file=prompt-stage-1-defer.md
Tune Hermes, stage 1: Defer What You Rarely Call. Work in five steps, one change at a time.
MEASURE: Run `hermes config get tools.tool_search.enabled` and `hermes config get tools.tool_search.defer`, and use `hermes insights --days 30` to see how often I used manage_connections, browser_exec, text_to_speech, vision_analyze and execute_code. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: Propose one `hermes config set tools.tool_search.defer '<JSON list>'` command, the list written as JSON with no spaces, that keeps every name already in the list, in order, and appends whichever of those five tools I do not use every session, because the list you set replaces the whole setting instead of adding to it. If tool search is off, propose only `hermes config set tools.tool_search.enabled auto`. Apply it with that command and never edit config.yaml with write_file or patch, which Hermes refuses. Show the exact command, or the exact lines of config.yaml before and after, and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: Copy config.yaml to a dated backup next to it with `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in its folder, never overwriting an earlier backup, then make only the change I approved.
VERIFY: Run `hermes config get tools.tool_search.defer` and confirm that every name from before is still in the list. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

```checklist
[ ] `hermes config get tools.tool_search.defer` lists every curated name, then the heavy tools you chose
[ ] `hermes prompt-size` shows fewer tool schema bytes than your baseline
[ ] In a new session, `/context all` shows a smaller total and a larger (unknown) row
[ ] A task that needs a deferred tool still works: Hermes finds it through tool search
```

## Stage 2: Pick a Toolset Profile

![What turning one toolset off saves](assets/art/v6-toolset-savings.webp)

### What this stage changes

The toolsets your CLI turns on, written as one list in config.yaml. A toolset you turn off stops sending its schemas, and any text the system prompt carries for it, on every call. Unlike Stage 1 this takes capabilities away, so pick by the work you do and keep what you use.

### What each toolset costs

Turning off one default toolset at a time on the fresh install saves what the second column shows. The third column is Hermes's own schema price from `/context all`.

```table
| Toolset | Turning it off saves | Its schemas in /context all | What you lose |
| skills | 3,111 | 1,241, 3 tools | Loading, listing and writing skills, and the skills index |
| terminal | 1,599 | 686 | Shell commands and background processes; the stage prompts then ask you to run their commands |
| file | 1,588 | 1,419, 4 tools | Reading, writing, patching and searching files |
| delegation | 1,166 | 1,165, billed as subagent definitions | Subagents |
| connections | 1,163 | 1,130 | Hosted app connectors and their accounts |
| memory | 1,082 | 821 | Saving to memory; what MEMORY.md and USER.md already hold stays in the prompt (Stage 4) |
| browser | 854 | 831, as browser-use | Browser automation |
| code_execution | 769 | 770 | Python scripts that call tools |
| web | 596 | 478, 2 tools | Web search and page extraction |
| clarify | 455 | 454 | Clarifying questions with choices |
| tts | 380 | 380 | Text to speech |
| vision | 211 | 212 | Image analysis |
| cronjob | 28 | Deferred, inside the (unknown) row | Managing cron jobs from a session |
| session_search | 25 | Deferred, inside the (unknown) row | Searching past sessions |
| computer_use | 25 | Deferred, inside the (unknown) row | Desktop control |
| todo | 20 | Deferred, inside the (unknown) row | The task list for multi-step work |
| image_gen | 0 | None: gated until an image provider is set up, and deferred | Image generation |
```

The two columns differ because the saving is everything that leaves the request, not only the schemas: turning skills off removes the whole skills index along with its three tools, and a toolset's saving also covers any text the system prompt carries for it. Delegation is the case where the two match: its one schema is nearly its whole cost.

Kanban is off by default, and turning it on adds 6,602 tokens. The toolsets that are already deferred save only 20 to 28 tokens each, their listing lines, so turning them off buys almost nothing.

![Same agent, five budgets: the toolset profiles measured](assets/art/v6-profiles.webp)

### Four ready profiles

Three profiles cover the four kinds of work, with operator serving both running a business and automating a company, and the fourth, lean chat, cuts Hermes down to chat in the terminal. Each was measured on the cli platform, on exactly the list shown, with the 58 bundled skills and with only the one essential skill that Stage 3 explains.

```table
| Your work | Profile | Toolsets | Tokens, 58 bundled skills | Tokens, essential skill only | You give up |
| Agentic coding | coder | terminal, file, code_execution, web, skills, memory, todo, clarify, session_search, delegation | 11,109 | 9,726 | browser, vision, image_gen, tts, connections, cronjob, computer_use |
| Research | researcher | web, browser, file, memory, skills, session_search, clarify, todo, vision | 8,681 | 7,317 | terminal, code_execution, image_gen, tts, connections, delegation, cronjob, computer_use |
| Running a business or automating a company | operator | web, file, memory, skills, cronjob, clarify, todo, session_search, delegation, connections, terminal | 11,529 | 10,148 | browser, code_execution, vision, image_gen, tts, computer_use |
| Chat in the terminal | lean chat | web, memory, clarify, session_search, todo | 3,931 | 3,931 | browser, terminal, file, code_execution, vision, image_gen, tts, skills, connections, delegation, cronjob, computer_use |
| Anything, untuned | the default | All 17 default toolsets | 13,769 | 12,388 | Nothing |
```

Lean chat sends 71 percent less than the default, and the same with either skill set, because a profile without the skills toolset has no skills index at all. Its 3,931 is a CLI figure, like every figure in the table. A phone gateway takes the same list under its own platform, in `platform_toolsets.telegram` for Telegram or with `hermes tools disable --platform telegram` and the same names, and this volume did not measure that budget.

Each profile is a list to merge into config.yaml by hand. The files live in the [hermes-tune skill](https://github.com/jasonjeske/hermes-master-class/tree/main/skills/hermes-tune/references/profiles), so the skill and this page show the same lists:

```code lang=yaml file=coder.yaml
TUNE_PROFILE_CODER_YAML
```

```code lang=yaml file=researcher.yaml
TUNE_PROFILE_RESEARCHER_YAML
```

```code lang=yaml file=operator.yaml
TUNE_PROFILE_OPERATOR_YAML
```

```code lang=yaml file=lean-chat.yaml
TUNE_PROFILE_LEAN_CHAT_YAML
```

Or reach the same list from a default install with one command, the way the stage prompt applies it. None of the four names `--platform`, so each changes the CLI's list, `platform_toolsets.cli`, the lean chat command included:

```code lang=bash file=coder.sh
hermes tools disable browser vision image_gen tts connections cronjob computer_use
```

```code lang=bash file=researcher.sh
hermes tools disable terminal code_execution image_gen tts connections delegation cronjob computer_use
```

```code lang=bash file=operator.sh
hermes tools disable browser code_execution vision image_gen tts computer_use
```

```code lang=bash file=lean-chat.sh
hermes tools disable browser terminal file code_execution vision image_gen tts skills connections delegation cronjob computer_use
```

### Applying a profile

`hermes tools disable` saves your choice as an explicit `platform_toolsets.cli` list in config.yaml. In our test config it also rewrote the model block as it saved: the `model:` line inside it became a `default:` line. Expect both in the diff against your dated backup.

The top-level `toolsets:` key is legacy; editing it changes nothing, so use `platform_toolsets.cli` or `hermes tools` instead. `agent.disabled_toolsets` is the other lever: it subtracts toolsets on every platform at once, after everything else, so it always wins. It reaches cron too: every cron job loses those toolsets, whatever toolsets the job names, and nothing warns you (`cron/scheduler.py:414-433`). Put terminal there and the weekly audit in Stage 8, which runs on the terminal and file toolsets, can no longer run the commands it measures with.

Each chat platform keeps its own list. Add `--platform telegram` to `hermes tools disable` to trim Telegram's, which lands in `platform_toolsets.telegram`, and measure it with `hermes prompt-size --platform telegram --json`. Giving every platform its own smaller toolset is a habit [witcheer](https://x.com/witcheer/status/2089706892993941840) recommends.

A toolset profile is a list inside one Hermes home. It is not a Hermes profile, the separate homes of [Volume 1, Build 7](https://github.com/jasonjeske/hermes-master-class/blob/main/masterclass/build-07-profiles.md). To give one of those a toolset profile, start the command with `hermes -p <name>`, as in `hermes -p coder tools disable browser vision image_gen tts connections cronjob computer_use`.

To pick from your own history, run `hermes insights --days 30`: its top tools show what you actually use. A toolset whose tools never appear there is a candidate to turn off.

Whatever you change lands next session. The session you change it from keeps its tool list until it ends, so open a new one before you measure with `/context`.

### The stage prompt

It reads your toolsets and your recent tool use, proposes one profile, and waits for your yes.

```code lang=markdown file=prompt-stage-2-profile.md
Tune Hermes, stage 2: Pick a Toolset Profile. Work in five steps, one change at a time.
MEASURE: Run `hermes tools list` to see which toolsets are on and `hermes insights --days 30` to see which tools I used in the last 30 days. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: Propose the one profile that fits how I use you, as the `hermes tools disable` command that gets there from what is on now (with `hermes tools enable` for anything it keeps that is off), and name every toolset it turns off that I used in the last 30 days. The profiles keep these toolsets: coder keeps terminal, file, code_execution, web, skills, memory, todo, clarify, session_search and delegation; researcher keeps web, browser, file, memory, skills, session_search, clarify, todo and vision; operator keeps web, file, memory, skills, cronjob, clarify, todo, session_search, delegation, connections and terminal; lean chat keeps web, memory, clarify, session_search and todo. Apply it with those commands and never edit config.yaml with write_file or patch, which Hermes refuses. Show the exact command, or the exact lines of config.yaml before and after, and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: Copy config.yaml to a dated backup next to it with `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in its folder, never overwriting an earlier backup, then make only the change I approved.
VERIFY: Run `hermes tools list` again and confirm that exactly the profile's toolsets are on. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

```checklist
[ ] `hermes tools list` shows exactly the toolsets of the profile you picked
[ ] config.yaml holds an explicit `platform_toolsets.cli` list, and a dated `config-YYYY-MM-DD-HHMMSS.yaml` backup beside it holds the old config
[ ] `hermes prompt-size` shows fewer tool schema bytes than after Stage 1
[ ] A new session still does the work you picked the profile for
[ ] Every chat platform you use has its own list, measured with `--platform`
```
