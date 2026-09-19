# The Hermes Bots Masterclass

![The Hermes Bots Masterclass](../assets/art/v3-hero.webp)

## Contents

- [Orientation](#user-content-orientation)
- **[Build 0](#user-content-build-0-what-a-bot-is)** What a Bot Is
- **[Build 1](#user-content-build-1-design-the-roster)** Design the Roster
- **[Build 2](#user-content-build-2-a-model-per-bot)** A Model per Bot
- **[Build 3](#user-content-build-3-the-birth-of-a-bot)** The Birth of a Bot
- **[Build 4](#user-content-build-4-routines)** Routines
- **[Build 5](#user-content-build-5-bots-talking-to-each-other)** Bots Talking to Each Other
- **[Build 6](#user-content-build-6-rooms)** Rooms
- **[Build 7](#user-content-build-7-shared-memory-and-a-shared-board)** Shared Memory and a Shared Board
- **[Build 8](#user-content-build-8-bots-across-machines)** Bots Across Machines
- **[Build 9](#user-content-build-9-ship-the-team-grow-it-shrink-it)** Ship the Team, Grow It, Shrink It
- [The Bots Ledger](#user-content-the-bots-ledger)

---

## Orientation

Bot Mode is the part of Hermes Desktop that turns your profiles into a roster of named Bots, each with its own chat, role, model, memory, skills and avatar. Bots run routines, deliberate in group chats, and message each other directly. It ships built in and on by default. And there is no new primitive underneath it: a Bot is a profile, the same `~/.hermes/profiles/<name>/` you met in Volume 1, so everything you do in the roster is visible from the terminal too.

That last sentence is the whole design of this volume. Because a Bot is a profile, a team is a set of folders, and a set of folders can be written down, versioned, shared and installed. So this volume does not describe a team. It ships one: six bots with every file, the routines they run, the way they talk, and the prompts that add a seventh or retire one. You can build it in the app one dialog at a time, or clone the kit and be done in a minute. Both roads end in the same folders.

> 📝 **What this volume rests on**
>
> Every mechanism was checked against the official Bot Mode page, the Profiles page, the Profile Distributions page, the multi-connection guide and the Kanban page for the version installed while writing, plus the bundled files in the Hermes repository. Two operators who published early and detailed Bot Mode walkthroughs, Tonbi's AI Garage and Wanderloots, are quoted where their field experience adds something the docs do not, and always by name.

| Build | You end up with | Checked against | Time |
|---|---|---|---|
| 0 | The mental model: bot, profile, Bot Chat, routine, room, and the two markers that make it all work | Bot Mode, Profiles | 20 minutes |
| 1 | A roster designed from your real work, named so the tags work, sized so the machine keeps up | Bot Mode | 30 minutes |
| 2 | A model per bot with a reason and a cost, and the credential rule that bites | Profiles, Kanban | 30 minutes |
| 3 | Your first three bots born, from the dialog or the CLI, with SOULs written for their roles | Bot Mode, Personality | 45 minutes |
| 4 | Routines attached to the bots that own them, silent when nothing happened | Bot Mode, Cron | 30 minutes |
| 5 | Bots messaging each other, with the delivery contract understood | Bot Mode | 30 minutes |
| 6 | Group chats that plan, review and escalate without spinning | Bot Mode | 45 minutes |
| 7 | Shared memory and a shared board: Hindsight and Mnemosyne, and kanban as the queue | Memory Providers, Kanban | 60 minutes |
| 8 | Bots across machines: the mini, the VPS, one roster | Bot Mode, Multi-connection | 45 minutes |
| 9 | The team shipped as an installable distribution, and the prompts that grow or shrink it | Profile Distributions | 45 minutes |

### How to use a build

Same shape as the other volumes. **What you are building**, then **What the docs say** with the page named, then **Prompts** to paste into a Hermes chat and **Commands** for the terminal, then a **verify** list. The kit under `kits/bot-team/` holds one folder per bot: `SOUL.md`, `config.yaml`, `distribution.yaml`, `routines.sh` and a README.

## Build 0: What a Bot Is

![Build 0](../assets/art/part-11.webp)

### What you are building

The model in your head that makes every later build obvious: what the roster shows, what a Bot Chat is, why `/new` does not work in it, what a routine and a room are, and the two markers that switch the whole machinery on.

### What the docs say

Checked against the Bot Mode page and the Profiles page.

| Term | What it is |
|---|---|
| Profile | The persistent home for one agent's config, memory, skills, credentials and chat history: `~/.hermes/profiles/<name>/` |
| Bot | A profile presented in the roster with a title, an avatar, a section and a pinned canonical chat. Every Bot is a profile; a profile you only drive from the CLI or a gateway stays a plain profile |
| Bot Chat | The canonical, persistent conversation created the moment a Bot is born. Clicking the row always opens it. Typing `/new` or `/reset` inside it is rerouted to `/compact`, fresh working context in the same conversation, because forking the relationship is the one thing Bot Mode promises never happens |
| Routine | A recurring task attached to the Bot that does it. Under the hood it is a Hermes cron job named `[bot:<name>] <routine>`, so it also appears in `hermes cron list`; runs land in the Bot's own chat history |
| Room | A group chat of 2 to 6 Bots with one visible conversation, up to three serial rounds of member turns per message, and a needs-you badge when a Bot escalates with `@user` |
| Messaging bot | Different thing: an account on Telegram, Discord or Slack connected through the gateway |
| Subagent | Different thing: a child spawned by `delegate_task` with a fresh conversation, same profile |
| Warm backends | One backend process per local Bot. The cap is Settings, Advanced, Warm Bot Backends (default 3, "~60 MB each" in the page's words); idle backends are reaped after the timeout next to it, 10 minutes by default |
| Off switch | Bot Mode is a bundled desktop plugin; Capabilities, Plugins, Bots, Desktop switch. Your profiles, sessions and cron jobs are untouched either way |

**The two markers.** The messaging protocol and the `message_agent` tool are injected only when two conditions hold, and the Bots pane satisfies both the moment it creates a Bot: the session is titled exactly `Bot Chat`, and at least one profile on the install carries a `ui_meta: { hermes-bots: … }` block in its `profile.yaml`. That is why a headless install with no desktop never sees `message_agent`, and Build 5 gives the two lines that switch it on by hand.

| In Bot Mode | From a shell |
|---|---|
| Chat with a Bot | `hermes -p <bot> chat` |
| A Bot's files, skills, memory | `~/.hermes/profiles/<bot>/` |
| Routines | `hermes cron list`, jobs named `[bot:<name>] …` |
| Create or inspect | `hermes profile create`, `hermes profile list` |

> 📝 **From the field: Tonbi's first-day guide**
>
> Tonbi's Bot Mode walkthrough, recorded the day after the feature shipped, says the same thing in one line: "Bots themselves are not necessarily new. They're just profiles. What has changed is how they can work together and communicate with one another." He calls the canonical chat the bot's "agent inbox", a dedicated session for agent-to-agent traffic. The docs call it the Bot Chat; it is the same thing.

### Prompts

*`prompt-b0-show-me-my-roster.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode sections
"The Bots pane", "What actually makes a chat a Bot Chat" and "CLI parity".
Then run hermes profile list and, for each profile, tell me: whether it is a
Bot (does its profile.yaml carry a ui_meta hermes-bots block), whether it has
a session titled exactly "Bot Chat", its model, and how many cron jobs are
named [bot:<name>]. One table. Change nothing.
```

### Verify

- [ ] You can say in one sentence why /new does nothing in a Bot Chat and what it does instead
- [ ] hermes cron list shows any routine you created in the app, named [bot:<name>]
- [ ] hermes profile list matches the roster in the Bots tab
- [ ] Settings, Advanced shows the Warm Bot Backends count and you know what happens when it is exceeded

## Build 1: Design the Roster

![The roster, and who talks to whom](../assets/art/v3-message-paths.webp)

### What you are building

A roster written down before any bot exists: roles drawn from work you actually do every week, names that resolve as tags without colliding, a size the machine can keep warm, and a section layout that will still make sense in a month.

### What the docs say

Checked against the Bot Mode page: Creating a Bot, renamed Bots keep their tags in sync, Organize bots into sections, Warm Bot Backends, and the Kanban page's cost strategy.

| Rule | Why |
|---|---|
| Roles come from repeated work | The docs' own examples are specialists: a researcher, a reviewer, a scribe. A Bot earns its place by owning a kind of work that recurs, because it accumulates memory and skills only for what it does repeatedly |
| Names are tags | A Bot titled Research Buddy answers to `@research-buddy` and `@researchbuddy`; the profile name is matched first and can never be hijacked by a friendly name; a friendly name shared by two Bots is refused. Pick short, distinct, pronounceable names |
| The primary stays `@hermes` | Rename it Maia and prompts introduce it as `@maia`, but `@hermes` keeps working as an alias for the primary |
| Start at the warm limit | Warm Bot Backends defaults to 3. A fourth open Bot waits up to 30 seconds for a slot. Start with three bots doing real work, raise the setting and the machine's memory together when you add more |
| Sections are yours | Folders like Clients or Team, stored in each Bot's profile metadata, so a section follows the Bot to every desktop connected to that backend |
| Planner and workers | The Kanban page's cost strategy applies to rosters: decomposing work needs frontier-level judgment, executing a well-specified card usually does not, and workers are where the tokens go. Restrict the planner's toolsets so it cannot do the implementation work itself |

### The roster this volume ships

| Bot | Title | Owns | Talks to |
|---|---|---|---|
| atlas | Chief of staff | planning, routing, the standup, escalation to you | everyone; @user for decisions |
| scout | Researcher | finding out what is true, with sources | atlas, quill, forge on request |
| forge | Engineer | implementing well-specified changes, proving them | atlas for design questions, sentinel for review |
| quill | Writer | briefs, posts, docs, messages for a named reader | scout for missing facts, sentinel for review |
| sentinel | Reviewer | the last check before you: code, copy, plans, numbers | forge and quill with findings, atlas with blocks |
| ops | Operator | routines: briefs, sweeps, health, backups, weekly numbers | you, silently unless something is wrong |

Six is the full team. Three is the day-one team: atlas, forge and ops cover planning, doing and keeping the lights on. Add scout when research becomes a bottleneck, quill when you publish, sentinel when a mistake would cost you.

> 📝 **From the field: let a bot design the roster**
>
> Tonbi's most reusable idea is a meta-bot he calls bot HR, whose only job is to read a project brief and create the other bots for it, choosing their roles and models. His description for it was one sentence: "you are a bot who makes other bots based on project requirements and tells them their role." Handed a game spec, it split the work into render, gameplay, technical art and browser QA, created four profiles with a shared working directory, wrote each SOUL with a mission, and picked a different model for each with a stated reason. The gateway RPC the desktop uses for that, `profiles.create`, is documented on the Desktop Plugin SDK page, and the CLI twin is `hermes profile create`. Build 9 turns this into a prompt you can paste.

### Prompts

*`prompt-b1-design-my-roster.md`*

```markdown
Design my bot roster from evidence, not from imagination. Do these in order.

1. Read https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode
   sections "Creating a Bot", "Organize bots into sections" and "Warm Bot
   Backends", and the "Cost strategy" section of
   https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban.
2. Use session_search over my last four weeks and list the kinds of work I
   asked for repeatedly, with a count each. Ignore one-offs.
3. Propose a roster of at most five bots. For each: a one-word lowercase
   name that will read well as an @tag, a title, one sentence of what it
   owns, who it will talk to, and whether it is a planner (no terminal) or
   a worker.
4. Tell me which three to create first and why, given that my desktop keeps
   three backends warm.
5. Stop. Do not create anything.
```

### Verify

- [ ] Your roster document names at most five bots, each tied to work you did more than once this month
- [ ] Every name is lowercase, one word, and unlike every other name when spoken aloud
- [ ] Exactly one bot is the planner and its toolsets exclude the terminal
- [ ] You know which three you are creating first

## Build 2: A Model per Bot

![The model ladder](../assets/art/v3-model-ladder.webp)

### What you are building

A model, a provider and an effort level for each bot, chosen for the role and priced before the first message, plus the credential rule that decides whether a bot can even start.

### What the docs say

Checked against the Bot Mode page (Model and provider pin, Copy API keys), the Profiles page (Every profile owns its credentials), the Kanban page (Cost strategy) and the Configuration reference.

| Fact | Detail |
|---|---|
| Per-bot pin | The New Agent dialog's Advanced section pins a provider and model per Bot; different Bots run different models side by side. Unset means inherit from the launch profile. In the profile it is `model.default` in that profile's config.yaml |
| Effort | `agent.reasoning_effort` per profile: none, minimal, low, medium, high, xhigh, max, ultra |
| Keys are copied, logins are not | Copy API keys from the main profile is on by default and copies static keys into the Bot's own credential store. Single-use OAuth logins (Anthropic, OpenAI Codex, xAI) are never copied; sign the Bot in itself with `hermes -p <bot> auth add <provider>` |
| Why | A named profile resolves providers from its own `auth.json` and `.env` only. A copied OAuth refresh token is the same credential with two owners, and the first refresh breaks the other |
| The split that pays | Planner on a frontier model, workers on inexpensive models, quality-sensitive work pinned back up per task. Workers are where the vast majority of tokens are spent |

### The decision table

| Role | Model class | Effort | Why |
|---|---|---|---|
| Planner (atlas) | Frontier | high | Decomposition, routing and judgment are the expensive skills; the planner sends few tokens and each one steers many |
| Reviewer (sentinel) | Frontier or strong mid | high | A cheap reviewer approves cheap mistakes. This is the second place the money goes and the last place to save it |
| Engineer (forge) | Inexpensive coding model | medium | Well-specified cards are throughput work; a fast coding model on a card with a definition of done beats a frontier model on a vague one |
| Researcher (scout) | Mid model with strong web tools | medium | Reading and citing needs care, not genius; the browser and search tools matter more than the model |
| Writer (quill) | Mid model you like the voice of | medium | Voice is taste; pick the model whose prose you would sign |
| Operator (ops) | Inexpensive | low | Routines read tool output and format it; no reasoning budget needed |
| Anything touching private data | A local model | medium | Privacy is a property of where the tokens go, not of the prompt |

> 📝 **From the field: a bot's own reasons**
>
> When Tonbi's bot HR assigned models it explained itself. Gameplay code went to a high-throughput coding model because "gameplay is a large amount of iterative, relatively self-contained implementation work"; technical art went to a model it judged "suited to generative and creative implementation" because it had to "translate a detailed visual target into procedural geometry"; the WebGL lead got the strongest coding model available. His take: "interesting model choices, but you can see it's fairly well thought out." He also reports that the same project failed outright on a local model. Take both as data from one run, not as a rule.

### Commands

*`models.sh`*

```bash
# Pin a model per bot; this writes model.default in that profile's config.yaml
hermes -p atlas config set model.default "<frontier model>"
hermes -p forge config set model.default "<inexpensive coding model>"
hermes -p ops config set model.default "<inexpensive model>"

# Effort per bot
hermes -p atlas config set agent.reasoning_effort high
hermes -p ops config set agent.reasoning_effort low

# OAuth providers are signed in per profile, never copied
hermes -p atlas auth add <provider>

# Read it back
hermes -p forge config show | grep -A2 '^model:'
```

### Prompts

*`prompt-b2-price-the-roster.md`*

```markdown
Read the "Cost strategy" section of
https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban and
the "Every profile owns its credentials" section of
https://hermes-agent.nousresearch.com/docs/user-guide/profiles. Then, for the
roster in my roster document:

1. List the providers and models I actually have configured (hermes model,
   and each provider's status), with their prices per million tokens as
   the provider publishes them.
2. Assign one to each bot using the decision table (planner frontier,
   reviewer strong, workers inexpensive, private data local), and give the
   one-line reason.
3. Estimate a day's cost for a normal day: the planner runs a standup and
   routes ten cards, workers execute them, the operator runs three
   routines. Show your token assumptions.
4. Tell me which bots will need their own OAuth sign-in because the
   provider uses single-use tokens.

Stop there. Do not change any config.
```

### Verify

- [ ] Every bot has a model.default and an agent.reasoning_effort you chose, readable with hermes -p <bot> config show
- [ ] The planner and the reviewer are on the strongest models; the operator on the cheapest
- [ ] Any bot on an OAuth provider has completed its own sign-in and answers a test message
- [ ] You have a per-day estimate written down to compare against hermes insights in a week

## Build 3: The Birth of a Bot

![Build 3](../assets/art/part-01.webp)

### What you are building

Your first three bots, created either from the New Agent dialog or from its CLI twin, each with a SOUL written for its role, the right skills and toolsets ticked, and a first message that proves it knows who it is.

### What the docs say

Checked against the Bot Mode page (Creating a Bot, Edit Profile, Duplicate, Avatars) and the Personality page.

| Fact | Detail |
|---|---|
| The quick path | New Agent in the roster: Name, Title, Description, and the Bot exists in seconds, introducing itself as the first message of its Bot Chat |
| Advanced | Clone from an existing profile or start fresh; Create empty to skip the bundled skills; Model and provider pin; Custom SOUL.md; per-skill, per-toolset and per-MCP-server enablement; Copy API keys from the main profile |
| Description matters twice | It is the Bot's role text in every other Bot's teammate roster, and it is what the kanban decomposer routes by. Write it as what the Bot is good at |
| Edit Profile | Right-click a Bot to reopen the same surface on the live profile: avatar, title, description, model pin, skills, toolsets, MCP servers, the full SOUL.md |
| Duplicate and Delete | Duplicate makes a full clone: config, skills, SOUL.md, memory, look. Delete Profile is behind a destructive confirmation; the default profile cannot be deleted |
| The CLI twin | `hermes profile create <name> --description "<role>"` with `--clone`, `--clone-from <source>` or `--no-skills` as needed, then edit `~/.hermes/profiles/<name>/SOUL.md` |
| What belongs in a SOUL | Tone, directness, how to handle uncertainty and disagreement, what to avoid. Not file paths or project rules; those go in AGENTS.md |
| Avatars | A deterministic blob face from the name, a geometric face, an uploaded image, an AI-generated portrait when an image backend is configured, or a pixel pet |

### The SOUL for a bot is the SOUL for a role

Volume 1 taught the shape: observable rules, a clear list of nevers, no project facts. A bot's SOUL adds one section at the top, the role, because the bot has to know what it owns and what it hands to whom. Here are two of the six from the kit; the others are in `kits/bot-team/`.

*`~/.hermes/profiles/atlas/SOUL.md`*

```markdown
# Role

You are Atlas, the chief of staff of this roster. You plan, you decide once, you
hand work to the right teammate, and you keep the human out of the loop except
where a decision is genuinely theirs. You do not implement; you have no
terminal for a reason.

# How you work

- Every request becomes a plan with named owners before anything runs: who does
  what, in what order, with what definition of done. Decide every shared choice
  (names, formats, schemas) yourself and write it into each card so workers never
  have to guess the same thing twice.
- Hand work off with message_agent or a kanban card, never by describing it in
  chat and hoping. A handoff carries the goal, the context, the files that may be
  touched, and how the result will be checked.
- Ask the human with @user only for decisions that are theirs: money, publishing,
  deleting, anything outward-facing or irreversible.
- Report in the shape of a standup: done, in progress, blocked, needs you.

# Voice

- Short. One idea per sentence. No filler, no praise.
- Plain claims. When a teammate's result is unverified, say so.

# What you never do

- Never run code, edit files or publish anything yourself.
- Never approve spending, sending or deleting on the human's behalf.
- Never let a blocked card sit silently past one routine cycle: escalate it.
```

*`~/.hermes/profiles/forge/SOUL.md`*

```markdown
# Role

You are Forge, the engineer. You implement changes that arrive with a clear goal,
the relevant context and a definition of done, and you prove them before you
report them.

# How you work

- Read the card or message fully before touching a file. If the design is
  ambiguous, block the card with one specific question rather than guessing.
- Smallest change that satisfies the definition of done. No drive-by refactors.
- Tests or a reproducible check run before you report. "It should work" is not
  a report; the command you ran and its output is.
- Work in the worktree or directory the card names, never in another project.

# Voice

- Report what changed, what was verified, what is left. Nothing else.
- Diffs and command output over adjectives.

# What you never do

- Never push, deploy, delete data or change a public surface without @user.
- Never mark a card complete without the verification the card asked for.
- Never decide the design; that is Atlas's job, and the human's above that.
```

### Commands

*`birth.sh`*

```bash
# The CLI twin of the New Agent dialog, for the day-one three
hermes profile create atlas --clone --description "Plans work, decides shared choices once, routes cards and messages to the right teammate, escalates real decisions to the human. Never implements."
hermes profile create forge --clone --description "Implements well-specified changes in a repository, runs the tests, reports what changed and what was verified."
hermes profile create ops   --clone --description "Runs the routines: briefs, sweeps, health checks, backups, weekly numbers. Silent when nothing needs a human."

# Give each its SOUL from the kit
cp kits/bot-team/atlas/SOUL.md ~/.hermes/profiles/atlas/SOUL.md
cp kits/bot-team/forge/SOUL.md ~/.hermes/profiles/forge/SOUL.md
cp kits/bot-team/ops/SOUL.md   ~/.hermes/profiles/ops/SOUL.md

# --clone copies MEMORY.md and USER.md too (memory is treated as identity). Workers start blank:
: > ~/.hermes/profiles/forge/memories/MEMORY.md; : > ~/.hermes/profiles/forge/memories/USER.md
: > ~/.hermes/profiles/ops/memories/MEMORY.md;   : > ~/.hermes/profiles/ops/memories/USER.md

# The planner cannot execute, by construction, not by instruction
hermes -p atlas config set agent.disabled_toolsets "terminal,code_execution,browser,computer_use,delegation"

# Then, in the app: Bots tab, right-click each, Edit Profile, tick the toolsets:
#   atlas: kanban, memory, file, session_search (no terminal, on purpose; file is its notebook)
#   forge: terminal, file, code_execution, memory
#   ops:   terminal, file, memory, session_search, cronjob
# Open each Bot Chat and read its introduction.
```

> ⚠️ **Take the terminal away from the planner**
>
> The Kanban page recommends pairing the orchestrator profile with toolsets restricted to board operations so it "literally cannot execute implementation tasks even if it tries." The same rule keeps a chief of staff honest. If atlas has a terminal, one day it will fix something itself instead of routing it, and you will not know which bot to trust for what.

### Prompts

*`prompt-b3-first-words.md`*

```markdown
You were just born as <name>, the <title> on this roster. Before we do any
work:

1. Read your SOUL.md back to me in your own words: what you own, who you
   hand work to, what you never do.
2. List the toolsets you actually have. If you have one your SOUL says you
   should not, say so now.
3. Tell me the names and roles of your teammates as your system prompt
   describes them.
4. Ask me the one question about your role that your SOUL leaves open.
```

*`prompt-b3-write-a-soul-for-a-role.md`*

```markdown
Write a SOUL.md for a new bot on my roster. Read
https://hermes-agent.nousresearch.com/docs/user-guide/features/personality
section "What should go in SOUL.md" first. The bot: name <name>, title
<title>, owns <one sentence>, hands work to <teammates>, must never
<the irreversible things>. Structure: Role, How you work, Voice, What you
never do. Every line a rule an observer could check in a transcript; no
file paths, no project facts; under forty lines. Show it to me, then, after
I say go, create the profile with hermes profile create --description and
write the file to ~/.hermes/profiles/<name>/SOUL.md.
```

### Verify

- [ ] The three bots appear in the Bots tab with titles and their first message introduces the role you wrote
- [ ] hermes -p atlas chat opens the same Bot Chat the roster row opens
- [ ] Edit Profile on atlas shows the terminal toolset off
- [ ] Each bot answered the first-words prompt with the right teammates

## Build 4: Routines

![Build 4](../assets/art/part-06.webp)

### What you are building

Recurring work attached to the bot that owns it: a morning standup from atlas, a health brief and a nightly backup from ops, a source watch from scout. Each one silent when nothing happened, each one landing in that bot's own chat where you would have asked anyway.

### What the docs say

Checked against the Bot Mode page (Routines) and the Cron page.

| Fact | Detail |
|---|---|
| The pane | The Routines pane docks beside the chat while the Bots tab is active; a structured schedule picker builds the schedule, with an Advanced field for the raw Hermes schedule string |
| What a routine is | A plain Hermes cron job namespaced `[bot:<name>] <routine>`. It shows in `hermes cron list` and the core Cron page. Runs land in the Bot's own chat history |
| The CLI twin | `hermes -p <bot> cron create "<schedule>" "<prompt>" --name "<routine>"`, run under that bot's profile so the job belongs to it |
| Fresh session, every run | No chat history, no context file unless the job carries `--workdir`. The prompt plus the attached skills are the whole briefing |
| Silence | A final response containing `[SILENT]` delivers nothing and is still saved for audit. Failed runs always deliver |
| Per-job pins | A routine can pin its own model, provider and reasoning effort |
| Health | `hermes cron doctor` is the read-only check across every job; `hermes cron runs <id>` shows attempts; `hermes pause` is the global stop |

### The routines the kit ships

*`kits/bot-team/ops/routines.sh`*

```bash
#!/bin/sh
# Ops routines: the bot with a terminal gathers, and delivers where the decision gets made.
# Run once: sh kits/bot-team/ops/routines.sh (the -p flag scopes each job to the ops profile).
# Schedules the parser accepts: "every day at 07:30", "every sunday 18:00", "every 2h", or a cron expression.
# Every prompt is self-contained: a routine runs in a fresh session with no chat history and no message_agent;
# --deliver bot-chat:<profile> drops the output into that bot's Bot Chat as a message it answers, and there it can message teammates.

hermes -p ops cron create "every day at 07:30" \
  "Morning brief. Run hermes doctor, hermes cron doctor and hermes memory status and read their output. Then run hermes kanban list --status blocked and hermes kanban list --status running and pick out cards older than 24 hours. Report in four lines: machines, jobs, memory, board. If everything is healthy and nothing is stuck, reply with only [SILENT]." \
  --name "morning-brief"

hermes -p ops cron create "every day at 22:00" \
  "Nightly backup. Run hermes backup --quick --label nightly and report the path and size in one line. On failure report the exact error." \
  --name "nightly-backup"

hermes -p ops cron create "every sunday 18:00" \
  "Weekly numbers. Run hermes insights --days 7 and hermes insights --days 14 and summarize this week's tokens, cost and the three most active profiles in five lines, with last week's figures next to them. Deliver even when unchanged." \
  --name "weekly-numbers" --deliver bot-chat:atlas

hermes -p ops cron create "every 2h" \
  "Board sweep. Run hermes kanban list. List every card in running for more than 2 hours, blocked for more than 24 hours, or in review for more than 4 hours: card id, title, owner, how long. If the list is empty reply with only [SILENT]. Otherwise start the reply with '@atlas these cards look stalled; message each owner for a one-line status or a kanban_block with the reason:' followed by the list." \
  --name "board-sweep" --deliver bot-chat:atlas
```

*`kits/bot-team/atlas/routines.sh`*

```bash
#!/bin/sh
# Atlas routines. Atlas has no terminal: its routines use the kanban tools, the file tools and session_search, never the shell.
# Anything that needs a shell (hermes insights, hermes kanban list, hermes doctor) is gathered by ops and delivered into
# atlas's Bot Chat with --deliver bot-chat:atlas; atlas answers there, where message_agent exists.
# Run once: sh kits/bot-team/atlas/routines.sh

hermes -p atlas cron create "every day at 08:00" \
  "Standup. Use the kanban tools to read the board (every card, its status and owner) and session_search for what each teammate reported since yesterday. Write a standup in the shape done, in progress, blocked, needs you, one line per item, owners named. End with the one decision that is the human's today, or [SILENT] if the board is empty and nothing is blocked." \
  --name "standup" --deliver bot-chat:atlas

hermes -p atlas cron create "every saturday 17:00" \
  "Weekly review. Use the kanban tools to list this week's completed cards and session_search to find the weekly numbers ops delivered. Write five lines: what shipped, what slipped and why, what to stop, what to start, and the one decision that needs the human. Deliver even when short." \
  --name "weekly-review"
```

*`kits/bot-team/scout/routines.sh`*

```bash
#!/bin/sh
# Scout routine: a watch on the sources that matter to the team. Edit the list in the prompt.
# The result is delivered into atlas's Bot Chat; atlas decides who needs to hear it and messages them from there.
# Run once: sh kits/bot-team/scout/routines.sh

hermes -p scout cron create "every day at 06:30" \
  "Source watch. Read the Hermes Agent documentation changelog page, the Hermes GitHub releases page, and the two feeds named in your MEMORY.md under 'watch list'. For anything new since yesterday that changes how the team works (a renamed command, a new setting, a breaking change), write one line with the link and which teammate it affects. If nothing changed, reply with only [SILENT]. Otherwise start the reply with '@atlas source watch found changes that affect the team:' followed by the lines." \
  --name "source-watch" --deliver bot-chat:atlas
```

> ⚠️ **Three things a routine cannot do, and the flag that fixes two of them**
>
> A routine runs in a fresh headless session. It has no chat history, it has no message_agent (that tool exists only in canonical Bot Chat sessions), and @user means nothing to it, because a routine's output goes wherever its delivery target says. So a routine never "messages a teammate"; it gathers and reports. The kit's answer is --deliver bot-chat:<profile>: the output lands in that bot's Bot Chat as a message the bot answers, and in that reply the bot does have message_agent. That is why ops runs the board sweep and delivers it to atlas, and why the schedule strings read every day at 07:30 and every sunday 18:00: the parser accepts those, a cron expression, and plain intervals such as every 2h, and rejects every 1d at 07:30 even though an older docs example shows it.

> ℹ️ **Who gets a routine**
>
> Workers do not, by default. forge, quill and sentinel receive work as cards and messages; a routine on a worker is usually a sign that the planner should be sending it a card instead. The three bots with standing routines are the ones whose job is to look: the operator at the machines, the chief of staff at the board, the researcher at the sources.

### Prompts

*`prompt-b4-add-a-routine.md`*

```markdown
You are <bot>. Add a routine for yourself. Read
https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode section
"Routines" and the "[SILENT]" and "delivery" sections of
https://hermes-agent.nousresearch.com/docs/user-guide/features/cron. The
routine: <what, when, and what counts as nothing to report>. Write the
prompt for a stranger with no history: every path absolute, every check
explicit, the silent condition stated, the report shape stated. Show me the
exact cronjob tool call or hermes cron create command, then create it after
I say go, run it once, and show me the output in this chat.
```

### Verify

- [ ] hermes -p ops cron list, hermes -p atlas cron list and hermes -p scout cron list each show the jobs by name (the Routines pane adds its own [bot:<name>] prefix only to jobs it creates)
- [ ] hermes -p ops cron run board-sweep either ends in [SILENT] or lands in atlas's Bot Chat, where atlas answers it
- [ ] hermes cron doctor reports every routine healthy
- [ ] The Routines pane in the app lists the same jobs the CLI does

## Build 5: Bots Talking to Each Other

![Message paths between the six](../assets/art/v3-message-paths.webp)

### What you are building

The habit and the mechanics of handing work between bots: an @mention in any chat, a `message_agent` call from inside a Bot Chat, the roster every bot carries in its prompt, and the delivery contract that tells you what "queued" means and what happens when a turn fails.

### What the docs say

Checked against the Bot Mode page: Bot-to-bot messaging, What actually makes a chat a Bot Chat, Failed turns retry safely, When a delivery fails.

| Fact | Detail |
|---|---|
| @mentions | Type `@researcher have a look at this` in any chat; the composer resolves it against the live roster and the active Bot is told exactly who you mean. The Bot then composes its own message and sends it with `message_agent`. Your text is never forwarded verbatim |
| The tool | `message_agent(target="researcher", message="…")` from inside a canonical Bot Chat. The target is a profile name, a friendly name, or the `@` tag. The tool validates the target against the roster and prefixes `Message from 🤖 <name> (@<handle>):` automatically |
| Fire and forget | The sender gets `status: queued` plus a `delivery_id` and finishes its turn. The completion notification later carries the reply or the failure. Queued means handed off, not delivered |
| The roster in the prompt | Teammate names and roles, from each profile's title and description, are part of every Bot Chat's system prompt, so a bot knows who does what before choosing a recipient |
| Only in Bot Chats | `message_agent` exists only in canonical Bot Chat sessions on Bot-Mode-managed installs, never in regular chats, room member sessions or plain CLI sessions |
| Staying silent | A bot with nothing to add ends its turn with `[SILENT]` or `NO_REPLY`; the sender gets an empty reply instead of the token |
| Retries | A failed delivery turn is retried at most once and only when a retry can help: offline target, timeout, rate limit, server error, context overflow (compacted first). Auth, quota and configuration failures surface immediately |
| Reason codes | A failed turn carries a machine-readable reason: `provider_auth_or_access`, `provider_quota_limit`, `provider_rate_limit`, `provider_server_error`, `context_overflow`, `missing_config`, `model_unavailable`, `runtime_offline`, `queued_expired`, `delivery_timeout`, `target_busy`, `unknown` |
| The switch | `agent.bot_mode_protocol: true` in config.yaml (default on) injects the protocol into canonical Bot Chats only; your SOUL.md and regular sessions stay untouched |
| Headless | On a gateway-only install nothing writes the markers. To enable by hand: `hermes -p <bot> chat -c "Bot Chat" --create-if-missing` and an empty `ui_meta: { hermes-bots: {} }` block in one profile's profile.yaml |

*`~/.hermes/config.yaml`*

```yaml
agent:
  bot_mode_protocol: true   # inject the bot-to-bot messaging protocol into canonical Bot Chats
```

*`~/.hermes/profiles/atlas/profile.yaml`*

```yaml
ui_meta:
  hermes-bots: {}
```

### The message paths

The plate above is the whole team's wiring. Read it as five standing paths:

| From | To | Carries | Trigger |
|---|---|---|---|
| you | atlas | a goal | you type it in atlas's chat |
| atlas | forge, scout, quill | a card or a message with goal, context, files, definition of done | atlas's plan |
| forge, quill | sentinel | "review this" with the definition of done attached | the worker finishing |
| sentinel | forge, quill, atlas | findings ranked by severity, or a block | the review |
| anyone | you | `@user` with one specific question | a decision that is yours |

Everything else is noise. If a bot is messaging outside these paths, its SOUL is missing a line.

> 📝 **From the field: the first message you should send**
>
> Tonbi's very first test of bot-to-bot messaging is the right one to copy: he tells one bot, in plain language, "send a message to <other bot> asking to introduce itself, and then tell me the response." The exchange shows up in the receiver's Bot Chat, and the reply comes back to the sender. Do that once with every pair you expect to talk; it costs a minute and it proves the roster, the protocol and the routing in one go.

### Prompts

*`prompt-b5-handshake.md`*

```markdown
Send a message to @<other bot> asking it to introduce itself in two lines
and to tell you which toolsets it has. Tell me the delivery status you got
back, then the reply when it arrives. If the reply does not arrive, tell me
the reason code from the completion notification and what the docs say it
means.
```

*`prompt-b5-handoff-shape.md`*

```markdown
From now on, every handoff you send with message_agent carries four parts
in this order: the goal in one sentence; the context (paths, facts,
constraints) the recipient cannot see; the files it may touch; and the
definition of done, stated so the recipient can check it without you. Show
me the message you would send to @forge for this task before you send it:
<task>.
```

### Verify

- [ ] A handshake between every pair that should talk came back with a reply, and the exchange is visible in the receiver's Bot Chat
- [ ] The sender's completion notification showed the reply, not just queued
- [ ] A message to a bot that is signed out surfaced a provider_auth_or_access reason instead of hanging
- [ ] Your handoffs carry goal, context, files and definition of done

## Build 6: Rooms

![Three rounds, then the room settles](../assets/art/v3-room-rounds.webp)

### What you are building

Group chats that do real deliberation without spinning: a planning room where atlas, forge and scout agree a phase plan; a review room where sentinel judges before you do; and the habits, three rounds, @user escalation, threads, that keep a room useful.

### What the docs say

Checked against the Bot Mode page: Groups and group chats.

| Fact | Detail |
|---|---|
| Membership | 2 to 6 Bots per room. Right-click a Bot, Manage groups, or the room header's Manage members to edit the roster in place; a removed Bot takes no further turns, an added one reads recent history on its first turn |
| Rounds | In the page's words: "Your message triggers up to three serial rounds of member turns. @-mentioned Bots respond (everyone responds when nobody is mentioned); each Bot replies briefly or passes, and the room settles when a full round stays silent." Hard caps: 10 messages per send, 3 rounds |
| Not everyone speaks | Speaking is each member's choice; a Bot replies only when it has something new to add. Mentioning specific members scopes the round to them |
| Escalation | Bots pull each other in with `@name` and escalate to you with `@user`; the room row shows a needs-you badge, and command approvals in the room answer on the click |
| Threads | Reply in thread continues a topic without reordering the room; Activity is a status view, not the conversation |
| Handoff to the primary | `@hermes` reaches the primary Bot from any room |
| Keeps running | When every member lives on the same gateway, that gateway owns turn scheduling; closing the Desktop does not stop a room mid-discussion. Rooms are mirrored into every connected gateway's shared metadata |
| Cross-machine rooms | Members on other connections are seated with a device badge and a device-qualified handle such as `@reviewer-mini`; each member's turns run on its own machine |
| Holds | `stop @bot` holds a member; `@all resume` or any message addressing the room releases everyone |

### Two standing rooms

| Room | Members | When you open it | What good looks like |
|---|---|---|---|
| planning | atlas, forge, scout | a new project or a change of direction | a numbered phase plan with owners, the shared decisions written out, and one @user question at most |
| review | sentinel, forge, quill | before anything ships | findings ranked by severity, a verdict per artifact, and a block that stays a block |

> 📝 **From the field: plan first, then let the boss push**
>
> Tonbi's racing-game run is the clearest public example of a room doing work. His kickoff to the group was two moves: "everyone introduce yourselves and your role, take a look at the spec," then "decide amongst yourselves the phases for this project and the roles. Just plan it, no coding yet." The bots negotiated phases, asked each other real interface questions (texture atlas dimensions, of all things) and marked phase one parallel. Only then: "start working on this project based on this plan. Please report back when you are done with the task or if you hit any blockers, need help from me." He added his orchestrator bot afterward and told it to check in every twenty minutes and push anyone who had not started. His honest note: with no tool calls visible in a room, he repeatedly doubted whether work was happening. Threads are the cure; talk to the orchestrator in a separate thread and let the workers alone.

### Prompts

*`prompt-b6-planning-room.md`*

```markdown
@atlas @forge @scout Everyone introduce yourself in one line: your role and
what you own. Then read <the brief, attached or at this path> and decide
among yourselves the phases for this project and who owns each. Write the
shared decisions (names, formats, interfaces) into the plan so nobody has to
guess them later. Mark which phases can run in parallel. Plan only, no
work yet. When you agree, @atlas posts the plan as a numbered list and asks
me the one question you could not settle, if any.
```

*`prompt-b6-review-room.md`*

```markdown
@sentinel review <the artifact: a path, a diff, a draft> against this
definition of done: <paste it>. Rank findings by severity with location and
failure scenario. @forge and @quill answer only findings addressed to you,
with the fix or a reason to disagree, no rewrites in the room. @sentinel
closes with one of approve, changes requested, or blocked, and @user only if
the block needs my decision.
```

*`prompt-b6-start-work.md`*

```markdown
@atlas Start work on the plan we agreed. Hand each phase-one owner its card
or message with goal, context, files and definition of done. Check the room
every twenty minutes: nudge anyone who has not started, unblock what you can,
and post a standup line when a phase completes. Report to me in this thread
only when a phase is done or you are blocked on a decision that is mine.
```

### Verify

- [ ] The planning room produced a numbered plan with owners and settled at most three rounds after your kickoff
- [ ] A review room ended with a verdict per artifact and a needs-you badge only when a decision was genuinely yours
- [ ] Closing and reopening the Desktop found the room where it was
- [ ] Reply in thread kept a side question from reordering the main conversation

## Build 7: Shared Memory and a Shared Board

![One bank, one board, six bots](../assets/art/v3-memory-stack.webp)

### What you are building

The two things a team needs that a single agent never did: a memory the bots share on purpose, and a queue they work from instead of talking. The memory is Hindsight, one bank, local or cloud, joined by the bots whose context should compound and withheld from the ones whose notes should stay private. The queue is the kanban board, where a card carries the goal, the owner, the thread and the verdict, and the dispatcher does the handing out. Mnemosyne is here too, as the local-first provider for a bot whose data must never leave the machine.

### What the docs say

Checked against the Memory Providers page, the Profiles page (the caution box about two writers on one home), the multi-profile gateways page (which credentials follow which profile), the Kanban page, and the Hindsight and Mnemosyne READMEs at the versions installed while writing.

| Fact | Detail |
|---|---|
| Two memories, always | Built-in memory (MEMORY.md and USER.md, per profile) is always on. One external provider can sit beside it per profile, chosen with memory.provider in that profile's config.yaml; hermes memory setup picks it, hermes memory status shows it, hermes memory off drops it and the built-in files keep working |
| One provider per profile | The external slot is single-select. A bot is on Hindsight or on Mnemosyne, never both. Different bots may choose differently, because each bot is its own profile with its own config |
| Never share a home | The Profiles page is blunt: two agent processes on one profile both write memory and each loads the other's writes into its prompt "until it stops being anything you configured." Agents that need shared memory use an external provider. That sentence is why this build exists |
| What a provider does | Injects provider context into the system prompt, prefetches relevant memories before each turn in the background, syncs turns after each reply, extracts on session end where supported, mirrors built-in memory writes, and adds its own tools |
| Hindsight | Knowledge graph with entity resolution and multi-strategy retrieval. Tools hindsight_retain, hindsight_recall, hindsight_reflect (cross-memory synthesis, unique among the providers). Config at $HERMES_HOME/hindsight/config.json, so one file per bot. Modes in the README: cloud (API key), local_embedded (Hermes starts a daemon with built-in PostgreSQL, needs an LLM key or any OpenAI-compatible endpoint for extraction, stops after 5 minutes idle), local_external (a Hindsight you already run, one URL) |
| The bank is the sharing unit | bank_id names the bank, default hermes. bank_id_template derives it with placeholders such as {profile}; empty means every bot with the same bank_id shares one memory. HINDSIGHT_BANK_ID in a profile's own .env is honored per profile, never inherited from the default profile |
| Tags keep provenance | retain_tags stamps everything a bot writes; recall_tags filters what it reads back. A shared bank with per-bot retain tags tells you who learned what |
| recall_types | Defaults to observation only: the consolidated layer, deduplicated and refreshed. Set observation,world,experience to recall raw facts too. It applies to auto-recall and to the hindsight_recall tool alike |
| Mnemosyne | Third-party, MIT, local-first: one SQLite file with sqlite-vec plus FTS5, no daemon, no telemetry, no LLM needed to run. Installed into a venv of its own under $HERMES_HOME/.mnemosyne, exposed by its wrapper installer under ~/.hermes/plugins/mnemosyne, promoted to a provider with hermes memory setup, verified with hermes memory status and hermes mnemosyne stats. Its docs suggest turning off the built-in file injection for that profile, in config.yaml; Hindsight runs alongside the built-in files. Never hermes tools disable memory; that removes provider tools with the built-in ones |
| The board | A task has one assignee, a profile name, and a status in triage, todo, ready, running, blocked, review, done, archived. Comments are the inter-agent protocol: a respawned worker reads the whole thread. The dispatcher runs inside the gateway, ticks every 60 seconds, promotes todo to ready when parents are done, claims and spawns the assigned profile, and auto-blocks a task after two consecutive spawn failures |
| Who may create cards | The Desktop Kanban plugin displays the board; it grants nothing. Enable the kanban toolset on the bot that orchestrates: hermes -p atlas tools enable kanban. Workers get their lifecycle tools automatically from HERMES_KANBAN_TASK; they never shell out to the CLI |
| Workspaces | scratch (deleted on completion, declared artifacts survive), dir:<absolute path> (preserved), worktree (a git worktree, preserved). A relative dir path is rejected at dispatch |
| Shared boards | One kanban.db across several homes shares the board, and every home has a profile named default, so set kanban.dispatch_profiles per home to say which assignees it may claim |

> ⚠️ **Local or cloud is one decision, made once**
>
> Every bot that joins a bank must reach the same Hindsight. Pick the mode before the first bot: local_embedded when one machine hosts the team and you want zero services to run; local_external when the team spans machines and one always-on box (the mini, the VPS) runs Hindsight for all of them; cloud when the machines come and go. Mixing modes across bots gives you three banks that happen to share a name.

### Two shapes, both real

| Shape | Who writes | Who reads | When it fits | Who runs it |
|---|---|---|---|---|
| Shared bank, tagged | atlas, scout, quill, sentinel, each with retain_tags set to its own name | the same four | one project, one company, decisions that every planner and reviewer should know | the setup this volume ships; a working local_external install was read while writing |
| Single writer | the orchestrator only; workers stay on built-in memory | the orchestrator, then it briefs the workers | when workers fetch from outside and should not inherit the team's history, or when you distrust concurrent writes | Wanderloots, orchestrator plus researcher plus librarian |

> 📝 **From the field: why Wanderloots gave only one bot the external memory**
>
> "We don't necessarily want to have all of our bots writing to the same memory system, because they might be conflicting with one another. Instead, I'll leave that ability, the external memory provider, on orchestrator so that the orchestrator will be the only one able to write to that external memory system." His researcher kept persistent memory and the user profile on, "so that it slowly improves itself over time," and nothing else. Both shapes in the table above are defensible. The tagged shared bank trades his caution for provenance: conflicts become visible as two observations with different tags, and hindsight_reflect is the tool that reconciles them.

> 📝 **From the field: what Wanderloots learned running Hindsight for real**
>
> Two videos, one self-hosted Hindsight in Docker, first on a local model (a 20B open model, 13 GB on disk, and it must support tool calling) and later on a Codex subscription with a cheaper model for retain and a stronger one for consolidation and reflect. The rules he states: a bank is a hard recall boundary, one profile connects to exactly one bank, and there is no cross-bank query, so tags are the only soft partition you get; configure the bank before any agent connects (extraction mode concise, a mission statement for retain, custom entity labels such as project and harness turned on as tags, memory defense set to redact); put an API key on the connector and a separate key on the control plane; install backups with hindsight admin backup before the first agent joins and again before every upgrade. His bank held 33,000 memories after a week and a half, and a fact stored by one agent was recalled by another on the next turn. His verdict on the two providers is the Mnemosyne author's own: Hindsight is a memory engine, Mnemosyne is a memory layer. Test one for a week; you can export from one to the other.

> 📝 **From the field: the honest state of memory**
>
> HolmeBengt, 28 cron jobs and more than 30 self-built skills in: "Long-term memory is still the biggest unsolved problem. Dreaming helps, but session-to-session recall remains inconsistent." His fix is a 3 AM job that reads every conversation and writes a structured summary that loads at the start of every session. riceinmybelly runs three layers and caps the first: MEMORY.md at 2,200 characters for behavioral rules only, "larger MEMORY.md starts crowding out system prompt instructions"; an Obsidian vault for long-form knowledge; Hindsight synced from the vault every 30 minutes with a 90-second budget, additive on top. Build the shared bank; keep the nightly summary and the small MEMORY.md anyway.

### The kit

*`kits/bot-team/memory/hindsight-config.json`*

```json
{
  "mode": "local_external",
  "api_url": "http://127.0.0.1:8888",
  "bank_id": "team-shared",
  "bank_id_template": "",
  "memory_mode": "hybrid",
  "auto_retain": true,
  "auto_recall": true,
  "retain_async": true,
  "retain_every_n_turns": 1,
  "retain_tags": [
    "<bot-name>"
  ],
  "recall_tags": "",
  "recall_types": [
    "observation"
  ],
  "recall_budget": "mid",
  "recall_prefetch_method": "recall",
  "recall_sync": false,
  "recall_indicator": true,
  "retain_indicator": true
}
```

*`kits/bot-team/memory/hindsight-setup.sh`*

```bash
#!/bin/sh
# One shared Hindsight bank for the bots that share context. Run once per bot that joins the bank.
# Pick ONE mode and keep it for every bot: local_embedded (Hermes runs the daemon, free, needs an LLM key
# or a local OpenAI-compatible endpoint for extraction), local_external (a Hindsight you run yourself,
# Docker or bare, one URL), or cloud (an API key from ui.hindsight.vectorize.io).

BOT="${1:?usage: hindsight-setup.sh <bot> [bank]}"
BANK="${2:-team-shared}"
HOME_DIR="$HOME/.hermes/profiles/$BOT"

# 1. Interactive wizard, once per bot. It installs the client, asks the mode, and offers a starter
#    memory template (skip it for a bot joining an existing bank; it warns before overwriting).
hermes -p "$BOT" memory setup            # choose hindsight, then the mode you picked above

# 2. Point this bot at the shared bank and tag what it writes with its own name.
#    The config file is per profile: each bot has its own $HERMES_HOME/hindsight/config.json.
[ -f "$HOME_DIR/hindsight/config.json" ] || { echo "no $HOME_DIR/hindsight/config.json: the wizard did not finish for $BOT, run it again"; exit 1; }
python3 - "$HOME_DIR/hindsight/config.json" "$BANK" "$BOT" <<'PY'
import json, sys
path, bank, bot = sys.argv[1:4]
cfg = json.load(open(path))
cfg["bank_id"] = bank
cfg["bank_id_template"] = ""
cfg["retain_tags"] = [bot]
cfg["memory_mode"] = "hybrid"
json.dump(cfg, open(path, "w"), indent=2)
print("wrote", path, "bank", bank, "tags", cfg["retain_tags"])
PY

# 3. Read it back. The provider must say hindsight and available.
hermes -p "$BOT" memory status

# Rollback for one bot: hermes -p <bot> memory off   (built-in MEMORY.md and USER.md keep working)
```

*`kits/bot-team/memory/mnemosyne-setup.sh`*

```bash
#!/bin/sh
# Mnemosyne for a bot whose memory must never leave the machine. Local-first, one SQLite file, no daemon.
# A profile runs ONE external provider, so a bot is on Mnemosyne or on Hindsight, never both.
# Two rules learned in the field: never install into the Hermes-managed venv (hermes update rebuilds it and
# wipes extra packages), and if your terminal backend is Docker, run this from the host yourself, not via Hermes.

BOT="${1:?usage: mnemosyne-setup.sh <bot>}"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
VENV="$HERMES_HOME/.mnemosyne/venv"          # the side venv the Mnemosyne README's update path expects

# 1. A venv of its own, with local embeddings (about 800 MB of RAM at run time; the core-only profile is
#    about 50 MB but sends embeddings to a remote endpoint, which defeats the point of a private bot).
python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install --upgrade "mnemosyne-memory[embeddings]" mnemosyne-hermes

# 2. The wrapper install writes the plugin files under $HERMES_HOME/plugins/mnemosyne, where Hermes discovers them.
"$VENV/bin/mnemosyne-hermes" install --mode wrapper --force --python "$VENV/bin/python"

# 3. Select it for THIS bot and read it back. The README's path is the config key; in Wanderloots' recorded walkthrough the
#    same wizard (hermes memory setup) offered "Mnemosyne local" and asked for the default remember scope, which he set to
#    global rather than per session. If your wizard does not list Mnemosyne, the config key alone selects it.
hermes -p "$BOT" config set memory.provider mnemosyne
hermes -p "$BOT" memory setup
hermes -p "$BOT" memory status
hermes -p "$BOT" tools list | grep mnemosyne_
hermes -p "$BOT" mnemosyne stats 2>/dev/null || true   # the plugin's own CLI command as shown in that walkthrough; optional

# If memory status says plugin missing or the Python environments do not match, re-run step 2, then step 3.
# Mnemosyne's docs suggest turning the built-in MEMORY.md and USER.md injection off for this bot to avoid
# duplicate context; do that in the bot's config.yaml (memory.enabled, user_profile.enabled), not with
# `hermes tools disable memory`, which removes the whole memory toolset, provider tools included.
# Update later: "$VENV/bin/python" -m pip install --upgrade 'mnemosyne-memory[embeddings]' mnemosyne-hermes,
# re-run step 2, then hermes gateway restart. To leave: hermes -p <bot> memory off
```

> 📝 **Where Mnemosyne fits**
>
> The bottom rung of the model ladder in Build 2 was a local model for private data. Mnemosyne is the memory for that rung: nothing leaves the machine unless you point it at a remote embedding endpoint or turn on its sync. Two installation facts from the field: it must live in its own venv, because hermes update rebuilds the managed one and wipes extra packages, and if your terminal backend runs in Docker you install it from the host yourself rather than asking Hermes, or it lands inside the container. In Wanderloots' recorded walkthrough the setup wizard listed Mnemosyne and asked one decisive question, the default remember scope, which he set to global rather than per session; the README documents the config key, hermes config set memory.provider mnemosyne, which selects it either way. Its own README is unusually candid about benchmarks, which is a reason to trust it: the BEAM numbers were measured on an older version with a different judge than Hindsight's published score, and a LongMemEval figure was withdrawn until it can be reproduced. Read it as a local-first store that abstains rather than invents, not as a Hindsight replacement for the shared bank. On the machine this was written on it shows in hermes memory status as an installed provider, local, next to Hindsight.

### Commands

*`b7-commands.sh`*

```bash
# 1. The bank. Local external shown; the setup script asks the mode once per bot.
sh kits/bot-team/memory/hindsight-setup.sh atlas team-shared
sh kits/bot-team/memory/hindsight-setup.sh scout team-shared
sh kits/bot-team/memory/hindsight-setup.sh quill team-shared
sh kits/bot-team/memory/hindsight-setup.sh sentinel team-shared
# forge and ops stay on built-in memory: working notes, not team knowledge. (Born with --clone they carry a copy of the
# primary MEMORY.md and USER.md; Build 3 blanks those, so check that it happened.)

# 2. Prove the sharing, from the terminal, no app in the loop.
hermes -p scout chat -q "Use hindsight_retain to store: the team's release day is Thursday. Then reply done."
hermes -p atlas chat -q "Use hindsight_recall for 'release day' and tell me what you find and which tag it carries."

# 3. The board.
hermes kanban init
hermes -p atlas tools enable kanban          # atlas creates and routes cards
hermes gateway status                        # the dispatcher lives in the gateway; it must be up
hermes kanban create "Draft the release notes for Thursday" --assignee quill
hermes kanban watch                          # in a second terminal: claim, spawn, comments, done

# 4. A bot whose memory must stay on this machine, if you have one.
sh kits/bot-team/memory/mnemosyne-setup.sh vault
```

### Prompts

*`prompt-b7-memory-audit.md`*

```markdown
You are @ops, because this needs a shell. Audit the team's memory before we
share any of it. For every profile in hermes profile list, read
hermes -p <bot> memory status and that bot's
~/.hermes/profiles/<bot>/hindsight/config.json if it exists. Produce a
table: bot, provider, mode, bank_id, retain_tags, memory_mode. Flag: two
bots on different Hindsight modes; a bot on a bank nobody else uses that
should be shared; forge or ops on the external provider; any bot with
recall_tags set, since that hides teammates' memories. Propose the change
per bot as the exact command or JSON edit. Change nothing until I say go.
```

*`prompt-b7-first-shared-memories.md`*

```markdown
@atlas @scout @quill @sentinel Each of you: use hindsight_retain to store
three things a new teammate would need to know about your job on this
team, tagged as yourself. Then @atlas: run hindsight_reflect with the
question "what does this team know about how it works?" and post the
answer here. If two bots stored contradicting facts, say which two and
which one is right, and ask me only if you cannot tell.
```

*`prompt-b7-board-as-queue.md`*

```markdown
You are @atlas. From now on, work that takes more than one message becomes
a card, not a chat. For each item in <the plan, pasted or at this path>
call kanban_create with: a one-line title, a body carrying goal, context,
files and the definition of done, the assignee (forge, scout, quill or
sentinel), and links so review cards depend on the work they review. Put
build cards on a worktree workspace and writing cards on
dir:<absolute path to the drafts folder>. Post the list of card ids with
owners. Then leave the dispatcher alone; check hermes kanban list at the
standup, not every minute.
```

*`prompt-b7-worker-contract.md`*

```markdown
You are @forge on card <id>. Read the card with kanban_show and the whole
comment thread before doing anything. Work in the card's workspace only.
Post a comment when you start, when you hit a decision that is not yours,
and when you finish, naming the verification you ran and its output.
Declare every deliverable in kanban_complete artifacts, because a scratch
workspace is deleted on completion. If you are blocked, kanban_block with
the reason and stop; do not improvise around it.
```

### Verify

- [ ] hermes -p <bot> memory status says hindsight and available for every bot that joined the bank, and built-in only for forge and ops
- [ ] A fact retained by scout is recalled by atlas, and the recall carries scout's tag
- [ ] hindsight_reflect answered a question no single bot's memory could
- [ ] hermes kanban watch showed a card go ready, running, review, done without you touching the terminal
- [ ] The Desktop's Kanban page shows the same board the CLI lists
- [ ] A bot on Mnemosyne, if you set one up, lists mnemosyne_ tools and hermes memory status names it

## Build 8: Bots Across Machines

![One roster across three machines](../assets/art/v3-team-across-machines.webp)

### What you are building

The team spread over the machines you already own: the planner and the writer on your laptop, the engineer and the operator on an always-on Mac mini, the researcher and the reviewer on a VPS, all in one roster, messaging each other, sitting in the same rooms.

### What the docs say

Checked against the Bot Mode page (Bots across machines, Messaging across connected machines, Bot-initiated DMs across machines, One-way reachability) and the multi-connection guide.

| Fact | Detail |
|---|---|
| The union roster | Register several backends in Settings, Gateways and the Bots pane shows the Bots from every connected source, persistently. Unreachable machines keep their last-known rows |
| Handles | The same profile name on several sources disambiguates as `@name-device`, for example `@research-homelab` |
| Where a bot lives | Its chats, sessions, memory and routines live on the machine that owns the profile. Clicking a Connections Bot does not hop your window; @mention it, seat it in a room, or create new agents on it with the Create on picker |
| Create on | With more than one connection registered, New Agent grows a Create on picker; the profile is created on that machine's backend, cloning from that machine's `default` |
| The Desktop relay | Rosters propagate on their own while the Desktop runs; `message_agent` reaches bots on other connections, disambiguated as `target="moxie@<connection>"`; delivery rides the Desktop, which holds the sockets and credentials. Close the Desktop mid-delivery and the sender is told the reply did not arrive |
| Without a Desktop | Register the other gateway as a peer: `hermes peer add <name> --url http://host:8377 --key <API_SERVER_KEY>`; then `hermes peer dm <name>/<profile> < msg.txt` for short exchanges and `hermes peer run` with `--idempotency-key` for long ones. Once a peer is registered, every Bot Chat's protocol includes the peer roster and `message_agent` accepts `target="<peer>/<profile>"` |
| The peer's key | The peer machine runs the `api_server` gateway platform with a strong `API_SERVER_KEY`; the key lives in `~/.hermes/.env` as `HERMES_PEER_<NAME>_KEY`; peer names and URLs live in config.yaml under `bot_peers` |
| NAT | Cross-gateway links are direct. A gateway behind home NAT can dial out to a public peer; the reverse fails unless the network provides a route. Put a room's authority on the host every participant can reach, or bridge with Tailscale |
| Rooms across machines | Members on other connections are seated with a device badge and a device-qualified handle; each member's turns run on its own machine |

### Commands

*`peers.sh`*

```bash
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

*`prompt-b8-place-the-team.md`*

```markdown
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

- [ ] The Bots pane lists bots from every registered gateway, with @name-device handles where names collide
- [ ] A message from a laptop bot to a mini bot arrives with the Desktop open, and hermes peer dm works with it closed
- [ ] A room with members on two machines settles and shows device badges
- [ ] You know which machine holds authority for each cross-machine room

## Build 9: Ship the Team, Grow It, Shrink It

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

## The Bots Ledger

| Build | Proof |
|---|---|
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

> ✅ **What you have now**
>
> A team that is folders on disk. You can read every rule it runs by, version it, install it on a second machine in a minute, and change it with a prompt. Volume 4 puts this team to work on a company.
