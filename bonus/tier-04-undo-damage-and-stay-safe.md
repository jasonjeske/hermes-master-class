# Tier 4: Undo Damage and Stay Safe

What to type when the agent broke something, and the switches that decide how much it may do without asking.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 30 | `/rollback` | Lists filesystem checkpoints and restores one. A restore keeps your own hand edits unless you add `--all` | The agent broke files and you want them back as they were before its change | CLI and chat |
| 31 | `/diff` | Shows git changes in the working directory. `session` shows everything Hermes changed here (with checkpoints on), `--stat` only the file list | Before you commit, or to see exactly what the last run touched | CLI and chat |
| 32 | `/worktree` | Shows, lists, creates or prunes git worktrees. `new` moves the session's tools into a fresh branch under `.worktrees/` | Risky or parallel work that must not touch your main checkout | CLI |
| 33 | `/snapshot` `/snap` | Creates, restores or prunes snapshots of Hermes's own config and state | Before you change Hermes itself: a model swap, a plugin, a config edit | CLI |
| 34 | `/approvals` | Shows or sets how dangerous commands are approved: `manual`, `smart` or `off`, saved to config | Deciding once how much the agent may run without asking | CLI and chat |
| 35 | `/yolo` | Turns off every dangerous-command approval for this session, or turns them back on. A resumed session keeps the setting | Only in a sandbox or a throwaway container you are happy to lose | CLI and chat |
| 36 | `/approve` | Approves a pending dangerous command. `session` approves it for this session, `always` adds it to the permanent allowlist | Hermes asks from a chat and the command is exactly what you expect | Chat |
| 37 | `/deny` | Rejects a pending dangerous command, with an optional reason. `all` rejects every pending one | The command is wrong, or you want the agent to try another way | Chat |
| 38 | `/pause` | Puts all new work on hold (cron, kanban, gateway) until `/pause off`. Work in flight finishes | An emergency stop from your phone | Chat |
| 39 | `/discard` | Drops a turn lost in a restart so this chat's queued messages run again. The lost turn is not run again | Hermes tells you a conversation is paused on a lost turn | Chat |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
