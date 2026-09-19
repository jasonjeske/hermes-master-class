---
title: The Hermes Company Masterclass
subtitle: Volume 4 of the Hermes Agent Masterclass. Run your life, then your business, on a team of Hermes bots, built from what real operators actually run
why: Plenty of people say they run a company on Hermes. A few of them published enough detail to learn from. This volume turns those setups into files and prompts you can install, starting with your own week and ending with a company that ships while you sleep.
date: 2026-09-19
eyebrow: THE HERMES COMPANY · VOLUME 4
---

![The Hermes Company Masterclass](assets/art/v4-hero.webp)

## Orientation

Volumes 1 to 3 gave you the agent, the app and the team. This volume gives them a job. It is written in the order a real operator gets there: first your own week, because a founder who is the bottleneck of their own life never has the hours to run a company; then the company as an org chart of bots with decision rights and human gates; then the production lines that make and sell things; then the cadence and the numbers that tell you whether it is working.

Everything here is grounded in named, public setups. The official Hermes user stories corpus holds 326 stories; the ones that describe a business, an agency, a content operation or a whole life were opened at the source (Reddit threads, X posts, GitHub repositories, blogs) and are quoted by handle. Where a source has been removed or a number is self-reported, the text says so. Nothing is invented, and the honest limits are listed in Build 0 before anything else.

```callout kind=warn title="Read this before you copy anyone"
No revenue figure in this volume is audited. Two of the most-cited business posts have been deleted from Reddit and survive only as the Hermes team's curated quotes. No operator reports churn, a rollback, or a security review. The setups are real and the mechanisms are reusable; the money claims are one person's word. This volume teaches the mechanisms.
```

```table
| Build | You end up with | Grounded in | Time |
| 0 | The case: what people actually run, what it costs, what nobody has proven | 13 named cases | 20 minutes |
| 1 | Life first: inbox, calendar, health, money and the weekly review, as bots and routines | HolmeBengt, SquishyData, stan_frbd | 90 minutes |
| 2 | The company blueprint: a charter, an org of bots, decision rights, human gates | Jinn, RUDR9, ogiberstein | 60 minutes |
| 3 | The chief of staff: your planner bot owning the board and the cadence | RUDR9, Hermes Swarm | 45 minutes |
| 4 | Production lines: content, products, education, from research to a publish gate | cyrilXBT, Metics, kenmazaika | 90 minutes |
| 5 | Clients: research before calls, proposals, notes, invoices behind a gate | mvanhorn, IBuzovskyi, pacmanpill | 60 minutes |
| 6 | Money: the ledger as the books, a weekly P&L routine, what the fleet costs | HolmeBengt, witcheer, Volume 2's ledger | 45 minutes |
| 7 | The cadence: standup room, weekly review, monthly retro, the dashboard | Hermes Swarm, Gumroad | 45 minutes |
| 8 | Learn while you run: corrections become files, skills become SOPs | Gumroad, HolmeBengt, riceinmybelly | 45 minutes |
| 9 | Ship the company: one repo installs the whole roster; backups, security, the always-on box | RUDR9, stan_frbd | 60 minutes |
```

### How to use a build

Same shape as the other volumes: what you are building, what the sources say (here, cases rather than docs, with the Hermes docs cited where a mechanism needs it), prompts to paste, commands to run, a verify list. The kit under `kits/company/` holds the charter template, the org file, the policy-rules file and the life-ops routines. Volume 3's six bots are assumed; this volume adds the files that give them a company to run.

## Build 0: The Case

![Build 0](assets/art/part-02.webp)

### What you are building

A clear picture, from named operators, of what running a business on Hermes looks like day to day: the hardware it runs on, the shape of the fleets, the costs people attest to, and the eight mechanisms that repeat across every serious setup.

### What the sources say

Thirteen cases carry this volume. Nine were opened at the source (Reddit threads, GitHub repositories, blogs, the recorded videos); the four marked "curated" are X posts quoted as the Hermes documentation team curated them for the official user stories, and were not opened here.

