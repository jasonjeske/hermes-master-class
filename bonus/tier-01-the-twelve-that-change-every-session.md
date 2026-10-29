# Tier 1: The Twelve That Change Every Session

Learn these and stop here if you like. Every one of them is a habit, not a feature.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 1 | `/steer` `/s` | Slips a note into the running turn after the current tool call finishes. Nothing restarts and nothing already done is lost | The agent is heading the wrong way mid-task and the work so far is worth keeping | CLI and chat |
| 2 | `/queue` `/q` | Lines up a prompt to run as its own turn after this one. In the classic CLI, `list`, `edit`, `rm`, `move` and `clear` manage the line | You think of the next ask while Hermes is still working | CLI and chat |
| 3 | `/new` `/reset` | Starts a fresh session with an empty history. A name after it titles the session for `/resume` | You switch to unrelated work, so old context stops costing tokens and steering answers | CLI and chat |
| 4 | `/compress` `/compact` | Summarizes older turns to free context. `here N` keeps the last N turns word for word, a focus topic decides what the summary keeps, `--preview` shows the plan first | A long session slows down or `/context` shows the window filling, and you want to keep going | CLI and chat |
| 5 | `/model` | Switches the model for this session, or opens a picker. `--global` saves it, `--once` covers one turn, `--reasoning` sets effort in the same step | A hard step needs a stronger model, or routine work deserves a cheaper one. A switch resets the prompt cache, so do it between tasks | CLI and chat |
| 6 | `/undo` | Rewinds the last exchange, or the last N with `/undo N`, and puts your prompt back in the box to fix | The answer went wrong because the prompt was wrong | CLI and chat |
| 7 | `/retry` | Sends your last message again | A provider error or a weak answer, when the prompt itself was fine | CLI and chat |
| 8 | `/btw` | Answers a side question about the conversation from a snapshot, on a separate call, without touching the running turn or its cache | You need a quick fact mid-run and do not want to derail it | CLI and chat |
| 9 | `/status` | Shows model, provider, profile, session, tokens, and a recap of recent turns, tools and files. Computed locally, no model call | You come back to a session and need to know where it stands | CLI and chat |
| 10 | `/resume` | Reopens a named session with its full history. Bare `/resume` lists recent ones | Picking up yesterday's work where it stopped | CLI and chat |
| 11 | `/palette` | Opens the fuzzy command palette over every command and skill (also `Ctrl+P`). Enter inserts the command and never runs it | You know what you want but not what it is called | CLI |
| 12 | `/help` | Lists commands by category. `/help skills` lists your skill commands, `/help <text>` filters by a word | You want the list on screen, or every command that mentions a word | CLI and chat |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
