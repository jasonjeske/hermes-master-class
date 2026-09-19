---
title: The Hermes Bots Masterclass
subtitle: Volume 3 of the Hermes Agent Masterclass. Bot Mode in Hermes Desktop, from one profile to a team that plans, builds, reviews and reports while you do something else
why: Everyone shows the roster. Nobody hands you the roster's files. This volume gives you a six-bot team with every SOUL.md, every model pin, every routine and the message paths between them, and the prompts that grow or shrink it.
date: 2026-09-19
eyebrow: HERMES BOTS · VOLUME 3
---

![The Hermes Bots Masterclass](assets/art/v3-hero.webp)

## Orientation

Bot Mode is the part of Hermes Desktop that turns your profiles into a roster of named Bots, each with its own chat, role, model, memory, skills and avatar. Bots run routines, deliberate in group chats, and message each other directly. It ships built in and on by default. And there is no new primitive underneath it: a Bot is a profile, the same `~/.hermes/profiles/<name>/` you met in Volume 1, so everything you do in the roster is visible from the terminal too.

That last sentence is the whole design of this volume. Because a Bot is a profile, a team is a set of folders, and a set of folders can be written down, versioned, shared and installed. So this volume does not describe a team. It ships one: six bots with every file, the routines they run, the way they talk, and the prompts that add a seventh or retire one. You can build it in the app one dialog at a time, or clone the kit and be done in a minute. Both roads end in the same folders.

```callout kind=note title="What this volume rests on"
Every mechanism was checked against the official Bot Mode page, the Profiles page, the Profile Distributions page, the multi-connection guide and the Kanban page for the version installed while writing, plus the bundled files in the Hermes repository. Two operators who published early and detailed Bot Mode walkthroughs, Tonbi's AI Garage and Wanderloots, are quoted where their field experience adds something the docs do not, and always by name.
```

```table
| Build | You end up with | Checked against | Time |
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
```

### How to use a build

Same shape as the other volumes. **What you are building**, then **What the docs say** with the page named, then **Prompts** to paste into a Hermes chat and **Commands** for the terminal, then a **verify** list. The kit under `kits/bot-team/` holds one folder per bot: `SOUL.md`, `config.yaml`, `distribution.yaml`, `routines.sh` and a README.

## Build 0: What a Bot Is

![Build 0](assets/art/part-11.webp)

### What you are building

The model in your head that makes every later build obvious: what the roster shows, what a Bot Chat is, why `/new` does not work in it, what a routine and a room are, and the two markers that switch the whole machinery on.

### What the docs say

Checked against the Bot Mode page and the Profiles page.

```table
| Term | What it is |
| Profile | The persistent home for one agent's config, memory, skills, credentials and chat history: `~/.hermes/profiles/<name>/` |
| Bot | A profile presented in the roster with a title, an avatar, a section and a pinned canonical chat. Every Bot is a profile; a profile you only drive from the CLI or a gateway stays a plain profile |
| Bot Chat | The canonical, persistent conversation created the moment a Bot is born. Clicking the row always opens it. Typing `/new` or `/reset` inside it is rerouted to `/compact`, fresh working context in the same conversation, because forking the relationship is the one thing Bot Mode promises never happens |
| Routine | A recurring task attached to the Bot that does it. Under the hood it is a Hermes cron job named `[bot:<name>] <routine>`, so it also appears in `hermes cron list`; runs land in the Bot's own chat history |
| Room | A group chat of 2 to 6 Bots with one visible conversation, up to three serial rounds of member turns per message, and a needs-you badge when a Bot escalates with `@user` |
| Messaging bot | Different thing: an account on Telegram, Discord or Slack connected through the gateway |
| Subagent | Different thing: a child spawned by `delegate_task` with a fresh conversation, same profile |
| Warm backends | One backend process per local Bot. The cap is Settings, Advanced, Warm Bot Backends (default 3, "~60 MB each" in the page's words); idle backends are reaped after the timeout next to it, 10 minutes by default |
| Off switch | Bot Mode is a bundled desktop plugin; Capabilities, Plugins, Bots, Desktop switch. Your profiles, sessions and cron jobs are untouched either way |
```

