#!/bin/sh
# Company cadence. ops owns everything that needs a shell (hermes insights, hermes kanban list, ledger_report) and
# delivers into atlas's Bot Chat with --deliver bot-chat:atlas; atlas owns what needs judgment and the kanban, file
# and session_search tools it has. A routine runs in a fresh session with no chat history and no message_agent;
# the Bot Chat reply that a delivery triggers does have message_agent, which is how atlas nudges owners.
# Schedules: "every day at 08:00", "every sunday 18:00", "every 2h", or a cron expression like "0 20 28 * *".
# Replace <company folder> with the absolute path before running. Run once: sh kits/company/cadence/routines.sh

# Daily standup: atlas reads the board with the kanban tools and the company files with the file tools.
hermes -p atlas cron create "every day at 08:00" \
  "Standup. Read <company folder>/ORG.yaml and <company folder>/POLICIES.md with the file tools, then list the board with the kanban tools. Post one line per bot: what is running, what is blocked and why, what finished since yesterday. End with the one decision that is the human's today, or [SILENT] if there is none and nothing is blocked." \
  --name "standup" --deliver bot-chat:atlas

# Supervisor sweep: the Hermes Swarm pattern. ops finds the stalled cards; atlas, in its Bot Chat, nudges the owners.
hermes -p ops cron create "every 2h" \
  "Supervisor sweep. Run hermes kanban list. List every card in running for more than 2 hours, blocked for more than 24 hours, or in review for more than 4 hours: card id, title, owner, how long. If the list is empty reply with only [SILENT]. Otherwise start the reply with '@atlas these cards look stalled. Message each owner with message_agent: name the card and ask for a one-line status or a kanban_block with the reason. Do not create or close cards.' followed by the list." \
  --name "supervisor-sweep" --deliver bot-chat:atlas

# Sunday numbers: ops gathers the figures, atlas writes the page and the one decision.
hermes -p ops cron create "every sunday 18:00" \
  "Sunday numbers, data pass. Call ledger_report for this month. Run hermes insights --days 7 and hermes insights --days 14 for tokens and cost per profile. Run hermes kanban stats. Reply with the raw figures grouped as money, fleet cost this week versus last, board, and then the line '@atlas write this week's Sunday page from these figures: money in, money out, net; fleet cost this week versus last; cards shipped, cards blocked, the oldest open card; the one number from <company folder>/COMPANY.md and its trend; end with exactly one recommended decision for the human.' Deliver even when unchanged." \
  --name "sunday-numbers" --deliver bot-chat:atlas

# Month end: same split. ops gathers, atlas writes the P and L, the retro and the proposed rules.
hermes -p ops cron create "0 20 28 * *" \
  "Month end, data pass. Call ledger_report for this month and for last month. Run hermes insights --days 30. Run hermes kanban stats. Reply with the raw figures, then the line '@atlas write the month end: P and L, month over month variance by category, the fleet's model spend; a retro of three things that worked and three that did not, each tied to a card id or routine name; then read <company folder>/POLICIES.md and propose new dated rules for anything that went wrong twice. Propose only; the human edits POLICIES.md.'" \
  --name "month-end" --deliver bot-chat:atlas

# Nightly dreaming: the HolmeBengt pattern, owned by atlas with session_search, the file tools and the memory tool.
hermes -p atlas cron create "every day at 03:00" \
  "Dreaming. Using session_search over the last 24 hours across the team, extract decisions made, cards moved, mistakes that must not repeat, and open questions. Write a dated summary to <company folder>/journal/<date>.md with the file tools and update MEMORY.md with the memory tool with at most two behavioral rules if a mistake repeated. Reply with the file path and three lines." \
  --name "dreaming"

# Health every four hours, silent when fine. ops owns machines.
hermes -p ops cron create "every 4h" \
  "Health. Run hermes doctor and hermes gateway status. Check that the always-on box answers (ping the host named in <company folder>/ORG.yaml if any). Check free disk. If everything is healthy reply with only [SILENT]; otherwise three lines: what, since when, what you recommend." \
  --name "health-4h"
