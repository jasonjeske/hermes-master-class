## Build 7: The Cadence

![The company runs on routines you can read](assets/art/v4-cadence-wheel.webp)

### What you are building

The clock the company runs on: a standup that reads the board, a supervisor sweep that catches stalls, a Sunday page, a month end, a nightly dreaming pass and a health check that stays silent. All of it as routines you can list, read, pause and edit, owned by the bot that should own each. Plus the two places you look: the board and the standup room.

### What the sources say

```table
| Source | Their clock |
| HolmeBengt | 03:00 Dreaming, 06:30 Daily Status Report ("This is not the news. This is the tactical dashboard."), 12:00 Health Coach, 21:00 Study Audit, Saturdays writing analysis, Sunday 18:00 Finance Review, the 28th at 20:00 monthly P&L, every four hours infrastructure monitoring, every morning a compressed config backup |
| Gumroad | "cron jobs wake it up to check support tickets, watch X mentions, work on engineering tasks, update finance docs, and follow up on previous work" |
| Hermes Swarm | A supervisor that "periodically reviews each agent's transcripts" and nudges the stalled, the looping and the idle; a dashboard with a network graph of who is talking to whom |
| Tonbi's AI Garage | The orchestrator checks the room every twenty minutes and pushes anyone who has not started; the operator's own note is that with no tool calls visible in a room he kept doubting work was happening, and threads fixed it |
| stan_frbd | Daily lesson, daily backup "no LLM involved", daily wiki lint, daily dream, daily articles |
| Hermes docs and hermes cron create --help | A routine's --deliver can be bot-chat:<profile> (Cron page), which drops the output into that bot's Bot Chat as a message it answers; --monitor-script (in the command's own help, not yet on the docs page) runs a cheap script first and only wakes the model when its output changed byte for byte |
```

```callout kind=note title="Two tricks newer than every operator write-up"
Delivering a routine to bot-chat:atlas means the standup is not a report you read, it is a message atlas answers, in its own chat, with the board in front of it; it is also the only way a scheduled job reaches message_agent, which exists in Bot Chat sessions and nowhere else, so every kit routine that needs a teammate nudged is delivered to atlas rather than told to message anyone. And --monitor-script turns a noisy watch into a quiet one: a script prints the state, the model runs only when the bytes changed. The first is used throughout the kit's routines; the second is added by the quiet-watch prompt below.
```

### The routines the kit ships

```code lang=bash file=kits/company/cadence/routines.sh
CADENCE_ROUTINES_SH
```

### The two places you look

```table
| Place | What it shows | When |
| The Kanban page in the Desktop, or hermes kanban list and stats | every card, its owner, its status, its thread | any time, and at the standup |
| The standup room from Volume 3 (atlas, forge, scout, quill, sentinel) | the one conversation where the day gets settled, threads for side questions | 08:00, after atlas posts the standup line in its Bot Chat |
```

### Prompts

```code lang=markdown file=prompt-c7-install-the-clock.md
You are @ops. Read kits/company/cadence/routines.sh. For each routine
tell me: owner, schedule, what it reads, what it delivers, and its
silent condition. Flag any two routines that would collide (same hour,
same board reads) and any routine whose owner lacks a tool it needs.
Then show me the exact commands with <company folder> replaced by the
real path, and run them only when I say go. Afterward read back
hermes -p atlas cron list and hermes -p ops cron list and prove each job
exists by name.
```

```code lang=markdown file=prompt-c7-quiet-watch.md
You are @ops. Turn the health routine into a monitor: write
~/.hermes/scripts/health-state.sh that prints, one per line, gateway
status as a word, disk as ok or low against a 20 GB line (never the raw
number, the output must be byte-stable), and the reachability of the
always-on box from ORG.yaml as up or down. Then recreate the health routine with --monitor-script
health-state.sh so the model runs only when a line changes. Show me the
command first. Test by stopping nothing; just confirm two consecutive
ticks stayed silent.
```

```code lang=markdown file=prompt-c7-first-standup.md
@atlas @forge @scout @quill @sentinel Standup. atlas has posted the
board summary in its Bot Chat; each of you, one line: what you finished
since yesterday, what you are on, what you are blocked on, by card id.
Questions go in threads, not in the room. atlas closes with the one
decision that is mine today, or says there is none.
```

### Verify

