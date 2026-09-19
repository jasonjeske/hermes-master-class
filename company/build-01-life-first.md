# Build 1: Life First

![Build 1](../assets/art/part-03.webp)

### What you are building

The personal operations layer that buys back the hours: the ops bot from Volume 3 running your inbox sweep, calendar prep, health log, money ledger and a weekly review, with a human gate on anything that leaves the machine.

### What the sources say

| Source | The pattern |
|---|---|
| HolmeBengt's Daily Status Report at 6:30 AM | Calendar and what needs preparation, open to-dos, system health, anomalies from the overnight run. "This is not the news. This is the tactical dashboard." |
| HolmeBengt's Mail Gatekeeper | A local model judges mail as safe or blocked; blocked means 2FA codes, logins, password resets, bank transactions, spam; safe mail lands in a Telegram topic; an evening watchdog reviews the blocked folder for false positives. "There is no send endpoint anywhere in the system, Hermes can read and draft, but nothing can physically leave the machine" |
| HolmeBengt's Health Coach at noon | Wearable recovery and sleep, phone steps and resting heart rate, a self-built food log fed by Telegram text, photo or barcode, checked against a calorie and protein target |
| HolmeBengt's Finance Review | Sundays at 6 PM weekly, the 28th monthly: income, expenses, liquid assets, burn rate versus budget, month-over-month variance, savings rate, "delivered with voice" |
| SquishyData's signals | Twenty cron skills append to a daily ledger; one agentic job triages it; forwarding goes "to whoever can help or needs to know" |
| stan_frbd | A personal-coach profile for gym, running and nutrition, separate from work, with its own Telegram bot |
| kenmazaika | Dictate messy ideas from the phone into a Telegram topic; Hermes returns a structured outline plus a "riff" of connections; saved locally |

The Hermes mechanisms underneath: cron routines with `[SILENT]` (Volume 1, Build 8), the ledger plugin (Volume 2, Build 7), a profile per boundary (Volume 3), and the Telegram gateway for the phone (Volume 1, Part 7).

### The life routines the kit ships

*`kits/company/life/routines.sh`*

```bash
#!/bin/sh
# Life-ops routines, owned by ops. Run once: sh kits/company/life/routines.sh. Nothing here sends, pays, posts or deletes.
# ops needs the terminal, file, memory and session_search toolsets, and the ledger plugin for sunday-money.

hermes -p ops cron create "every day at 06:30" \
  "Tactical brief for today. If you have calendar access, list today's events with what each needs prepared; otherwise say calendar is not connected. List open to-dos from ~/inbox/todo.md if it exists. Add one line of machine health from hermes doctor. Add anomalies from the last 24 hours of error logs (hermes logs --level WARNING, summarized). Six lines maximum. If there are no events, no to-dos and no anomalies, reply with only [SILENT]." \
  --name "life-brief"

hermes -p ops cron create "every day at 12:00" \
  "Health check-in. Read ~/inbox/health.md (a log I append to by voice: sleep, training, food, weight). Compare today's entries against the targets at the top of the file. Reply with two lines: where I stand against each target, and the one thing to do this afternoon. If the file has no entry for today, reply with only [SILENT]." \
  --name "health-noon"

hermes -p ops cron create "every sunday 18:00" \
  "Sunday money. Call ledger_report for this month and for last month. Report income, expenses, net, the three biggest expense categories and how each moved versus last month, and the savings rate. Five lines. Deliver even when unchanged." \
  --name "sunday-money"

hermes -p ops cron create "every day at 21:00" \
  "Mail sweep, read only. If a mail tool is available, list unread messages from the last 24 hours that a human must answer, one line each with sender and ask; never draft a reply and never send. Skip newsletters, receipts and notifications. If nothing needs me, reply with only [SILENT]. If no mail tool is available, reply with only [SILENT]." \
  --name "mail-sweep"

hermes -p ops cron create "every saturday 17:00" \
  "Weekly review prep. Using session_search over the last seven days, list: decisions I made, things I said I would do and did not, and questions I asked more than once. Ten lines maximum, dated. Deliver even when short." \
  --name "weekly-review-prep"
```

> ⚠️ **Two gates that are not optional**
>
> Nothing in these routines sends mail, moves money or messages another person. Drafts, yes; sends, no. HolmeBengt built that as an architectural fact rather than a rule, by having no send endpoint at all. If you later give a bot a send tool, it goes on a separate profile with its own approvals, never on the one that reads everything.

### Prompts

*`prompt-c1-design-my-week.md`*

```markdown
You are @ops. Design my personal operations layer from evidence. Read my
calendar for the last four weeks if you have a tool for it, otherwise ask
me for the five things that recur weekly. Then propose at most six
routines, each with: name, schedule, the exact self-contained prompt, the
silent condition, and the delivery target. Rules: nothing sends, posts,
pays or deletes; anything that would needs a human gate and a separate
profile. Show me the hermes cron create commands. Do not create them until
I say go.
```

*`prompt-c1-dictation-inbox.md`*

```markdown
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

- [ ] A 6:30 AM brief arrives on your phone with calendar, to-dos and health, and is silent on empty days
- [ ] Money recorded by voice through the ledger tools shows up in the Sunday review
- [ ] A dictated ramble from your phone comes back as a structured file within a minute
- [ ] Nothing in the life layer has a send tool; you checked each profile's toolsets

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-COMPANY.md)
