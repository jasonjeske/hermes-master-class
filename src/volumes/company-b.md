## Build 3: The Chief of Staff

### What you are building

One bot that owns the board and the cadence so you do not: atlas, already born in Volume 3, given a company protocol, a supervisor routine, and the rule that it never does the work itself. Every multi-bot setup in the case file, and both recorded Bot Mode teams, put one agent in this seat, whatever they called it.

### What the sources say

```table
| Source | The pattern |
| RUDR9 | The default profile acts as CTO: "The CTO creates tasks, the dispatcher spawns the assigned profile as a worker, results flow through task comments and linked dependencies. You see everything on the board." |
| Hermes Swarm | "Every team also has a supervisor agent that periodically reviews each agent's transcripts. If someone is stalled, looping, or idle while still owing work, the supervisor nudges them back on track so tokens aren't wasted." |
| ogiberstein | "My 'main agent' is my 'Chief of Staff' who has his own memory cross-project/workflow. Every 'project' has its own agent sub-profile with its own memory." |
| Wanderloots | The orchestrator's soul gained one line that changed its behavior: "always state the outcome, acceptance criteria, owner, deliverable, and stop condition." And a removal: it may not research, so it always delegates |
| Tonbi's AI Garage | Added the orchestrator after the plan existed and told it to check in every twenty minutes and push anyone who had not started |
```

```callout kind=note title="The seat is defined by what it cannot do"
atlas has no terminal. That was decided in Volume 3 and this build keeps it, because the Wanderloots recording shows exactly what happens otherwise: the generated soul claimed "taking real action, using tools to research, build, run, and verify things," and the operator had to cut it. A chief of staff with a shell becomes the busiest worker on the team and the board goes quiet. Authority here is the kanban toolset, message_agent in its Bot Chat, memory, session_search, and the file tools for the company folder, which is its notebook. No terminal, no code execution, no browser, and the kit's config.yaml disables them so the rule holds by construction. Anything that needs a shell, hermes insights or hermes kanban list, ops gathers and delivers into atlas's Bot Chat.
```

### The protocol atlas carries

```code lang=markdown file=kits/company/ATLAS-PROTOCOL.md
ATLAS_PROTOCOL_MD
```

### Prompts

```code lang=markdown file=prompt-c3-install-the-protocol.md
You are @atlas. Read kits/company/ATLAS-PROTOCOL.md and merge it into
your SOUL.md under "How you work", without removing what is there. Then
tell me, in your own words, what changed about how you will handle the
next request I give you, and what you are now not allowed to do. If any
line conflicts with your existing SOUL, show me both lines and ask.
```

```code lang=markdown file=prompt-c3-first-week-on-the-board.md
You are @atlas. Here is what the company needs done this week:
<paste the list, one item per line>. For each item state outcome,
acceptance criteria, owner, deliverable and stop condition, then create
the card with kanban_create: title, body carrying those five, assignee,
parent links where one item waits on another, workspace worktree for
code and dir:<absolute drafts path> for writing. Post the card ids with
owners. Do none of the work yourself. If an item is not clear enough to
write acceptance criteria for, ask me about that one item only.
```

```code lang=markdown file=prompt-c3-supervisor-dry-run.md
You are @atlas. Run the supervisor sweep once, now, by hand: list the
board with the kanban tools, find anything running over two hours or
blocked over a day, and draft the nudge you would send each owner with
message_agent. Show me the drafts and do not send them. Then tell me
whether the every-two-hours schedule in kits/company/cadence/routines.sh
is right for how this team actually works, and why.
```

### Verify

```checklist
[ ] atlas's SOUL.md carries the protocol and hermes -p atlas tools list shows no terminal
[ ] A week's work exists as cards with owners and links, created by atlas, none of them assigned to atlas
[ ] The supervisor sweep is in hermes -p ops cron list and its first real run nudged nobody who did not need it
[ ] You asked atlas to write a paragraph and it delegated to quill instead
```

