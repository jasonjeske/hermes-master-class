# Appendix D: Failure Triage

The symptom you will actually observe, mapped to the cause and the check. Compiled from the failure modes named across Parts 2, 5, 6, 11 and 12.

| Symptom | Likely cause | The check |
|---|---|---|
| Agent forgets yesterday's conversation | Docker running without the ~/.hermes volume mount | Start a chat, stop, restart, run hermes -c |
| A tool the docs describe simply is not there | check_fn is failing: expired key, exhausted credit, unreachable backend | hermes tools and read the whole list |
| "all" toolset is on but kanban is missing | Specialist toolsets are opt-in alongside all | hermes tools, then add kanban explicitly |
| Your CLAUDE.md is being ignored | A .hermes.md or AGENTS.md in the same directory wins | Check which of the three exist |
| A cron job behaves as if its skill does not exist | The skill is not in the DEFAULT profile, which the gateway uses | Copy it to the default profile's skills directory |
| A cron job says it has no idea what you mean | The prompt is not self-contained; cron sessions have zero history | Rewrite the prompt with every detail inline |
| A subagent asks about context it should have | The goal field assumed parent history the child never had | Put file paths, errors and conventions in goal and context |
| The second gateway refuses to start | Two profiles sharing one bot token | Create a separate bot per profile |
| The research profile can read your coding project | Default home_mode shares your real home directory | Set terminal.home_mode: profile |
| A skill you wrote has vanished | Curator archived it after 90 days unused | Check ~/.hermes/skills/.archive/, restore, then PIN it |
| The agent has gone vague on a long task | Compression has fired and summarized the middle | Delegate or split the session past ~30 tool calls |
| Your local dev server appeared in a cloud provider log | Hybrid routing is not configured | Verify private addresses route to the local Chromium sidecar |
| One platform went quiet, the rest work | Circuit breaker tripped on that adapter | hermes gateway resume <platform> |

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
