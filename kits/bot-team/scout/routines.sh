#!/bin/sh
# Scout routine: a watch on the sources that matter to the team. Edit the list in the prompt.
# The result is delivered into atlas's Bot Chat; atlas decides who needs to hear it and messages them from there.
# Run once: sh kits/bot-team/scout/routines.sh

hermes -p scout cron create "every day at 06:30" \
  "Source watch. Read the Hermes Agent documentation changelog page, the Hermes GitHub releases page, and the two feeds named in your MEMORY.md under 'watch list'. For anything new since yesterday that changes how the team works (a renamed command, a new setting, a breaking change), write one line with the link and which teammate it affects. If nothing changed, reply with only [SILENT]. Otherwise start the reply with '@atlas source watch found changes that affect the team:' followed by the lines." \
  --name "source-watch" --deliver bot-chat:atlas