```checklist
[ ] hermes -p atlas cron list and hermes -p ops cron list show every routine from the kit by name
[ ] The 08:00 standup arrived in atlas's Bot Chat and atlas answered it with the board open
[ ] The supervisor sweep nudged a card you had deliberately left running, and nothing else
[ ] The health routine stayed silent for a whole day on a healthy machine
[ ] The Sunday page and the month end both delivered even when nothing changed
```

## Build 8: Learn While You Run

### What you are building

The mechanism that makes the company better every week without you rewriting prompts: corrections become dated rules in POLICIES.md, repeated corrections become changes to a bot's own instructions, and repeated workflows become skills. This is the single most repeated pattern in the case file, and it is the one that separates operators who are still running from operators who quit.

### What the sources say

```table
| Source | The loop |
| Gumroad | "When Gumclaw makes a mistake, the correction becomes a dated policy rule that every future session must read." |
| HolmeBengt | "Every time I correct something Hermes wrote, the before-and-after gets saved to Notion with notes on what was wrong and why my version was better. On Saturdays, Hermes analyzes the full collection looking for patterns in my corrections. Then it updates its own system prompt to fix those patterns permanently." |
| riceinmybelly | MEMORY.md capped at 2,200 characters, his own convention rather than a Hermes limit, for behavioral rules only; lessons too detailed for it go to Meta/hermes-learnings/ in the vault. His own caveat on the whole setup: "nowhere near an example to follow" |
| aakashgupta | "it writes its own skills. My competitive briefing went from 20 min to 8 min over 6 weeks. Same prompt." |
| Yashica Jain | "Every time you do something, for example, using Hermes to write a LinkedIn post, it uses that experience to create a new skill." |
| Better Stack | "Brand new session test: it recalled everything, including preferred emojis." |
| Wanderloots | refine at the end of a session "will review the conversation and save what it needs to its own skills and memories"; @all plus an explicit memory instruction does it for a room. The orchestrator learned where raw reports go and never had to be told again |
| HolmeBengt, the warning | "Thirty-plus skills means thirty-plus things that can break when APIs or Hermes itself updates." |
```

```callout kind=note title="What the kit gives Build 8"
Three templates: kits/company/POLICIES.md for the fast loop, kits/company/corrections/README.md for the format of a saved correction, and kits/company/SKILLS-LEDGER.md for the skills you build and must retest after every update.
```

```callout kind=note title="Three files, three speeds"
POLICIES.md is the fast loop: one dated line the day something goes wrong, read by every bot before work. A bot's SOUL.md or MEMORY.md is the weekly loop: only after the same correction shows up three times does a rule move into the bot's own instructions, and MEMORY.md stays small on purpose. A skill is the slow loop: a workflow you have run five times the same way becomes a file with a name, and gets a line in the ledger of things that can break on the next update.
```

### Prompts

```code lang=markdown file=prompt-c8-correction-to-rule.md
You are @atlas. I just corrected <bot> on <what happened>. Write the
POLICIES.md line in the kit's format, dated today, naming the bot, the
rule and the why in one sentence each. Show me the line. When I approve,
append it, then message <bot> with message_agent: quote the new rule and
ask it to confirm in one line how its next similar task changes.
```

```code lang=markdown file=prompt-c8-saturday-patterns.md
You are @quill. Read every file in <company folder>/corrections/ (each
one holds a before, an after, and my note on why mine was better). Find
the patterns: filler words, wrong register for the channel, over-
explaining, invented specifics, anything that appears three times or
more. For each pattern propose the exact line to add to your SOUL.md
under Voice. Show me the proposals with the three examples behind each.
Change your SOUL only when I say which ones.
```

```code lang=markdown file=prompt-c8-workflow-to-skill.md
You are @<bot>. We have done <the workflow> the same way at least five
times; find the sessions with session_search and read how it actually
went. Write a skill with skill_manage: a name, when to use it, the steps
as we really run them, the checks that caught mistakes, and the output
format. Keep it to one job with no dependencies. Then run it once on
<a real input> and show me the result next to the last manual run. Add
the skill's name to <company folder>/SKILLS-LEDGER.md with today's date
and the Hermes version, so we know what to retest after an update.
```

