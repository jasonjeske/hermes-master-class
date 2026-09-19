---
title: The Hermes Desktop Masterclass
subtitle: Volume 2 of the Hermes Agent Masterclass. Ten builds that take the desktop app from first launch to a toolbox of plugins you wrote yourself
why: The app is the same agent as the CLI with a real interface on top, and nobody shows you how to make it yours. This volume does, with files you paste and prompts you run.
date: 2026-09-19
eyebrow: HERMES DESKTOP · VOLUME 2
---

![The Hermes Desktop Masterclass](assets/art/v2-hero.webp)

## Orientation

Hermes Desktop is not a second product. It is the same agent you get from the CLI and the gateway, with the same config, keys, sessions, skills and memory, driven through a native window with panes, a terminal, a file browser, git review, voice, a HUD that floats over other apps, and a plugin system that lets one JavaScript file add a pane to the window. Everything you set up in Volume 1 is already here, and everything you do here shows up in the terminal.

This volume is a build track like Volume 1's second half. Ten builds, in dependency order, each ending with files you paste and prompts you run. The center of gravity is Builds 5 to 8: a plugin workshop that ends with three working plugins in the app and the prompt that makes Hermes write the fourth.

```callout kind=note title="What this volume rests on"
Every path, key, command, menu name and SDK call was checked against the official Hermes documentation for the version installed while writing (the Desktop page, the Desktop Plugin SDK page, Build a Hermes Plugin, the multi-connection guide, and the configuration reference) and against the bundled files in the Hermes repository. Where a tip comes from an operator's video or post rather than the docs, it says so. Where the docs do not cover something, the text says that too rather than guessing.
```

```table
| Build | You end up with | Checked against | Time |
| 0 | The app installed, permissions settled once, the local backend understood | Installation, Desktop | 30 minutes |
| 1 | The window at your fingertips: sessions, panes, terminal, git review, HUD, palette, the keys you will actually use | Desktop | 45 minutes |
| 2 | The settings that decide cost and behavior, set on purpose, and an audit prompt for the rest | Desktop, Configuration | 30 minutes |
| 3 | Skills, plugins, tools and MCP managed from the app, the two safety plugins on | Desktop, Plugins | 20 minutes |
| 4 | The app talking to a Hermes on another machine, with the registry of every gateway you own | Desktop, Multi-connection | 45 minutes |
| 5 | Your first desktop plugin, loaded live | Desktop Plugin SDK | 30 minutes |
| 6 | A Prompt Library page with persistent storage | Desktop Plugin SDK | 30 minutes |
| 7 | A Ledger plugin with agent tools, a backend and a desktop page in one package | Build a Hermes Plugin, SDK | 60 minutes |
| 8 | The Fleet Board, and the prompt that makes Hermes write your next plugin | SDK, Plugins | 30 minutes |
| 9 | Updates, permissions after updates, logs, recovery and uninstall, all understood before you need them | Desktop | 20 minutes |
```

### How to use a build

Each build has four pieces. **What you are building** says what exists at the end. **What the docs say** is the short list of facts the build rests on, with the page named. **Prompts** are blocks marked with a file name like `prompt-d2-audit.md`: paste the whole block into a Hermes chat, in the app or anywhere else. **Commands** run in the app's own terminal pane or in your shell. Every build ends with a **verify** list, and a build is not done until that list passes.

```callout kind=info title="The kits"
Builds 5 to 8 ship their plugins as complete folders in the repository under `kits/`, validated against the loader's contract and, for the Python half, against `hermes plugins doctor --ci`. Copy a prompt and have Hermes type them, or clone the folder and drop it in place. Both roads end in the same file.
```

## Build 0: Install and First Launch

![Build 0](assets/art/part-02.webp)

### What you are building

The app on your Mac, the local backend it manages, the one permission grant that stops macOS from asking about every folder, and a clear picture of what lives where.

### What the docs say

Checked against the Installation page, the Platform Support page, and the Desktop page.

```table
| Fact | Detail |
| Two sanctioned installs | The Hermes Desktop installer from the website installs both the command line and the app, and is the recommended path on macOS. Or install the CLI first with the one-line installer, then run `hermes desktop`, which builds and launches the app against your existing config, keys, sessions and skills |
| Platform | macOS on Apple Silicon, Windows 10 and 11, and Linux or WSL2 all have a Desktop build; Intel Macs do not. This volume is written on macOS and says so where a step differs |
| The same home | On first launch the app can install the Hermes runtime into `~/.hermes`, the same layout a CLI install uses. That is why the two are interchangeable |
| What runs | The app launches a headless `hermes serve` backend for you and talks to it over JSON-RPC and WebSocket. It never needs the web dashboard |
| Folder prompts | macOS prompts per folder as Hermes touches Desktop, Downloads, Documents. One Full Disk Access grant for Hermes.app (and your terminal) covers all of them. `hermes doctor` reports whether the grant is present |
| Grants survive updates | Grants are remembered against the code-signing identity. Locally built and self-updated apps carry a stable identity, so grants persist. For a certificate-anchored identity run `hermes desktop --setup-tcc-identity` once, and re-run it after updates to re-sign |
| Stuck permission | `tccutil reset All com.nousresearch.hermes`, then re-grant and fully relaunch |
| Logs | Boot logs land in `~/.hermes/logs/desktop.log`; `hermes logs gui -f` tails them |
```

