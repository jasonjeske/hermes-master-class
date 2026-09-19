# Build 9: Ship the Company

### What you are building

The whole company as something that installs: the roster from Volume 3 as distributions, the company files from this volume in one repository, the routines as scripts, a backup that runs with no model, and the security lines that the case file's operators learned the hard way. The end state is that a fresh Mac with Hermes on it becomes your company in the time it takes to sign in to your providers.

### What the sources say

| Source | What they did |
|---|---|
| RUDR9 | One installer, a fresh install becomes eight profiles plus a CTO. "Install time is about 30 seconds. The first version took 8 minutes because the ponytail skill was getting downloaded and security-scanned once per profile (8 times). Fixed by installing it once on the default profile before cloning." A Dockerfile "so you don't risk your own setup" |
| stan_frbd | A dedicated VM for Hermes, services on another, Cloudflare Tunnels with access restrictions, a daily git backup with no LLM involved. "Never run Hermes from your personal daily-use environment." |
| HolmeBengt | Full config compressed and backed up to iCloud every morning; two macOS users so the reading agent and the rest are "completely disconnected"; "There is no send endpoint anywhere in the system" |
| riceinmybelly | Three repositories backed up nightly, a launchd job copying the board database at 03:05, and "Hermes has no admin access to Gitea anywhere, I keep that hard." Also: "tons of security holes (which are kind of fine since it's local)", by his own edit |
| ogiberstein | The whole system on a VPS with fallback routing and a nightly backup to GitHub |
| Hermes docs | hermes backup zips configuration, skills, sessions and data; --quick snapshots critical state; the Profile Distributions page from Volume 3 is the install format; kanban.dispatch_profiles fences which assignees a home may claim |

> ⚠️ **Four lines from the operators, in order of how much they cost to learn late**
>
> One. A dedicated environment: a user account, a VM, a mini, a VPS, never the machine you read your own mail on. Two. No send endpoint on the bot that reads everything; sending is a separate profile with its own approvals, if it exists at all. Three. The agent never holds admin on the thing that stores its backups. Four. Secrets live in each profile's .env and never in the repository you are about to create; sweep before the first push, because history is forever.

### The repository

*`company-repo-layout.txt`*

```text
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

*`c9-commands.sh`*

```bash
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

*`prompt-c9-write-the-installer.md`*

```markdown
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

*`prompt-c9-secrets-sweep.md`*

```markdown
You are @sentinel. Before the first push of this repository, sweep it:
every file, for API keys, tokens, .env contents, OAuth JSON, client
names next to anything private, absolute paths that reveal a person or
a machine, and anything under notes/ or drafts/. List every hit with
file and line. Then propose the .gitignore. If you find one real secret,
say so first and stop; I rotate it before anything else happens.
```

*`prompt-c9-restore-drill.md`*

```markdown
You are @ops. Prove the backup restores. Take the newest hermes backup
zip, unpack it under a scratch path, and tell me which of these it
contains: every profile's config.yaml, SOUL.md and MEMORY.md; the cron
jobs; the kanban database; the ledger database under plugin-data. For
anything missing, tell me what would restore it (the repository, a
re-install, or nothing). Do not restore over the live install.
```

### Verify

- [ ] A spare machine ran install.sh and ended with six profiles, the routines listed by name, and an empty board
- [ ] The secrets sweep found nothing, and the .gitignore keeps notes, drafts, journal and .env out
- [ ] The nightly backup ran with no model and the restore drill named what it contains
- [ ] The bots run under a dedicated user or machine, and the one that reads your mail has no send tool
- [ ] kanban.dispatch_profiles on every machine names only the bots that live there

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-COMPANY.md)
