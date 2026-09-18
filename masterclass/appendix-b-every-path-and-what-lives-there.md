# Appendix B: Every Path and What Lives There

**The ~/.hermes tree, as the series and the official docs describe it**

```text
~/.hermes/                          the entire agent, one directory (HERMES_HOME)
  config.yaml                       non-secret settings, per profile
  .env                              secrets and tokens, never config
  SOUL.md                           agent identity, slot 1, loaded from here only
  state.db                          SQLite: sessions, titles, FTS5 search, lineage
  memories/
    MEMORY.md                       agent notes · 2,200 char hard limit
    USER.md                         your profile · 1,375 char hard limit
  skills/
    <category>/<name>/SKILL.md      one skill, frontmatter + four sections
    .archive/                       curator-archived skills (recoverable)
    .curator_backups/<utc>/         tar.gz snapshot before every curator pass
  skill-bundles/<slug>.yaml         one bundle = one slash command
  plugins/<name>/                   user plugins: plugin.yaml + __init__.py
  profiles/<name>/                  each profile is a whole separate home
  cron/
    jobs.json                       the job store, atomically written
    output/<job_id>/<timestamp>.md  every run's output, kept for audit
  kanban.db                         SQLite task board for multi-agent work
  honcho.json                       provider settings when Honcho is active
  mem0.json                         provider settings when Mem0 is active
  hindsight/config.json             provider settings when Hindsight is active
  import-sync.json                  what hermes import-agent pulled, and from where
  hermes-agent/                     the installed code (curl installer default)
  workspace/                        scratch the agent and some plugins use

  (in Docker, all of the above is mounted at /opt/data)

project directory/                  context tier, ONE type loads, first match wins
  .hermes.md                          1st
  AGENTS.override.md                  2nd, personal, replaces AGENTS.md, keep it gitignored
  AGENTS.md                           3rd, merged as a chain from the git root down
  CLAUDE.md                           4th
  .cursorrules                        5th
```

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
