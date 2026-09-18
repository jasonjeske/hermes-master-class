# Appendix B: Every Path and What Lives There

**The ~/.hermes tree, as the series describes it**

```text
~/.hermes/                          the entire agent, one directory
  config.yaml                       per-profile configuration
  state.db                          SQLite: sessions, titles, FTS5 search, lineage
  MEMORY.md                         agent notes · ~2,200 char hard limit
  USER.md                           your profile · preferences and style
  SOUL.md                           agent identity (stable prompt tier)
  skills/
    <category>/<name>/SKILL.md      one skill, frontmatter + four sections
    .archive/                       curator-archived skills (recoverable)
  cron/
    jobs.json                       the job store, atomically written
    .tick.lock                      prevents overlapping 60s ticks
    output/<job_id>/<timestamp>.md  every run's output, kept for audit
  kanban/                           SQLite task board for multi-agent work
  home/                             per-profile home when home_mode: profile

  (in Docker, all of the above is mounted at /opt/data)

project directory/                  context tier, ONE of these, by priority
  .hermes.md                          1st, wins over the others
  AGENTS.md                           2nd
  CLAUDE.md                           3rd, only if neither above exists
```

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