**The two markers.** The messaging protocol and the `message_agent` tool are injected only when two conditions hold, and the Bots pane satisfies both the moment it creates a Bot: the session is titled exactly `Bot Chat`, and at least one profile on the install carries a `ui_meta: { hermes-bots: … }` block in its `profile.yaml`. That is why a headless install with no desktop never sees `message_agent`, and Build 5 gives the two lines that switch it on by hand.

```table
| In Bot Mode | From a shell |
| Chat with a Bot | `hermes -p <bot> chat` |
| A Bot's files, skills, memory | `~/.hermes/profiles/<bot>/` |
| Routines | `hermes cron list`, jobs named `[bot:<name>] …` |
| Create or inspect | `hermes profile create`, `hermes profile list` |
```

```callout kind=note title="From the field: Tonbi's first-day guide"
Tonbi's Bot Mode walkthrough, recorded the day after the feature shipped, says the same thing in one line: "Bots themselves are not necessarily new. They're just profiles. What has changed is how they can work together and communicate with one another." He calls the canonical chat the bot's "agent inbox", a dedicated session for agent-to-agent traffic. The docs call it the Bot Chat; it is the same thing.
```

### Prompts

```code lang=markdown file=prompt-b0-show-me-my-roster.md
Read https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode sections
"The Bots pane", "What actually makes a chat a Bot Chat" and "CLI parity".
Then run hermes profile list and, for each profile, tell me: whether it is a
Bot (does its profile.yaml carry a ui_meta hermes-bots block), whether it has
a session titled exactly "Bot Chat", its model, and how many cron jobs are
named [bot:<name>]. One table. Change nothing.
```

### Verify

```checklist
[ ] You can say in one sentence why /new does nothing in a Bot Chat and what it does instead
[ ] hermes cron list shows any routine you created in the app, named [bot:<name>]
[ ] hermes profile list matches the roster in the Bots tab
[ ] Settings, Advanced shows the Warm Bot Backends count and you know what happens when it is exceeded
```

## Build 1: Design the Roster

![The roster, and who talks to whom](assets/art/v3-message-paths.webp)

### What you are building

A roster written down before any bot exists: roles drawn from work you actually do every week, names that resolve as tags without colliding, a size the machine can keep warm, and a section layout that will still make sense in a month.

### What the docs say

Checked against the Bot Mode page: Creating a Bot, renamed Bots keep their tags in sync, Organize bots into sections, Warm Bot Backends, and the Kanban page's cost strategy.

```table
| Rule | Why |
| Roles come from repeated work | The docs' own examples are specialists: a researcher, a reviewer, a scribe. A Bot earns its place by owning a kind of work that recurs, because it accumulates memory and skills only for what it does repeatedly |
| Names are tags | A Bot titled Research Buddy answers to `@research-buddy` and `@researchbuddy`; the profile name is matched first and can never be hijacked by a friendly name; a friendly name shared by two Bots is refused. Pick short, distinct, pronounceable names |
| The primary stays `@hermes` | Rename it Maia and prompts introduce it as `@maia`, but `@hermes` keeps working as an alias for the primary |
| Start at the warm limit | Warm Bot Backends defaults to 3. A fourth open Bot waits up to 30 seconds for a slot. Start with three bots doing real work, raise the setting and the machine's memory together when you add more |
| Sections are yours | Folders like Clients or Team, stored in each Bot's profile metadata, so a section follows the Bot to every desktop connected to that backend |
| Planner and workers | The Kanban page's cost strategy applies to rosters: decomposing work needs frontier-level judgment, executing a well-specified card usually does not, and workers are where the tokens go. Restrict the planner's toolsets so it cannot do the implementation work itself |
```

### The roster this volume ships