### Commands

```code lang=bash file=day-one-desktop.sh
# A. Already have the CLI from Volume 1? Build and launch the app on top of it.
hermes desktop

# B. Fresh Mac: download the Hermes Desktop installer from hermes-agent.nousresearch.com and run it.
#    It installs the CLI and the app together. Then:
hermes doctor                 # includes the Full Disk Access check on macOS
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
#    enable Hermes.app and your terminal, then fully quit and relaunch both

# C. Anchor the signing identity so permission grants outlive every update
hermes desktop --setup-tcc-identity

# D. Know where things are
hermes status
hermes logs gui -f            # the app's boot log, live
```

```callout kind=note title="If you run Omarchy"
Hermes Desktop installs from Omarchy's own menu (Install, AI, Hermes Desktop), follows the system theme, and can be set as the default agent with `omarchy default agent hermes`. Tonbi's warning is the one line to remember: launched that way, the agent starts in YOLO mode, which bypasses the dangerous-command approvals, so treat the default-agent binding as a power tool and read Build 10 of Volume 1 before you leave it on.
```

```callout kind=warn title="Two prompts people report after updates"
Operators on the Hermes forums and issue tracker describe two recurring prompts after an update: macOS asking again for folder or screen permissions, and a keychain prompt for the app's saved credentials. The documented cure for the first is the identity anchor above plus a `tccutil reset` and a fresh grant when a stale grant lingers. For the keychain prompt, the community advice is to allow it rather than delete the keychain item, since the item holds the app's stored credentials. Treat that second point as field advice, not a documented guarantee; the docs cover the permissions side in detail.
```

```callout kind=note title="From the field: Tonbi's Desktop Masterclass, part 1"
Tonbi's September 2026 rebuild of his desktop guide opens with the sentence this whole volume rests on: "It's a front end. It's not a separate agent." He also notes that his own June guide covered, by his count, about forty percent of the app after five major releases, which is the honest reason this volume names the documentation page for every fact instead of a video. When a video and the docs disagree, the docs are newer.
```

### Prompts

```code lang=markdown file=prompt-d0-what-did-the-app-install.md
Read https://hermes-agent.nousresearch.com/docs/user-guide/desktop
sections "How it works" and "Connecting to a remote backend" (just the first
paragraphs). Then look at this machine and tell me, with paths:

1. Where the Hermes runtime the app uses lives, and whether it is the same
   ~/.hermes my terminal uses (compare hermes status from both).
2. Which process the app is talking to right now (name and port) and whether
   it is the local backend or a remote one.
3. Whether Full Disk Access is granted for the terminal and for Hermes.app,
   from hermes doctor.
4. The last twenty lines of ~/.hermes/logs/desktop.log, summarized in three
   lines, with any warning quoted.

Change nothing.
```

### Verify

```checklist
[ ] The app opens to a chat on your existing profile, with your sessions from the CLI visible
[ ] hermes doctor shows Full Disk Access granted for the terminal, and the app no longer prompts per folder
[ ] hermes logs gui -f shows a clean boot with the backend ready
[ ] A message sent in the app appears in hermes sessions list from the terminal
```

## Build 1: The Window

![The app, mapped](assets/art/v2-app-map.webp)

### What you are building

Fluency. The dozen moves that make the app faster than the terminal for daily work: tabs and panes, the embedded terminal, the file browser, git review and worktrees, the HUD over other apps, Quick Entry from anywhere, the command palette, and the shortcuts worth remapping.

### What the docs say

Checked against the Desktop page: Chat, Status bar, Windows tabs and panes, Terminal, Git review and worktrees, Memory Graph, Quick Entry, Voice, HUD mode, Keyboard and navigation.

