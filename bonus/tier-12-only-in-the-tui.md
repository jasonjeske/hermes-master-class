# Tier 12: Only in the TUI

The TUI (`hermes --tui`) runs every command above through its own copy of the CLI, and adds these of its own. They rank last because they exist in one interface; the first four are worth knowing if you live in the TUI.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 105 | `/details` `/detail` | Controls how much of the agent's work shows, for everything or per section | The TUI shows too much or too little of what the agent is doing | TUI |
| 106 | `/connectors` | Manages connector accounts: list, rename, add another, reconnect, remove | A connected account expired, or you need a second one | TUI |
| 107 | `/theme` | Pins light or dark mode, or goes back to detecting it | The TUI guesses your terminal background wrong | TUI |
| 108 | `/density` | Turns the compact display on or off | You want more on the screen | TUI |
| 109 | `/logs` | Shows the gateway logs | Something failed and the reason is in the logs | TUI |
| 110 | `/replay` | Replays a completed spawn tree: the subagents a turn launched and what each one did | You want to see how a delegated job actually ran | TUI |
| 111 | `/replay-diff` | Diffs two completed spawn trees | Comparing two runs of the same delegated job | TUI |
| 112 | `/setup` | Runs the full setup wizard, `hermes setup` | Adding a provider or redoing setup without leaving the TUI | TUI |
| 113 | `/terminal-setup` | Sets up your IDE terminal's keys for multiline input and undo | Enter sends when you meant a new line, inside VS Code or Cursor | TUI |
| 114 | `/mouse` `/scroll` | Sets the mouse tracking preset | Mouse selection or scrolling misbehaves | TUI |
| 115 | `/mem` | Prints live memory numbers for the TUI process | The TUI feels slow after a long session | TUI |
| 116 | `/heapdump` | Writes a heap snapshot and memory diagnostics | A developer asked for one to chase a memory leak | TUI |
| 117 | `/theme-info` | Prints live theme diagnostics | The colors are wrong and you are reporting it | TUI |
| 118 | `/widgets-reload` | Rescans your TUI widgets folder and registers what it finds | You wrote or changed a TUI widget | TUI |
| 119 | `/fortune` | Prints a random fortune, or the day's fortune with `daily`, locally | You earned a break | TUI |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
