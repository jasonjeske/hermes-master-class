## Build 8: Bots Across Machines

![One roster across three machines](assets/art/v3-team-across-machines.webp)

### What you are building

The team spread over the machines you already own: the planner and the writer on your laptop, the engineer and the operator on an always-on Mac mini, the researcher and the reviewer on a VPS, all in one roster, messaging each other, sitting in the same rooms.

### What the docs say

Checked against the Bot Mode page (Bots across machines, Messaging across connected machines, Bot-initiated DMs across machines, One-way reachability) and the multi-connection guide.

```table
| Fact | Detail |
| The union roster | Register several backends in Settings, Gateways and the Bots pane shows the Bots from every connected source, persistently. Unreachable machines keep their last-known rows |
| Handles | The same profile name on several sources disambiguates as `@name-device`, for example `@research-homelab` |
| Where a bot lives | Its chats, sessions, memory and routines live on the machine that owns the profile. Clicking a Connections Bot does not hop your window; @mention it, seat it in a room, or create new agents on it with the Create on picker |
| Create on | With more than one connection registered, New Agent grows a Create on picker; the profile is created on that machine's backend, cloning from that machine's `default` |
| The Desktop relay | Rosters propagate on their own while the Desktop runs; `message_agent` reaches bots on other connections, disambiguated as `target="moxie@<connection>"`; delivery rides the Desktop, which holds the sockets and credentials. Close the Desktop mid-delivery and the sender is told the reply did not arrive |
| Without a Desktop | Register the other gateway as a peer: `hermes peer add <name> --url http://host:8377 --key <API_SERVER_KEY>`; then `hermes peer dm <name>/<profile> < msg.txt` for short exchanges and `hermes peer run` with `--idempotency-key` for long ones. Once a peer is registered, every Bot Chat's protocol includes the peer roster and `message_agent` accepts `target="<peer>/<profile>"` |
| The peer's key | The peer machine runs the `api_server` gateway platform with a strong `API_SERVER_KEY`; the key lives in `~/.hermes/.env` as `HERMES_PEER_<NAME>_KEY`; peer names and URLs live in config.yaml under `bot_peers` |
| NAT | Cross-gateway links are direct. A gateway behind home NAT can dial out to a public peer; the reverse fails unless the network provides a route. Put a room's authority on the host every participant can reach, or bridge with Tailscale |
| Rooms across machines | Members on other connections are seated with a device badge and a device-qualified handle; each member's turns run on its own machine |
```

### Commands

```code lang=bash file=peers.sh
# On the laptop: reach the mini's bots without the Desktop in the loop
hermes peer add mini --url http://<mini-tailscale-ip>:8377 --key <the mini's API_SERVER_KEY>
hermes peer list
echo "Introduce yourself in two lines and list your toolsets." > /tmp/dm.txt
hermes peer dm mini/forge < /tmp/dm.txt

# A long job on the mini, idempotent, polled
hermes peer run mini --idempotency-key nightly-2026-09-19 "$(cat /tmp/long-task.txt)"
hermes peer status mini <run_id>
```

### Prompts

```code lang=markdown file=prompt-b8-place-the-team.md
Read https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode sections
"Bots across machines", "Messaging across connected machines", "Bot-initiated
DMs across machines" and the NAT note. I have these machines: <list, with
which are always on and how they reach each other>. For my roster, propose
where each bot lives and why (always-on for routines and long jobs, the
laptop for what I talk to most), which handles will need a device suffix,
whether I need hermes peer for machine-to-machine messaging when the
Desktop is closed, and where a room's authority should sit given my NAT.
Then give me the hermes peer add command for each pair that needs one.
Do not run anything.
```

### Verify

```checklist
[ ] The Bots pane lists bots from every registered gateway, with @name-device handles where names collide
[ ] A message from a laptop bot to a mini bot arrives with the Desktop open, and hermes peer dm works with it closed
[ ] A room with members on two machines settles and shows device badges
[ ] You know which machine holds authority for each cross-machine room
```

## Build 9: Ship the Team, Grow It, Shrink It

![Build 9](assets/art/part-12.webp)

### What you are building

The roster as something you can hand to another machine, another person or your future self: each bot as a profile distribution, the export file for the quick case, and the prompts that add a bot for a new kind of work or retire one that stopped earning its place.

### What the docs say

Checked against the Profile Distributions page, the Profile Commands reference and the Bot Mode page.

```table
| Fact | Detail |
| Two ways to share | A distribution is a git repo installed with `hermes profile install <repo> --alias` and updated with `hermes profile update`; an export file is a `.tar.gz` from `/export` or `hermes profile export`, imported with `/import` or `hermes profile import`. The export also carries the desktop theme and layout |
| The manifest | `distribution.yaml` with `name` (required), `version`, `description`, `hermes_requires`, `author`, `license`, and `env_requires` entries (`name`, `description`, `required`, `default`) |
| What ships | `SOUL.md`, `config.yaml`, `mcp.json`, `skills/`, `cron/`, `distribution.yaml`. Never memories, sessions, `state.db`, `auth.json`, `.env`, logs, workspace |
| On update | Distribution-owned files are replaced; `config.yaml` is preserved unless `--force-config`; user data is never touched. Override the owned list with `distribution_owned` in the manifest |
| Install | Clones, shows the manifest, checks each required env var against your shell and the profile's `.env`, asks, copies, writes `.env.EXAMPLE`, and with `--alias` gives you a `<name>` command. `--name` installs under a different local name. A local directory path works during development |
| Inspect | `hermes profile info <name>`; `hermes profile list` shows a Distribution column |
| More bots | Duplicate in the roster clones config, skills, SOUL, memory and look; `hermes profile create --clone-from <bot>` is the CLI twin |
| Fewer bots | Hide Bot keeps it working but out of the roster; Delete Profile removes it behind a confirmation that names its distribution; the default profile cannot be deleted |
```

### The kit as distributions

Each folder under `kits/bot-team/` is already a distribution: `distribution.yaml`, `SOUL.md`, `config.yaml` (model pin, effort, and for atlas the disabled toolsets), a README, and `routines.sh` beside them rather than inside `cron/`, because Hermes owns `cron/` for job state. Install a bot from a local clone, or push a folder to a repo of your own and install from there.

```code lang=yaml file=kits/bot-team/atlas/distribution.yaml
name: atlas
version: 1.0.0
description: "Chief of staff for a Hermes bot team. Plans work, decides shared choices once, routes cards and messages to the right teammate, escalates real decisions to the human. Never implements."
hermes_requires: ">=0.21.0"
author: "Hermes Agent Masterclass, Volume 3"
license: "CC-BY-4.0"
env_requires: []
```

```code lang=bash file=install-the-team.sh
git clone https://github.com/jasonjeske/hermes-master-class.git
cd hermes-master-class/kits/bot-team

