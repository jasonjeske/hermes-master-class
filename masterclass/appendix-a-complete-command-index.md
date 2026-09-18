# Appendix A: Complete Command Index

Every command the twelve parts name, collected. Commands are grouped by what you are trying to do rather than by subsystem, because that is how you will look for them.

*`hermes-command-index.sh`*

```bash
# ── Sessions ────────────────────────────────────────────────────────────────
hermes -c                                  # continue the most recent session
hermes chat                                # new session in the current profile
hermes chat --toolsets "web,terminal,file" # new session, scoped toolset

# ── Tools ───────────────────────────────────────────────────────────────────
hermes tools                               # what is ACTUALLY loaded right now

# ── Skills ──────────────────────────────────────────────────────────────────
hermes skills browse                       # see what exists on the hub
hermes skills search <keyword>             # find by topic
hermes skills inspect <name>               # READ IT before installing
hermes skills install <name>               # install (runs a security scan)
hermes skills tap add <org/repo>           # add a team's GitHub skill repo
/skills pending                            # review staged skill proposals

# ── Curator ─────────────────────────────────────────────────────────────────
hermes curator run                         # run the deterministic phase now
hermes curator run --consolidate           # include the optional LLM phase
hermes curator pin <name>                  # immune to all automated transitions
hermes curator restore <name>              # bring a skill back from .archive/
hermes curator rollback                    # undo the last run (itself reversible)

# ── Memory ──────────────────────────────────────────────────────────────────
/memory pending                            # review staged memory proposals

# ── Gateway ─────────────────────────────────────────────────────────────────
hermes gateway setup                       # the interactive platform wizard
hermes gateway resume <platform>           # clear a tripped circuit breaker
/platform                                  # list adapters from any chat
/platform resume <name>                    # resume one adapter, no restart

# ── Profiles ────────────────────────────────────────────────────────────────
hermes profile create <name>                       # blank, fresh config
hermes profile create <name> --clone-from default  # config + skills + SOUL
hermes profile create <name> --clone-all           # + memories, sessions, cron
hermes profile export <name>                       # shareable archive
hermes profile install <archive>                   # install on another machine
hermes -p <name> chat                              # run in a specific profile
<name> chat                                        # the auto-created alias

# ── In-session control ──────────────────────────────────────────────────────
/stop                                      # cancel an in-flight API call
/model                                     # switch model (rebuilds the prompt)
/agents                                    # TUI live tree of the delegation fan-out
/github-pr-workflow /test-driven-development <task>   # stack two skills
```

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