## Build 4: Production Lines

![The gate is the product](assets/art/v4-production-line.webp)

### What you are building

The things your company makes, written down as lines: brief in, research, draft, review, your gate, publish, ledger entry. One file per line, one card per step, the same shape for a blog post, a client report, a video script or a software release. The front end is a brainstorming session that refuses bad ideas, the back end is a gate only you can open.

### What the sources say

```table
| Source | The line they run |
| cyrilXBT | "It researches the topic, writes the script, formats the slides, outputs in the exact dimensions TikTok needs. 10 slideshows a week manually takes 30-40 hours. With Hermes it takes the time to review and approve." |
| Metics Media | The exact routine prompt: "Research the top trending AI tools right now and come back with the top three that would make for an interesting tutorial video. Create a new skill based on your approach and call it YouTube-video-research. Can you set up a weekly job that runs every Monday at 9:00 AM using that skill?" |
| kenmazaika | Dictation on the phone, a dedicated Telegram topic, a structured outline with a "riff" section of connections, a local markdown file, then a document generated from it. "Automate the 97%, don't kill the project trying to automate the last 3%." |
| mvanhorn | "Weekly podcast digest replaced 10+ hrs of listening with a 2hr Hermes workflow." Content ops: blogs, cold emails, lead scraping |
| Wanderloots | Research, orchestrator quality check with one revision, human approval, librarian files it. The orchestrator rejected a first draft because "the evidence base is vendor authored and contains no 2026 study," and the operator agreed |
| Tonbi's AI Garage | A brainstorming skill the agent wrote itself over months: orient, research the reality, find the wedge, a verdict of yes, maybe or no, keep a living record, hand off a spec. "It's not sycophantic. It's not just going to be a yes man." |
```

```callout kind=note title="From the field: the idea goes in through a bot that says no"
Tonbi's brainstorming agent lives on a seven-year-old laptop, runs a mid-tier model because the frontier one "is way overkill for this, and it's too slow," and its whole job is to take a half-formed idea and pressure-test it against what exists, who pays, and what the smallest first offer would be. The output is a spec with five sections: original spark, destination, open uncertainty, validation plan, recommended first offer. His rule: the agent does not generate the idea, you bring it; the agent researches and challenges it. That spec is the brief a production line starts from.
```

### The file

```code lang=markdown file=kits/company/production/LINE-TEMPLATE.md
LINE_TEMPLATE_MD
```

### Prompts

```code lang=markdown file=prompt-c4-pressure-test-an-idea.md
You are @scout, acting as a brainstorming partner, not a cheerleader. I
have a half-formed idea: <one or two sentences>. Work in five moves.
Orient: ask me at most three questions that change what you would
research. Research the reality: who does this today, what they charge,
what the buyers complain about, with sources. Find the wedge: the
narrowest version a real person would pay for first. Verdict: yes, maybe
or no, with the reason, and change your verdict as evidence comes in.
Record: write <company folder>/ideas/<slug>.md with sections original
spark, destination, open uncertainty, validation plan, recommended first
offer. Do not flatter the idea. If it is a no, say so and say why.
```

```code lang=markdown file=prompt-c4-define-a-line.md
You are @atlas. We are going to make <the deliverable> repeatedly. Copy
kits/company/production/LINE-TEMPLATE.md to <company folder>/lines/<name>.md
with the file tools and fill it in from these facts: <where it lands, who
the reader is, what sources are allowed, the house voice, the cadence>.
Owners come from ORG.yaml. The gate step is always the human. Show me the
file and the one step you think will fail first and why.
```

```code lang=markdown file=prompt-c4-run-the-line-once.md
You are @atlas. Run <company folder>/lines/<name>.md once for this brief:
<paragraph>. Create one card per step with kanban_create, linked in
order so each waits on the previous, owners from the line file, the
review card carrying the definition of done from the line. When the
review card reaches done, message me with the verdict and the path to
the draft, and stop. Nothing publishes until I comment approve on the
gate card.
```

