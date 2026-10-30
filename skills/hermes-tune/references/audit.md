# Weekly Audit

Audit mode is the weekly scheduled run, or any run the user asks to be report only. It measures, compares with `tune/baseline.json`, saves a report and proposes changes. It changes nothing: no config, toolsets, skills, memory or cron jobs, and the baseline stays as it is. Run every command through `terminal`, read files with `read_file`, and save the report with `write_file`.

Two guards back that up, and neither covers everything. Hermes's file tools refuse to write the active config.yaml, and `approvals.cron_mode`, `deny` by default, blocks every command Hermes flags as dangerous in a scheduled run, `hermes update` among them. A plain `hermes config set` passes both, so the run proves it changed nothing: it fingerprints config.yaml, cron/jobs.json, skills/ and memories/ at the start and at the end, and the report names any difference.

## Steps

1. Find the state. Run `hermes config path`; `tune/` is the folder beside that config.yaml, and the shell commands below run in that folder. Read `tune/baseline.json`. Done when you have the baseline's date, version label, byte figures and tool count, or know there is no baseline.
2. Fingerprint. Run `mkdir -p tune` when the folder is missing, then `shasum -a 256 config.yaml cron/jobs.json > tune/fingerprint-start.txt`, then `find skills memories -type f ! -name '.*' -exec wc -c {} + | sort -k2 >> tune/fingerprint-start.txt`. The file holds hashes, names and sizes, never content. Names and sizes catch a file added, removed or resized, and a same-size edit slips past them. The dot files the listing skips are the ones Hermes writes when a skill loads. Done when the file exists.
3. Measure. Run `hermes --version` and `hermes prompt-size --json`, and work out estimated tokens: the system prompt bytes plus the tool schema bytes, divided by four. Done when you have the version label (the first line of `hermes --version`), both byte figures, the tool count and the estimated tokens.
4. Run the twelve checks in the table below, in order. Note each value and whether its "Report it when" condition holds. Done when every check has a value, or a line saying why it could not be read.
5. Measure and fingerprint again. Run `hermes prompt-size --json`, then the two step 2 commands with `tune/fingerprint-end.txt` in place of the start file, then `diff tune/fingerprint-start.txt tune/fingerprint-end.txt`. Done when both byte figures match step 3 and you have the diff output, which is empty when nothing changed.
6. Fill the report template below and save it as `tune/audit-YYYY-MM-DD.md` with today's date. Done when the file exists and its last line is the template's closing line.
7. Reply with the report's path, its fingerprint line, its drift lines and its proposals. Done when the reply names the file.

With no baseline: write none in the baseline column, judge each check by its "Report it when" condition alone, and make the first proposal "Run Stage 0 of `references/ladder.md` in a session to save a baseline."

A fingerprint difference goes in the report as the diff printed it. The scheduler rewrites cron/jobs.json whenever any job starts or ends, so when another job ran during the audit, add that a cron/jobs.json line may be the scheduler's.

## Checks

| Check | Command | Report it when |
|---|---|---|
| A1 Version | `hermes --version` | Its first line differs from the baseline's version_label |
| A2 Budget | `hermes prompt-size --json` | Estimated tokens up 5 percent or more on the baseline, or the tool count changed |
| A3 Toolsets | `hermes tools list` | A toolset is on that the baseline did not have |
| A4 Tool search | `hermes config get tools.tool_search.enabled` and `hermes config get tools.tool_search.defer` | Tool search is off, or an explicit defer list lacks a curated default name |
| A5 Skills | `hermes skills list --enabled-only` and `hermes config get skills.auto_load` | A skill appeared since the baseline, any auto_load entry, any description over 60 characters |
| A6 Memory | `wc -m memories/MEMORY.md memories/USER.md`, `hermes config get memory.memory_char_limit` and `hermes config get memory.user_char_limit` | Either store at nine tenths of its cap or more |
| A7 Cache and compression | `hermes config get prompt_caching.cache_ttl` and `hermes config get compression.threshold` | Always: report the values and what they mean for this model |
| A8 Side tasks | `hermes config get auxiliary.compression.provider`, `hermes config get auxiliary.background_review.enabled` and `hermes config get auxiliary.background_review.provider` | A side task is on `auto`, which runs on the main model |
| A9 Caps | `hermes config get agent.max_turns`, `hermes config get delegation.max_iterations` and `hermes config get delegation.max_concurrent_children` | A cap is unlimited |
| A10 Cron | `hermes cron list`, `hermes config get cron.model`, and `read_file` on `cron/jobs.json` for each job's `model` and `enabled_toolsets` | A job sets no toolsets, or has no model while `cron.model` is empty |
| A11 Session store | `hermes sessions stats` | The store is near the 1 GB that hermes doctor warns about |
| A12 MCP | `hermes mcp list` | A server's Tools column does not read `N selected`, so it has no include list |