```table
| Bot | Title | Owns | Talks to |
| atlas | Chief of staff | planning, routing, the standup, escalation to you | everyone; @user for decisions |
| scout | Researcher | finding out what is true, with sources | atlas, quill, forge on request |
| forge | Engineer | implementing well-specified changes, proving them | atlas for design questions, sentinel for review |
| quill | Writer | briefs, posts, docs, messages for a named reader | scout for missing facts, sentinel for review |
| sentinel | Reviewer | the last check before you: code, copy, plans, numbers | forge and quill with findings, atlas with blocks |
| ops | Operator | routines: briefs, sweeps, health, backups, weekly numbers | you, silently unless something is wrong |
```

Six is the full team. Three is the day-one team: atlas, forge and ops cover planning, doing and keeping the lights on. Add scout when research becomes a bottleneck, quill when you publish, sentinel when a mistake would cost you.

```callout kind=note title="From the field: let a bot design the roster"
Tonbi's most reusable idea is a meta-bot he calls bot HR, whose only job is to read a project brief and create the other bots for it, choosing their roles and models. His description for it was one sentence: "you are a bot who makes other bots based on project requirements and tells them their role." Handed a game spec, it split the work into render, gameplay, technical art and browser QA, created four profiles with a shared working directory, wrote each SOUL with a mission, and picked a different model for each with a stated reason. The gateway RPC the desktop uses for that, `profiles.create`, is documented on the Desktop Plugin SDK page, and the CLI twin is `hermes profile create`. Build 9 turns this into a prompt you can paste.
```

### Prompts

```code lang=markdown file=prompt-b1-design-my-roster.md
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

```checklist
[ ] Your roster document names at most five bots, each tied to work you did more than once this month
[ ] Every name is lowercase, one word, and unlike every other name when spoken aloud
[ ] Exactly one bot is the planner and its toolsets exclude the terminal
[ ] You know which three you are creating first
```

## Build 2: A Model per Bot

![The model ladder](assets/art/v3-model-ladder.webp)

### What you are building

A model, a provider and an effort level for each bot, chosen for the role and priced before the first message, plus the credential rule that decides whether a bot can even start.

### What the docs say

Checked against the Bot Mode page (Model and provider pin, Copy API keys), the Profiles page (Every profile owns its credentials), the Kanban page (Cost strategy) and the Configuration reference.

```table
| Fact | Detail |
| Per-bot pin | The New Agent dialog's Advanced section pins a provider and model per Bot; different Bots run different models side by side. Unset means inherit from the launch profile. In the profile it is `model.default` in that profile's config.yaml |
| Effort | `agent.reasoning_effort` per profile: none, minimal, low, medium, high, xhigh, max, ultra |
| Keys are copied, logins are not | Copy API keys from the main profile is on by default and copies static keys into the Bot's own credential store. Single-use OAuth logins (Anthropic, OpenAI Codex, xAI) are never copied; sign the Bot in itself with `hermes -p <bot> auth add <provider>` |
| Why | A named profile resolves providers from its own `auth.json` and `.env` only. A copied OAuth refresh token is the same credential with two owners, and the first refresh breaks the other |
| The split that pays | Planner on a frontier model, workers on inexpensive models, quality-sensitive work pinned back up per task. Workers are where the vast majority of tokens are spent |
```

### The decision table

```table
| Role | Model class | Effort | Why |
| Planner (atlas) | Frontier | high | Decomposition, routing and judgment are the expensive skills; the planner sends few tokens and each one steers many |
| Reviewer (sentinel) | Frontier or strong mid | high | A cheap reviewer approves cheap mistakes. This is the second place the money goes and the last place to save it |
| Engineer (forge) | Inexpensive coding model | medium | Well-specified cards are throughput work; a fast coding model on a card with a definition of done beats a frontier model on a vague one |
| Researcher (scout) | Mid model with strong web tools | medium | Reading and citing needs care, not genius; the browser and search tools matter more than the model |
| Writer (quill) | Mid model you like the voice of | medium | Voice is taste; pick the model whose prose you would sign |
| Operator (ops) | Inexpensive | low | Routines read tool output and format it; no reasoning budget needed |
| Anything touching private data | A local model | medium | Privacy is a property of where the tokens go, not of the prompt |
```

```callout kind=note title="From the field: a bot's own reasons"
When Tonbi's bot HR assigned models it explained itself. Gameplay code went to a high-throughput coding model because "gameplay is a large amount of iterative, relatively self-contained implementation work"; technical art went to a model it judged "suited to generative and creative implementation" because it had to "translate a detailed visual target into procedural geometry"; the WebGL lead got the strongest coding model available. His take: "interesting model choices, but you can see it's fairly well thought out." He also reports that the same project failed outright on a local model. Take both as data from one run, not as a rule.
```

### Commands

```code lang=bash file=models.sh
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