```code lang=markdown file=prompt-c4-weekly-research-watch.md
You are @scout. Create a routine on yourself: every Monday at 09:00,
research what changed in <the niche> in the last seven days, pick the
three items most worth making something about, and for each write two
lines: why now, and which production line it feeds. Save the result to
<company folder>/inbox/watch-<date>.md and deliver the three items to
atlas's Bot Chat. Show me the hermes cron create command before you run
it, with the schedule "every monday at 09:00" and --deliver bot-chat:atlas.
```

### Verify

```checklist
[ ] One line file exists with every step owned by a bot that has the tools that step needs
[ ] A brief went in and a reviewed draft came out without you touching a step between the brief and the gate
[ ] The gate card waited for your comment; nothing reached its destination before it
[ ] The first unit's cycle time and cost are written at the bottom of the line file
[ ] A bad idea got a no from the pressure test, with sources
```

## Build 5: Clients

### What you are building

The part of the company that talks to people who pay: research before every call, notes within the hour, proposals and invoices drafted from the books, one profile per client whose data must stay apart, and a send button that only you press. This is the build with the most money in the case file and the least evidence, so the limits are stated first.

### What the sources say

```table
| Source | The pattern | Treat as |
| mvanhorn | "Client research before calls saves 20-30 min every time. Meeting notes [to] follow-up drafts." | first-hand, self-reported |
| u/Elegant_Emergency859 (Reddit, July 2026), a web agency | A 50-page client PDF forwarded over Telegram; the agent cloned the repo, learned the i18n conventions, added the file, ran build, typecheck and all 48 tests, spawned a reviewer subagent, got APPROVED, opened a PR and pinged the human to merge. Twenty to thirty minutes of fiddly work, done while making coffee | first-hand, post intact |
| IBuzovskyi | "one Hermes profile per client, fully isolated, each gets their own SOUL.md, memory, cron. Charge $497/month per client to manage their workflows." | a single X post, quoted as curated in the official user stories |
| pacmanpill | EUR 2,700 in a month installing Hermes for French small businesses. The post is now removed; the surviving detail is a commenter's reply putting maintenance at EUR 200 per client per month with clients paying their own model use | second-hand, post removed |
| OkSucco, same thread | The same play with a Tailscale hub: "a beefy box sitting on prem that I can do whatever I want with," same 200 a month, "This will not last long" | first-hand comment |
| Voxandr, same thread | "Don't charge too low. at the end they are replacing employees and atleast we should save enough before we are out of job , replacing ourselves." (verbatim) | opinion |
| Silent-Nectarine6798, same thread | Asked whether clients raise GDPR. No answer survives | an open question |
| stan_frbd | "Never run Hermes from your personal daily-use environment. Give it a dedicated environment and keep clear separation between personal usage, work, and automation." | first-hand |
```

```callout kind=warn title="What nobody in the case file has shown"
No churn, no client who left, no security review, no answer to the data-protection question. The French installer reportedly disclaimed responsibility for the security of the setups he sold. If you sell this, the client template below has a compliance section for a reason: write down whose law applies, what you told the client about where their data is processed, and who is responsible for the install's security, before the first invoice. Those three lines are the difference between a service and a liability.
```

### The files

```code lang=markdown file=kits/company/clients/CLIENT-TEMPLATE.md
CLIENT_TEMPLATE_MD
```

```code lang=markdown file=kits/company/clients/OFFER-TEMPLATE.md
OFFER_TEMPLATE_MD
```

### Commands

