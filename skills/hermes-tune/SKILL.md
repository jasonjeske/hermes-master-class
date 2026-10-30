---
name: hermes-tune
description: Measure, trim and audit what Hermes sends each call.
version: 0.1.0
author: Jason Jeske (jasonjeske)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [tuning, tokens, context, audit, cost]
    related_skills: [hermes-agent]
    blueprint:
      schedule: "0 9 * * 1"
      prompt: "Run the hermes-tune weekly audit in audit mode: measure, compare with the saved baseline, save the report, propose changes, and change nothing."
      enabled_toolsets: [terminal, file]
---

# Hermes Tune Skill

Measure what Hermes sends with every call before the first message, cut it one approved change at a time, and audit the install every week so the cuts hold. The commands it runs read Hermes's own offline byte counts and local config, need no API key and make no provider call. The scheduled weekly audit is itself a full agent run, on the job's pinned model, else `cron.model`, else the main model. It changes config only after the user says yes in a session, and only through `hermes config set` or `hermes tools`; the weekly audit reports and changes nothing.

## When to Use

- The user asks why Hermes sends so many tokens, or asks to measure, cut, tune or audit what each call carries.
- The user wants a toolset profile for agentic coding, research, running a business or automating a company, or lean chat in the terminal.
- The weekly scheduled run starts with a prompt that names audit mode.
- Hermes was updated and the user wants to know what the update did to the fixed budget.

Don't use for: provider bills, account limits or rate limits (`/usage` asks the provider for those), choosing a model or provider, or installing and removing skills.

## Prerequisites

- The `terminal` and `file` toolsets in the session. With no terminal tool, give the user each command and wait for their output.
- No API key: `hermes prompt-size` runs offline, and the checks read local config and local state. The skill never runs `hermes update`, not even `--check`: Hermes flags every `hermes update` as dangerous and a scheduled run refuses it, so the user runs it.
- State lives in a `tune/` folder beside the active profile's config.yaml, and `hermes config path` prints where that is. `tune/baseline.json` is the `hermes prompt-size --json` output plus `date` and `version_label`, the first line of `hermes --version`. Reports are `tune/audit-YYYY-MM-DD.md`.

## How to Run

Run Hermes's own commands through the `terminal` tool, read state with `read_file` and save it with `write_file`:

```text
terminal(command="hermes config path")
terminal(command="hermes --version")
terminal(command="hermes prompt-size --json")
terminal(command="hermes config get <key>")
```

From the JSON, take the system prompt bytes, the tool schema bytes and the tool count. Estimated tokens are the two byte figures added together and divided by four, the estimate `/context` makes from bytes.

- **Guided tuning**, a person in a session: walk `references/ladder.md` one stage at a time. Measure, propose one change, wait for yes, back up config.yaml, apply it with `hermes config set` or `hermes tools`, measure again, then refresh `tune/baseline.json` once the user confirms the result.
- **Audit mode**, the weekly scheduled run: follow `references/audit.md`. Fingerprint the files it must not change, measure, compare with the baseline, save the report, propose, and change nothing. Audit mode never moves the baseline.

## Quick Reference

| Use | Command |
|---|---|
| Fixed budget, offline, in bytes | `hermes prompt-size --json` |
| The same on a messaging platform | `hermes prompt-size --platform telegram --json` |
| Version label, its first line | `hermes --version` |
| Updates, the user runs it | `hermes update --check` |
| Where config.yaml and `tune/` live | `hermes config path` |
| One key | `hermes config get <key>` |
| One value, guided mode, after a yes | `hermes config set <key> <value>` |
| A list as JSON with no spaces, after a yes (example) | `hermes config set skills.disabled '["p5js","humanizer"]'` |
| Toolsets on and off | `hermes tools list` |
| Skills that load | `hermes skills list --enabled-only` |
| MCP servers and their tool filters | `hermes mcp list` |
| Memory size in characters, counts only | `wc -m memories/MEMORY.md memories/USER.md` |
| What the user actually ran | `hermes insights --days 30` |
| Session store size | `hermes sessions stats` |
| Scheduled jobs | `hermes cron list` |

Files: `references/ladder.md` (the nine stages), `references/audit.md` (the checks and the report template), and the profile lists `references/profiles/coder.yaml`, `references/profiles/researcher.yaml`, `references/profiles/operator.yaml`, `references/profiles/lean-chat.yaml` and `references/profiles/defer-heavy.yaml`.

## Procedure

- Never change config, toolsets, skills, memory or cron jobs during a scheduled run.
- Never apply a change before the user replies yes in this session.
- Never write config.yaml with write_file or patch: Hermes refuses both. Change config only with `hermes config set` or `hermes tools`.
- Never run hermes doctor, hermes status --deep or hermes debug: they call providers or upload logs.
- Never read or print secrets: no .env files, no config get --raw, no HERMES_DUMP_REQUESTS, and no `hermes config show` or `hermes config get mcp_servers`, which print MCP commands, args and urls unmasked.
- Never prune, archive or delete sessions, skills, memories or backups, and never cut memory or rule files: give the user the exact change.
- Never install, remove or update skills, plugins or Hermes itself, and never run any `hermes update`, not even `--check` or `--plan`. Give the user the exact command, `hermes skills opt-out --remove` and this skill's own install included.
- Never schedule, edit, pin or remove cron jobs; the user schedules the weekly audit from /suggestions and pins its model.
- Never commit or push a Hermes home or a Hermes backup to git; both hold .env and auth files.

