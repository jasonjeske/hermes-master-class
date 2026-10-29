# Tier 8: How It Looks and Sounds

The screen, the footer and the voice. Set them once.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 73 | `/focus` | Shows only your prompt and the final answer. Tool lines are hidden, never dropped | You want to read results, not watch the work | CLI |
| 74 | `/verbose` | Cycles tool progress: off, new, all, verbose | Debugging what the agent is actually doing | CLI, chat opt-in |
| 75 | `/personality` | Sets a predefined personality for the session. `none` clears it | A task wants a different voice, like terse reviews or patient teaching | CLI and chat |
| 76 | `/footer` | Adds a footer to final replies with the model, the context percentage and the working directory | You want every chat reply to show which model answered and how full the context is | CLI and chat |
| 77 | `/statusbar` `/sb` | Shows or hides the context and model status bar | You want the screen space, or the gauge back | CLI |
| 78 | `/timestamps` `/ts` | Adds `[HH:MM]` times to messages and to `/history` | Long sessions where you need to know when something happened | CLI |
| 79 | `/voice` | Turns voice mode and spoken replies on or off. On Discord, `join`, `channel` and `leave` manage voice channels | Hands-free work, or replies you would rather hear | CLI and chat |
| 80 | `/wake` | Turns the "Hey Hermes" wake word listener on or off | You want to start talking without touching the keyboard | CLI |
| 81 | `/skin` | Shows or changes the display theme | Readability, or telling profiles apart at a glance | CLI |
| 82 | `/indicator` | Picks the busy indicator style: kaomoji, emoji, unicode or ascii | Your terminal draws the default badly | CLI |
| 83 | `/battery` | Adds a color-coded battery read-out to the status bar | Working unplugged on a laptop | CLI |
| 84 | `/redraw` | Repaints the whole screen (also `Ctrl+L`) | The screen is garbled after a tmux resize or an SSH reconnect | CLI |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