```code lang=bash file=c5-commands.sh
# A client whose data must stay apart gets its own profile, cloned from the worker that will serve it.
hermes profile create acme --description "Client work for Acme only. Data lives in the Acme folder." --clone-from quill
# --clone-from copies config, .env, SOUL and skills, plus MEMORY.md and USER.md; a client profile starts with blank memory.
: > ~/.hermes/profiles/acme/memories/MEMORY.md; : > ~/.hermes/profiles/acme/memories/USER.md
# Sign in its providers separately; OAuth is never copied between profiles.
hermes -p acme auth add
# Plugins are not cloned either; the client profile records its own money.
hermes -p acme plugins enable ledger
# Give it the smallest toolset that does the work, then read it back.
hermes -p acme tools list
# Client work rides the board under a tenant, so one fleet serves many clients with separate workspaces.
hermes kanban create "Acme: monthly report" --assignee acme --tenant acme --workspace "dir:$HOME/company/clients/acme"
```

### Prompts

```code lang=markdown file=prompt-c5-before-the-call.md
You are @atlas. I have a call with <client> at <time>. Have @scout write
five lines on what changed for them since our last notes (their site,
their news, their market), each with a source, and write yourself the
open items from <client folder>/notes/, the promises we made, and three
questions worth asking. Deliver both to me in one message thirty minutes
before the call. Do not contact the client.
```

```code lang=markdown file=prompt-c5-after-the-call.md
You are @quill. Here are my raw notes from the <client> call: <paste or
dictate>. Write <client folder>/notes/<date>.md with decisions, promises
with dates, and open questions. Draft the follow-up email in my voice,
save it as <client folder>/drafts/<date>-followup.md, and tell atlas
which promises should become cards. Do not send anything.
```

```code lang=markdown file=prompt-c5-proposal-and-invoice.md
You are @quill. From <client folder>/CLIENT.md and the ledger
(ledger_report, category client:<slug>), draft two documents: a proposal
for <the new work> with scope, what is not included, price and terms in
the same format we used last time, and this month's invoice from the
ledger entries. Save both under <client folder>/drafts/. List every
number you used and where it came from. I send; you do not.
```

```code lang=markdown file=prompt-c5-scope-the-service.md
You are @atlas. Before we sell installs or managed workflows to anyone,
fill in kits/company/clients/OFFER-TEMPLATE.md as <company folder>/OFFER.md
from these constraints: what we install, what we maintain and how often,
what the client pays for themselves (their model use, their machine),
what we are responsible for and what we are not, where the client's data
is processed and under whose law, and how a client leaves with their
data. Use plain words. Mark every line you are unsure about and I will
answer them.
```

### Verify

```checklist
[ ] A client profile exists with its own sign-ins, blank memory files, the ledger plugin, and a toolset smaller than quill's
[ ] A pre-call brief arrived with sources before a real call, and you used at least one line of it
[ ] Notes were on disk within the hour and the follow-up draft waited for you to send it
[ ] Every invoice and payment for one client is in the ledger under client:<slug>
[ ] OFFER.md answers the data and responsibility questions the Reddit thread never did
```

## Build 6: Money

![If the fleet costs more than it earns, you will know on Sunday](assets/art/v4-money-loop.webp)

### What you are building

The books and the bill for the bots, in one loop: every dollar in and out goes through the ledger plugin from Volume 2, model spend comes from hermes insights per profile, and a Sunday routine puts both on one page with one recommended decision. The case file has the cheapest always-on setups on record and no cost figure for any multi-bot fleet. This build is how you become the first person who knows theirs.

### What the sources say

