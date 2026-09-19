#!/bin/sh
# Atlas routines. Atlas has no terminal: its routines use the kanban tools, the file tools and session_search, never the shell.
# Anything that needs a shell (hermes insights, hermes kanban list, hermes doctor) is gathered by ops and delivered into
# atlas's Bot Chat with --deliver bot-chat:atlas; atlas answers there, where message_agent exists.
# Run once: sh kits/bot-team/atlas/routines.sh

hermes -p atlas cron create "every day at 08:00" \
  "Standup. Use the kanban tools to read the board (every card, its status and owner) and session_search for what each teammate reported since yesterday. Write a standup in the shape done, in progress, blocked, needs you, one line per item, owners named. End with the one decision that is the human's today, or [SILENT] if the board is empty and nothing is blocked." \
  --name "standup" --deliver bot-chat:atlas

hermes -p atlas cron create "every saturday 17:00" \
  "Weekly review. Use the kanban tools to list this week's completed cards and session_search to find the weekly numbers ops delivered. Write five lines: what shipped, what slipped and why, what to stop, what to start, and the one decision that needs the human. Deliver even when short." \
  --name "weekly-review"
