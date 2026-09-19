# Build 5: Clients

### What you are building

The part of the company that talks to people who pay: research before every call, notes within the hour, proposals and invoices drafted from the books, one profile per client whose data must stay apart, and a send button that only you press. This is the build with the most money in the case file and the least evidence, so the limits are stated first.

### What the sources say

| Source | The pattern | Treat as |
|---|---|---|
| mvanhorn | "Client research before calls saves 20-30 min every time. Meeting notes [to] follow-up drafts." | first-hand, self-reported |
| u/Elegant_Emergency859 (Reddit, July 2026), a web agency | A 50-page client PDF forwarded over Telegram; the agent cloned the repo, learned the i18n conventions, added the file, ran build, typecheck and all 48 tests, spawned a reviewer subagent, got APPROVED, opened a PR and pinged the human to merge. Twenty to thirty minutes of fiddly work, done while making coffee | first-hand, post intact |
| IBuzovskyi | "one Hermes profile per client, fully isolated, each gets their own SOUL.md, memory, cron. Charge $497/month per client to manage their workflows." | a single X post, quoted as curated in the official user stories |
| pacmanpill | EUR 2,700 in a month installing Hermes for French small businesses. The post is now removed; the surviving detail is a commenter's reply putting maintenance at EUR 200 per client per month with clients paying their own model use | second-hand, post removed |
| OkSucco, same thread | The same play with a Tailscale hub: "a beefy box sitting on prem that I can do whatever I want with," same 200 a month, "This will not last long" | first-hand comment |
| Voxandr, same thread | "Don't charge too low. at the end they are replacing employees and atleast we should save enough before we are out of job , replacing ourselves." (verbatim) | opinion |
| Silent-Nectarine6798, same thread | Asked whether clients raise GDPR. No answer survives | an open question |
| stan_frbd | "Never run Hermes from your personal daily-use environment. Give it a dedicated environment and keep clear separation between personal usage, work, and automation." | first-hand |

> ⚠️ **What nobody in the case file has shown**
>
> No churn, no client who left, no security review, no answer to the data-protection question. The French installer reportedly disclaimed responsibility for the security of the setups he sold. If you sell this, the client template below has a compliance section for a reason: write down whose law applies, what you told the client about where their data is processed, and who is responsible for the install's security, before the first invoice. Those three lines are the difference between a service and a liability.

### The files

*`kits/company/clients/CLIENT-TEMPLATE.md`*

```markdown
# Client: <name>

One folder per client, one profile per client when their data must stay apart. Copy to <company folder>/clients/<slug>/CLIENT.md.

## Boundary
- Profile: <slug> (hermes profile create <slug> --description "..."), or "shared" when nothing here is confidential
- Data lives in: <absolute path to the client folder>; nothing about this client is stored anywhere else
- Tools this client's profile has: <the smallest list that does the work>
- Never: send on the client's behalf, log in as the client, store their credentials in a chat

## What we do for them
- Offer: <the service in one sentence>
- Cadence: <weekly, monthly, on request>
- Price and terms: <amount, currency, billing day, what is included>
- The number they care about: <what they will judge us on>

## Before every call
- scout: what changed for them since last time (their site, their news, their market), five lines with sources
- atlas: open items from the last notes, promises we made, questions to ask
- Delivered to the human 30 minutes before the call, in one message

## After every call
- Notes in <client folder>/notes/<date>.md within the hour: decisions, promises, dates
- Follow-up draft written by quill, sent by the human only
- New work becomes cards with this client's tenant on the board

## Money
- Every invoice and every payment is a ledger_add entry with category client:<slug>
- Invoices are drafted by quill from the ledger and this file; the human sends them
- Model spend for this client's profile is read from hermes insights and compared with the price monthly

## Notes on compliance
- Whose data protection rules apply: <country and law>
- What we told the client about where their data is processed: <the sentence, dated>
- Who is responsible for the security of the install: <written down, agreed, signed>
```

*`kits/company/clients/OFFER-TEMPLATE.md`*

```markdown
# The offer

What we sell when we install or run Hermes for someone else. Written before the first invoice, because the case file shows the questions nobody answered.

## What we install
- <the profiles, the routines, the integrations, in plain words>

## What we maintain, and how often
- <updates, gateway restarts, routine health, skill retests after an update>
- Response time: <hours or days>

## What the client pays for themselves
- Their model use (their own keys or subscriptions), their machine or VPS, any paid data source

## What we are responsible for, and what we are not
- We are: <the install working as described, the routines running, the backups existing>
- We are not: <the client's model bills, decisions the client makes on the agent's output, the security of accounts the client connects>

## Where the client's data is processed, and under whose law
- Processing: <on their machine only | on our machine | at these model providers>
- Law: <country; the data protection rules that apply>
- What we told them, in one sentence, dated: <...>

## Security of the install
- Who holds admin on the machine: <...>
- Who can read the agent's memory and sessions: <...>
- What is backed up, where, and who can restore it: <...>

## How a client leaves
- They get: <their profile export, their files, their ledger>
- We delete: <what, when, and how we prove it>
```

### Commands

*`c5-commands.sh`*

```bash
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

*`prompt-c5-before-the-call.md`*

```markdown
You are @atlas. I have a call with <client> at <time>. Have @scout write
five lines on what changed for them since our last notes (their site,
their news, their market), each with a source, and write yourself the
open items from <client folder>/notes/, the promises we made, and three
questions worth asking. Deliver both to me in one message thirty minutes
before the call. Do not contact the client.
```

*`prompt-c5-after-the-call.md`*

```markdown
You are @quill. Here are my raw notes from the <client> call: <paste or
dictate>. Write <client folder>/notes/<date>.md with decisions, promises
with dates, and open questions. Draft the follow-up email in my voice,
save it as <client folder>/drafts/<date>-followup.md, and tell atlas
which promises should become cards. Do not send anything.
```

*`prompt-c5-proposal-and-invoice.md`*

```markdown
You are @quill. From <client folder>/CLIENT.md and the ledger
(ledger_report, category client:<slug>), draft two documents: a proposal
for <the new work> with scope, what is not included, price and terms in
the same format we used last time, and this month's invoice from the
ledger entries. Save both under <client folder>/drafts/. List every
number you used and where it came from. I send; you do not.
```

*`prompt-c5-scope-the-service.md`*

```markdown
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

- [ ] A client profile exists with its own sign-ins, blank memory files, the ledger plugin, and a toolset smaller than quill's
- [ ] A pre-call brief arrived with sources before a real call, and you used at least one line of it
- [ ] Notes were on disk within the hour and the follow-up draft waited for you to send it
- [ ] Every invoice and payment for one client is in the ledger under client:<slug>
- [ ] OFFER.md answers the data and responsibility questions the Reddit thread never did

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-COMPANY.md)
