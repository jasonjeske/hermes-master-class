# Hermes Power User: Every Slash Command, Ranked

![Hermes Power User](../assets/art/bonus-hero.webp)

## Contents

- [Orientation](#user-content-orientation)
- **[Tier 1](#user-content-tier-1-the-twelve-that-change-every-session)** The Twelve That Change Every Session
- **[Tier 2](#user-content-tier-2-hand-off-longer-work)** Hand Off Longer Work
- **[Tier 3](#user-content-tier-3-watch-cost-speed-and-context)** Watch Cost, Speed and Context
- **[Tier 4](#user-content-tier-4-undo-damage-and-stay-safe)** Undo Damage and Stay Safe
- **[Tier 5](#user-content-tier-5-make-it-learn)** Make It Learn
- **[Tier 6](#user-content-tier-6-sessions-files-and-sharing)** Sessions, Files and Sharing
- **[Tier 7](#user-content-tier-7-tools-and-integrations)** Tools and Integrations
- **[Tier 8](#user-content-tier-8-how-it-looks-and-sounds)** How It Looks and Sounds
- **[Tier 9](#user-content-tier-9-chat-platforms-only)** Chat Platforms Only
- **[Tier 10](#user-content-tier-10-account-and-upkeep)** Account and Upkeep
- **[Tier 11](#user-content-tier-11-just-for-fun)** Just for Fun
- **[Tier 12](#user-content-tier-12-only-in-the-tui)** Only in the TUI
- [Keys That Pair With the Commands](#user-content-keys-that-pair-with-the-commands)
- [Shortcuts Hiding in Plain Sight](#user-content-shortcuts-hiding-in-plain-sight)
- [Where the Docs and the Code Disagree](#user-content-where-the-docs-and-the-code-disagree)
- [The Bonus Ledger](#user-content-the-bonus-ledger)

---

## Orientation

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

## Tier 1: The Twelve That Change Every Session

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

## Tier 2: Hand Off Longer Work

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

## Tier 3: Watch Cost, Speed and Context

Six commands that tell you what a session costs and let you change it.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 24 | `/usage` | Shows tokens, estimated cost, session time and, where the provider reports them, your account limits. `reset` redeems a banked Codex limit reset | Before a long run, and whenever spend looks wrong | CLI and chat |
| 25 | `/context` `/ctx` | Breaks the context window down by category and lists every context file with whether it loaded. `all` adds the cost of each skill and toolset. No model call | Answers get worse or slower, or your `AGENTS.md` seems to be ignored | CLI and chat |
| 26 | `/reasoning` | Sets reasoning effort from `none` to `ultra`, and shows or hides the reasoning. `--global` saves it | Raise it for a hard problem, lower it for routine work to save time and tokens | CLI and chat |
| 27 | `/fast` | Turns on priority processing where the provider offers it: every request (`fast`), the first minute of each turn (`auto`), or that first minute on a session's first turn only (`cold`). `ultrafast` only where supported | Latency matters more than price for a while | CLI and chat |
| 28 | `/insights` | Shows usage analytics for the last 30 days, or the number of days you name | Your weekly look at where the tokens went | CLI and chat |
| 29 | `/busy` | Decides what plain typing does while Hermes works: `queue`, `steer` or `interrupt` | Once, to match your habit. `steer` turns everything you type mid-turn into a steer | CLI and chat |

## Tier 4: Undo Damage and Stay Safe

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

## Tier 5: Make It Learn

Hermes improves itself after turns on its own. These commands make it learn on purpose, and let you check what it kept.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 40 | `/refine` | Runs the memory and skill review now, instead of waiting for the automatic one after a turn. Focus text steers it | You just finished something worth keeping, for example `/refine save the deploy steps as a skill` | CLI and chat |
| 41 | `/learn` | Writes a reusable skill from anything you point at: a folder, a URL, this chat, pasted notes | You walked the agent through a procedure and never want to explain it again | CLI and chat |
| 42 | `/init` | Scans the repo and writes its `AGENTS.md`, or merges new findings into the one you have | The first session in a new project | CLI and chat |
| 43 | `/memory` | Shows memory writes waiting behind the approval gate, approves or rejects them, and turns the gate on or off | You want to see what Hermes will remember before it does | CLI and chat |
| 44 | `/skills` | Searches, browses, inspects, installs and audits skills. In chat, only the approval review (`pending`, `diff`, `approve`, `reject`) and only while the skill approval gate is on | Finding a skill someone already wrote, or reviewing one the agent wants to save | CLI, chat opt-in |
| 45 | `/curator` | Reports, runs, pauses and resumes the background skill maintenance. `pin` keeps a skill safe from its archiving pass | Your skill list is going stale, or a skill you rely on must never be archived | CLI and chat |
| 46 | `/bundles` | Lists skill bundles: one `/name` that loads several skills at once | You keep loading the same three skills together | CLI and chat |
| 47 | `/reload-skills` `/reload_skills` | Rescans the skills folder for skills you added or removed | You installed or edited a skill and the session cannot see it | CLI and chat |
| 48 | `/journey` `/learning` `/memory-graph` | Opens the timeline of what Hermes has learned, skills and memories, with `delete` and `edit` | You want to check, prune or fix what it learned | CLI |

## Tier 6: Sessions, Files and Sharing

Finding old work, forking it, moving it to your phone, and getting text and images in and out.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 49 | `/title` | Names the current session | Right after you start work you will want to find again | CLI and chat |
| 50 | `/sessions`, TUI `/switch` `/session` | Browses previous sessions and resumes one. In chat, `search` filters and `all` lists every origin (admins only). In the TUI it switches between the sessions open right now | You know the work exists but not what you called it | CLI and chat |
| 51 | `/branch` `/fork` | Copies the session into an independent branch. On Discord, Telegram, Slack and Matrix the branch opens in a new thread, and `--here` moves this chat onto it instead | You want to try a different approach without losing the current one | CLI and chat |
| 52 | `/handoff` | Moves the session to a messaging platform. The gateway picks it up there with the full transcript, and the CLI exits | You leave the desk and want to keep going from your phone. Needs the gateway running and a home channel set | CLI |
| 53 | `/save` | Exports the conversation as `json`, `md` or `html`. `redact` strips secrets from messages and tool output. In chat the file arrives as a document | You need a record to share, file or feed into something else | CLI and chat |
| 54 | `/history` | Prints the conversation so far | You want to reread what was said without scrolling | CLI |
| 55 | `/copy` | Copies the last response, or the Nth from last, to the clipboard | You want the answer in another app without terminal formatting | CLI |
| 56 | `/prompt` `/compose` | Opens your text editor to write the next prompt in markdown, then sends it (also `Ctrl+G`) | Long, structured prompts you want to edit properly | CLI |
| 57 | `/paste` | Attaches the image on your clipboard to the next prompt | You copied a screenshot and want Hermes to see it | CLI |
| 58 | `/image` | Attaches a local image file to the next prompt | The picture is on disk, not on the clipboard | CLI |
| 59 | `/export` | Packs a profile (skills, memory, persona, crons, plugins, settings) into a `.tar.gz`, with credentials stripped | Backing up a profile, or giving it to someone | CLI |
| 60 | `/import` | Installs a profile archive as a new profile. It never overwrites one you have | Setting up a profile someone exported | CLI |
| 61 | `/clear` | Clears the screen and starts a new session | You want a clean screen and a clean context together | CLI |

## Tier 7: Tools and Integrations

What the agent can reach, and the commands that change it without a restart.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 62 | `/tools` | Lists tools, or turns tools off and on for this session. Changing them resets the session | A tool keeps getting called when it should not, or one you need is off | CLI |
| 63 | `/toolsets` | Lists the toolsets available | Checking what a profile can reach before you give it a job | CLI |
| 64 | `/plugins` | Lists installed plugins and whether each one is enabled | A plugin's tools are missing and you want to know why | CLI |
| 65 | `/reload-mcp` `/reload_mcp` | Reloads MCP servers from config and checks again which tools are available | You added an MCP server or a credential mid-session | CLI and chat |
| 66 | `/reload` | Reloads `.env` variables into the running session | You added an API key and do not want to restart | CLI |
| 67 | `/browser` | Connects the browser tools to your running Chrome, Brave, Chromium or Edge, or switches to Browser Use mode | The agent needs your logged-in browser, not a fresh headless one | CLI |
| 68 | `/cron` | Lists, adds, edits, pauses, resumes, runs and removes scheduled jobs | Jobs that must run without you (Volume 1, Build 8) | CLI |
| 69 | `/suggestions` `/suggest` | Lists automations Hermes has suggested. `accept` creates one, `dismiss` drops it, `catalog` adds curated starters | You want automations without writing cron jobs by hand | CLI and chat |
| 70 | `/blueprint` `/bp` | Sets up an automation from a template, step by step or in one line with `slot=value` | You want a known automation filled in for you | CLI and chat |
| 71 | `/egress` | Shows the Docker egress proxy: whether it runs, where its credentials come from, and the next fix | You run Hermes in Docker and a provider call is blocked | CLI and chat |
| 72 | `/codex-runtime` `/codex_runtime` | Hands eligible OpenAI and Codex turns to a `codex app-server` subprocess, or back. Takes effect next session | You want Codex's own shell and patch tools, and ChatGPT subscription sign-in, on OpenAI models | CLI and chat |

## Tier 8: How It Looks and Sounds

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

## Tier 9: Chat Platforms Only

Commands the terminal does not have, because they only make sense in a chat.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 85 | `/sethome` `/set-home` | Marks this chat as the home channel, where cron and other deliveries land | Setting up a new bot chat, and before a `/handoff` to it | Chat |
| 86 | `/platform` | Lists every platform adapter with its state, pauses one, or resumes it and clears a tripped breaker | One platform is failing and you want to stop it without stopping the rest | Chat |
| 87 | `/restart` | Restarts the gateway once active runs drain, then confirms in this chat | A config change needs a restart and you are on your phone | Chat |
| 88 | `/topic` | Turns on Telegram DM topics, so each topic is its own session. `off` turns them off | You want several parallel conversations with one bot on Telegram | Chat |
| 89 | `/commands` | Pages through every command and skill | Your platform's command menu cuts the list short | Chat |
| 90 | `/start` | Acknowledges a platform's first-contact ping without a reply and without starting a turn | You want to check the gateway answers without spending a turn | Chat |

## Tier 10: Account and Upkeep

Updates, versions, sign-in, and the housekeeping you do once a month.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 91 | `/update` | Updates Hermes Agent to the latest version | A fix or feature you need just shipped | CLI and chat |
| 92 | `/version` `/v` | Shows the version, build and environment | Before you report a bug, or follow a guide written for another version | CLI and chat |
| 93 | `/debug` | Uploads a debug report with the last 200 log lines to a public paste service and prints the links, with no confirmation step. `local` prints it here and uploads nothing | Run `/debug local` first and read it. Upload only when someone asks you for the links | CLI and chat |
| 94 | `/whoami` | Shows your command access in this chat: admin or user | A command is refused and you want to know why | CLI and chat |
| 95 | `/profile` | Shows the active profile name and its home folder | Making sure you are in the profile you think you are | CLI and chat |
| 96 | `/config` | Shows the current configuration | Checking a setting without leaving the session | CLI |
| 97 | `/platforms` `/gateway` | Shows the status of every messaging platform | A bot stopped answering | CLI |
| 98 | `/login` | Signs in with a Nous account. In chat, paired direct messages only | Setting up Nous Portal billing or tools | CLI and chat |
| 99 | `/topup` | Shows your Nous balance and opens billing | Your Nous credits are running low | CLI and chat |
| 100 | `/subscription` `/upgrade` | Shows your Nous plan and opens the page to change it | Changing your Nous plan | CLI |
| 101 | `/autoprune` | Turns automatic pruning of old ended sessions on or off. Hermes asks once when the disk runs low | The session database keeps growing and the disk is filling | CLI and chat |
| 102 | `/quit` `/exit` | Exits the CLI. `--delete` also deletes this session's history | You are done. Add `--delete` only for a session you never want back | CLI |

## Tier 11: Just for Fun

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 103 | `/pet` | Shows, hides or adopts a petdex mascot | You want company in the terminal | CLI |
| 104 | `/hatch` `/generate-pet` | Generates a new pet from a description with your configured image backend | You want a mascot nobody else has. It spends an image generation | CLI |

## Tier 12: Only in the TUI

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

## Keys That Pair With the Commands

The classic CLI binds these. Several are faster than the command they match.

| Key | What it does |
|---|---|
| `Ctrl+P` | Opens the command palette, same as `/palette` |
| `Ctrl+C` | Interrupts the running turn. A second press within two seconds forces an exit. On an empty prompt with nothing running, it exits |
| `Ctrl+D` | Exits on an empty prompt. Mid-turn it detaches and lets the gateway finish the turn |
| `Ctrl+T` or `F6` | Opens the live work monitor for subagents, where `s` steers one |
| `Ctrl+G` (`Alt+G` in VS Code and Cursor) | Opens the draft in your editor, like `/prompt` |
| `Ctrl+S` | Stashes the draft and clears the box. On an empty box it brings one stash back, or opens the list when there are several |
| `Esc` `Esc` | Discards the draft and any attached images |
| `Esc` then `Enter`, or `Ctrl+J` | A new line without sending |
| `Ctrl+L` | Repaints the screen, like `/redraw` |
| `Ctrl+B` | Push to talk in voice mode (change it with `voice.record_key`) |

## Shortcuts Hiding in Plain Sight

### Short prefixes, and the ones that surprise you

The classic CLI runs a command from the first few letters. An exact name or alias always wins. Otherwise, when one command starts with what you typed, it runs; when several do, the one shortest name wins; when they tie, Hermes lists them and runs nothing. Installed skills join the race, so a skill name can change the result. On v0.22.5 with no skill sharing the letters:

| You type | It runs | Watch out |
|---|---|---|
| `/h` | `/hb`, the heartbeat | Not `/help`. Type `/he` |
| `/res` | `/reset`, a new session | Not `/resume`. The confirmation catches it, but type `/resu` |
| `/st` | `/stop` | Not `/status` or `/steer`. Use `/ste` or `/s` for steer |
| `/sk` | `/skin` | Not `/skills`. Type `/ski` |
| `/co` | `/copy` | Not `/compress` or `/context`. Use `/ctx` |
| `/qu` | `/quit` | It exits. Use `/q` for queue |
| `/mod`, `/u`, `/g`, `/k`, `/l` | `/model`, `/undo`, `/goal`, `/kanban`, `/loop` | Safe |

### Your skills are commands

Every installed skill is also a command: `/github-pr-workflow`, `/excalidraw`, whatever you have. When a skill's name matches a built-in command or alias, the built-in wins and the skill gets no command of its own, so give your skills names no command uses. A bundle (`/bundles`) is one command that loads several skills.

### Commands you make yourself

`quick_commands` in `config.yaml` adds your own: `type: exec` runs a shell command (30 seconds at most, with a cleaned environment) and `type: alias` points at another slash command. Built-in commands are resolved first, so a quick command named like a built-in never runs in the CLI. `model_aliases` gives `/model` short names: `hermes config set model.aliases.fav anthropic/claude-opus-4.6`, then `/model fav`.

### Commands that ask first

`/clear`, `/new`, `/reset`, `/undo` and `/quit --delete` open a confirmation in the CLI because they throw away history. Add `now`, `--yes` or `-y` to skip it once (`/new -y`), or set `approvals.destructive_slash_confirm: false` to turn it off.

### In Slack threads

Slack does not deliver slash commands inside threads. Use `!` instead (`!stop`, `!status`), or `/hermes <command>` anywhere.

### Who may run what in chat

On platforms with an allowlist, admins get every command and everyone else gets the names in `user_allowed_commands`, plus `/help` and `/whoami`. Set `allow_admin_from` and `user_allowed_commands` in the platform's `extra:` block.

> ⚠️ **Gotchas worth knowing before you rely on them**
>
> `/debug` with no argument posts your last 200 log lines to a public paste service and the act of typing it is the consent: read `/debug local` first. `/model` resets the prompt cache, so the next turn rereads the whole conversation at full input price, and `/tools` resets the session: change them between tasks, not inside one. `/yolo` lasts for the whole session, and resuming that session brings it back. `/goal` keeps spending turns until its judge says done, so give it a finish line a reviewer could check. In chat, setting a goal while a turn is running needs `/stop` first.

## Where the Docs and the Code Disagree

Checked against the official Slash Commands reference on October 29, 2026. In every case the rows above follow the code.

| Topic | The docs say | v0.22.5 does |
|---|---|---|
| `/steer` | The note is appended to the last tool result | Saves the note as its own user message, the change Volume 5 described in v0.21.2 |
| Short prefixes | `/h` resolves to `/help`, and an ambiguous prefix takes the first match in registry order | The one shortest match wins, so `/h` runs `/hb`, and a tie runs nothing |
| `/save` | CLI only | Also works in chat, where the export arrives as a document |
| `/undo` | Removes the last exchange | Takes a count, `/undo 3`, and puts your prompt back in the box |
| Quick commands | The example names one `status` | Built-in `/status` wins in the CLI, so that quick command never runs there |
| TUI commands | Only `/connectors` is listed as TUI only | The TUI has fifteen commands of its own (Tier 12) and three extra aliases: `/background`, `/switch`, `/session` |

## The Bonus Ledger

### Prompts

*`prompt-bonus-audit.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/reference/slash-commands.
Then search my last 20 sessions and find five moments where one slash
command would have saved me time or tokens: a turn I restarted instead of
steering, a follow-up I waited to type instead of queueing, a session that
ran long without /compress or /new, a model left on a frontier tier for
routine work. For each, quote the moment, name the command, and say what it
would have saved. Change nothing.
```

*`prompt-bonus-setup.md`*

```markdown
Set up three things for this profile and show me each change before you
make it: display.busy_input_mode set to steer, a quick command /deploy of
type exec that runs scripts/deploy.sh, and a model alias "fast" for the
cheapest model I already have configured. Then run /busy status and show
me the quick command and the alias in config.yaml.
```

### Verify

- [ ] `/help` lists the commands this class ranks, and `/help skills` lists your skill commands
- [ ] A `/steer` changed a running turn, and a `/queue` prompt ran after it as its own turn
- [ ] `/undo` put your last prompt back in the box
- [ ] `/context` listed your `AGENTS.md` as loaded
- [ ] `/debug local` printed a report and uploaded nothing
- [ ] `Ctrl+P` found a command from part of its name

> ✅ **What you have now**
>
> Every command Hermes has, in the order that pays. You steer and queue instead of waiting, you start fresh and compress instead of dragging a stale context, you undo a bad prompt instead of arguing with its answer, and you hand long work to a goal, a loop or the board while you do something else. The rest of the list is there when the moment comes, one row away.