```code lang=markdown file=prompt-c8-end-of-session.md
@all Before we close: each of you, update your own memory with anything
you learned in this session that will save a step next time. Say in one
line what you saved, or say nothing if there was nothing. atlas, check
that no two of you saved contradicting rules.
```

### Verify

```checklist
[ ] POLICIES.md has a rule dated this week that came from a real mistake, and the bot that made it confirmed the change
[ ] A Saturday pass over your corrections produced at least one SOUL.md line you accepted
[ ] One repeated workflow is now a skill, ran once on real input, and is listed in SKILLS-LEDGER.md with a version
[ ] MEMORY.md on every bot is still short after a month (riceinmybelly caps his at 2,200 characters; pick your line and hold it)
```

## Build 9: Ship the Company

### What you are building

The whole company as something that installs: the roster from Volume 3 as distributions, the company files from this volume in one repository, the routines as scripts, a backup that runs with no model, and the security lines that the case file's operators learned the hard way. The end state is that a fresh Mac with Hermes on it becomes your company in the time it takes to sign in to your providers.

### What the sources say

```table
| Source | What they did |
| RUDR9 | One installer, a fresh install becomes eight profiles plus a CTO. "Install time is about 30 seconds. The first version took 8 minutes because the ponytail skill was getting downloaded and security-scanned once per profile (8 times). Fixed by installing it once on the default profile before cloning." A Dockerfile "so you don't risk your own setup" |
| stan_frbd | A dedicated VM for Hermes, services on another, Cloudflare Tunnels with access restrictions, a daily git backup with no LLM involved. "Never run Hermes from your personal daily-use environment." |
| HolmeBengt | Full config compressed and backed up to iCloud every morning; two macOS users so the reading agent and the rest are "completely disconnected"; "There is no send endpoint anywhere in the system" |
| riceinmybelly | Three repositories backed up nightly, a launchd job copying the board database at 03:05, and "Hermes has no admin access to Gitea anywhere, I keep that hard." Also: "tons of security holes (which are kind of fine since it's local)", by his own edit |
| ogiberstein | The whole system on a VPS with fallback routing and a nightly backup to GitHub |
| Hermes docs | hermes backup zips configuration, skills, sessions and data; --quick snapshots critical state; the Profile Distributions page from Volume 3 is the install format; kanban.dispatch_profiles fences which assignees a home may claim |
```

```callout kind=warn title="Four lines from the operators, in order of how much they cost to learn late"
One. A dedicated environment: a user account, a VM, a mini, a VPS, never the machine you read your own mail on. Two. No send endpoint on the bot that reads everything; sending is a separate profile with its own approvals, if it exists at all. Three. The agent never holds admin on the thing that stores its backups. Four. Secrets live in each profile's .env and never in the repository you are about to create; sweep before the first push, because history is forever.
```

### The repository

```code lang=text file=company-repo-layout.txt
your-company/
  README.md                      how to install on a fresh machine, in ten lines
  COMPANY.md  ORG.yaml  POLICIES.md
  lines/                         one file per production line
  clients/<slug>/CLIENT.md       one per client; notes and drafts are NOT committed
  cadence/routines.sh            the clock
  life/routines.sh               your own week
  bots/<name>/                   SOUL.md, config.yaml, distribution.yaml, routines.sh (Volume 3's kit)
  scripts/                       backup.sh from the kit, plus spend-guard.sh and health-state.sh once written; installed to ~/.hermes/scripts/
  SKILLS-LEDGER.md               every self-built skill, with the version it was last tested on
  .gitignore                     .env, *.db, notes/, drafts/, journal/, anything a client sent
```

### Commands

```code lang=bash file=c9-commands.sh
# Install the roster on a fresh machine (Volume 3, Build 9), then sign in per bot.
for b in atlas forge scout quill sentinel ops; do hermes profile install ./bots/$b --name $b --alias; done
# Skills once, on default, before cloning anything: the RUDR9 lesson.
hermes skills install <your skill source>
# Company files where every bot can read them; ORG.yaml names the path.
mkdir -p "$HOME/company" && cp -R COMPANY.md ORG.yaml POLICIES.md lines cadence life "$HOME/company/"
# The clock (after replacing <company folder> in cadence/routines.sh with the real path).
sh cadence/routines.sh && sh life/routines.sh
# A backup with no model in it, nightly, owned by ops. Scripts must live under ~/.hermes/scripts/.
mkdir -p ~/.hermes/scripts && cp scripts/backup.sh ~/.hermes/scripts/backup.sh
hermes -p ops cron create "every day at 03:00" --no-agent --script backup.sh --name "backup-nightly"
hermes -p ops cron doctor      # reports missing scripts, so run it after every script job you create
# What may this machine claim from a shared board? Fence it.
hermes config set kanban.dispatch_profiles "atlas,forge,scout,quill,sentinel,ops"
# Prove it from a cold start.
hermes profile list && hermes cron list && hermes kanban stats && hermes memory status
```

