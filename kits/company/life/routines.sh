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