# The day-one three
hermes profile install ./atlas --alias
hermes profile install ./forge --alias
hermes profile install ./ops --alias

# Later
hermes profile install ./scout --alias
hermes profile install ./quill --alias
hermes profile install ./sentinel --alias

# Each bot's model pin is a placeholder in config.yaml; set yours
hermes -p atlas config set model.default "<frontier model>"
hermes -p forge config set model.default "<inexpensive coding model>"
hermes -p ops   config set model.default "<inexpensive model>"

# Routines: each file scopes its jobs to its owner with -p
sh ./ops/routines.sh
sh ./atlas/routines.sh
sh ./scout/routines.sh

hermes profile list          # the Distribution column shows atlas@1.0.0 and friends
```

```callout kind=warn title="What install does not do"
It does not sign a bot into an OAuth provider (each profile does that itself), it does not tick toolsets in the app (Edit Profile does), and it does not create the routines (the shell scripts do, so you read them first). That is deliberate: credentials, capabilities and schedules are the three things you should never inherit blindly.
```

### Prompts

```code lang=markdown file=prompt-b9-add-a-bot.md
Add a bot to my roster. Read
https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode section
"Creating a Bot" and https://hermes-agent.nousresearch.com/docs/user-guide/profiles
section "Creating a profile". The new kind of work: <what keeps landing on
the wrong bot>. Propose: a one-word name that does not collide with any
existing tag, a title, a description written as what it is good at, which
existing bot to clone from and why, the model from the decision table in
Build 2, the toolsets, and a SOUL.md in the kit's shape. Show me all of it,
then after I say go create it with hermes profile create, write the SOUL,
and message it from @atlas asking it to introduce itself.
```

```code lang=markdown file=prompt-b9-bot-hr.md
You are Bot HR. Your only job is to read a project brief and create the bots
it needs. Read <the brief> and:

1. Split the work into at most five roles that will recur across the
   project, not tasks. Say why each role exists.
2. For each role: name (one lowercase word, no collisions with my roster),
   title, description as what it is good at, model from my configured
   providers with a one-line reason, toolsets, and a forty-line SOUL.md in
   the shape Role, How you work, Voice, What you never do.
3. Name the shared working directory every role uses and the shared
   decisions (names, formats, interfaces) you are stamping into every SOUL
   so the bots never negotiate them twice.
4. Show me everything. After I say go, create the profiles with
   hermes profile create --description, write the SOULs, and message each
   new bot from @atlas asking it to introduce itself and name its
   teammates.
```

```code lang=markdown file=prompt-b9-retire-a-bot.md
You are @ops, the one bot with a shell for this. Audit my roster for bots that stopped earning their place. For each bot:
messages sent and received in the last thirty days (session_search), cards
completed (hermes kanban list --assignee), routines and their last status
(hermes cron list), and its model cost from hermes insights. Recommend one
of keep, merge into <other bot>, hide, or delete, with a reason. For any
delete, remind me what Delete Profile removes and that an export file
first would let me bring it back. Change nothing.
```

### Verify

```checklist
[ ] hermes profile list shows the kit bots with a Distribution version
[ ] hermes profile info atlas shows the manifest you installed
[ ] A new bot created by the add-a-bot prompt introduced itself to the roster from @atlas
[ ] An export of one bot imports on another machine with its SOUL, skills and look intact
```

## The Bots Ledger

```table
| Build | Proof |
| 0 What a bot is | You can explain the two markers and why /new becomes /compact |
| 1 The roster | At most five roles, all from repeated work, one planner without a terminal |
| 2 Models | Every bot has a model.default and effort you chose; OAuth bots signed in themselves |
| 3 Birth | Three bots introduced themselves in their own words with the right teammates |
| 4 Routines | hermes cron list shows [bot:…] jobs and hermes cron doctor is clean |
| 5 Messaging | Every pair that should talk completed a handshake with a reply |
| 6 Rooms | A planning room settled on a numbered plan; a review room ended in a verdict |
| 7 Shared memory and board | Two bots recalled the same fact from the shared bank; a card moved from ready to done by a worker |
| 8 Across machines | A message crossed machines with the Desktop open and with hermes peer closed |
| 9 Ship | hermes profile list shows the team with distribution versions; one bot was added by prompt |
```

```callout kind=success title="What you have now"
A team that is folders on disk. You can read every rule it runs by, version it, install it on a second machine in a minute, and change it with a prompt. Volume 4 puts this team to work on a company.
```