```table
| Source | The number or the mechanism |
| HolmeBengt | Finance Review, Sunday at 18:00 and the 28th at 20:00: income, expenses, liquid assets, burn rate versus budget weekly; P&L, month-over-month variance, net worth trajectory and savings rate monthly. Total cost about USD 17 a month, agreed to in a comment rather than stated; DeepSeek's API "way cheaper than using an account" |
| witcheer | "I've been running a 24/7 AI agent on a Mac Mini for 2 months. 18 cron jobs, 35 scripts, 6 custom skills, a structured context system that makes every session smarter than the last. Total cost: $21/month." |
| SquishyData | Twenty signals on plain cron append to a ledger; one agentic job triages it. The cheap layer is deterministic, only the triage spends a model |
| Hermes Swarm | "track costs with daily budget caps" |
| stan_frbd | "For everyday usage, you don't need the biggest models. I use GPT-5.4-mini by default. I use GPT-5.5 for orchestrating multiple agents and for important tasks" |
| Wanderloots | "I can delegate specific tasks or bots to local models so that a more powerful cloud agent like the orchestrator can delegate to local models to do most of the work and still maintain the same level of quality but significantly reduce the cost." |
| Hermes docs | hermes insights --days N reports tokens, cost, tool patterns and activity per session source; hermes cron create --no-agent --script runs a deterministic watchdog with no model at all |
```

```callout kind=note title="What the fleet costs is a routine, not a feeling"
Nobody in the case file reports a multi-bot number because nobody made a bot report it. Volume 3 already gave ops a weekly-numbers routine over hermes insights. This build gives the team the Sunday page that joins that number to the ledger: ops gathers the figures with the shell and delivers them into atlas's Bot Chat, atlas writes the page and the decision it implies: a model down, a bot retired, a price up.
```

### Commands

```code lang=bash file=c6-commands.sh
# The books: the ledger plugin from Volume 2, Build 8, enabled on the bots that record money.
hermes -p ops plugins enable ledger
hermes -p quill plugins enable ledger
# Record by voice or by chat; read back by month. --oneshot answers and exits; -q alone opens a session, and it never parses slash commands.
hermes -p ops chat --oneshot -q "Call ledger_add with amount 497.00, kind income, category client:acme, note September retainer, and confirm the id."
hermes -p ops chat --oneshot -q "Call ledger_report for this month and show me the table."
# The bill for the bots, per profile, last 7 days.
hermes insights --days 7
hermes -p forge insights --days 7
# A watchdog that costs nothing: a script under ~/.hermes/scripts/ that prints only when spend crosses a line.
hermes -p ops cron create "every day at 07:00" --no-agent --script spend-guard.sh --name "spend-guard"
```

### Prompts

```code lang=markdown file=prompt-c6-cost-per-bot.md
You are @ops, because this needs the shell. Run hermes insights --days 30
for every profile in hermes profile list. Table: bot, model, sessions,
tokens, cost, cost per card completed (from hermes kanban stats). Then
three recommendations with the saving each: a bot that could drop one
model tier, a routine that could run --no-agent, a bot whose sessions are
mostly idle chatter. Change nothing; atlas decides.
```

```code lang=markdown file=prompt-c6-sunday-page.md
You are @atlas. ops has posted this week's figures in your Bot Chat (or
I paste them here). Produce the Sunday page: money in and out this month
with the biggest three categories; fleet cost this week versus last;
cards shipped and blocked; the one number from COMPANY.md and its trend.
End with exactly one recommended decision and the number that would
change if I take it. One page. If nothing moved, say so in one line and
stop.
```

```code lang=markdown file=prompt-c6-spend-guard.md
You are @ops. Write ~/.hermes/scripts/spend-guard.sh: a script with no
model call that reads the last 24 hours of cost from hermes insights
--days 1, compares it to a line in <company folder>/budget.txt, and
prints one line only when the cost is over the line, otherwise prints
nothing. Test it twice: once with the line above today's spend (silent)
and once below it (one line). Then show me the hermes cron create
--no-agent --script command and wait.
```

### Verify

```checklist
[ ] ledger_report for this month matches your bank to the dollar for the entries you recorded
[ ] hermes insights gives you a number per bot, and the Sunday page shows it next to money in
[ ] The spend guard printed nothing on a normal day and one line when you lowered the budget
[ ] You made one decision from a Sunday page and wrote it into POLICIES.md or ORG.yaml
```