A1, A2, A3 and the new-skill part of A5 report a change since the baseline. A4, the rest of A5, A6, A8, A9, A10, A11 and A12 report a standing condition, every week it holds, until the user fixes it: a default install trips A8 and A9 every week, and A10 trips on this audit's own job until the user pins its model. A7 reports its values every week.

## Report template

Copy it as it stands and replace each part in braces. Keep the closing line exactly.

```markdown
# Hermes tune audit, {date}

Version label: {the first line of hermes --version}, {the same as, or different from} the baseline's. This run never checks for a newer release: run `hermes update --check` yourself.

Fingerprint of config.yaml, cron/jobs.json, skills/ and memories/: {unchanged, or each line the diff printed}.

| Budget | Baseline, {baseline date} | Now | Change |
|---|---|---|---|
| System prompt bytes | {b} | {n} | {d} |
| Tool schema bytes | {b} | {n} | {d} |
| Estimated tokens, bytes divided by 4 | {b} | {n} | {d} |

## Drift
- {check id}: {what changed, or the standing condition}

## Proposals
1. {what to change} | {exact command} | {expected effect}

Nothing was changed. To apply a proposal, open a session, load the hermes-tune skill and name its number.
```

## Example lines

A drift line names the check and what changed or what stands. A proposal line names one change, its exact command, and its expected effect:

```markdown
- A3: browser is on; the baseline had no browser toolset.
- A8: compaction runs on the main model (`auxiliary.compression.provider` is auto).
- A10: blueprint:hermes-tune, the audit job itself, has no model and `cron.model` is empty, so it runs on the main model.

1. Turn off the browser toolset (Stage 2) | `hermes tools disable browser` | saves about 854 tokens on a fresh install
2. Pin the audit job's model (Stage 7, the user runs it) | `hermes cron edit <job_id> --model <cheap-model> --provider <provider>` | the weekly run stops using the main model
```

## Reading each check

- A1 Version: compare today's first line of `hermes --version` with the baseline's version_label. A different line means a new release or build: report it, and propose refreshing the baseline in a session once the user has read this report. Never run `hermes update --check` or `--plan`: Hermes flags every `hermes update` as dangerous and a scheduled run refuses it, so the report hands that check to the user.
- A2 Budget: the change is now minus the baseline, for the system prompt bytes, the tool schema bytes and the estimated tokens. Report it when the estimate rose by 5 percent of the baseline or more, or when the tool count differs at all.
- A3 Toolsets: compare the toolset names in the per-toolset list of the JSON with the baseline's, and name each new one with its status from `hermes tools list`.
- A4 Tool search: the curated default names are the names in `references/profiles/defer-heavy.yaml` before manage_connections. An explicit list that misses one of them makes that tool eager again.
- A5 Skills: compare the skill names in the per-skill list with the baseline's. Read the description lines of the installed skills with `search_files` in the skills folder beside config.yaml, and report any over 60 characters, because the index cuts them.
- A6 Memory: `wc -m` counts characters and prints no content; a missing file counts as none. Divide the MEMORY.md count by `memory.memory_char_limit` and the USER.md count by `memory.user_char_limit`, and report a store at 0.9 or more. Never divide the prompt-size memory bytes by the caps: they include about 335 bytes of wrapper per store.
- A7 Cache and compression: `5m` is the default cache time to live, and `auto` means one hour for sessions a person drives. A `compression.threshold` of `0.50` acts as `0.75` when this model's window is under 512K.
- A8 Side tasks: `auto` runs the side task on the main model. Propose a cheaper route from Stage 6 of `references/ladder.md`.
- A9 Caps: an `agent.max_turns` printed as null or None is unlimited.
- A10 Cron: a job whose `enabled_toolsets` is empty or null runs the whole cron toolset. A job with no `model` follows `cron.model`, and the main model when that is empty; every run of an agent job is a full agent run. Copy only each job's id, name and these two fields into the report. The skill never edits jobs: the proposal gives the user the `hermes cron edit` command from Stage 7, or proposes setting `cron.model`.
- A11 Session store: report a database size of nine tenths of 1 GB or more.
- A12 MCP: use only the Name and Tools columns, and never copy the Transport column into the report, since it prints the start of each server's command, args or url. `N selected` means an include list; `all` or `-N excluded` means the server pays for every tool it registers, less any excluded, in the bridge listing. `hermes config get mcp_servers.<name>.tools` shows one server's filters. Never run `hermes config get mcp_servers` or `hermes config show`: they print commands, args and urls unmasked.

## Proposals

- One change per proposal, numbered, each with the stage of `references/ladder.md` it comes from, the exact command, and the effect that stage's figures lead you to expect.
- Mark a proposal the user must run as theirs: cron job edits and pins, skill installs and removals (`hermes skills opt-out --remove` included), cuts to memory or rule files, session pruning, and any `hermes update`.
- Never put a key, token or password into a proposal.
- With no drift and nothing to propose, write "None." under both headings.