```table
| Surface | What it does | Open it |
| Tabs and windows | Several sessions at once; pop a session into its own window for another monitor | `Cmd+T` new session tab, `Ctrl+Tab` cycle, `Cmd+Shift+N` new window, `Cmd+W` close, `Cmd+Shift+T` reopen |
| Sidebars | Left is navigation, right holds preview, files, terminal, review | `Cmd+B` left, `Cmd+J` right, `Cmd+\` swap sides |
| Terminal | A real shell in the right sidebar; shells persist while hidden; select output and Add to chat | `` Ctrl+` `` show, `` Ctrl+Shift+` `` another, `Ctrl+Shift+W` close |
| File browser | Browse and preview the working directory as the agent edits it; set the start folder with `hermes desktop --cwd <path>` | right sidebar |
| Git review | Branch status, changed files, diffs scoped to Uncommitted, Branch or Last turn; stage, commit, push, Create PR with `gh`, or Ask Hermes to open PR | `Cmd+G` |
| Worktrees | A parallel copy of the repo on a new branch so an agent works without touching your checkout; shows as its own lane | `Cmd+Shift+B` |
| Preview rail | Web pages, files and tool outputs beside the chat; Hide keeps a live page or shell mounted, Close releases it | right rail |
| Comment mode | Click elements on a live page in the preview, type notes, then attach cropped screenshots plus selectors to the composer in one batch | Annotate in the preview bar |
| Status bar | Context meter with a token breakdown by category, per-session YOLO toggle, optional cache hit rate and tokens per second, right-click to choose items | bottom of the chat, `Cmd+Shift+S` hides it |
| Memory Graph | A zoomable map of learned skills and memories with a timeline | palette, Memory Graph; or `/journey` in chat |
| Quick Entry | A small composer summoned from anywhere on the system | `Cmd+Shift+Space` (Ctrl on Windows and Linux) after enabling it in Settings, Advanced |
| HUD | The chat detached into a chrome-free bar that floats over whatever you work in; where you park it tells Hermes which app and screen you mean | `Cmd+Shift+H`, `Cmd+Shift+G` snaps it to the cursor |
| Palette | Every page, setting, session, model, theme, terminal spawn, gateway restart and update from the keyboard | `Cmd+K` or `Cmd+P` |
| Shortcuts | Almost every binding is rebindable, conflicts flagged; `Cmd+1` to `9` switch profiles, `Cmd+Shift+F` searches sessions | `Cmd+/` |
| Conversation timeline rail | On long chats, a slim rail of markers along the transcript, one per prompt; hover to list the prompts, click to jump, then Show earlier pages back from there | long chats |
```

```callout kind=note title="From the field: sessions as context, panes as a desk"
Two moves Tonbi found in the app and now uses daily: drag a previous session into the current one to give it as context (start fresh, drop the old session in, ask "summarize this session"), and split a pane right or down to turn tabs into side-by-side sessions, which need not belong to the same project. He built his first desktop widget in one video, a memory monitor and then a baseball scoreboard, the scores widget from two prompts, the memory widget from one plus a follow-up to make it draggable, while watching the agent's own cursor move around the window to test it.
```

```callout kind=info title="The three that change how you work"
The HUD, because it turns "look at this" into a question about the window under the bar. Comment mode in the preview, because it turns a design review into a batch of tasks with selectors attached instead of a paragraph of description. And the Last turn diff scope in git review, because it shows exactly what the agent changed in its most recent turn, which is the review that actually matters.
```

```callout kind=note title="From the field: sessions are a cost control"
Tonbi's complete guide makes a point the docs state only in passing: one giant thread drags its whole history into every message, and splitting work into small sessions is what keeps that from compounding. His line: "you can end up paying three, four times what you actually need to." The status bar's context meter is where you watch it happen, and `hermes prompt-size` is where you see what every new session already carries before you type a word.
```

```callout kind=note title="From the field: the HUD does not notice you switched apps"
Tonbi's HUD video runs the bar over a terminal, Steam, Spotify, TradingView, Chrome and a video editor in one sitting, and the one rule he repeats is this: if you change apps mid-conversation and keep talking, the agent assumes you are still on the previous one. Say "what app am I on now" or "I have switched" and it looks again; nothing needs restarting. His other trick is worth stealing: the HUD is a separate agent from whatever runs in the window under it, so a local Hermes in the HUD can read and double-check a remote Hermes working in an SSH terminal beneath it, on a different model.
```

### Prompts

The first prompt is one you type into the HUD while it floats over another application; it proves the bar carries context.

```code lang=markdown file=prompt-d1-hud-context.md
I have parked you over a window. Tell me which application and which screen
you think I am asking about, then describe what you can see in it in three
lines. If you cannot see it, say what permission is missing and where to
grant it.
```

```code lang=markdown file=prompt-d1-review-last-turn.md
Make one small, safe change in this repository: add a line to the README
that names today's date and the model you are running on. Then stop. I am
going to open the review pane with Cmd+G, switch the scope to "Last turn",
and expect to see exactly that one file with exactly that one addition.
Tell me before you start whether anything you plan to do would touch a
second file.
```

### Verify