```table
| Operator | What runs | The transferable mechanism |
| @scotty529 (X, July 2026, curated), a Gumroad operation | An agent named Gumclaw on a dedicated Mac, woken by cron to check support tickets, watch X mentions, do engineering tasks, update finance docs, and follow up on earlier work | "When Gumclaw makes a mistake, the correction becomes a dated policy rule that every future session must read." |
| u/HolmeBengt (Reddit, June 2026) | 28 cron jobs and 30 or more self-built skills on a Mac mini running a local model 24/7 plus a VPS: a 3 AM Dreaming job, a local mail gatekeeper that never sends, a health coach, a finance review, infrastructure checks, a 6:30 AM tactical report | "Each skill is one file, one job, no dependencies." Attested cost about 17 dollars a month, agreed to a commenter's figure |
| u/humanth-shashani, RUDR9 (Reddit and GitHub, July 2026, MIT) | One installer that turns a fresh Hermes into what the post counts as eight specialist profiles plus a CTO (it lists seven: planner, architect, version control, builder, security auditor, performance auditor, reviewer), coordinated through the built-in kanban board | "Authority is enforced by toolset restrictions, not just system prompt instructions. The planner profile doesn't have the file write tool." |
| u/TotalGod, Jinn (Reddit and GitHub, July 2026, MIT) | A self-hosted workspace that treats agents as "a small local company": employees are YAML org nodes with a role, an engine and a model; work moves through chat, sessions, cron and a board | "The goal is not to replace coding agents. It's to give them a shared operating layer: who owns what, what is in progress, what needs review, and what got handed off." |
| u/Upset_Simple_4858, Hermes Swarm (Reddit and GitHub, June 2026) | Teams of full Hermes agents running 24/7 for a SaaS's marketing: blog posts, social, prospect lists, email outreach; each agent has its own terminal, browser and shared filesystem | "Every team also has a supervisor agent that periodically reviews each agent's transcripts. If someone is stalled, looping, or idle while still owing work, the supervisor nudges them." Decisions, approvals and credentials route to a human inbox |
| u/stan_frbd (Reddit, July 2026), a DFIR analyst | Three profiles, work, personal coach and homelab guardian, each with its own Telegram bot; daily lesson, backup, wiki lint and dream crons; a mini PC running Proxmox | "Never run Hermes from your personal daily-use environment. Give it a dedicated environment and keep clear separation between personal usage, work, and automation." |
| u/SquishyData (Reddit, July 2026) | About twenty cron "signals" that only append to a daily ledger, then one agentic job that triages the ledger and notifies whoever needs to know | The cheap layer is deterministic; only the triage step spends a model |
| u/kenmazaika (Reddit, July 2026), a content business | Phone dictation into a Telegram topic, shaped by Hermes into a structured outline with a section of connections he did not see, saved locally | "Automate the 97 percent, don't kill the project trying to automate the last 3 percent." |
| u/Godzillaton (Reddit, June 2026), construction | Eleven WhatsApp site groups read through a self-hosted WhatsApp API on an 8 GB laptop, summarized to three lines, with scheduled outbound messages, controlled from Telegram | "82 WhatsApp messages boiled down to 3 lines." |
| u/pacmanpill (Reddit, June 2026, post since removed) | Installing and adapting Hermes for French small businesses, reported at about 2,700 euros in a month; a commenter cites 200 euros a month per client for maintenance | The value, per the surviving quote, "is not just installing an AI agent. It's adapting it to the company's real workflows." A GDPR question in the thread never got an answer |
| @IBuzovskyi (X, May 2026, curated) | "One Hermes profile per client, fully isolated, each gets their own SOUL.md, memory, cron," at a stated 497 dollars a month per client | The client boundary is a profile |
| @ogiberstein (Discord, curated) | A Chief of Staff agent with cross-project memory, one sub-profile per project where one project is one Slack channel, on a VPS with backup routing | The planner is a separate agent from the doers |
| @witcheer (X, March 2026, curated) | A 24/7 agent on a Mac mini for two months: 18 cron jobs, 35 scripts, 6 skills, "a structured context system that makes every session smarter than the last," at a stated 21 dollars a month | Always-on is a small machine and a small bill |
```

### The eight mechanisms that repeat

```table
| Mechanism | Who does it | Where this volume builds it |
| Corrections become files, not chat | Gumroad's dated policy rules, HolmeBengt's Saturday rewrite of his own prompt from saved corrections, riceinmybelly's lessons folder (his own verdict on his setup: "nowhere near an example to follow") | Build 8 |
| Cheap deterministic collection, expensive selective triage | SquishyData's ledger, HolmeBengt's local mail judge | Builds 1 and 7 |
| One profile per boundary | stan_frbd's three lives, IBuzovskyi's one profile per client | Builds 2 and 5 |
| Authority by removing tools, not by asking nicely | RUDR9's planner without file write and auditor without terminal | Builds 2 and 3 |
| A board plus a dispatcher, not agents talking freely | RUDR9, Jinn, riceinmybelly | Build 3 |
| A supervisor that reads transcripts and nudges | Hermes Swarm | Build 7 |
| The human gate is the design | kenmazaika's 97 percent, Hermes Swarm's inbox and browser handoff | every build |
| Always-on is small | Mac minis, an 8 GB laptop, a mini PC, a cheap VPS; attested bills of 17 and 21 dollars a month | Build 9 |
```

