# Where the Docs and the Code Disagree

Checked against the official docs as they ship in the v0.22.5 source (commit bf0203a): docs paths are relative to `website/docs/`, while code paths, the seeded SOUL.md and the example config are relative to the root of the checkout, and every stage above follows the code.

| Topic | The docs say | v0.22.5 does | Stage |
|---|---|---|---|
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

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-TUNING.md)
