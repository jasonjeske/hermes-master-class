# The Hermes Desktop Masterclass

![The Hermes Desktop Masterclass](../assets/art/v2-hero.webp)

## Contents

- [Orientation](#user-content-orientation)
- **[Build 0](#user-content-build-0-install-and-first-launch)** Install and First Launch
- **[Build 1](#user-content-build-1-the-window)** The Window
- **[Build 2](#user-content-build-2-the-settings-that-matter)** The Settings That Matter
- **[Build 3](#user-content-build-3-capabilities-in-the-app)** Capabilities in the App
- **[Build 4](#user-content-build-4-gateways-and-other-machines)** Gateways and Other Machines
- **[Build 5](#user-content-build-5-plugin-workshop-i-hello-hermes)** Plugin Workshop I, Hello Hermes
- **[Build 6](#user-content-build-6-plugin-workshop-ii-the-prompt-library)** Plugin Workshop II, the Prompt Library
- **[Build 7](#user-content-build-7-plugin-workshop-iii-the-ledger-agent-and-desktop-in-one-package)** Plugin Workshop III, the Ledger (agent and desktop in one package)
- **[Build 8](#user-content-build-8-plugin-workshop-iv-let-hermes-build-the-next-one)** Plugin Workshop IV, let Hermes build the next one
- **[Build 9](#user-content-build-9-care-and-feeding)** Care and Feeding
- [The Desktop Ledger](#user-content-the-desktop-ledger)

---

## Orientation

Hermes Desktop is not a second product. It is the same agent you get from the CLI and the gateway, with the same config, keys, sessions, skills and memory, driven through a native window with panes, a terminal, a file browser, git review, voice, a HUD that floats over other apps, and a plugin system that lets one JavaScript file add a pane to the window. Everything you set up in Volume 1 is already here, and everything you do here shows up in the terminal.

This volume is a build track like Volume 1's second half. Ten builds, in dependency order, each ending with files you paste and prompts you run. The center of gravity is Builds 5 to 8: a plugin workshop that ends with three working plugins in the app and the prompt that makes Hermes write the fourth.

> 📝 **What this volume rests on**
>
> Every path, key, command, menu name and SDK call was checked against the official Hermes documentation for the version installed while writing (the Desktop page, the Desktop Plugin SDK page, Build a Hermes Plugin, the multi-connection guide, and the configuration reference) and against the bundled files in the Hermes repository. Where a tip comes from an operator's video or post rather than the docs, it says so. Where the docs do not cover something, the text says that too rather than guessing.

| Build | You end up with | Checked against | Time |
|---|---|---|---|
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

### How to use a build

Each build has four pieces. **What you are building** says what exists at the end. **What the docs say** is the short list of facts the build rests on, with the page named. **Prompts** are blocks marked with a file name like `prompt-d2-audit.md`: paste the whole block into a Hermes chat, in the app or anywhere else. **Commands** run in the app's own terminal pane or in your shell. Every build ends with a **verify** list, and a build is not done until that list passes.

> ℹ️ **The kits**
>
> Builds 5 to 8 ship their plugins as complete folders in the repository under `kits/`, validated against the loader's contract and, for the Python half, against `hermes plugins doctor --ci`. Copy a prompt and have Hermes type them, or clone the folder and drop it in place. Both roads end in the same file.

## Build 0: Install and First Launch

![Build 0](../assets/art/part-02.webp)

### What you are building

The app on your Mac, the local backend it manages, the one permission grant that stops macOS from asking about every folder, and a clear picture of what lives where.

### What the docs say

Checked against the Installation page, the Platform Support page, and the Desktop page.

| Fact | Detail |
|---|---|
| Two sanctioned installs | The Hermes Desktop installer from the website installs both the command line and the app, and is the recommended path on macOS. Or install the CLI first with the one-line installer, then run `hermes desktop`, which builds and launches the app against your existing config, keys, sessions and skills |
| Platform | macOS on Apple Silicon, Windows 10 and 11, and Linux or WSL2 all have a Desktop build; Intel Macs do not. This volume is written on macOS and says so where a step differs |
| The same home | On first launch the app can install the Hermes runtime into `~/.hermes`, the same layout a CLI install uses. That is why the two are interchangeable |
| What runs | The app launches a headless `hermes serve` backend for you and talks to it over JSON-RPC and WebSocket. It never needs the web dashboard |
| Folder prompts | macOS prompts per folder as Hermes touches Desktop, Downloads, Documents. One Full Disk Access grant for Hermes.app (and your terminal) covers all of them. `hermes doctor` reports whether the grant is present |
| Grants survive updates | Grants are remembered against the code-signing identity. Locally built and self-updated apps carry a stable identity, so grants persist. For a certificate-anchored identity run `hermes desktop --setup-tcc-identity` once, and re-run it after updates to re-sign |
| Stuck permission | `tccutil reset All com.nousresearch.hermes`, then re-grant and fully relaunch |
| Logs | Boot logs land in `~/.hermes/logs/desktop.log`; `hermes logs gui -f` tails them |

### Commands

*`day-one-desktop.sh`*

```bash
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

> 📝 **If you run Omarchy**
>
> Hermes Desktop installs from Omarchy's own menu (Install, AI, Hermes Desktop), follows the system theme, and can be set as the default agent with `omarchy default agent hermes`. Tonbi's warning is the one line to remember: launched that way, the agent starts in YOLO mode, which bypasses the dangerous-command approvals, so treat the default-agent binding as a power tool and read Build 10 of Volume 1 before you leave it on.

> ⚠️ **Two prompts people report after updates**
>
> Operators on the Hermes forums and issue tracker describe two recurring prompts after an update: macOS asking again for folder or screen permissions, and a keychain prompt for the app's saved credentials. The documented cure for the first is the identity anchor above plus a `tccutil reset` and a fresh grant when a stale grant lingers. For the keychain prompt, the community advice is to allow it rather than delete the keychain item, since the item holds the app's stored credentials. Treat that second point as field advice, not a documented guarantee; the docs cover the permissions side in detail.

> 📝 **From the field: Tonbi's Desktop Masterclass, part 1**
>
> Tonbi's September 2026 rebuild of his desktop guide opens with the sentence this whole volume rests on: "It's a front end. It's not a separate agent." He also notes that his own June guide covered, by his count, about forty percent of the app after five major releases, which is the honest reason this volume names the documentation page for every fact instead of a video. When a video and the docs disagree, the docs are newer.

### Prompts

*`prompt-d0-what-did-the-app-install.md`*

```markdown
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

- [ ] The app opens to a chat on your existing profile, with your sessions from the CLI visible
- [ ] hermes doctor shows Full Disk Access granted for the terminal, and the app no longer prompts per folder
- [ ] hermes logs gui -f shows a clean boot with the backend ready
- [ ] A message sent in the app appears in hermes sessions list from the terminal

## Build 1: The Window

![The app, mapped](../assets/art/v2-app-map.webp)

### What you are building

Fluency. The dozen moves that make the app faster than the terminal for daily work: tabs and panes, the embedded terminal, the file browser, git review and worktrees, the HUD over other apps, Quick Entry from anywhere, the command palette, and the shortcuts worth remapping.

### What the docs say

Checked against the Desktop page: Chat, Status bar, Windows tabs and panes, Terminal, Git review and worktrees, Memory Graph, Quick Entry, Voice, HUD mode, Keyboard and navigation.

| Surface | What it does | Open it |
|---|---|---|
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

> 📝 **From the field: sessions as context, panes as a desk**
>
> Two moves Tonbi found in the app and now uses daily: drag a previous session into the current one to give it as context (start fresh, drop the old session in, ask "summarize this session"), and split a pane right or down to turn tabs into side-by-side sessions, which need not belong to the same project. He built his first desktop widget in one video, a memory monitor and then a baseball scoreboard, the scores widget from two prompts, the memory widget from one plus a follow-up to make it draggable, while watching the agent's own cursor move around the window to test it.

> ℹ️ **The three that change how you work**
>
> The HUD, because it turns "look at this" into a question about the window under the bar. Comment mode in the preview, because it turns a design review into a batch of tasks with selectors attached instead of a paragraph of description. And the Last turn diff scope in git review, because it shows exactly what the agent changed in its most recent turn, which is the review that actually matters.

> 📝 **From the field: sessions are a cost control**
>
> Tonbi's complete guide makes a point the docs state only in passing: one giant thread drags its whole history into every message, and splitting work into small sessions is what keeps that from compounding. His line: "you can end up paying three, four times what you actually need to." The status bar's context meter is where you watch it happen, and `hermes prompt-size` is where you see what every new session already carries before you type a word.

> 📝 **From the field: the HUD does not notice you switched apps**
>
> Tonbi's HUD video runs the bar over a terminal, Steam, Spotify, TradingView, Chrome and a video editor in one sitting, and the one rule he repeats is this: if you change apps mid-conversation and keep talking, the agent assumes you are still on the previous one. Say "what app am I on now" or "I have switched" and it looks again; nothing needs restarting. His other trick is worth stealing: the HUD is a separate agent from whatever runs in the window under it, so a local Hermes in the HUD can read and double-check a remote Hermes working in an SSH terminal beneath it, on a different model.

### Prompts

The first prompt is one you type into the HUD while it floats over another application; it proves the bar carries context.

*`prompt-d1-hud-context.md`*

```markdown
I have parked you over a window. Tell me which application and which screen
you think I am asking about, then describe what you can see in it in three
lines. If you cannot see it, say what permission is missing and where to
grant it.
```

*`prompt-d1-review-last-turn.md`*

```markdown
Make one small, safe change in this repository: add a line to the README
that names today's date and the model you are running on. Then stop. I am
going to open the review pane with Cmd+G, switch the scope to "Last turn",
and expect to see exactly that one file with exactly that one addition.
Tell me before you start whether anything you plan to do would touch a
second file.
```

### Verify

- [ ] You opened a second session tab, popped one into its own window, and closed it with Cmd+W
- [ ] The terminal pane kept its shell and scrollback after being hidden and restored
- [ ] Cmd+G showed the Last turn diff with exactly the change you asked for
- [ ] The HUD answered with the right application under it, or named the permission it needed

## Build 2: The Settings That Matter

![Build 2](../assets/art/part-05.webp)

### What you are building

The handful of settings that decide what the app costs and how it behaves, set deliberately, plus an audit prompt that reads the rest back to you from the docs so nothing is left at a default you never chose.

### What the docs say

Checked against the Desktop page (Choosing a model, Settings and onboarding, Per-profile settings, Fonts, Repository discovery) and the Configuration reference.

| Setting | Where | What it really does |
|---|---|---|
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

*`~/.hermes/config.yaml`*

```yaml
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

> 📝 **From the field: read the prompt before you tune the model**
>
> Tonbi's habit when the agent "is not performing as well": run `hermes prompt-size` and look at what every new session is already carrying, skills index, memory, tool schemas, before touching the model. Too many enabled skills is the usual answer, and the Skills pane in Build 3 is where you trim them.

### Prompts

*`prompt-d2-audit-my-settings.md`*

```markdown
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

*`prompt-d2-one-setting.md`*

```markdown
Set <key> to <value> in my config.yaml for the <profile> profile. Read the
matching row on https://hermes-agent.nousresearch.com/docs/user-guide/configuration
first and quote it. Show me the diff before you save. After I say go, save
it and tell me whether the running app picks it up live or needs a new
session.
```

### Verify

- [ ] Settings, Model shows the default you chose, and the composer picker shows the same unless you deliberately changed it for one chat
- [ ] The auxiliary rows show a cheaper model or a lower effort for compression and titles
- [ ] The Applies to chip row appears once you have two profiles and follows the active one
- [ ] hermes config show reads back every key from the block above

## Build 3: Capabilities in the App

![Build 3](../assets/art/part-04.webp)

### What you are building

The management surface used from the app instead of the terminal: skills and plugins with an Installed view and a Browse view of the public catalogs, tools and MCP servers per agent, messaging setup with a QR code, and the two bundled safety plugins switched on for every profile you run.

### What the docs say

Checked against the Desktop page (Management panes, Where Browse gets its data, Extending the desktop app) and the Plugins and Plugin Catalog pages.

| Fact | Detail |
|---|---|
| Skills | Capabilities, Skills. Installed shows the selected profile's real skills and enable state; Browse searches the same published catalog as the public Skills Hub |
| Plugins | Capabilities, Plugins, same layout. Installed shows one row per plugin with a Desktop switch and an Agent switch; a plugin that ships both halves is one row. Browse shows the public Plugin Catalog. Install from Git takes any repo and can pin a commit |
| Where Browse reads | Native views over the same CDN snapshots the website uses (`/docs/api/skills.json`, `/docs/api/plugins.json`); no live GitHub calls |
| Install links | Hub pages carry `hermes://skill/install` and `hermes://plugin/install` links; the app always shows a review dialog before installing |
| The two switches | Desktop is app-level, one value everywhere. Agent is per profile, with the profile selector in that column's header |
| Tools and MCP | The Capabilities page has a Configuring selector that lists every agent on every connected machine; picking one edits that machine's toolsets and MCP servers |
| Messaging | The Messaging pane sets up gateway channels; Telegram has a Quick setup card that creates the bot from a QR code, detects your user id, saves credentials and restarts the gateway |
| Cron, Profiles, Agents, Command Center | Scheduled jobs, profile switching, and the orchestration surfaces, all reachable from the sidebar |

> 📝 **From the field: where plugins moved**
>
> Tonbi's part 3 flags a change that trips people following older videos: plugins used to live in Settings and now live under Capabilities beside Skills, Tools and MCP, with the desktop switch app-wide and the profile selector living only in the agent column's header. He also names the plugins he wrote for himself, a trading pane, a weather pane, a slide presenter, a YouTube planner, which is the best argument for Builds 5 to 8: the app becomes whatever panes you need.

### Commands

*`capabilities.sh`*

```bash
# The terminal twins of what Build 3 does in the app
hermes plugins list                      # every plugin and its state
hermes plugins enable security-guidance  # pattern-matches dangerous writes and warns or blocks
hermes plugins enable disk-cleanup       # tracks temp and test files the agent creates and cleans them
hermes skills list
hermes skills browse
```

> 📝 **From the field: the board decides who works**
>
> The Kanban board is a bundled desktop plugin and, in Tonbi's words, "the flagship plugin of Hermes desktop." His demonstration is the cleanest public example of the decomposer at work: a one-line idea dropped into triage fanned out into research, write and verify cards, each claimed by a different profile he had never assigned, because the Orchestration settings pane knows what each profile is good at from its description. The verifier card waited, blocked, until the writer card finished, then promoted itself to ready. His two tips: the Estimate effort button makes a real model call and tells you the token cost before you commit, and if you do not name a workspace the output lands in the board's attachments directory. Volume 3, Build 7 uses this board as the team's queue.

### Prompts

*`prompt-d3-capabilities-audit.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins
and https://hermes-agent.nousresearch.com/docs/user-guide/features/plugin-catalog
then run hermes plugins list and hermes skills list and tell me:

1. Which bundled plugins are enabled, and which of security-guidance and
   disk-cleanup are not.
2. Which catalog plugins would help the way I actually use you (read my
   last ten session titles first), three at most, with one line of why and
   the risk each one carries.
3. Which skills I have installed but have not loaded in the last thirty
   days (hermes curator status).

Then enable security-guidance and disk-cleanup with the config diff shown
first. Do not install anything from the catalog until I pick.
```

*`prompt-d3-telegram-from-the-app.md`*

```markdown
I am going to set up Telegram from Capabilities, Messaging with the QR
card. Before I do, read
https://hermes-agent.nousresearch.com/docs/user-guide/messaging and tell me
in five lines what the quick setup will write (which keys, which file),
what "allowlist" means for my user id, and what the Restart now banner is
waiting for. After I finish, verify from the terminal that the gateway is
running and the Telegram adapter connected, quoting the log line.
```

### Verify

- [ ] Capabilities, Plugins, Installed shows security-guidance and disk-cleanup with the Agent switch on for your profile
- [ ] Browse loads the catalog with cards, and opening a card shows an Install button, not a website
- [ ] The Configuring selector on Capabilities lists every profile you have
- [ ] If you set up Telegram, a message from your phone reaches the app and the reply comes back

## Build 4: Gateways and Other Machines

![Every gateway you own, in one window](../assets/art/v2-gateways-map.webp)

### What you are building

The app on your laptop talking to a Hermes that never sleeps on another machine: a Mac mini in the closet, a VPS, a box behind Tailscale. Then the registry that holds every gateway you own, so one window can reach all of them and update all of them.

### What the docs say

Checked against the Desktop page (Connecting to a remote backend, The multi-connection registry, On the backend, In the app, Troubleshooting) and the Connecting Desktop to Many Hermes Instances guide.

| Fact | Detail |
|---|---|
| What a remote backend is | A `hermes serve` process running on the other machine. The app attaches to it; it does not start it for you. Messaging channels are a separate gateway process you also keep running |
| Where it is set | Settings, Gateways. Connection mode offers Remote gateway (a URL plus sign-in) and Hermes Cloud (sign in and pick an agent). The registry below it holds named connections: Local, Remote gateway, SSH, Hermes Cloud |
| Auth on the backend | Binding to a non-loopback address engages the auth gate. Username and password for a trusted LAN or VPN; OAuth through Nous Portal (`hermes dashboard register`) for anything reachable from the internet |
| The env vars | `HERMES_DASHBOARD_BASIC_AUTH_USERNAME`, `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD` (or `_PASSWORD_HASH`), and `HERMES_DASHBOARD_BASIC_AUTH_SECRET` so sessions survive restarts, in `~/.hermes/.env` on the backend |
| Tailscale | Bind `hermes serve` to the machine's tailscale IP and use `http://<tailscale-ip>:9119` as the Remote URL so only your tailnet can reach it |
| Names | Every connection needs a unique device name; when the same profile exists on several gateways, handles disambiguate as `@profile-device` |
| SSH kind | An install reached over SSH; the app opens the tunnel and starts the backend for you; connect on demand, never spawned by a hover |
| Test | Probes the HTTP and WebSocket legs, so a pass means chat will work |
| Update all | Settings, Gateways, Update all instances dispatches `hermes update` to every eligible gateway and updates the app last |
| Sessions stay scoped | Sessions show one active gateway at a time; profiles, chats, messaging, cron, settings, files and memory all belong to the active gateway and profile pair |

> 📝 **From the field: SSH is the two-click path**
>
> Tonbi reached his always-on box through the VS Code Remote SSH extension until the SSH connection kind arrived. His account: update Hermes on both machines, have SSH keys already set up, pick the host in Settings, Gateways, save and reconnect, and "the desktop app handles everything. It handles the whole tunneling and everything else." Remote files, artifacts, images and the remote agent's learned skills all appear in the window. Two prerequisites, two clicks, and no auth gate to configure, which makes SSH the right first connection for a machine you own; the username-and-password path below is for a backend that must accept connections without an SSH login.

### Commands

*`on-the-remote-machine.sh`*

```bash
# On the machine that will serve (a Mac mini over Tailscale, say)
# An unquoted heredoc, so the secret is generated, not written literally.
cat >> ~/.hermes/.env <<ENV
HERMES_DASHBOARD_BASIC_AUTH_USERNAME=admin
HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=$(openssl rand -base64 18)
HERMES_DASHBOARD_BASIC_AUTH_SECRET=$(openssl rand -base64 32)
ENV
grep -c 'openssl' ~/.hermes/.env    # must print 0: both values were expanded
tail -2 ~/.hermes/.env             # copy the password somewhere safe now
chmod 600 ~/.hermes/.env

# Bind to the tailscale address, not 0.0.0.0, so only your tailnet can reach it
hermes serve --host <tailscale-ip> --port 9119
# keep it running under launchd, tmux or your process manager

# Confirm the gate is on
curl -s http://<tailscale-ip>:9119/api/status | jq '.auth_required, .auth_providers'
```

*`on-the-laptop.sh`*

```bash
# In the app: Settings, Gateways, Remote gateway
#   Remote URL: http://<tailscale-ip>:9119
#   Sign in with the username and password from the backend's .env
#   Save and reconnect
# Or set the URL before launch:
HERMES_DESKTOP_REMOTE_URL=http://<tailscale-ip>:9119 open -a Hermes
```

> ⚠️ **Password auth is for your own network**
>
> The backend reads and writes the remote machine's `.env` and runs agent commands. The docs are explicit: never expose a password-protected backend directly to the open internet. Put it behind Tailscale or a VPN, or use the OAuth provider for anything public. The stable secret matters too; without it the signing key is regenerated per boot and you are logged out on every restart.

> ⚠️ **If you are following an older video**
>
> Tonbi's June 2026 guide runs the remote backend with `hermes dashboard --no-open --host 0.0.0.0 --port 9119`. The current docs run it with `hermes serve`, and his own September masterclass says so. The auth environment variables and the Tailscale advice are unchanged; the command is not.

### Prompts

*`prompt-d4-prepare-the-mini.md`*

```markdown
You are running on the machine that will become my always-on Hermes
backend. Read
https://hermes-agent.nousresearch.com/docs/user-guide/desktop section
"Connecting to a remote backend" and the Tailscale note, then:

1. Tell me this machine's tailscale IP (tailscale ip -4) and whether
   hermes serve is already running (and on which host and port).
2. Show me the three HERMES_DASHBOARD_BASIC_AUTH_* lines you would append to
   ~/.hermes/.env, with the password replaced by <redacted> in your
   message. Generate the secret with openssl.
3. Show me the hermes serve command bound to the tailscale IP and a
   launchd plist that keeps it running after logout, as a file for me to
   review. Do not install it yet.
4. After I say go: write the env lines, load the plist, and prove the gate
   is on with curl against /api/status.
```

*`prompt-d4-registry-check.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/user-guide/multi-connection-desktop
sections "The gateway registry" and "Agents across gateways". I have
registered a second gateway named <device>. Tell me which of my profile
names now collide across machines and what their @name-device handles will
be, and which gateway is Primary. Then explain in three lines what stays
scoped to the active gateway when I switch, so I know what I will and will
not see.
```

### Verify

- [ ] curl against /api/status on the backend reports auth_required true and lists the provider
- [ ] The app's Test button reports Reachable for the new connection
- [ ] Sessions started on the remote gateway show up in hermes sessions list on that machine, not on the laptop
- [ ] Update all instances lists both gateways and the app itself

## Build 5: Plugin Workshop I, Hello Hermes

![Build 5](../assets/art/v2-plugin-anatomy.webp)

### What you are building

Your first desktop plugin: a pane in the right dock, a chip in the status bar, a palette command and a keybind, in one file of about eighty lines, loaded live into the running app without a build step. It does nothing useful yet. It proves the loop: write a file, watch the app pick it up, see it in Capabilities, and learn the six rules every plugin after this one obeys.

### What the docs say

Checked against the Desktop Plugin SDK page and the Extending section of the Desktop page.

| Fact | Detail |
|---|---|
| One file | `~/.hermes/desktop-plugins/<id>/plugin.js`, plain ESM, loaded uncompiled. The folder name must equal the plugin's `id` |
| Three imports only | `@hermes/plugin-sdk`, `react`, `react/jsx-runtime`. Anything else fails to resolve on purpose |
| No JSX syntax | The file is not compiled, so write `jsx()` and `jsxs()` calls from `react/jsx-runtime` |
| The contract | Default-export `{ id, name, defaultEnabled, register(ctx) }`. `register` receives a scoped context and calls `ctx.register` or `ctx.registerMany` with contributions `{ id, area, title, order, when, render, data }` |
| Where things can go | Panes (`placement` main, left, right, top, bottom, optional `dock`), full pages (`ROUTES_AREA`), sidebar nav, status bar left or right, title bar, palette commands, keybinds, themes, composer slots, transcript directives |
| Styling | Theme variables only, in the `text-(--ui-text-tertiary)` form. Never a literal color. Leave the background alone |
| Hot reload | The app watches the folder, loads a new file within seconds, and reloads on every save. `Cmd+K`, Reload desktop plugins, forces it. Errors show as a toast and in `hermes logs gui -f` |
| App level | A desktop plugin is the same on every profile, gateway and remote machine the window connects to |
| Authority | A loaded plugin runs in the renderer with the app's full authority; the loader isolates errors, not intent. Load only files you or your agent wrote |

> 📝 **From the field: form follows the job**
>
> Tonbi's plugin guide counts twenty-five places a contribution can land and sorts them into four forms: compact (a status-bar item, "one factor, one action that should always be nearby"), anchored (a popover for detail and quick control without leaving the chat), expansive (a route with a sidebar entry, for real applications and dense data) and declarative (structured data the host decides how to show). His rule: decide the form from what the plugin is for before writing a line. His limits are worth pinning too: a plugin's storage is small JSON state, not a database; a plugin only runs while the app is open; it can only occupy areas the app itself consumes; and "a renderer-only plugin is strong for UI. A plugin plus a Python backend can become a real product." Builds 5, 6 and 7 walk that ladder in order.

### The file

*`~/.hermes/desktop-plugins/hello-hermes/plugin.js`*

```javascript
// Hello Hermes - a Hermes Desktop plugin. Folder name must equal the id.
// Loaded uncompiled: no JSX syntax, and only these specifiers resolve.
import { host, haptic, useValue, STATUSBAR_AREAS, PALETTE_AREA, KEYBINDS_AREA } from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'

function HelloHermesPane() {
  const gateway = useValue(host.state.gateway)
  const profile = useValue(host.state.profile)

  return jsxs('div', {
    className: 'flex h-full flex-col gap-2 p-3 text-sm',
    children: [
      jsx('div', { className: 'font-medium', children: "Hello Hermes" }),
      jsx('div', {
        className: 'text-(--ui-text-tertiary)',
        children: 'gateway: ' + String(gateway)
      }),
      jsx('div', {
        className: 'text-(--ui-text-tertiary)',
        children: 'profile: ' + String(profile)
      })
    ]
  })
}

function HelloHermesChip() {
  return jsx('button', {
    type: 'button',
    className: 'px-1.5 text-[0.6875rem] text-(--ui-text-tertiary)',
    onClick: () => {
      haptic('tap')
      host.notify({ kind: 'info', message: "Hello Hermes is loaded." })
    },
    children: "hello-hermes"
  })
}

export default {
  id: "hello-hermes",
  name: "Hello Hermes",
  defaultEnabled: false,
  register(ctx) {
    ctx.register({
      id: 'pane',
      area: 'panes',
      title: "Hello Hermes",
      data: { placement: "right", width: "280px" },
      render: () => jsx(HelloHermesPane, {})
    })

    ctx.register({
      id: 'chip',
      area: STATUSBAR_AREAS.right,
      order: 130,
      render: () => jsx(HelloHermesChip, {})
    })

    ctx.register({
      id: 'open',
      area: PALETTE_AREA,
      data: {
        id: "hello-hermes.open",
        label: "Open Hello Hermes",
        keywords: ["hello-hermes", 'hermes', 'pane'],
        run: () => host.notify({ kind: 'info', message: "Hello Hermes pane is in the right dock." })
      }
    })

    ctx.register({
      id: 'keybind',
      area: KEYBINDS_AREA,
      data: {
        id: "hello-hermes.focus",
        label: "Focus Hello Hermes",
        category: "Hello Hermes",
        defaults: ['mod+alt+h'],
        run: () => host.notify({ kind: 'info', message: "Hello Hermes focused." })
      }
    })
  }
}
```

> ℹ️ **Why defaultEnabled is false**
>
> A plugin with `defaultEnabled: false` inventories in Capabilities, Plugins and stays dark until you flip it on. That is the right default for anything you are still writing: the app loads the file, you enable it when you want to see it, and a broken save never surprises you mid-conversation. Ship it that way too; the person installing it decides.

### Commands

*`hello.sh`*

```bash
mkdir -p ~/.hermes/desktop-plugins/hello-hermes
# paste the file above as ~/.hermes/desktop-plugins/hello-hermes/plugin.js
# then in the app: Cmd+K, "Reload desktop plugins", then Capabilities, Plugins, switch Hello Hermes on
hermes logs gui -f            # the load line, or the error toast's cause
```

### Prompts

*`prompt-d5-explain-my-plugin.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk
sections "Mental model", "The plugin contract" and "Pitfalls". Then read the
file ~/.hermes/desktop-plugins/hello-hermes/plugin.js and explain it to me
contribution by contribution: what each register call adds, which area it
lands in, and which host door it uses. Finish with the three rules from the
Pitfalls section that this file already obeys and the one thing I would
break first if I edited it carelessly.
```

*`prompt-d5-change-one-thing.md`*

```markdown
Change the Hello Hermes plugin so the pane also shows the active model
(host.state.model) and the chip shows the gateway state instead of the
word hello-hermes. Keep every rule of the format: only the three imports,
jsx() calls, theme variables, folder name equal to id. Show me the diff
before you write it. After I say go, save it and tell me what I should see
after the hot reload, then tail hermes logs gui for ten seconds and report
any error.
```

### Verify

- [ ] Capabilities, Plugins lists Hello Hermes with a Desktop switch; flipping it on adds the pane to the right dock
- [ ] The status bar shows the hello-hermes chip and clicking it toasts
- [ ] Cmd+K finds "Open Hello Hermes"; Cmd+Option+H fires the keybind (Cmd+Shift+H is taken: it toggles the HUD)
- [ ] hermes logs gui -f shows the load with no error line

## Build 6: Plugin Workshop II, the Prompt Library

![Build 6](../assets/art/part-03.webp)

### What you are building

A full page in the app, reachable from the sidebar, the palette and a keybind, that stores the prompts you paste most: search them, copy one to the clipboard, or open a fresh chat in the current profile with the prompt ready to paste. State persists per plugin through the SDK's storage. It ships with three starter prompts from this masterclass so it is useful the second it loads.

### What the docs say

Checked against the Desktop Plugin SDK page: Pages and sidebar nav, Palette commands and keybinds, Host API, the `ctx.os` door, Settings and storage, the UI kit.

| Fact | Detail |
|---|---|
| A page | `ROUTES_AREA` with `data: { path }` mounts a full page in the workspace; pair it with `SIDEBAR_NAV_AREA` (`path`, `label`, `codicon`) and navigate with `host.navigate(path)` |
| Storage | `ctx.storage.get(key, fallback)`, `.set`, `.remove`, namespaced under `hermes.plugin.<id>.*`. Renaming the plugin loses its stored state |
| The OS door | `ctx.os.writeClipboard(text)` resolves false when unavailable; `ctx.os.openExternal(url)`, `ctx.os.revealPath(path)`, `ctx.os.notify` for native notifications |
| New chats | `host.newChat(profile)` opens a fresh chat, optionally in another profile |
| The UI kit | Import the app's own components (`Button`, `Input`, `Textarea`, `ScrollArea`, `EmptyState` and the rest) so the page is native by default |
| State in React | Subscribe with `useValue(atom)` only in the component that renders the value; read atoms with `.get()` in handlers |

### The file

*`~/.hermes/desktop-plugins/prompt-library/plugin.js`*

```javascript
// Prompt Library, a Hermes Desktop plugin. Folder name must equal the id.
// One ESM file, loaded uncompiled: no JSX syntax, only the three allowed imports.
import {
  host, haptic, useValue, Button, Input, Textarea, ScrollArea, EmptyState,
  ROUTES_AREA, SIDEBAR_NAV_AREA, PALETTE_AREA, KEYBINDS_AREA, STATUSBAR_AREAS
} from '@hermes/plugin-sdk'
import { useState } from 'react'
import { jsx, jsxs } from 'react/jsx-runtime'

const ROUTE = '/prompt-library'

// Storage lives under hermes.plugin.prompt-library.* and is namespaced by the host.
function loadPrompts(ctx) {
  return ctx.storage.get('prompts', [])
}
function savePrompts(ctx, prompts) {
  ctx.storage.set('prompts', prompts)
}

const STARTERS = [
  {
    id: 'change-a-setting',
    title: 'Change one setting safely',
    tags: 'config docs diff',
    body: 'Read the "<section>" section of https://hermes-agent.nousresearch.com/docs/user-guide/configuration and set <key> to <value> in my config.yaml. Show me the diff before you save it. After I say go, save it and run hermes config show to confirm.'
  },
  {
    id: 'write-a-skill',
    title: 'Turn what we just did into a skill',
    tags: 'skill procedure',
    body: 'Turn the workflow we just completed into a skill under ~/.hermes/skills/<category>/<name>/SKILL.md with a description under sixty characters phrased as the request it answers, then When to Use, Procedure, Pitfalls and Verification. Show me the file before creating it with skill_manage.'
  },
  {
    id: 'build-a-desktop-plugin',
    title: 'Build me a desktop plugin',
    tags: 'plugin desktop sdk',
    body: 'Load the bundled hermes-desktop-plugins skill and write a Hermes Desktop plugin at ~/.hermes/desktop-plugins/<id>/plugin.js that <does one thing>. Only import from @hermes/plugin-sdk, react and react/jsx-runtime, no JSX syntax, theme variables only, folder name equal to the id. Show me the file, then tell me the exact palette command to reload plugins and what I should see.'
  }
]

function PromptCard({ prompt, onCopy, onChat, onDelete }) {
  return jsxs('div', {
    className: 'flex flex-col gap-1 rounded border border-(--ui-stroke-secondary) p-2',
    children: [
      jsxs('div', { className: 'flex items-center justify-between gap-2', children: [
        jsx('div', { className: 'font-medium', children: prompt.title }),
        jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-quaternary)', children: prompt.tags || '' })
      ]}),
      jsx('div', { className: 'whitespace-pre-wrap text-(--ui-text-secondary)', children: prompt.body }),
      jsxs('div', { className: 'flex gap-2 pt-1', children: [
        jsx(Button, { size: 'sm', onClick: () => onCopy(prompt), children: 'Copy' }),
        jsx(Button, { size: 'sm', variant: 'outline', onClick: () => onChat(prompt), children: 'New chat' }),
        jsx(Button, { size: 'sm', variant: 'ghost', onClick: () => onDelete(prompt), children: 'Delete' })
      ]})
    ]
  })
}

function PromptLibraryPage({ ctx }) {
  const [prompts, setPrompts] = useState(() => {
    const stored = ctx.storage.get(KEY, null)
    if (stored === null) { savePrompts(ctx, STARTERS); return STARTERS }
    return stored
  })
  const [query, setQuery] = useState('')
  const [title, setTitle] = useState('')
  const [tags, setTags] = useState('')
  const [body, setBody] = useState('')
  const profile = useValue(host.state.profile)

  const persist = (next) => { setPrompts(next); savePrompts(ctx, next) }
  const q = query.trim().toLowerCase()
  const visible = prompts.filter(p => !q || (p.title + ' ' + p.tags + ' ' + p.body).toLowerCase().includes(q))

  const copy = async (p) => {
    const ok = await ctx.os.writeClipboard(p.body)
    haptic('tap')
    host.notify({ kind: ok ? 'info' : 'warning', message: ok ? 'Prompt copied. Paste it into any chat.' : 'Clipboard is not available here.' })
  }
  const chat = async (p) => {
    await ctx.os.writeClipboard(p.body)
    host.newChat(profile)
    host.notify({ kind: 'info', message: 'New chat opened in ' + profile + '. The prompt is on your clipboard: paste and send.' })
  }
  const remove = (p) => persist(prompts.filter(x => x.id !== p.id))
  const add = () => {
    if (!title.trim() || !body.trim()) {
      host.notify({ kind: 'warning', message: 'A prompt needs a title and a body.' })
      return
    }
    const id = title.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') + '-' + Date.now().toString(36)
    persist([{ id, title: title.trim(), tags: tags.trim(), body: body.trim() }, ...prompts])
    setTitle(''); setTags(''); setBody('')
  }

  return jsxs('div', {
    className: 'flex h-full flex-col gap-3 p-4 text-sm',
    children: [
      jsxs('div', { className: 'flex items-center justify-between', children: [
        jsx('div', { className: 'text-base font-medium', children: 'Prompt Library' }),
        jsx('div', { className: 'text-(--ui-text-tertiary)', children: String(prompts.length) + ' prompts, profile ' + profile })
      ]}),
      jsx(Input, { value: query, placeholder: 'Search title, tags, text', onChange: (e) => setQuery(e.target.value) }),
      jsxs('div', { className: 'grid gap-2 rounded border border-(--ui-stroke-secondary) p-2', children: [
        jsx(Input, { value: title, placeholder: 'Title', onChange: (e) => setTitle(e.target.value) }),
        jsx(Input, { value: tags, placeholder: 'tags, space separated', onChange: (e) => setTags(e.target.value) }),
        jsx(Textarea, { value: body, rows: 5, placeholder: 'The prompt, exactly as you would paste it', onChange: (e) => setBody(e.target.value) }),
        jsx('div', { children: jsx(Button, { size: 'sm', onClick: add, children: 'Save prompt' }) })
      ]}),
      jsx(ScrollArea, { className: 'min-h-0 flex-1', children:
        visible.length
          ? jsx('div', { className: 'flex flex-col gap-2 pr-2', children: visible.map(p => jsx(PromptCard, { key: p.id, prompt: p, onCopy: copy, onChat: chat, onDelete: remove })) })
          : jsx(EmptyState, { title: 'No prompts match', description: 'Clear the search or save a new prompt above.' })
      })
    ]
  })
}

function CountChip({ ctx }) {
  return jsx('button', {
    type: 'button',
    className: 'px-1.5 text-[0.6875rem] text-(--ui-text-tertiary)',
    onClick: () => host.navigate(ROUTE),
    children: 'prompts ' + String(loadPrompts(ctx).length)
  })
}

export default {
  id: 'prompt-library',
  name: 'Prompt Library',
  defaultEnabled: false,
  register(ctx) {
    ctx.registerMany([
      { id: 'page', area: ROUTES_AREA, data: { path: ROUTE }, render: () => jsx(PromptLibraryPage, { ctx }) },
      { id: 'nav', area: SIDEBAR_NAV_AREA, data: { path: ROUTE, label: 'Prompts', codicon: 'book' } },
      { id: 'chip', area: STATUSBAR_AREAS.right, order: 125, render: () => jsx(CountChip, { ctx }) },
      { id: 'open', area: PALETTE_AREA, data: { id: 'prompt-library.open', label: 'Open Prompt Library', keywords: ['prompt', 'library', 'template'], run: () => host.navigate(ROUTE) } },
      { id: 'keybind', area: KEYBINDS_AREA, data: { id: 'prompt-library.open', label: 'Open Prompt Library', category: 'Prompt Library', defaults: ['mod+shift+p'], run: () => host.navigate(ROUTE) } }
    ])
  }
}
```

> 📝 **Why copy and paste, not inject**
>
> The SDK gives a plugin a curated set of doors and a composer middleware for transforming a draft on its way out, but no documented call that writes text into the composer of an existing chat. So the library does the honest thing: it puts the prompt on your clipboard and, if you ask, opens a fresh chat in the current profile for you to paste into. One keystroke more, zero reliance on an undocumented method that a release could remove.

### Prompts

*`prompt-d6-seed-my-library.md`*

```markdown
Open the Prompt Library page in the app is my job; yours is the content.
Read every prompt I have pasted into you in the last two weeks
(session_search across my sessions for messages that start with "Read
https://hermes-agent.nousresearch.com/docs" or with "Build me"), pick the
eight I reuse most, and give each a title under six words and three tags.
Return them as a JSON array of {title, tags, body} so I can paste them into
the library one by one. Do not rewrite the bodies.
```

*`prompt-d6-extend-it.md`*

```markdown
Read the Prompt Library plugin at
~/.hermes/desktop-plugins/prompt-library/plugin.js and add one feature:
an "Export" button that writes all prompts as JSON to the clipboard, and an
"Import" textarea that merges a pasted JSON array into storage without
duplicating ids. Keep the format rules. Show me the diff before saving.
```

### Verify

- [ ] The sidebar shows Prompts; the page opens with the three starter prompts
- [ ] Saving a prompt survives an app restart (storage is persisted)
- [ ] Copy puts the body on the clipboard; New chat opens a chat in the current profile
- [ ] Cmd+Shift+P opens the page

## Build 7: Plugin Workshop III, the Ledger (agent and desktop in one package)

![Build 7](../assets/art/v2-unified-package.webp)

### What you are building

The first plugin with two halves in one folder. The agent gets two tools, `ledger_add` and `ledger_report`, and a `/ledger` slash command, so telling Hermes "I paid 42.50 for groceries" records it and "how much did I spend this month" answers from real numbers. The desktop gets a Ledger page that reads the same database through the plugin's own backend routes, with a form and bars by category. Money lands in a SQLite file under the plugin data directory, never in the plugin folder, so updates cannot erase it.

### What the docs say

Checked against Build a Hermes Plugin, the Desktop Plugin SDK's "One package, both SDKs" and "The Python side", and Extending the Dashboard.

| Fact | Detail |
|---|---|
| Layout | `~/.hermes/plugins/<id>/` with `plugin.yaml`, `__init__.py` (`register(ctx)`), `schemas.py`, `tools.py`, `dashboard/manifest.json` plus `dashboard/plugin_api.py`, and `desktop/plugin.js`. One installable folder |
| Manifest v2 | `manifest_version: 2`, `api_version: 1`, `name`, `version`, `description`, `license`, `tags`, `provides_tools`; optional `requires_env`, `python_dependencies` or a `pyproject.toml`, `config_schema` |
| Handlers | `def handler(args: dict, **kwargs) -> str`: always a JSON string, never raise. The schema description is what makes the model call the tool |
| Slash commands | `ctx.register_command("ledger", handler, description=...)` gives `/ledger` on every surface |
| Durable state | `from plugins.plugin_storage import plugin_db` returns a SQLite connection at `<home>/plugin-data/<id>/data.db`, WAL mode. Never write into the plugin directory |
| The backend | `dashboard/manifest.json` is `{"name": "<id>", "api": "plugin_api.py"}`; `plugin_api.py` exports a FastAPI `router`; routes mount under `/api/plugins/<id>/` inside the gateway, at startup, only when the plugin is in `plugins.enabled` |
| The desktop half | `desktop/plugin.js` is an ordinary disk plugin; the app copies it to `~/.hermes/desktop-plugins/<id>/` when the package is installed and reaches the backend with `ctx.rest('/summary')` |
| Two switches | The Python half is gated by `plugins.enabled` in config.yaml; the desktop half by its own switch in Capabilities, Plugins. Both default to off |
| Doctor | `hermes plugins doctor ~/.hermes/plugins/ledger --ci` runs real discovery, manifest parsing, import and registration |

### The files

*`~/.hermes/plugins/ledger/plugin.yaml`*

```yaml
name: ledger
version: 1.0.0
description: "A personal money ledger: the agent records entries by tool, the desktop shows the month."
manifest_version: 2
api_version: 1
license: MIT
tags: [finance, personal, desktop]
provides_tools:
  - ledger_add
  - ledger_report
```

*`~/.hermes/plugins/ledger/schemas.py`*

```python
"""JSON schemas for the ledger tools. The description is how the model decides to call them."""

from __future__ import annotations

LEDGER_ADD = {
    "name": "ledger_add",
    "description": (
        "Record one money entry in the personal ledger: an expense or an income, "
        "with an amount, a category, an optional note and an optional date. "
        "Use it whenever the user mentions spending, paying, earning, or receiving money."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "amount": {"type": "number", "description": "Positive amount in the ledger currency, e.g. 42.50"},
            "kind": {"type": "string", "enum": ["expense", "income"], "description": "expense or income"},
            "category": {
                "type": "string",
                "description": "Short category such as groceries, rent, software, transport, salary, client",
            },
            "note": {"type": "string", "description": "What it was, in a few words"},
            "date": {"type": "string", "description": "ISO date YYYY-MM-DD; today when omitted"},
        },
        "required": ["amount", "kind", "category"],
    },
}

LEDGER_REPORT = {
    "name": "ledger_report",
    "description": (
        "Summarize the personal ledger for a month: totals for income and expenses, "
        "the net, and expenses grouped by category. Use it when the user asks how much "
        "they spent or earned, where the money went, or for a monthly budget check."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "month": {"type": "string", "description": "Month as YYYY-MM; the current month when omitted"},
            "limit": {"type": "integer", "description": "How many recent entries to include, default 10"},
        },
        "required": [],
    },
}
```

*`~/.hermes/plugins/ledger/ledger_core.py`*

```python
"""Ledger core: the SQLite store and the two operations. No Hermes imports at module level,
so both the agent tools and the dashboard API can load this file.

Durable state lives under <hermes home>/plugin-data/ledger/ through plugins.plugin_storage,
never inside the plugin folder (updates and removals wipe the folder).
"""

from __future__ import annotations

import datetime as dt

_SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  kind TEXT NOT NULL CHECK (kind IN ('expense', 'income')),
  category TEXT NOT NULL,
  amount REAL NOT NULL CHECK (amount > 0),
  note TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS entries_date ON entries(date);
"""


def db():
    """Open the plugin's SQLite database (WAL mode, created on first use)."""
    from plugins.plugin_storage import plugin_db

    conn = plugin_db("ledger")
    conn.executescript(_SCHEMA)
    return conn


def _month(value: str | None) -> str:
    if value and len(value) == 7 and value[4] == "-":
        return value
    return dt.date.today().strftime("%Y-%m")


def add_entry(amount: float, kind: str, category: str, note: str = "", date: str | None = None) -> dict:
    day = date or dt.date.today().isoformat()
    dt.date.fromisoformat(day)  # raises on a bad date
    conn = db()
    with conn:
        cur = conn.execute(
            "INSERT INTO entries(date, kind, category, amount, note, created_at) VALUES (?,?,?,?,?,?)",
            (day, kind, category.strip().lower(), float(amount), note.strip(), dt.datetime.now().isoformat(timespec="seconds")),
        )
    return {"id": cur.lastrowid, "date": day, "kind": kind, "category": category.strip().lower(), "amount": float(amount), "note": note.strip()}


def month_report(month: str | None = None, limit: int = 10) -> dict:
    month = _month(month)
    conn = db()
    like = month + "-%"
    income = conn.execute("SELECT COALESCE(SUM(amount),0) FROM entries WHERE kind='income' AND date LIKE ?", (like,)).fetchone()[0]
    expense = conn.execute("SELECT COALESCE(SUM(amount),0) FROM entries WHERE kind='expense' AND date LIKE ?", (like,)).fetchone()[0]
    by_cat = conn.execute(
        "SELECT category, ROUND(SUM(amount),2) AS total, COUNT(*) AS n FROM entries "
        "WHERE kind='expense' AND date LIKE ? GROUP BY category ORDER BY total DESC",
        (like,),
    ).fetchall()
    recent = conn.execute(
        "SELECT id, date, kind, category, amount, note FROM entries WHERE date LIKE ? ORDER BY date DESC, id DESC LIMIT ?",
        (like, int(limit)),
    ).fetchall()
    return {
        "month": month,
        "income": round(income, 2),
        "expenses": round(expense, 2),
        "net": round(income - expense, 2),
        "by_category": [{"category": c, "total": t, "count": n} for c, t, n in by_cat],
        "recent": [
            {"id": i, "date": d, "kind": k, "category": c, "amount": a, "note": nt} for i, d, k, c, a, nt in recent
        ],
    }
```

*`~/.hermes/plugins/ledger/tools.py`*

```python
"""Handlers for the ledger tools.

Rules Hermes holds every handler to: take the parsed args dict, return a JSON
string, never raise.
"""

from __future__ import annotations

import json
from typing import Any

from . import ledger_core as core


def ledger_add(args: dict, **kwargs: Any) -> str:
    try:
        amount = float(args.get("amount", 0))
        kind = str(args.get("kind", "expense")).lower()
        category = str(args.get("category", "")).strip()
        if amount <= 0 or kind not in ("expense", "income") or not category:
            return json.dumps({"error": "need a positive amount, a kind of expense or income, and a category"})
        entry = core.add_entry(amount, kind, category, str(args.get("note", "")), args.get("date") or None)
        return json.dumps({"ok": True, "entry": entry})
    except Exception as exc:  # a handler never raises
        return json.dumps({"error": str(exc)})


def ledger_report(args: dict, **kwargs: Any) -> str:
    try:
        return json.dumps(core.month_report(args.get("month"), int(args.get("limit", 10) or 10)))
    except Exception as exc:
        return json.dumps({"error": str(exc)})
```

*`~/.hermes/plugins/ledger/__init__.py`*

```python
"""ledger plugin for Hermes Agent: two tools and one slash command.

register() runs once at load. A crash here disables only this plugin.
"""

from __future__ import annotations

import json
import logging

from . import ledger_core as core, schemas, tools

logger = logging.getLogger(__name__)

TOOLSET = "ledger"


def _slash_ledger(raw_args: str) -> str:
    """/ledger [YYYY-MM]: print the month summary without spending a model turn."""
    try:
        report = core.month_report(raw_args.strip() or None, limit=5)
    except Exception as exc:
        return f"ledger: {exc}"
    lines = [
        f"Ledger {report['month']}: income {report['income']:.2f}, expenses {report['expenses']:.2f}, net {report['net']:.2f}",
    ]
    for row in report["by_category"][:8]:
        lines.append(f"  {row['category']:<16} {row['total']:>10.2f}  ({row['count']})")
    return "\n".join(lines)


def register(ctx) -> None:
    ctx.register_tool(name="ledger_add", toolset=TOOLSET, schema=schemas.LEDGER_ADD, handler=tools.ledger_add)
    ctx.register_tool(name="ledger_report", toolset=TOOLSET, schema=schemas.LEDGER_REPORT, handler=tools.ledger_report)
    ctx.register_command("ledger", _slash_ledger, description="Month summary of the personal ledger, e.g. /ledger 2026-09")
    logger.debug("ledger registered: %s", json.dumps(["ledger_add", "ledger_report", "/ledger"]))
```

*`~/.hermes/plugins/ledger/dashboard/manifest.json`*

```json
{
  "name": "ledger",
  "api": "plugin_api.py"
}
```

*`~/.hermes/plugins/ledger/dashboard/plugin_api.py`*

```python
"""Backend routes for the ledger desktop page. Mounted at /api/plugins/ledger/ inside the gateway.

The dashboard loads this file by path, not as part of the plugin package, so the core
module is loaded by path too (the same pattern the bundled examples use).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from fastapi import APIRouter, HTTPException

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("hermes_ledger_core", _HERE.parent / "ledger_core.py")
core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(core)

router = APIRouter()


@router.get("/summary")
async def summary(month: str | None = None) -> dict:
    return core.month_report(month, limit=20)


@router.post("/entries")
async def create(body: dict) -> dict:
    try:
        amount = float(body.get("amount", 0))
        kind = str(body.get("kind", "expense")).lower()
        category = str(body.get("category", "")).strip()
        if amount <= 0 or kind not in ("expense", "income") or not category:
            raise ValueError("need a positive amount, a kind, and a category")
        return {"ok": True, "entry": core.add_entry(amount, kind, category, str(body.get("note", "")), body.get("date") or None)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/entries/{entry_id}")
async def remove(entry_id: int) -> dict:
    conn = core.db()
    with conn:
        cur = conn.execute("DELETE FROM entries WHERE id = ?", (int(entry_id),))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="no such entry")
    return {"ok": True, "deleted": int(entry_id)}
```

*`~/.hermes/plugins/ledger/desktop/plugin.js`*

```javascript
// Desktop half of the ledger plugin: a page that reads /api/plugins/ledger/ through ctx.rest.
// Loaded uncompiled: no JSX syntax, only the three allowed imports, theme variables only.
import {
  host, useQuery, useQueryClient, Button, Input, ScrollArea, EmptyState,
  ROUTES_AREA, SIDEBAR_NAV_AREA, PALETTE_AREA
} from '@hermes/plugin-sdk'
import { useState } from 'react'
import { jsx, jsxs } from 'react/jsx-runtime'

const ID = 'ledger'
const ROUTE = '/ledger'

function thisMonth() {
  const d = new Date()
  return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0')
}

function money(n) {
  return (Math.round(Number(n) * 100) / 100).toFixed(2)
}

function Bar({ label, value, max, count }) {
  const pct = max > 0 ? Math.max(2, Math.round((value / max) * 100)) : 0
  return jsxs('div', { className: 'flex flex-col gap-0.5', children: [
    jsxs('div', { className: 'flex justify-between text-[0.75rem]', children: [
      jsx('span', { children: label + (count ? '  (' + count + ')' : '') }),
      jsx('span', { className: 'text-(--ui-text-tertiary)', children: money(value) })
    ]}),
    jsx('div', { className: 'h-1.5 w-full rounded bg-(--ui-stroke-secondary)', children:
      jsx('div', { className: 'h-1.5 rounded bg-(--ui-accent)', style: { width: pct + '%' } })
    })
  ]})
}

function LedgerPage({ ctx }) {
  const qc = useQueryClient()
  const [month, setMonth] = useState(thisMonth())
  const [amount, setAmount] = useState('')
  const [kind, setKind] = useState('expense')
  const [category, setCategory] = useState('')
  const [note, setNote] = useState('')
  const { data, isLoading, error } = useQuery({
    queryKey: [ID, 'summary', month],
    queryFn: () => ctx.rest('/summary?month=' + encodeURIComponent(month)),
    refetchInterval: 20000
  })
  const invalidate = () => qc.invalidateQueries({ queryKey: [ID, 'summary'] })

  const add = async () => {
    try {
      await ctx.rest('/entries', { method: 'POST', body: { amount: Number(amount), kind, category, note } })
      setAmount(''); setCategory(''); setNote('')
      invalidate()
      host.notify({ kind: 'info', message: 'Entry saved.' })
    } catch (e) {
      host.notifyError(e, 'Could not save the entry. Is the ledger plugin enabled in plugins.enabled?')
    }
  }
  const remove = async (id) => {
    try { await ctx.rest('/entries/' + id, { method: 'DELETE' }); invalidate() } catch (e) { host.notifyError(e, 'Could not delete.') }
  }

  const cats = (data && data.by_category) || []
  const max = cats.reduce((m, c) => Math.max(m, c.total), 0)

  return jsxs('div', { className: 'flex h-full flex-col gap-3 p-4 text-sm', children: [
    jsxs('div', { className: 'flex items-center justify-between', children: [
      jsx('div', { className: 'text-base font-medium', children: 'Ledger' }),
      jsx(Input, { value: month, className: 'w-28', onChange: (e) => setMonth(e.target.value), placeholder: 'YYYY-MM' })
    ]}),
    error ? jsx('div', { className: 'text-(--ui-text-tertiary)', children: 'Backend not reachable: ' + String(error.message || error) + '. Enable the ledger plugin and restart the gateway.' }) : null,
    data ? jsxs('div', { className: 'grid grid-cols-3 gap-2', children: [
      jsxs('div', { className: 'rounded border border-(--ui-stroke-secondary) p-2', children: [ jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-tertiary)', children: 'Income' }), jsx('div', { className: 'font-medium', children: money(data.income) }) ]}),
      jsxs('div', { className: 'rounded border border-(--ui-stroke-secondary) p-2', children: [ jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-tertiary)', children: 'Expenses' }), jsx('div', { className: 'font-medium', children: money(data.expenses) }) ]}),
      jsxs('div', { className: 'rounded border border-(--ui-stroke-secondary) p-2', children: [ jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-tertiary)', children: 'Net' }), jsx('div', { className: 'font-medium', children: money(data.net) }) ]})
    ]}) : (isLoading ? jsx('div', { className: 'text-(--ui-text-tertiary)', children: 'Loading' }) : null),
    jsxs('div', { className: 'grid gap-2 rounded border border-(--ui-stroke-secondary) p-2', children: [
      jsxs('div', { className: 'grid grid-cols-4 gap-2', children: [
        jsx(Input, { value: amount, placeholder: 'Amount', onChange: (e) => setAmount(e.target.value) }),
        jsx('select', { value: kind, className: 'rounded border border-(--ui-stroke-secondary) bg-transparent px-2', onChange: (e) => setKind(e.target.value), children: [
          jsx('option', { value: 'expense', children: 'expense' }),
          jsx('option', { value: 'income', children: 'income' })
        ]}),
        jsx(Input, { value: category, placeholder: 'Category', onChange: (e) => setCategory(e.target.value) }),
        jsx(Input, { value: note, placeholder: 'Note', onChange: (e) => setNote(e.target.value) })
      ]}),
      jsx('div', { children: jsx(Button, { size: 'sm', onClick: add, children: 'Add entry' }) })
    ]}),
    jsx(ScrollArea, { className: 'min-h-0 flex-1', children: jsxs('div', { className: 'flex flex-col gap-3 pr-2', children: [
      cats.length ? jsx('div', { className: 'flex flex-col gap-2', children: cats.map(c => jsx(Bar, { key: c.category, label: c.category, value: c.total, max, count: c.count })) })
                  : (data ? jsx(EmptyState, { title: 'No expenses this month', description: 'Add one above, or tell Hermes what you spent.' }) : null),
      data && data.recent && data.recent.length ? jsx('div', { className: 'flex flex-col gap-1', children: data.recent.map(r => jsxs('div', { key: r.id, className: 'flex items-center justify-between gap-2 text-[0.75rem]', children: [
        jsx('span', { className: 'text-(--ui-text-tertiary)', children: r.date }),
        jsx('span', { className: 'flex-1', children: r.category + (r.note ? ', ' + r.note : '') }),
        jsx('span', { className: r.kind === 'income' ? '' : 'text-(--ui-text-secondary)', children: (r.kind === 'income' ? '+' : '-') + money(r.amount) }),
        jsx(Button, { size: 'sm', variant: 'ghost', onClick: () => remove(r.id), children: 'x' })
      ]})) }) : null
    ]}) })
  ]})
}

export default {
  id: 'ledger',
  name: 'Ledger',
  defaultEnabled: false,
  register(ctx) {
    ctx.registerMany([
      { id: 'page', area: ROUTES_AREA, data: { path: ROUTE }, render: () => jsx(LedgerPage, { ctx }) },
      { id: 'nav', area: SIDEBAR_NAV_AREA, data: { path: ROUTE, label: 'Ledger', codicon: 'graph' } },
      { id: 'open', area: PALETTE_AREA, data: { id: 'ledger.open', label: 'Open Ledger', keywords: ['ledger', 'money', 'budget'], run: () => host.navigate(ROUTE) } }
    ])
  }
}
```

### Commands

*`ledger-install.sh`*

```bash
# 1. Put the folder in place (or clone it from the masterclass repo's kits/)
cp -R kits/agent-plugins/ledger ~/.hermes/plugins/ledger     # from a clone of the masterclass repo
/bin/ls ~/.hermes/plugins/ledger ~/.hermes/plugins/ledger/dashboard ~/.hermes/plugins/ledger/desktop

# 2. Prove the agent half before enabling it
hermes plugins doctor ~/.hermes/plugins/ledger --ci

# 3. Enable the Python half (this is the security gate for the backend routes too)
hermes plugins enable ledger
hermes plugins list | grep ledger

# 4. Restart the gateway so the routes mount, then make the app copy the desktop half and switch it on
hermes gateway restart
# In the app: Capabilities, Plugins, Rescan. That copies desktop/plugin.js to ~/.hermes/desktop-plugins/ledger/
# beside a .hermes-package.json marker (hermes plugins update does the same). Then: Ledger, Desktop switch on.
/bin/ls ~/.hermes/desktop-plugins/ledger/     # plugin.js and .hermes-package.json must both be there

# 5. Talk to it
hermes chat -q "I paid 42.50 for groceries today, record it in the ledger"
hermes chat -q "How much did I spend this month and on what?"
```

> ⚠️ **If the page says the backend is not reachable**
>
> Four causes, in order: the desktop half was never copied because nothing triggered a Rescan (check for `~/.hermes/desktop-plugins/ledger/.hermes-package.json`), the plugin is not in `plugins.enabled` (the desktop switch alone never imports Python, by design), the gateway was not restarted after enabling (routes mount at startup), or the route failed to import. The last one leaves a line in `~/.hermes/logs/errors.log` reading `Failed to load plugin ledger API routes`.

### Prompts

*`prompt-d7-install-and-prove.md`*

```markdown
Install the ledger plugin from the masterclass kit. Do these in order and
show me the output of each step:
1. Read https://hermes-agent.nousresearch.com/docs/developer-guide/plugins
   section "Store durable state" and tell me where the ledger's database
   will live on this machine.
2. Copy the kit folder to ~/.hermes/plugins/ledger and run
   hermes plugins doctor ~/.hermes/plugins/ledger --ci.
3. Show me the diff hermes plugins enable ledger would make to my
   config.yaml, then run it after I say go, then restart the gateway.
4. Record one expense and one income with the ledger tools, run
   ledger_report for this month, and show me the JSON.
5. Tell me exactly where to click in the app to switch the desktop half on.
```

*`prompt-d7-categorize-with-the-model.md`*

```markdown
Extend the ledger plugin's Python half with one auxiliary task: when
ledger_add is called without a category, classify the note into one of my
categories with ctx.llm. Read
https://hermes-agent.nousresearch.com/docs/developer-guide/plugin-llm-access
first and register the task with ctx.register_auxiliary_task("ledger_classifier")
so I can pin it to a cheap model under auxiliary.ledger_classifier in
config.yaml. Keep the handler contract: JSON string back, never raise, the
classification failing must fall back to the category "uncategorized".
Show me the diff, then run the doctor.
```

### Verify

- [ ] hermes plugins doctor ~/.hermes/plugins/ledger --ci prints OK and registrations: 2 tool(s)
- [ ] After enable and restart, hermes plugins list shows ledger enabled and the banner lists ledger_add, ledger_report
- [ ] /ledger in any chat prints the month summary without a model call
- [ ] The Ledger page shows the entry the agent recorded, and an entry added on the page shows up in ledger_report
- [ ] ~/.hermes/plugin-data/ledger/data.db exists and the plugin folder holds no database

## Build 8: Plugin Workshop IV, let Hermes build the next one

![Build 8](../assets/art/part-11.webp)

### What you are building

The habit that turns Hermes Desktop into your own toolbox: you describe a pane, Hermes writes it against the documented contract, validates it, and you switch it on. The worked example is the Fleet Board, a pane that lists every profile on the gateway with its last activity, built from a documented gateway call and nothing else. Then the shape of a sharing link, so the plugins you make can be installed by anyone with one click.

### What the docs say

Checked against the Desktop Plugin SDK page (Host API, the agents section, distributing with an install link) and the Plugins page.

| Fact | Detail |
|---|---|
| The agent's own checklist | When an agent writes a desktop plugin it should load the bundled `hermes-desktop-plugins` skill, which carries the contract in agent-facing form and a ready `templates/plugin.js` |
| The gateway door | `host.request(method, params)` is the same JSON-RPC the app uses. `profiles.list` returns every profile with its most recent conversation as `last_session`; `profiles.create` creates one with `name`, `description`, `clone_from`, `soul` and a model pin |
| Data layer | `useQuery` from the SDK shares the app's query client: cache, dedupe, `refetchInterval`. Do not poll faster than a few seconds |
| Install links | `<a href="hermes://plugin/install?repo=owner/repo&enable=1">` opens a confirmation dialog that lists what the repo ships; deep links never auto-install |
| Where to look | Capabilities, Plugins, Installed shows one row per plugin with Desktop and Agent switches; Browse is the public catalog; Install from Git takes any repo and can pin a commit |

### The file

*`~/.hermes/desktop-plugins/fleet-board/plugin.js`*

```javascript
// Fleet Board, a Hermes Desktop plugin: every profile (every Bot) at a glance, with its last activity.
// Reads the gateway through host.request('profiles.list'), the same RPC the app uses. No backend needed.
import {
  queryClient,
  host, useValue, useQuery, relativeTime, Button, ScrollArea, EmptyState, StatusDot,
  PANES_AREA, PALETTE_AREA, STATUSBAR_AREAS
} from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'

const ID = 'fleet-board'

function useFleet() {
  return useQuery({
    queryKey: [ID, 'profiles'],
    queryFn: () => host.request('profiles.list', { include_sessions: true }),
    refetchInterval: 30000
  })
}

function rowsOf(data) {
  const list = Array.isArray(data) ? data : (data && Array.isArray(data.profiles) ? data.profiles : [])
  return list.map(p => {
    const name = p.name || p.profile || String(p)
    const last = p.last_session || null
    const when = last && (last.updated_at || last.last_active || last.created_at) || null
    return { name, title: p.title || p.description || '', when, model: p.model || '' }
  })
}

function FleetPane() {
  const { data, isLoading, error, refetch } = useFleet()
  const busy = useValue(host.state.busy)
  const rows = rowsOf(data)
  return jsxs('div', {
    className: 'flex h-full flex-col gap-2 p-3 text-sm',
    children: [
      jsxs('div', { className: 'flex items-center justify-between', children: [
        jsx('div', { className: 'font-medium', children: 'Fleet' }),
        jsx(Button, { size: 'sm', variant: 'ghost', onClick: () => refetch(), children: 'Refresh' })
      ]}),
      error ? jsx('div', { className: 'text-(--ui-text-tertiary)', children: 'Could not read profiles: ' + String(error.message || error) }) : null,
      isLoading ? jsx('div', { className: 'text-(--ui-text-tertiary)', children: 'Loading the roster' }) : null,
      jsx(ScrollArea, { className: 'min-h-0 flex-1', children:
        rows.length
          ? jsx('div', { className: 'flex flex-col gap-1', children: rows.map(r => jsxs('button', {
              type: 'button',
              key: r.name,
              className: 'flex items-center justify-between gap-2 rounded px-2 py-1 text-left hover:bg-(--ui-accent)/10',
              onClick: () => host.newChat(r.name),
              children: [
                jsxs('div', { className: 'flex items-center gap-2', children: [
                  jsx(StatusDot, { status: r.when ? 'ok' : 'idle' }),
                  jsxs('div', { children: [
                    jsx('div', { children: r.name }),
                    r.title ? jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-tertiary)', children: r.title }) : null
                  ]})
                ]}),
                jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-quaternary)', children: r.when ? relativeTime(r.when) : 'no sessions yet' })
              ]
            })) })
          : (!isLoading && !error ? jsx(EmptyState, { title: 'No profiles', description: 'Create a Bot in the Bots tab and it appears here.' }) : null)
      }),
      jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-quaternary)', children: busy ? 'focused chat is working' : 'idle' })
    ]
  })
}

function FleetChip() {
  const { data } = useFleet()
  const n = rowsOf(data).length
  return jsx('button', {
    type: 'button',
    className: 'px-1.5 text-[0.6875rem] text-(--ui-text-tertiary)',
    onClick: () => host.notify({ kind: 'info', message: String(n) + ' profiles on this gateway. The Fleet pane lists them.' }),
    children: 'fleet ' + String(n)
  })
}

export default {
  id: 'fleet-board',
  name: 'Fleet Board',
  defaultEnabled: false,
  register(ctx) {
    ctx.registerMany([
      { id: 'pane', area: PANES_AREA, title: 'Fleet', data: { placement: 'right', width: '300px' }, render: () => jsx(FleetPane, {}) },
      { id: 'chip', area: STATUSBAR_AREAS.right, order: 128, render: () => jsx(FleetChip, {}) },
      { id: 'open', area: PALETTE_AREA, data: { id: 'fleet-board.open', label: 'Fleet Board: refresh roster', keywords: ['fleet', 'bots', 'profiles'], run: () => { queryClient.invalidateQueries({ queryKey: ['fleet-board', 'profiles'] }); host.notify({ kind: 'info', message: 'Fleet roster refreshed.' }) } } }
    ])
  }
}
```

### Prompts

The first prompt is the one you will reuse for every plugin after this. It names the skill, the contract, the validation and the proof, and leaves the idea to you.

*`prompt-d8-build-me-a-plugin.md`*

```markdown
Build me a Hermes Desktop plugin. Do these in order.

1. Load the bundled hermes-desktop-plugins skill and read its template.
2. The plugin: <one sentence: what it shows or does, and where it lives:
   a right pane, a full page, or a status bar chip>. Its id is <id>.
3. Write ~/.hermes/desktop-plugins/<id>/plugin.js obeying the format:
   only @hermes/plugin-sdk, react and react/jsx-runtime imports; jsx()
   calls, no JSX syntax; theme variables only, no literal colors; folder
   name equal to id; defaultEnabled false; every identifier you use is in
   the import line; atoms read with .get() in handlers and useValue only
   in the component that renders them; no polling faster than ten seconds.
4. For data use host.request with a method that is documented on the
   Desktop Plugin SDK page or the web dashboard page; if the data needs a
   backend, stop and propose a unified package instead.
5. Show me the file before writing it. After I say go, write it, tell me
   the palette command to reload plugins, and watch hermes logs gui for
   fifteen seconds. Report the load line or the exact error.
```

*`prompt-d8-share-it.md`*

```markdown
Prepare the <id> plugin for sharing. Create a git repository containing
only the plugin folder and a README that explains what it does, what it
reads, and how to install it: an "Install in Hermes" link of the form
hermes://plugin/install?repo=<owner>/<repo>&enable=1 plus the manual copy
path. Confirm from
https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
what the install dialog will show for a desktop-only repo. Do not push;
show me the repository contents and the README first.
```

> 📝 **From the field: the two-minute plugin**
>
> In part 3 of his desktop masterclass Tonbi builds a plugin live from a single dictated prompt: a status-bar item that opens a popover with the latest AI news from a few RSS feeds and an update button. His verbatim ask, lightly cleaned: "make a Hermes desktop app plugin using the plugin SDK. I want to fetch the latest AI news from free RSS feeds. I want an update button that will update the news. It should have a popover style with the title on the status bar. I can click and then see three to four news items and the update button." It came back in a couple of minutes, missing the update button, which took seconds to fix. His own caveat is the useful part: "usually won't one shot these. You need to edit it a little bit." Write the spec anyway; the edit is smaller when the spec was bigger.

### Ideas that are one prompt away

| Pane | Reads | Why it earns its place |
|---|---|---|
| Cost today | `host.state.focusedUsage` and `hermes insights` through a Python half | The number you want in the corner of your eye, not in a report |
| Cron board | the cron JSON-RPC the Scheduled Jobs page uses | Every routine, its last run and next run, without leaving the chat |
| Kanban lane | the kanban RPC the Kanban page uses | Your three active cards beside the conversation that feeds them |
| Health log | a Python half with plugin_db | Sleep, training, supplements: a form and a week view, and the agent can write to it too |
| Reading list | `ctx.storage` and `ctx.os.openExternal` | Links you save from chats, one click to open, one to send to a Bot |

### Verify

- [ ] Fleet Board lists every profile hermes profile list knows about, with a last-activity time where one exists
- [ ] Clicking a row opens a new chat in that profile
- [ ] The build prompt produced a plugin that validated and loaded without an error toast
- [ ] Your README's install link opens the app's confirmation dialog rather than installing silently

## Build 9: Care and Feeding

![Build 9](../assets/art/part-12.webp)

### What you are building

The maintenance you understand before you need it: how updates work across the app and its backends, what to do when permissions or credentials get asked for again, where every log lives, how to recover a stuck backend, and the three levels of uninstall.

### What the docs say

Checked against the Desktop page: Updating, Uninstalling, Troubleshooting, macOS permissions and local rebuilds.

| Fact | Detail |
|---|---|
| Updates | The app checks in the background and offers a one-click update. With several gateways registered, Update now updates the connected backend first, then every other eligible gateway, then the app itself last. After a backend update the app re-checks its own version |
| Rate limits on the check | Anonymous GitHub requests are capped per network address; the check uses `GITHUB_TOKEN`, then `GH_TOKEN`, then the GitHub CLI's login, then anonymous |
| Update logs | Detailed build output streams to the profile's `logs/update.log` |
| Permissions after updates | Grants follow the signing identity; `hermes desktop --setup-tcc-identity` anchors it, re-run after updates. A stuck grant: `tccutil reset All com.nousresearch.hermes`, re-grant, fully relaunch |
| Reconnect | If a chat stops responding while Connected, the status bar's gateway menu has Reconnect gateway, which redials without restarting the app |
| Backend crashed | The app restarts a local backend that exits and shows a notice; `~/.hermes/logs/desktop.log` records the exit code and the last output lines |
| Failed turns | The error card names the failing layer (provider, endpoint, streaming, auth, billing, gateway, runtime, disk) and offers Retry, Switch provider, Open logs, Send diagnostics (redacted, consented) and Copy error details |
| Resets | Force a clean first launch by removing `~/.hermes/hermes-agent/.hermes-bootstrap-complete`; rebuild a broken venv by removing `~/.hermes/hermes-agent/venv`; reset a stuck microphone prompt with `tccutil reset Microphone com.nousresearch.hermes` |
| SSH host key changed | The app fails closed; `ssh-keygen -R <host>` then Retry |
| Uninstall | Settings, About, Danger zone: app only (`hermes uninstall --gui`), app and agent keeping data (`hermes uninstall`), or everything (`hermes uninstall --full`) |

### Commands

*`care.sh`*

```bash
hermes update --check                       # preview
hermes backup --quick --label "pre-update"  # snapshot the home first
hermes update --backup                      # then update
hermes desktop --setup-tcc-identity         # re-anchor the signing identity after the update
hermes logs gui -f                          # the app's boot log
hermes doctor                               # health, including Full Disk Access
```

### Prompts

*`prompt-d9-before-i-update.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/user-guide/desktop section
"Updating" and https://hermes-agent.nousresearch.com/docs/getting-started/updating
then tell me, before I press Update:

1. What hermes update --check says is waiting.
2. Whether I have more than one gateway registered and therefore what will
   be updated in which order.
3. Take hermes backup --quick --label pre-update and show me the path.
4. Whether any local source edits exist in ~/.hermes/hermes-agent that an
   update would stash (git status there).

Then stop. I will press Update myself and ask you to verify afterwards.
```

*`prompt-d9-after-the-update.md`*

```markdown
The update finished. Verify it: hermes --version, hermes doctor, the last
thirty lines of ~/.hermes/logs/desktop.log summarized, hermes plugins list
compared with the list from before the update, and whether Full Disk
Access still reads as granted. If anything regressed, quote the exact line
and name the documented fix from the Desktop page's Troubleshooting
section. Do not apply a fix until I say so.
```

### Verify

- [ ] You know the path of a backup taken before your last update
- [ ] After an update the app reports its own version matches the backend, and no permission prompt reappears
- [ ] You can find desktop.log and update.log without searching
- [ ] You know which of the three uninstall levels you would pick, and that two of them keep your data

## The Desktop Ledger

Ten builds, one line each, with the proof.

| Build | Proof |
|---|---|
| 0 Install | hermes doctor clean with Full Disk Access granted; a message sent in the app appears in the CLI's session list |
| 1 The window | A Last turn diff in the review pane showed exactly one intended change |
| 2 Settings | hermes config show reads back your default model and cheaper auxiliary models |
| 3 Capabilities | security-guidance and disk-cleanup enabled for your profile |
| 4 Gateways | Test reports Reachable for a remote gateway, and its sessions live on that machine |
| 5 Hello Hermes | The pane, the chip, the palette command and the keybind all work after a hot reload |
| 6 Prompt Library | A saved prompt survives a restart; Copy and New chat both work |
| 7 Ledger | The doctor passes, /ledger prints a summary, and the page shows what the agent recorded |
| 8 Fleet Board | Every profile listed with its last activity; your own prompt produced a plugin that loaded |
| 9 Care | A pre-update backup exists and the post-update check came back clean |

> ✅ **What you have now**
>
> The app is no longer a nicer chat window. It is your own workbench: a page for your prompts, your money in a plugin you can read the source of, a board of your agents, and a habit of asking Hermes to build the next tool against a documented contract. Volume 3 turns the profiles you see in the Fleet Board into a team.
