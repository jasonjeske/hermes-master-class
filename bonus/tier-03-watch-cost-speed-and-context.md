# Tier 3: Watch Cost, Speed and Context

Six commands that tell you what a session costs and let you change it.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 24 | `/usage` | Shows tokens, estimated cost, session time and, where the provider reports them, your account limits. `reset` redeems a banked Codex limit reset | Before a long run, and whenever spend looks wrong | CLI and chat |
| 25 | `/context` `/ctx` | Breaks the context window down by category and lists every context file with whether it loaded. `all` adds the cost of each skill and toolset. No model call | Answers get worse or slower, or your `AGENTS.md` seems to be ignored | CLI and chat |
| 26 | `/reasoning` | Sets reasoning effort from `none` to `ultra`, and shows or hides the reasoning. `--global` saves it | Raise it for a hard problem, lower it for routine work to save time and tokens | CLI and chat |
| 27 | `/fast` | Turns on priority processing where the provider offers it: every request (`fast`), the first minute of each turn (`auto`), or that first minute on a session's first turn only (`cold`). `ultrafast` only where supported | Latency matters more than price for a while | CLI and chat |
| 28 | `/insights` | Shows usage analytics for the last 30 days, or the number of days you name | Your weekly look at where the tokens went | CLI and chat |
| 29 | `/busy` | Decides what plain typing does while Hermes works: `queue`, `steer` or `interrupt` | Once, to match your habit. `steer` turns everything you type mid-turn into a steer | CLI and chat |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
