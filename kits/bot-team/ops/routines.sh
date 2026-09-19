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
