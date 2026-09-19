#!/bin/sh
# Mnemosyne for a bot whose memory must never leave the machine. Local-first, one SQLite file, no daemon.
# A profile runs ONE external provider, so a bot is on Mnemosyne or on Hindsight, never both.
# Two rules learned in the field: never install into the Hermes-managed venv (hermes update rebuilds it and
# wipes extra packages), and if your terminal backend is Docker, run this from the host yourself, not via Hermes.

BOT="${1:?usage: mnemosyne-setup.sh <bot>}"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
VENV="$HERMES_HOME/.mnemosyne/venv"          # the side venv the Mnemosyne README's update path expects

# 1. A venv of its own, with local embeddings (about 800 MB of RAM at run time; the core-only profile is
#    about 50 MB but sends embeddings to a remote endpoint, which defeats the point of a private bot).
python3 -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install --upgrade "mnemosyne-memory[embeddings]" mnemosyne-hermes

# 2. The wrapper install writes the plugin files under $HERMES_HOME/plugins/mnemosyne, where Hermes discovers them.
"$VENV/bin/mnemosyne-hermes" install --mode wrapper --force --python "$VENV/bin/python"

# 3. Select it for THIS bot and read it back. The README's path is the config key; in Wanderloots' recorded walkthrough the
#    same wizard (hermes memory setup) offered "Mnemosyne local" and asked for the default remember scope, which he set to
#    global rather than per session. If your wizard does not list Mnemosyne, the config key alone selects it.
hermes -p "$BOT" config set memory.provider mnemosyne
hermes -p "$BOT" memory setup
hermes -p "$BOT" memory status
hermes -p "$BOT" tools list | grep mnemosyne_
hermes -p "$BOT" mnemosyne stats 2>/dev/null || true   # the plugin's own CLI command as shown in that walkthrough; optional

# If memory status says plugin missing or the Python environments do not match, re-run step 2, then step 3.
# Mnemosyne's docs suggest turning the built-in MEMORY.md and USER.md injection off for this bot to avoid
# duplicate context; do that in the bot's config.yaml (memory.enabled, user_profile.enabled), not with
# `hermes tools disable memory`, which removes the whole memory toolset, provider tools included.
# Update later: "$VENV/bin/python" -m pip install --upgrade 'mnemosyne-memory[embeddings]' mnemosyne-hermes,
# re-run step 2, then hermes gateway restart. To leave: hermes -p <bot> memory off