```code lang=markdown file=prompt-b2-price-the-roster.md
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

```checklist
[ ] Every bot has a model.default and an agent.reasoning_effort you chose, readable with hermes -p <bot> config show
[ ] The planner and the reviewer are on the strongest models; the operator on the cheapest
[ ] Any bot on an OAuth provider has completed its own sign-in and answers a test message
[ ] You have a per-day estimate written down to compare against hermes insights in a week
```

## Build 3: The Birth of a Bot

![Build 3](assets/art/part-01.webp)

### What you are building

Your first three bots, created either from the New Agent dialog or from its CLI twin, each with a SOUL written for its role, the right skills and toolsets ticked, and a first message that proves it knows who it is.

### What the docs say

Checked against the Bot Mode page (Creating a Bot, Edit Profile, Duplicate, Avatars) and the Personality page.

```table
| Fact | Detail |
| The quick path | New Agent in the roster: Name, Title, Description, and the Bot exists in seconds, introducing itself as the first message of its Bot Chat |
| Advanced | Clone from an existing profile or start fresh; Create empty to skip the bundled skills; Model and provider pin; Custom SOUL.md; per-skill, per-toolset and per-MCP-server enablement; Copy API keys from the main profile |
| Description matters twice | It is the Bot's role text in every other Bot's teammate roster, and it is what the kanban decomposer routes by. Write it as what the Bot is good at |
| Edit Profile | Right-click a Bot to reopen the same surface on the live profile: avatar, title, description, model pin, skills, toolsets, MCP servers, the full SOUL.md |
| Duplicate and Delete | Duplicate makes a full clone: config, skills, SOUL.md, memory, look. Delete Profile is behind a destructive confirmation; the default profile cannot be deleted |
| The CLI twin | `hermes profile create <name> --description "<role>"` with `--clone`, `--clone-from <source>` or `--no-skills` as needed, then edit `~/.hermes/profiles/<name>/SOUL.md` |
| What belongs in a SOUL | Tone, directness, how to handle uncertainty and disagreement, what to avoid. Not file paths or project rules; those go in AGENTS.md |
| Avatars | A deterministic blob face from the name, a geometric face, an uploaded image, an AI-generated portrait when an image backend is configured, or a pixel pet |
```

### The SOUL for a bot is the SOUL for a role

Volume 1 taught the shape: observable rules, a clear list of nevers, no project facts. A bot's SOUL adds one section at the top, the role, because the bot has to know what it owns and what it hands to whom. Here are two of the six from the kit; the others are in `kits/bot-team/`.

```code lang=markdown file=~/.hermes/profiles/atlas/SOUL.md
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

```code lang=markdown file=~/.hermes/profiles/forge/SOUL.md
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

```code lang=bash file=birth.sh
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

```callout kind=warn title="Take the terminal away from the planner"
The Kanban page recommends pairing the orchestrator profile with toolsets restricted to board operations so it "literally cannot execute implementation tasks even if it tries." The same rule keeps a chief of staff honest. If atlas has a terminal, one day it will fix something itself instead of routing it, and you will not know which bot to trust for what.
```

### Prompts

```code lang=markdown file=prompt-b3-first-words.md
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

```code lang=markdown file=prompt-b3-write-a-soul-for-a-role.md
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

```checklist
[ ] The three bots appear in the Bots tab with titles and their first message introduces the role you wrote
[ ] hermes -p atlas chat opens the same Bot Chat the roster row opens
[ ] Edit Profile on atlas shows the terminal toolset off
[ ] Each bot answered the first-words prompt with the right teammates
```
