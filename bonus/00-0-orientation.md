# Orientation

![Hermes Power User](../assets/art/bonus-hero.webp)

The five volumes built the agent, the app, the team and the company, and Volume 5 showed two habits that change how a session feels. This bonus class is the reference those habits grow from: every slash command Hermes has, on one page, ranked by how much it changes your work.

The order is the point. Read the first tier and stop, and your sessions already change: you steer instead of restarting, you queue instead of waiting, you start fresh when the context goes stale, and you undo a bad prompt instead of arguing with its answer. Each tier after that buys something specific: longer work handed off, cost under control, damage undone, a Hermes that learns. The last tiers are the commands you will reach for once a month, and the ones that exist only in the TUI.

Every row says what the command does in one line and when to use it in another. The ranking is judgment, not data: how often a power user reaches for the command, times how much it changes the result in time saved, money saved or mistakes avoided. Your top ten may differ. The first twenty-three are the ones that change how Hermes feels.

> 📝 **What this class rests on**
>
> Every command, alias and flag was checked against the installed source of Hermes Agent v0.22.5 (commit bf0203a, October 22, 2026): the command registry every surface reads, the TUI's own command files, and the handlers where a command's help line leaves out something that matters. The official Slash Commands reference was read alongside it. Where the two disagree, the row follows the code, and the closing section lists every disagreement found.

### How to read Works in

| Works in | Meaning |
|---|---|
| CLI and chat | The terminal and every messaging platform |
| CLI | The terminal only: the classic CLI (`hermes`) and the TUI (`hermes --tui`), which runs the same commands through its own copy of the CLI |
| Chat | Messaging platforms only: Telegram, Discord, Slack, WhatsApp, Signal, email and the rest of the gateway |
| CLI, chat opt-in | The terminal, plus chat once a config switch is on |
| TUI | Only inside `hermes --tui` |

Hermes Desktop has no column of its own because it treats commands five different ways: some run as app actions, `/model` and `/resume` open a picker, some go straight to the backend, and the rest show the reason they are not in the app (terminal only, messaging only, or in Settings). Type `/` in the composer and the app shows what it offers.

### The tiers at a glance

| Tier | Commands | What it buys you |
|---|---|---|
| 1 | 12 | The habits that change every session |
| 2 | 11 | Longer work handed off and running without you |
| 3 | 6 | Cost, speed and context under control |
| 4 | 10 | Mistakes undone and risky commands gated |
| 5 | 9 | A Hermes that keeps what it learns |
| 6 | 13 | Sessions you can find, fork, move and share |
| 7 | 11 | Tools, browsers, schedules and integrations |
| 8 | 12 | A screen and a voice set up your way |
| 9 | 6 | Commands that exist only in chat |
| 10 | 12 | Account, updates and upkeep |
| 11 | 2 | Pets |
| 12 | 15 | Commands only the TUI has |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