```checklist
[ ] You opened a second session tab, popped one into its own window, and closed it with Cmd+W
[ ] The terminal pane kept its shell and scrollback after being hidden and restored
[ ] Cmd+G showed the Last turn diff with exactly the change you asked for
[ ] The HUD answered with the right application under it, or named the permission it needed
```

## Build 2: The Settings That Matter

![Build 2](assets/art/part-05.webp)

### What you are building

The handful of settings that decide what the app costs and how it behaves, set deliberately, plus an audit prompt that reads the rest back to you from the docs so nothing is left at a default you never chose.

### What the docs say

Checked against the Desktop page (Choosing a model, Settings and onboarding, Per-profile settings, Fonts, Repository discovery) and the Configuration reference.

```table
| Setting | Where | What it really does |
| The composer model picker | left of the microphone in the composer | Sticky per device and per chat; it never writes your default. Mid-chat switches reset the prompt cache, so on a long chat a fresh chat on the new model is often cheaper |
| The default model | Settings, Model | The per-profile default that new chats, crons, subagents and auxiliary tasks start from. The only place that writes it |
| Auxiliary models and effort | Settings, Model, Auxiliary models | Each side task (compression, titling, vision, background review) gets its own provider, model and reasoning effort; saved as `auxiliary.<task>.reasoning_effort`, the same key `hermes model` writes |
| Applies to | top of the config-backed settings pages when you have two or more profiles | Selects which profile your edits target; it follows the active profile by default and resets when you switch |
| Reasoning blocks | Settings, Chat, or `/reasoning show` | `display.show_reasoning`; whether the model's thinking is shown in the transcript |
| Reopen last chat | Settings, Appearance | `display.resume_last_session`; off means every cold start begins fresh |
| Keep computer awake | Settings, Advanced | Stops sleep during long or overnight runs; per computer |
| Fonts | Settings, Appearance | `desktop.font_family` for the UI, `terminal.font_family` for the terminal pane, per profile |
| Repository discovery | Settings, Workspace | `desktop.repo_scan_enabled`, `desktop.repo_scan_roots`, `desktop.repo_scan_exclude_paths`: where the Projects sidebar looks |
| Quick Entry | Settings, Advanced | The global hotkey composer; needs at least one modifier |
| Themes | Settings, Appearance | Built-in presets plus any VS Code Marketplace theme, converted and installed |
```

```code lang=yaml file=~/.hermes/config.yaml (what these settings write)
display:
  show_reasoning: false           # Settings, Chat, Reasoning Blocks
  resume_last_session: true       # Settings, Appearance, Reopen Last Chat on Launch
desktop:
  font_family: ""                 # blank means the theme's font
  repo_scan_enabled: true
  repo_scan_roots: []             # empty means the default home scan
  repo_scan_exclude_paths: []
terminal:
  font_family: ""                 # blank means the bundled JetBrains Mono
auxiliary:
  compression:
    reasoning_effort: "low"       # summaries do not need deep thinking
  title_generation:
    reasoning_effort: "none"
```

```callout kind=note title="From the field: read the prompt before you tune the model"
Tonbi's habit when the agent "is not performing as well": run `hermes prompt-size` and look at what every new session is already carrying, skills index, memory, tool schemas, before touching the model. Too many enabled skills is the usual answer, and the Skills pane in Build 3 is where you trim them.
```

### Prompts

```code lang=markdown file=prompt-d2-audit-my-settings.md
Read https://hermes-agent.nousresearch.com/docs/user-guide/desktop sections
"Choosing a model" and "Settings & onboarding", then read my config.yaml and
answer, one line each:

1. My default model per profile (model.default) and which composer picks I
   have made that are NOT my default (say which is which).
2. Every auxiliary task that runs on my main model instead of a cheaper one,
   and the auxiliary.<task> keys I would set to move each.
3. Whether reasoning blocks are shown, whether the last chat reopens on
   launch, and whether keep awake is on.
4. What repo_scan is scanning right now and whether that is more than I
   need.

Then propose the diff for the changes you recommend, and stop. Do not save.
```

```code lang=markdown file=prompt-d2-one-setting.md
Set <key> to <value> in my config.yaml for the <profile> profile. Read the
matching row on https://hermes-agent.nousresearch.com/docs/user-guide/configuration
first and quote it. Show me the diff before you save. After I say go, save
it and tell me whether the running app picks it up live or needs a new
session.
```

### Verify

```checklist
[ ] Settings, Model shows the default you chose, and the composer picker shows the same unless you deliberately changed it for one chat
[ ] The auxiliary rows show a cheaper model or a lower effort for compression and titles
[ ] The Applies to chip row appears once you have two profiles and follows the active one
[ ] hermes config show reads back every key from the block above
```
