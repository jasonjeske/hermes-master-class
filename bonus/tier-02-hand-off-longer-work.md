# Tier 2: Hand Off Longer Work

The commands that let Hermes keep going while you do something else, and that let you check on it without interrupting.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 13 | `/goal` | Sets a standing goal. After each turn a judge model decides whether it is done, and Hermes keeps going until it is, you stop it, or the budget runs out (20 turns by default). `draft`, `show`, `gate add`, `pause` and `clear` manage it | Multi-step work with a finish line you can state in one sentence | CLI and chat |
| 14 | `/subgoal` | Adds a criterion to the active goal without restarting it. `remove N` and `clear` take criteria back | You realize mid-run that done needs one more condition | CLI and chat |
| 15 | `/bg`, TUI `/background` | Runs a prompt in a separate background session. The result comes back as a panel in the terminal or a message in chat | An independent job that should not block the chat you are in | CLI and chat |
| 16 | `/agents` `/tasks` | Shows active agents and running tasks | Checking what is still running before you stop, switch or walk away | CLI and chat |
| 17 | `/kanban` | Drives the shared board from the session: create, assign, comment, unblock, dispatch, switch boards | Work that splits into cards several profiles can take in parallel (Volume 5, Tip 2) | CLI and chat |
| 18 | `/plan` | Writes a markdown implementation plan to `.hermes/plans/` and executes nothing | Before a large change, so you approve the approach before any file moves | CLI and chat |
| 19 | `/review` | Spawns an independent reviewer subagent with full tool access on the work just discussed: a PR, code, docs. Its review comes back into this session | Before you merge, ship or publish something the agent built | CLI and chat |
| 20 | `/loop` `/proactive` | Re-runs a prompt on an interval in this session. With no interval it paces itself: one minute, doubling while nothing changes, up to fifteen. `--times` and `--until` stop it | Watching something until it changes: a deploy, a CI run, a queue | CLI and chat |
| 21 | `/heartbeat` `/hb` | Re-enters this session with a prompt whenever it is idle and the interval has passed (60 seconds at least) | A live session should check on something by itself while you are away. Use `hermes cron` when it must outlive the session | CLI and chat |
| 22 | `/moa` | Runs one prompt through the default Mixture of Agents preset, then puts your model back | A hard question where several models answering beats one | CLI and chat |
| 23 | `/stop` | Stops the running turn and kills every background process | Something is running that should not be | CLI and chat |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
