# Build 9: Ship the Team, Grow It, Shrink It

![Build 9](../assets/art/part-12.webp)

### What you are building

The roster as something you can hand to another machine, another person or your future self: each bot as a profile distribution, the export file for the quick case, and the prompts that add a bot for a new kind of work or retire one that stopped earning its place.

### What the docs say

Checked against the Profile Distributions page, the Profile Commands reference and the Bot Mode page.

| Fact | Detail |
|---|---|
| Two ways to share | A distribution is a git repo installed with `hermes profile install <repo> --alias` and updated with `hermes profile update`; an export file is a `.tar.gz` from `/export` or `hermes profile export`, imported with `/import` or `hermes profile import`. The export also carries the desktop theme and layout |
| The manifest | `distribution.yaml` with `name` (required), `version`, `description`, `hermes_requires`, `author`, `license`, and `env_requires` entries (`name`, `description`, `required`, `default`) |
| What ships | `SOUL.md`, `config.yaml`, `mcp.json`, `skills/`, `cron/`, `distribution.yaml`. Never memories, sessions, `state.db`, `auth.json`, `.env`, logs, workspace |
| On update | Distribution-owned files are replaced; `config.yaml` is preserved unless `--force-config`; user data is never touched. Override the owned list with `distribution_owned` in the manifest |
| Install | Clones, shows the manifest, checks each required env var against your shell and the profile's `.env`, asks, copies, writes `.env.EXAMPLE`, and with `--alias` gives you a `<name>` command. `--name` installs under a different local name. A local directory path works during development |
| Inspect | `hermes profile info <name>`; `hermes profile list` shows a Distribution column |
| More bots | Duplicate in the roster clones config, skills, SOUL, memory and look; `hermes profile create --clone-from <bot>` is the CLI twin |
| Fewer bots | Hide Bot keeps it working but out of the roster; Delete Profile removes it behind a confirmation that names its distribution; the default profile cannot be deleted |

### The kit as distributions

Each folder under `kits/bot-team/` is already a distribution: `distribution.yaml`, `SOUL.md`, `config.yaml` (model pin, effort, and for atlas the disabled toolsets), a README, and `routines.sh` beside them rather than inside `cron/`, because Hermes owns `cron/` for job state. Install a bot from a local clone, or push a folder to a repo of your own and install from there.

*`kits/bot-team/atlas/distribution.yaml`*

```yaml
name: atlas
version: 1.0.0
description: "Chief of staff for a Hermes bot team. Plans work, decides shared choices once, routes cards and messages to the right teammate, escalates real decisions to the human. Never implements."
hermes_requires: ">=0.21.0"
author: "Hermes Agent Masterclass, Volume 3"
license: "CC-BY-4.0"
env_requires: []
```

*`install-the-team.sh`*

```bash
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

> ⚠️ **What install does not do**
>
> It does not sign a bot into an OAuth provider (each profile does that itself), it does not tick toolsets in the app (Edit Profile does), and it does not create the routines (the shell scripts do, so you read them first). That is deliberate: credentials, capabilities and schedules are the three things you should never inherit blindly.

### Prompts

*`prompt-b9-add-a-bot.md`*

```markdown
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

*`prompt-b9-bot-hr.md`*

```markdown
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

*`prompt-b9-retire-a-bot.md`*

```markdown
You are @ops, the one bot with a shell for this. Audit my roster for bots that stopped earning their place. For each bot:
messages sent and received in the last thirty days (session_search), cards
completed (hermes kanban list --assignee), routines and their last status
(hermes cron list), and its model cost from hermes insights. Recommend one
of keep, merge into <other bot>, hide, or delete, with a reason. For any
delete, remind me what Delete Profile removes and that an export file
first would let me bring it back. Change nothing.
```

### Verify

- [ ] hermes profile list shows the kit bots with a Distribution version
- [ ] hermes profile info atlas shows the manifest you installed
- [ ] A new bot created by the add-a-bot prompt introduced itself to the roster from @atlas
- [ ] An export of one bot imports on another machine with its SOUL, skills and look intact

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-BOTS.md)