```callout kind=info title="What nobody has proven"
No audited revenue. No client counts over time. No churn, no rollback, no security review. Several stories in the official corpus are feature requests filed alongside running systems. A second removed post, a "Twin AI" for a physical-product business, is left out of this volume for that reason. And riceinmybelly, cited here for his three-layer memory and his backups, prefaced his own write-up with "this is nowhere near an example to follow. It is messy, has tons of security holes"; he is quoted for mechanisms, never as a setup to copy. The mechanisms above are real and repeat across independent operators; treat every dollar figure as one person's report until your own ledger says otherwise.
```

### Prompts

```code lang=markdown file=prompt-c0-what-would-i-run.md
Read these two public write-ups and summarize each in five lines: what
runs, on what hardware, which pieces are cron and which are agents, how
the human stays in the loop, and what the author warns about.
- https://www.reddit.com/r/hermesagent/comments/1udesr1/
- https://github.com/ardhaecosystem/RUDR9
Then look at my own last four weeks (session_search) and tell me which of
their mechanisms I am already doing by hand, and which single one would
save me the most hours if a routine did it. Change nothing.
```

### Verify

```checklist
[ ] You can name the operator behind each of the eight mechanisms without looking
[ ] You wrote down the one mechanism you will build first and why
[ ] You know which source in this build is a deleted post, which second deleted post was left out, and why neither is cited for detail
```

## Build 1: Life First

![Build 1](assets/art/part-03.webp)

### What you are building

The personal operations layer that buys back the hours: the ops bot from Volume 3 running your inbox sweep, calendar prep, health log, money ledger and a weekly review, with a human gate on anything that leaves the machine.

### What the sources say

```table
| Source | The pattern |
| HolmeBengt's Daily Status Report at 6:30 AM | Calendar and what needs preparation, open to-dos, system health, anomalies from the overnight run. "This is not the news. This is the tactical dashboard." |
| HolmeBengt's Mail Gatekeeper | A local model judges mail as safe or blocked; blocked means 2FA codes, logins, password resets, bank transactions, spam; safe mail lands in a Telegram topic; an evening watchdog reviews the blocked folder for false positives. "There is no send endpoint anywhere in the system, Hermes can read and draft, but nothing can physically leave the machine" |
| HolmeBengt's Health Coach at noon | Wearable recovery and sleep, phone steps and resting heart rate, a self-built food log fed by Telegram text, photo or barcode, checked against a calorie and protein target |
| HolmeBengt's Finance Review | Sundays at 6 PM weekly, the 28th monthly: income, expenses, liquid assets, burn rate versus budget, month-over-month variance, savings rate, "delivered with voice" |
| SquishyData's signals | Twenty cron skills append to a daily ledger; one agentic job triages it; forwarding goes "to whoever can help or needs to know" |
| stan_frbd | A personal-coach profile for gym, running and nutrition, separate from work, with its own Telegram bot |
| kenmazaika | Dictate messy ideas from the phone into a Telegram topic; Hermes returns a structured outline plus a "riff" of connections; saved locally |
```

The Hermes mechanisms underneath: cron routines with `[SILENT]` (Volume 1, Build 8), the ledger plugin (Volume 2, Build 7), a profile per boundary (Volume 3), and the Telegram gateway for the phone (Volume 1, Part 7).

### The life routines the kit ships

```code lang=bash file=kits/company/life/routines.sh
LIFE_ROUTINES
```

```callout kind=warn title="Two gates that are not optional"
Nothing in these routines sends mail, moves money or messages another person. Drafts, yes; sends, no. HolmeBengt built that as an architectural fact rather than a rule, by having no send endpoint at all. If you later give a bot a send tool, it goes on a separate profile with its own approvals, never on the one that reads everything.
```

### Prompts

