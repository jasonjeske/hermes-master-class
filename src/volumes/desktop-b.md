## Build 3: Capabilities in the App

![Build 3](assets/art/part-04.webp)

### What you are building

The management surface used from the app instead of the terminal: skills and plugins with an Installed view and a Browse view of the public catalogs, tools and MCP servers per agent, messaging setup with a QR code, and the two bundled safety plugins switched on for every profile you run.

### What the docs say

Checked against the Desktop page (Management panes, Where Browse gets its data, Extending the desktop app) and the Plugins and Plugin Catalog pages.

```table
| Fact | Detail |
| Skills | Capabilities, Skills. Installed shows the selected profile's real skills and enable state; Browse searches the same published catalog as the public Skills Hub |
| Plugins | Capabilities, Plugins, same layout. Installed shows one row per plugin with a Desktop switch and an Agent switch; a plugin that ships both halves is one row. Browse shows the public Plugin Catalog. Install from Git takes any repo and can pin a commit |
| Where Browse reads | Native views over the same CDN snapshots the website uses (`/docs/api/skills.json`, `/docs/api/plugins.json`); no live GitHub calls |
| Install links | Hub pages carry `hermes://skill/install` and `hermes://plugin/install` links; the app always shows a review dialog before installing |
| The two switches | Desktop is app-level, one value everywhere. Agent is per profile, with the profile selector in that column's header |
| Tools and MCP | The Capabilities page has a Configuring selector that lists every agent on every connected machine; picking one edits that machine's toolsets and MCP servers |
| Messaging | The Messaging pane sets up gateway channels; Telegram has a Quick setup card that creates the bot from a QR code, detects your user id, saves credentials and restarts the gateway |
| Cron, Profiles, Agents, Command Center | Scheduled jobs, profile switching, and the orchestration surfaces, all reachable from the sidebar |
```

```callout kind=note title="From the field: where plugins moved"
Tonbi's part 3 flags a change that trips people following older videos: plugins used to live in Settings and now live under Capabilities beside Skills, Tools and MCP, with the desktop switch app-wide and the profile selector living only in the agent column's header. He also names the plugins he wrote for himself, a trading pane, a weather pane, a slide presenter, a YouTube planner, which is the best argument for Builds 5 to 8: the app becomes whatever panes you need.
```

### Commands

```code lang=bash file=capabilities.sh
# The terminal twins of what Build 3 does in the app
hermes plugins list                      # every plugin and its state
hermes plugins enable security-guidance  # pattern-matches dangerous writes and warns or blocks
hermes plugins enable disk-cleanup       # tracks temp and test files the agent creates and cleans them
hermes skills list
hermes skills browse
```

```callout kind=note title="From the field: the board decides who works"
The Kanban board is a bundled desktop plugin and, in Tonbi's words, "the flagship plugin of Hermes desktop." His demonstration is the cleanest public example of the decomposer at work: a one-line idea dropped into triage fanned out into research, write and verify cards, each claimed by a different profile he had never assigned, because the Orchestration settings pane knows what each profile is good at from its description. The verifier card waited, blocked, until the writer card finished, then promoted itself to ready. His two tips: the Estimate effort button makes a real model call and tells you the token cost before you commit, and if you do not name a workspace the output lands in the board's attachments directory. Volume 3, Build 7 uses this board as the team's queue.
```

### Prompts

```code lang=markdown file=prompt-d3-capabilities-audit.md
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

```code lang=markdown file=prompt-d3-telegram-from-the-app.md
I am going to set up Telegram from Capabilities, Messaging with the QR
card. Before I do, read
https://hermes-agent.nousresearch.com/docs/user-guide/messaging and tell me
in five lines what the quick setup will write (which keys, which file),
what "allowlist" means for my user id, and what the Restart now banner is
waiting for. After I finish, verify from the terminal that the gateway is
running and the Telegram adapter connected, quoting the log line.
```

### Verify

```checklist
[ ] Capabilities, Plugins, Installed shows security-guidance and disk-cleanup with the Agent switch on for your profile
[ ] Browse loads the catalog with cards, and opening a card shows an Install button, not a website
[ ] The Configuring selector on Capabilities lists every profile you have
[ ] If you set up Telegram, a message from your phone reaches the app and the reply comes back
```

## Build 4: Gateways and Other Machines

![Every gateway you own, in one window](assets/art/v2-gateways-map.webp)

### What you are building

The app on your laptop talking to a Hermes that never sleeps on another machine: a Mac mini in the closet, a VPS, a box behind Tailscale. Then the registry that holds every gateway you own, so one window can reach all of them and update all of them.

### What the docs say

Checked against the Desktop page (Connecting to a remote backend, The multi-connection registry, On the backend, In the app, Troubleshooting) and the Connecting Desktop to Many Hermes Instances guide.

```table
| Fact | Detail |
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
```

```callout kind=note title="From the field: SSH is the two-click path"
Tonbi reached his always-on box through the VS Code Remote SSH extension until the SSH connection kind arrived. His account: update Hermes on both machines, have SSH keys already set up, pick the host in Settings, Gateways, save and reconnect, and "the desktop app handles everything. It handles the whole tunneling and everything else." Remote files, artifacts, images and the remote agent's learned skills all appear in the window. Two prerequisites, two clicks, and no auth gate to configure, which makes SSH the right first connection for a machine you own; the username-and-password path below is for a backend that must accept connections without an SSH login.
```

### Commands

```code lang=bash file=on-the-remote-machine.sh
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

```code lang=bash file=on-the-laptop.sh
# In the app: Settings, Gateways, Remote gateway
#   Remote URL: http://<tailscale-ip>:9119
#   Sign in with the username and password from the backend's .env
#   Save and reconnect
# Or set the URL before launch:
HERMES_DESKTOP_REMOTE_URL=http://<tailscale-ip>:9119 open -a Hermes
```

```callout kind=warn title="Password auth is for your own network"
The backend reads and writes the remote machine's `.env` and runs agent commands. The docs are explicit: never expose a password-protected backend directly to the open internet. Put it behind Tailscale or a VPN, or use the OAuth provider for anything public. The stable secret matters too; without it the signing key is regenerated per boot and you are logged out on every restart.
```

```callout kind=warn title="If you are following an older video"
Tonbi's June 2026 guide runs the remote backend with `hermes dashboard --no-open --host 0.0.0.0 --port 9119`. The current docs run it with `hermes serve`, and his own September masterclass says so. The auth environment variables and the Tailscale advice are unchanged; the command is not.
```

### Prompts

```code lang=markdown file=prompt-d4-prepare-the-mini.md
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

```code lang=markdown file=prompt-d4-registry-check.md
Read https://hermes-agent.nousresearch.com/docs/user-guide/multi-connection-desktop
sections "The gateway registry" and "Agents across gateways". I have
registered a second gateway named <device>. Tell me which of my profile
names now collide across machines and what their @name-device handles will
be, and which gateway is Primary. Then explain in three lines what stays
scoped to the active gateway when I switch, so I know what I will and will
not see.
```

### Verify

```checklist
[ ] curl against /api/status on the backend reports auth_required true and lists the provider
[ ] The app's Test button reports Reachable for the new connection
[ ] Sessions started on the remote gateway show up in hermes sessions list on that machine, not on the laptop
[ ] Update all instances lists both gateways and the app itself
```