1. Pick the mode. A prompt that names audit mode is the weekly run: audit mode. Anything else is guided tuning. Done when the first line of your reply names the mode.
2. Find the state. Run `hermes config path`; `tune/` is the folder beside the config.yaml it prints. Read `tune/baseline.json` with `read_file` if it exists. Done when you can quote the config path and the baseline date, or have said there is no baseline.
3. Measure. Run `hermes --version` and `hermes prompt-size --json`. Done when you have the version label (the first line of `hermes --version`), both byte figures, the tool count and the estimated tokens.
4. Audit mode: work through `references/audit.md`. Fingerprint config.yaml, cron/jobs.json, skills/ and memories/ first, run the A1 to A12 checks, fingerprint again, fill its report template, and save the report with `write_file` as `tune/audit-YYYY-MM-DD.md`. Done when the report exists, its fingerprint line says unchanged or names each difference, and its last line is the template's closing line.
5. Guided tuning: open `references/ladder.md` at Stage 0 when there is no baseline, otherwise at the stage the user names, otherwise at Stage 1. Done when you have named the stage and what it changes.
6. Measure and propose. Run the stage's reads and `hermes prompt-size --json`, then propose exactly one change from the stage's list: the exact command, with one line on what it saves, what it costs and how it undoes. A change the never list keeps from you is the user's to run: give the exact command. Never put a key, token or password into config. Done when the proposal is on screen and you have asked for a yes.
7. Wait. Anything but yes leaves config as it is; offer the next stage instead. Done when the user has answered.
8. Apply. Copy config.yaml to a dated backup next to it with `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in its folder, never overwriting an earlier backup (`-p` keeps the 0600 mode, and config.yaml can hold keys), then make only the change the user approved: `hermes config set <key> <value>` for one value, `hermes config set <key> '<JSON list>'` for a list, or `hermes tools disable` for toolsets. Done when the backup exists and `hermes config get <key>` or `hermes tools list` shows the new value.
9. Verify. Run the stage's check and `hermes prompt-size --json` again, and show a table of before, after and the difference. Say that this session keeps its old prompt and that a new session shows the change with `/context all`. Done when the table is on screen.
10. Refresh the baseline. Once the user confirms they keep the result, save the latest measurement as `tune/baseline.json` with today's date and the version label. Done when `read_file` on it shows today's date.

## Pitfalls

- This session keeps the system prompt and tool list it started with, so `/context` here shows the old budget. Measure with `hermes prompt-size --json` and check the result in a new session with `/context all`.
- `/context` shows Skills 0 even with skills installed: the skills index is billed under System prompt.
- Bytes divided by four is Hermes's own estimate, not a bill. `/usage` asks the provider and shows no cost line; `/insights` and `hermes insights` read local state and are a lower bound. The provider's bill is the record.
- An explicit `tools.tool_search.defer` list replaces the curated default: a short list makes the curated tools eager again, and `defer: []` makes every tool eager. Start from `references/profiles/defer-heavy.yaml`, which keeps the curated names first.
- Hermes's file tools refuse to write the active config.yaml: write_file and patch stop before any approval. Every change goes through `hermes config set`, which parses a list literal, or `hermes tools`. Write a list as JSON with no spaces inside single quotes. On `skills.disabled` and `skills.platform_disabled` the "not a recognized config key" notice is expected: Hermes reads both keys anyway.
- `hermes config show` and `hermes config get mcp_servers` print each MCP server's command, args and url unmasked, and those often carry tokens. Read MCP state from the Tools column of `hermes mcp list`, or per server from `hermes config get mcp_servers.<name>.tools`.
- Turning the memory toolset off keeps MEMORY.md and USER.md in every call; only `memory.memory_enabled` and `memory.user_profile_enabled` remove them.
- The memory and user profile bytes in `hermes prompt-size` include about 335 bytes of wrapper per store. Compare the `wc -m` character counts with the caps, and never print the files.
- The profile commands assume a default install, and `hermes tools disable` writes `platform_toolsets.cli` as an explicit list. On a changed install, propose the profile's list from its file as one `hermes config set platform_toolsets.cli` command. The top-level `toolsets:` key is legacy and changes nothing.
- Lean chat is a `platform_toolsets.cli` list measured on the CLI, a lean terminal profile. On a phone gateway the same list goes under that platform, for example `platform_toolsets.telegram`, and that was not measured.
- A toolset change, a model switch or a compaction rebuilds the prompt and pays a full cache re-write: apply changes between tasks, not in the middle of one.
- `hermes --version` names the release: its first line starts `Hermes Agent v<semver> (<date>)`, and the rest of the line names the build, such as its channel and commit. Store that whole first line as version_label and compare lines; only the date in parentheses can be stale.
- The user installs this skill with `hermes skills install jasonjeske/hermes-master-class/skills/hermes-tune --yes`, which offers the weekly audit under `/suggestions`. It is never scheduled automatically, and a scheduled job fires only while a gateway runs.
- Accepting the audit creates a job named `blueprint:hermes-tune` with no model of its own: every run is a full agent run on `cron.model`, or on the main model when that is empty, and then A10 reports the job each week. After accepting it, the user pins a cheap model, for example `hermes cron edit <job_id> --model <cheap-model> --provider <provider>` with their own choices and the id from `hermes cron list`, or sets `cron.model` first.
- `skills.auto_load` pins whole skills into every session's prompt; never pin this skill there.

## Verification

- `tune/baseline.json` exists and holds the date, the version label and the prompt-size JSON.
- After a guided stage, `config-YYYY-MM-DD-HHMMSS.yaml` sits next to config.yaml, and the before and after table matches a fresh `hermes prompt-size --json`.
- After an audit, `tune/audit-YYYY-MM-DD.md` exists and ends with "Nothing was changed. To apply a proposal, open a session, load the hermes-tune skill and name its number.", its fingerprint line shows the start and end fingerprints match, and `hermes prompt-size --json` reports the same bytes at the end of the run as at the start.
- In a new session, `/context all` agrees with the change: for example, a toolset that was turned off has no row.