### Prompts

```code lang=markdown file=prompt-c9-write-the-installer.md
You are @forge. Read this repository. Write scripts/install.sh that
takes a fresh machine with Hermes installed to a running company: profile
install for every bot, skills once on default before any clone, the
company folder in place, both routine scripts run, the backup job
created, kanban.dispatch_profiles fenced. Every step prints what it did
and stops on the first failure, and remember that hermes cron create can
exit 0 on failure, so read back hermes cron list and count. Do not
include any secret, any sign-in, or any client file. Show me the script;
I will run it on the spare machine.
```

```code lang=markdown file=prompt-c9-secrets-sweep.md
You are @sentinel. Before the first push of this repository, sweep it:
every file, for API keys, tokens, .env contents, OAuth JSON, client
names next to anything private, absolute paths that reveal a person or
a machine, and anything under notes/ or drafts/. List every hit with
file and line. Then propose the .gitignore. If you find one real secret,
say so first and stop; I rotate it before anything else happens.
```

```code lang=markdown file=prompt-c9-restore-drill.md
You are @ops. Prove the backup restores. Take the newest hermes backup
zip, unpack it under a scratch path, and tell me which of these it
contains: every profile's config.yaml, SOUL.md and MEMORY.md; the cron
jobs; the kanban database; the ledger database under plugin-data. For
anything missing, tell me what would restore it (the repository, a
re-install, or nothing). Do not restore over the live install.
```

### Verify

```checklist
[ ] A spare machine ran install.sh and ended with six profiles, the routines listed by name, and an empty board
[ ] The secrets sweep found nothing, and the .gitignore keeps notes, drafts, journal and .env out
[ ] The nightly backup ran with no model and the restore drill named what it contains
[ ] The bots run under a dedicated user or machine, and the one that reads your mail has no send tool
[ ] kanban.dispatch_profiles on every machine names only the bots that live there
```

## The Company Ledger

Everything this volume built, where it lives, and the one probe that proves it.

```table
| Build | Artifact | Where | Proof |
| 0 | The case, with limits | this volume | you can name the two removed posts and why the money claims are unaudited |
| 1 | Life routines | kits/company/life/routines.sh | the 06:30 brief arrived and was silent on an empty day |
| 2 | COMPANY.md, ORG.yaml, POLICIES.md | kits/company/ | one ORG node per profile; POLICIES.md has a dated rule |
| 3 | The chief of staff | atlas's SOUL.md plus kits/company/ATLAS-PROTOCOL.md | atlas delegated a paragraph instead of writing it |
| 4 | Production lines | kits/company/production/LINE-TEMPLATE.md, lines/ | a brief became a reviewed draft that waited at your gate |
| 5 | Clients | kits/company/clients/CLIENT-TEMPLATE.md and OFFER-TEMPLATE.md | a pre-call brief with sources; an invoice from the ledger |
| 6 | Money | the ledger plugin, hermes insights, spend-guard.sh | the Sunday page shows money in next to fleet cost |
| 7 | The cadence | kits/company/cadence/routines.sh | every routine listed by name; health silent all day |
| 8 | The learning loop | kits/company/POLICIES.md, corrections/README.md, SKILLS-LEDGER.md | a rule from a real mistake; a skill from a repeated workflow |
| 9 | The shipped company | the repository, install.sh, kits/company/scripts/backup.sh | a spare machine became the company from a cold start |
```

```callout kind=note title="What to read next"
Volume 1 for the agent under all of this, Volume 2 for the app and the plugins that give the company its pages, Volume 3 for the team. And the case file's own advice, from the operator with 28 routines: outline the goal and the constraints, let the agent draft, simplify, build the first version, test immediately because it never works the first time, fix and simplify again. One file, one job, no dependencies. That is the whole process.
```
