# Build 0: The Case

![Build 0](../assets/art/part-02.webp)

### What you are building

A clear picture, from named operators, of what running a business on Hermes looks like day to day: the hardware it runs on, the shape of the fleets, the costs people attest to, and the eight mechanisms that repeat across every serious setup.

### What the sources say

Thirteen cases carry this volume. Nine were opened at the source (Reddit threads, GitHub repositories, blogs, the recorded videos); the four marked "curated" are X posts quoted as the Hermes documentation team curated them for the official user stories, and were not opened here.

| Operator | What runs | The transferable mechanism |
|---|---|---|
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

### The eight mechanisms that repeat

| Mechanism | Who does it | Where this volume builds it |
|---|---|---|
| Corrections become files, not chat | Gumroad's dated policy rules, HolmeBengt's Saturday rewrite of his own prompt from saved corrections, riceinmybelly's lessons folder (his own verdict on his setup: "nowhere near an example to follow") | Build 8 |
| Cheap deterministic collection, expensive selective triage | SquishyData's ledger, HolmeBengt's local mail judge | Builds 1 and 7 |
| One profile per boundary | stan_frbd's three lives, IBuzovskyi's one profile per client | Builds 2 and 5 |
| Authority by removing tools, not by asking nicely | RUDR9's planner without file write and auditor without terminal | Builds 2 and 3 |
| A board plus a dispatcher, not agents talking freely | RUDR9, Jinn, riceinmybelly | Build 3 |
| A supervisor that reads transcripts and nudges | Hermes Swarm | Build 7 |
| The human gate is the design | kenmazaika's 97 percent, Hermes Swarm's inbox and browser handoff | every build |
| Always-on is small | Mac minis, an 8 GB laptop, a mini PC, a cheap VPS; attested bills of 17 and 21 dollars a month | Build 9 |

> ℹ️ **What nobody has proven**
>
> No audited revenue. No client counts over time. No churn, no rollback, no security review. Several stories in the official corpus are feature requests filed alongside running systems. A second removed post, a "Twin AI" for a physical-product business, is left out of this volume for that reason. And riceinmybelly, cited here for his three-layer memory and his backups, prefaced his own write-up with "this is nowhere near an example to follow. It is messy, has tons of security holes"; he is quoted for mechanisms, never as a setup to copy. The mechanisms above are real and repeat across independent operators; treat every dollar figure as one person's report until your own ledger says otherwise.

### Prompts

*`prompt-c0-what-would-i-run.md`*

```markdown
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

- [ ] You can name the operator behind each of the eight mechanisms without looking
- [ ] You wrote down the one mechanism you will build first and why
- [ ] You know which source in this build is a deleted post, which second deleted post was left out, and why neither is cited for detail

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-COMPANY.md)
