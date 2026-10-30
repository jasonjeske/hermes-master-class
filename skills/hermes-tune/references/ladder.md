# The Tuning Ladder

The nine stages of Volume 6 of the Hermes Agent Masterclass, written for the agent ([the stage pages](https://github.com/jasonjeske/hermes-master-class/tree/main/tune)). Climb in order: measure first, take the free wins, then the trade-offs. Take one stage at a time and propose one change per stage. Run every command through `terminal`.

Every figure below is Hermes's own estimate (bytes divided by four) from a sealed, throwaway install of v0.22.5 with the 58 bundled skills, on the cli platform. The user's install will differ: quote their numbers, and use these only to say what to expect.

## The loop, every stage

1. Measure: the stage's reads, then `hermes prompt-size --json`. Show the system prompt bytes, the tool schema bytes and their sum divided by four.
2. Propose one change from the stage's list: the exact command, and one line on what it saves, what it costs and how it undoes. Never put a key, token or password into config.
3. Wait: change nothing until the user replies yes.
4. Apply: copy config.yaml to a dated backup next to it with `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in its folder, never overwriting an earlier backup (`-p` keeps the 0600 mode, and config.yaml can hold keys), then make only the change the user approved.
5. Verify: the stage's own check, then `hermes prompt-size --json` again and a table of before, after and the difference. Say that this session keeps its old prompt and that a new session shows the change with `/context all`.

Every change goes through a command. Hermes's file tools refuse to write the active config.yaml: write_file and patch stop before any approval. One value takes `hermes config set <key> <value>`. A list takes `hermes config set <key> '<JSON list>'`, written as JSON with no spaces, for example `hermes config set skills.disabled '["p5js","humanizer"]'`; `hermes config set` parses the list. On `skills.disabled` and `skills.platform_disabled` the "not a recognized config key" notice is expected: Hermes reads both keys anyway. The YAML in this file and in `references/profiles/` is the user's path for making the same change by hand.

Undo: the dated backup restores config. Copying it back over config.yaml (`cp -p config-YYYY-MM-DD-HHMMSS.yaml config.yaml`) is a command Hermes flags, so it runs only after the user approves it. Each stage names any other undo it has.

Stages 6 and 7 change no fixed budget: their reads are `hermes config get` lines, and their check shows the budget unchanged. A proposal marked "the user runs it" is one the never list in SKILL.md keeps you from running: give the exact command and let the user run it.

## Stage 0: Measure Before You Change Anything

Reads: `hermes config path`, `hermes --version` and `hermes prompt-size --json`. For a messaging platform, `hermes prompt-size --platform telegram --json`.

From the JSON: the system prompt bytes; the tool schema bytes and the tool count; the skills index, memory and user profile bytes; the per-toolset and per-skill lists, largest first.

Fresh install: 13,769 tokens before the first message. Tool definitions 9,170, system prompt 3,433 (the skills index sits inside it), subagent definitions 1,166. With no toolsets at all: 778.

Propose: save this measurement as `tune/baseline.json` in the folder that holds config.yaml. It is the `hermes prompt-size --json` output with two more top-level keys, `date` (YYYY-MM-DD) and `version_label` (the first line `hermes --version` printed). This stage changes no config, so it has nothing to undo.

Check: `read_file` on `tune/baseline.json` shows today's date, the version label and both byte figures.

Know before the next stage:

- `/context` shows Skills 0 with 58 skills installed: the index sits in the volatile tier and is billed as System prompt.
- `/context` and `/context all` are local estimates, and `hermes prompt-size` is offline and reports bytes. Compare prompt-size with prompt-size.
- Money is a different measurement. `/usage` asks the provider for account limits and shows no cost line on the CLI or the gateway. `/insights` and `hermes insights` read the local state.db and are a lower bound. The provider's bill is the record.

## Stage 1: Defer What You Rarely Call

Reads: `hermes config get tools.tool_search.enabled` and `hermes config get tools.tool_search.defer`, then prompt-size for the tool count and the tool schema bytes.

How it works: with tool search on (the default, `auto`), a deferred tool leaves the tool list the model sees. Three bridge tools, tool_search, tool_describe and tool_call, carry a compact listing in its place: the name plus a first sentence of at most 60 characters. MCP and plugin tools always defer while the bridge is on; core tools defer only when `tools.tool_search.defer` names them. `/context all` bills the bridge as "(unknown)": 3 tools and 745 tokens on a fresh install.

Measured on a fresh install:

| Setting | Tokens | Against the default |
|---|---|---|
| `defer: []`, every tool eager | 19,158 | plus 5,389 |
| tool search off | 18,628 | plus 4,859 |
| the default install | 13,769 | none |
| five heavy tools deferred as well | 10,555 | minus 3,214, or 23 percent |

Propose (you apply it after a yes): the list in `references/profiles/defer-heavy.yaml`, in its order, as one command:

```text
hermes config set tools.tool_search.defer '["computer_use","session_search","image_generate","todo_list","process_manage","cronjob_manage","browser_vault","drive_preview","gui_tour","desktop_preview","annotate_preview","manage_catalog","show_tip","desktop_project","close_terminal","set_theme","read_terminal","read_window_below","focus_pane","manage_connections","browser_exec","text_to_speech","vision_analyze","execute_code"]'
```

The list starts with every curated default name, because an explicit list replaces the default. Never propose a shorter list or `defer: []`.

The five extra names are execute_code (the code_execution toolset), manage_connections (connections), browser_exec (browser), text_to_speech (tts) and vision_analyze (vision). Keep eager what the user runs every session: a coder who runs code every session drops execute_code from the list.

What it costs: a deferred tool sits in the listing at about 25 tokens instead of its full schema, but every use takes a search round trip, and the first use takes 3 to 5 bridge calls.

Check: `hermes config get tools.tool_search.defer` lists every curated name plus the new ones, and the tool count and tool schema bytes went down.

Undo: restore the backup.

## Stage 2: Pick a Toolset Profile

Reads: `hermes tools list`, `hermes insights --days 30` for the tools the user actually calls, and the per-toolset list from prompt-size.

What turning one default toolset off saves on a fresh install, in tokens:

| Toolset | Saves | Toolset | Saves |
|---|---|---|---|
| skills | 3,111 | browser | 854 |
| terminal | 1,599 | code_execution | 769 |
| file | 1,588 | web | 596 |
| delegation | 1,166 | clarify | 455 |
| connections | 1,163 | tts | 380 |
| memory | 1,082 | vision | 211 |

Toolsets whose tools are already deferred save only 20 to 28 tokens: cronjob, session_search, computer_use and todo. image_gen saves nothing without a key. Turning kanban on adds 6,602. Turning skills off also removes the whole skills index and skill loading.

The four profiles, measured; each list is a file in `references/profiles/`:

| Work | Profile | Tokens, 58 bundled skills | Tokens, essential skill only |
|---|---|---|---|
| agentic coding | coder | 11,109 | 9,726 |
| research | researcher | 8,681 | 7,317 |
| running a business or automating a company | operator | 11,529 | 10,148 |
| plain chat, a lean terminal profile | lean chat | 3,931 | 3,931 |
| the default install, for comparison | default | 13,769 | 12,388 |

Lean chat is 71 percent under the default. Like every row here it is a `platform_toolsets.cli` list measured on the CLI. On a phone gateway the same list goes under that platform, for example `platform_toolsets.telegram`, and that was not measured.

Propose (you apply it after a yes): one profile. On a default install, its command:

| Profile | Command | List |
|---|---|---|
| coder | `hermes tools disable browser vision image_gen tts connections cronjob computer_use` | `references/profiles/coder.yaml` |
| researcher | `hermes tools disable terminal code_execution image_gen tts connections delegation cronjob computer_use` | `references/profiles/researcher.yaml` |
| operator | `hermes tools disable browser code_execution vision image_gen tts computer_use` | `references/profiles/operator.yaml` |
| lean chat | `hermes tools disable browser terminal file code_execution vision image_gen tts skills connections delegation cronjob computer_use` | `references/profiles/lean-chat.yaml` |

On an install that is not the default, propose the profile's list from its file instead, in the file's order, as one command:

| Profile | Command |
|---|---|
| coder | `hermes config set platform_toolsets.cli '["terminal","file","code_execution","web","skills","memory","todo","clarify","session_search","delegation"]'` |
| researcher | `hermes config set platform_toolsets.cli '["web","browser","file","memory","skills","session_search","clarify","todo","vision"]'` |
| operator | `hermes config set platform_toolsets.cli '["web","file","memory","skills","cronjob","clarify","todo","session_search","delegation","connections","terminal"]'` |
| lean chat | `hermes config set platform_toolsets.cli '["web","memory","clarify","session_search","todo"]'` |

Applying it:

- `hermes tools disable` writes `platform_toolsets.cli` as an explicit list. The top-level `toolsets:` key is legacy, and changing it changes nothing. `agent.disabled_toolsets` removes a toolset on every platform.
- Another platform takes the same command with `--platform telegram`, which writes `platform_toolsets.telegram`, or the profile's list with `hermes config set platform_toolsets.telegram '<JSON list>'`; measure it with `hermes prompt-size --platform telegram --json`.
- A toolset profile is a list inside one Hermes home, not a Hermes profile. `hermes -p <name>` runs a command against a named Hermes profile.
- The change shows in the next session.

Check: `hermes tools list` shows only the chosen toolsets on cli, the tool count and tool schema bytes went down, and in a new session `/context all` lists the same toolsets.

Undo: restore the backup, or `hermes tools enable <toolset>` to turn one toolset back on.

## Stage 3: Trim the Skills

Reads: `hermes skills list --enabled-only`, `hermes config get skills.auto_load`, and from prompt-size the skills index bytes and the per-skill list, which gives each skill's SKILL.md size as its read cost.

How it costs:

- The index rides in every call: header prose, one row per skill with its description cut to 60 characters, and category lines with no cap. Its prose tells the model it MUST load any skill that is even partly relevant.
- Loading a skill returns its whole SKILL.md into the transcript for the rest of the session. The largest bundled ones are claude-code, humanizer and p5js.
- `skills.auto_load` pins whole skills into every session's prompt.

Measured on a fresh install: opting out to the one essential skill, hermes-agent, gave 12,388, minus 1,381. Turning the skills toolset off saves 3,111 and removes the index and skill loading.

Propose (you apply it after a yes):

- A `skills.disabled` list naming the skills the user never uses, for example `hermes config set skills.disabled '["p5js","humanizer"]'`, or `skills.platform_disabled.<platform>` for one platform. Hermes prints that the key is not recognized and reads it anyway.
- An empty `skills.auto_load` when it pins skills the user does not need in every session: `hermes config set skills.auto_load '[]'`.

Propose (the user runs it):

- `hermes skills config`, an interactive checklist that takes no argument and writes the same `skills.disabled` list.
- `hermes skills opt-out`, which only writes a marker: the bundled copies stay on disk and in the index until `hermes skills opt-out --remove`. `hermes skills opt-in --sync` brings them back.

The curator archives unused agent-created skills on its own and spends no tokens unless `curator.consolidate` is true. It leaves bundled skills alone by default (`curator.prune_builtins: true` lets them age out too), and it never touches hub-installed skills.

Check: `hermes skills list --enabled-only` no longer lists the disabled skills, the skills index bytes went down, and `hermes config get skills.auto_load` prints an empty list.

Undo: restore the backup for `skills.disabled` and `skills.auto_load`. Skills removed with `hermes skills opt-out --remove` come back with `hermes skills opt-in --sync`, which the user runs.

## Stage 4: Memory and Context Files

Reads: `wc -m memories/MEMORY.md memories/USER.md` in the folder that holds config.yaml, counts only and never the content, then `hermes config get memory.memory_char_limit` and `hermes config get memory.user_char_limit` (defaults 2,200 and 1,375 characters). The memory and user profile bytes in prompt-size include about 335 bytes of wrapper per store, so compare the `wc -m` counts with the caps.

How it costs:

- MEMORY.md and USER.md ride in every call as a snapshot taken when the session starts; a memory write reaches the prompt at the next compaction or session.
- Filled toward their caps on a fresh install, the two stores cost 686 more (14,456 in all). With the memory toolset off the total was 13,374 and the memory row stayed at 686. With `memory.memory_enabled` and `memory.user_profile_enabled` both false it fell to 12,687, minus 1,769.
- A 2.4 KB AGENTS.md in the working folder cost 876 as rules and 525 in the system prompt.
- One project rule file wins: .hermes.md, then the AGENTS.md chain, then CLAUDE.md, then .cursorrules. Every subagent pays the AGENTS.md chain again.
- SOUL.md loads from the Hermes home in every session, and a change to it applies in the next one.
- `agent.coding_context: focus` changed nothing in an empty folder; its names-only demotion needs a detected coding project.

Propose (you apply it after a yes):

- When the user wants no saved memory in this Hermes home, both lines as one change: `hermes config set memory.memory_enabled false` and `hermes config set memory.user_profile_enabled false`.

Propose (the user runs it):

- For a long project rule file: show its size and propose a shorter version as before and after excerpts, moving rarely needed sections to a file the agent reads only when needed. The user keeps a copy of the file, then makes the cut.

Never delete or cut memory entries: the never list forbids it. The user trims them.

Check: the memory and user profile counts, or the rule file's size, went down, and a new session's `/context` shows the change.

Undo: restore the backup for the two memory switches. A cut rule file or memory entry comes back only from the copy the user kept.

## Stage 5: MCP Servers

Reads: `hermes mcp list`, whose Tools column shows each server's filter (`all`, `N selected` or `-N excluded`), and for one server `hermes config get mcp_servers.<name>.tools`; then prompt-size. Never print `hermes config get mcp_servers` or `hermes config show`: each server's command, args and url print unmasked and often carry tokens.

How it costs: while tool search is on, every MCP tool is deferred, so a server costs listing lines in the bridge instead of schemas, and `/context` shows MCP 0 with the listing billed to the bridge, "(unknown)". The listing is capped at the smaller of `tools.tool_search.listing_max_tokens` and `tools.tool_search.threshold_pct` of the window. Measured: the official filesystem server, 14 tools, added 326 to the listing, and 54 with an include list of 2 tools. Children keep the parent's MCP servers while `delegation.inherit_mcp_toolsets` is true, its default.

Propose (you apply it after a yes): an include list for a server with many tools, as one command that sets only the server's tools block, never its command, args or env:

```text
hermes config set mcp_servers.<name>.tools.include '["<tool>","<tool>"]'
```

The same block, for a user who edits config.yaml by hand:

```yaml
mcp_servers:
  filesystem:
    tools:
      include: [<tool>, <tool>]
```

The other filters take the same command: `mcp_servers.filesystem.tools.exclude`, `mcp_servers.filesystem.tools.resources` and `mcp_servers.filesystem.tools.prompts` set to false, and `mcp_servers.filesystem.enabled` set to false to turn a server off. `mcp_servers.filesystem.lazy` defers the connection itself.

Check: the server's Tools column in `hermes mcp list` reads `N selected`, and in a new session the "(unknown)" row of `/context all` is smaller.

Undo: restore the backup.

## Stage 6: Cache, Compression and Side Tasks

Reads: `hermes config get prompt_caching.cache_ttl`, `hermes config get compression.threshold`, `hermes config get auxiliary.compression.provider`, `hermes config get auxiliary.background_review.enabled` and `hermes config get auxiliary.background_review.provider`.

How it costs:

- The system prompt and the tool list are frozen per session. Memory writes, skill installs, SOUL.md or AGENTS.md changes and the date rollover keep the cache warm; a compaction, a model switch, a prompt rebuild and a toolset change break it. Keep one model per session and change toolsets between sessions.
- `prompt_caching.cache_ttl` defaults to `5m`. `auto` uses one hour for sessions a person drives, so a re-write after an idle gap costs less; subagents and cron stay on five minutes. A falsy value turns caching off.
- A `compression.threshold` of `0.50` is floored to `0.75` for any model window under 512K. Each compaction is one side call, on the main model unless `auxiliary.compression` is routed elsewhere, followed by a full cache re-write.
- Every side task on `provider: auto` runs on the main model first. The background review fork runs every 10 user turns for memory and every 10 tool iterations for skills, capped at 16 iterations. Smart approvals spend a side call on each flagged command.

Propose (you apply it after a yes):

- For work a person does at the keyboard: `hermes config set prompt_caching.cache_ttl auto`.
- Route `auxiliary.compression` to a cheaper model the user already has a provider for, with two commands that set only its provider and model, for example `hermes config set auxiliary.compression.provider <provider>` and `hermes config set auxiliary.compression.model <cheap-model>`, both placeholders for the user's choice; the same pair under `auxiliary.background_review`.
- When the user does not want automatic memory and skill reviews: `hermes config set auxiliary.background_review.enabled false`.

Check: `hermes config get` prints the new value, and `hermes prompt-size --json` shows the fixed budget unchanged.

Undo: restore the backup.

## Stage 7: Cap the Runaways

Reads: `hermes config get agent.max_turns`, `hermes config get delegation.max_iterations`, `hermes config get delegation.max_concurrent_children`, `hermes config get cron.model`, `hermes cron list` and `hermes sessions stats`.

How it costs:

- An `agent.max_turns` of null is unlimited in the CLI and the gateway; the TUI falls back to 500, and a `hermes -z` run has no cap. Delegation allows 250 iterations times 10 children. A tool_search loop has no per-turn cap in v0.22.5.
- Every cron fire is a fresh agent with the whole cron toolset unless the job sets its own toolsets, and a job with no pinned model uses `cron.model`, or the main model when that is empty, at fire time. Fires that need no model at all: a script with empty output, a script whose last line is `{"wakeAgent": false}`, an unchanged monitor, and a no-agent job.
- Session auto-prune was on from v0.21.1 to v0.22.2 and is opt-in from v0.22.3.

Propose (you apply it after a yes):

- `hermes config set agent.max_turns <n>`, with a number the user picks above their longest normal task; the same shape for `delegation.max_iterations`.
- A cheap default for every unpinned cron job, the weekly audit included: `hermes config set cron.model <cheap-model>` and `hermes config set cron.model_provider <provider>`, both placeholders for the user's choice.

Propose (the user runs it):

- Pin a cron job's model: `hermes cron edit <job_id> --pin` locks the current main model onto the job, and `--model` with `--provider` names one, for example `hermes cron edit <job_id> --model <cheap-model> --provider <provider>`. The weekly hermes-tune audit needs this once the user accepts it: it has no model of its own, and every run is a full agent run.
- Review old sessions: `hermes sessions prune --dry-run --older-than <age>` lists what would go and changes nothing; the user decides what to do next.

Check: `hermes config get agent.max_turns` prints the cap, and `hermes prompt-size --json` shows the fixed budget unchanged.

Undo: restore the backup for the caps and `cron.model`. A pin comes off with `hermes cron edit <job_id> --unpin`, which the user runs.

## Stage 8: Keep It Tuned

Budgets drift with releases: the fixed prefix of a default install has grown between releases and shrunk again when upstream cut it. Measure after every update.

Reads: `hermes --version`, whose first line names the release: `Hermes Agent v<semver> (<date>)`, then the build, such as its channel and commit. Compare that whole line with the baseline's version_label; only the date in parentheses can be stale.

Propose (the user runs it): `hermes update --check`, and `hermes update --plan`, which shows the update plan and changes nothing. Hermes flags every `hermes update` as dangerous, these two included, and a scheduled run refuses it, so the user runs them and any update.

This skill is the Stage 8 install, and the user runs it: `hermes skills install jasonjeske/hermes-master-class/skills/hermes-tune --yes`. That install scans it at community trust and offers its weekly audit under `/suggestions`; the audit is never scheduled for the user. The skill costs one more row in the skills index, which its own prompt-size shows.

Propose (the user runs it): schedule the weekly audit from `/suggestions`, then pin its model as in Stage 7; `hermes cron list` shows the job as `blueprint:hermes-tune` with its id. It runs Mondays at 9:00 (`0 9 * * 1`) with only the terminal and file toolsets, runs the A1 to A12 checks in `references/audit.md`, saves `tune/audit-YYYY-MM-DD.md` beside config.yaml, and changes nothing. Each run is a full agent run, and a scheduled job fires only while a gateway runs.

After every Hermes update: run audit mode once by hand, then, after a yes, refresh `tune/baseline.json`.

Check: `hermes cron list` shows the weekly job once the user schedules it, and the first report sits in `tune/` after it fires.