```code lang=markdown file=prompt-c1-design-my-week.md
You are @ops. Design my personal operations layer from evidence. Read my
calendar for the last four weeks if you have a tool for it, otherwise ask
me for the five things that recur weekly. Then propose at most six
routines, each with: name, schedule, the exact self-contained prompt, the
silent condition, and the delivery target. Rules: nothing sends, posts,
pays or deletes; anything that would needs a human gate and a separate
profile. Show me the hermes cron create commands. Do not create them until
I say go.
```

```code lang=markdown file=prompt-c1-dictation-inbox.md
Set up the dictation inbox. Read
https://hermes-agent.nousresearch.com/docs/user-guide/messaging and tell
me how to give a Telegram topic its own handling, then write the standing
instruction for it: when a long dictated message arrives, shape it into a
structured outline, add a short section of connections to things I have
said before (session_search), save it as a markdown file under
<path>/inbox/<date>-<slug>.md, and reply with the file path and a
three-line summary. Never act on the content; only structure it.
```

### Verify

```checklist
[ ] A 6:30 AM brief arrives on your phone with calendar, to-dos and health, and is silent on empty days
[ ] Money recorded by voice through the ledger tools shows up in the Sunday review
[ ] A dictated ramble from your phone comes back as a structured file within a minute
[ ] Nothing in the life layer has a send tool; you checked each profile's toolsets
```

## Build 2: The Company Blueprint

![The org, as bots](assets/art/v4-org-chart.webp)

### What you are building

Three files that turn a roster into a company: a charter that says what the company is for and what only you decide; an org file that names every bot, its role, its model and what it may touch; and a policy-rules file that every bot reads and that grows every time something goes wrong.

### What the sources say

```table
| Source | The pattern |
| Jinn | "You define an org: employees are YAML org nodes; each employee has a role, engine, and model; skills are separate reusable workflows; work can move through chat, sessions, cron jobs, and a Kanban-style board." |
| RUDR9 | Nine roles, coordinated through the kanban board; authority by toolset restriction; an honest limitations section; and a reviewer who told the author nine roles was over-engineered and three would do |
| ogiberstein | A Chief of Staff with cross-project memory; one sub-profile per project |
| @code_rams | "A smarter model will not give you an AI cofounder. What the agent is allowed to own will." |
| @shannholmberg | A maturity ladder: "once a workflow is solid, break it out into its own agent with its own credentials, memory and scope." |
```

```callout kind=note title="ORG.yaml is a planning file, not a Hermes setting"
Hermes has no org file. Jinn and RUDR9 each invented their own way to write the org down, and so does this kit: `ORG.yaml` is the document your chief-of-staff bot reads at the start of every planning routine, and the source of truth you edit when the company changes. The Hermes-native truth stays where Hermes keeps it: profiles, SOULs, toolsets, cron jobs, the board. The prompts in this build keep the two in step.
```

### The files

```code lang=markdown file=kits/company/COMPANY.md
COMPANY_MD
```

```code lang=yaml file=kits/company/ORG.yaml
ORG_YAML
```

```code lang=markdown file=kits/company/POLICIES.md
POLICIES_MD
```

### Prompts

```code lang=markdown file=prompt-c2-write-the-charter.md
You are @atlas. Interview me in three short rounds and then write
COMPANY.md from the kit template. Round one: what the company makes and
for whom, in plain words, and the one number that tells us it is working.
Round two: the decisions that are mine alone (money out, publishing,
hiring a bot, deleting anything, anything with my name on it). Round
three: the lines we never cross. Then show me the file, and separately the
list of things I said that belong in ORG.yaml instead.
```

```code lang=markdown file=prompt-c2-org-from-roster.md
You are @ops, because this needs the shell; atlas owns the file and will
write it from your findings. Read kits/company/ORG.yaml and run
hermes profile list and hermes -p <bot> tools list for each bot. For every
bot in the roster draft its ORG.yaml node: role, what it owns, model
and effort from its config, toolsets as they are actually enabled, who it
reports to, and the human gates that apply to it. Flag every place the
file and the install disagree (a toolset ORG.yaml forbids that the profile
has, a bot in the roster with no node). Propose the fix on whichever side
is wrong. Change nothing until I say go.
```

### Verify

```checklist
[ ] COMPANY.md names the product, the customer, the one number, and the decisions that are yours alone
[ ] ORG.yaml has one node per bot in hermes profile list, and the toolsets in it match Edit Profile
[ ] POLICIES.md exists, is loaded by every bot (a line in each SOUL), and has at least one dated rule
[ ] The planner's node has no terminal and the file says why
```
