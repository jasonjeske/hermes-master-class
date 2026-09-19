#!/bin/sh
# One shared Hindsight bank for the bots that share context. Run once per bot that joins the bank.
# Pick ONE mode and keep it for every bot: local_embedded (Hermes runs the daemon, free, needs an LLM key
# or a local OpenAI-compatible endpoint for extraction), local_external (a Hindsight you run yourself,
# Docker or bare, one URL), or cloud (an API key from ui.hindsight.vectorize.io).

BOT="${1:?usage: hindsight-setup.sh <bot> [bank]}"
BANK="${2:-team-shared}"
HOME_DIR="$HOME/.hermes/profiles/$BOT"

# 1. Interactive wizard, once per bot. It installs the client, asks the mode, and offers a starter
#    memory template (skip it for a bot joining an existing bank; it warns before overwriting).
hermes -p "$BOT" memory setup            # choose hindsight, then the mode you picked above

# 2. Point this bot at the shared bank and tag what it writes with its own name.
#    The config file is per profile: each bot has its own $HERMES_HOME/hindsight/config.json.
[ -f "$HOME_DIR/hindsight/config.json" ] || { echo "no $HOME_DIR/hindsight/config.json: the wizard did not finish for $BOT, run it again"; exit 1; }
python3 - "$HOME_DIR/hindsight/config.json" "$BANK" "$BOT" <<'PY'
import json, sys
path, bank, bot = sys.argv[1:4]
cfg = json.load(open(path))
cfg["bank_id"] = bank
cfg["bank_id_template"] = ""
cfg["retain_tags"] = [bot]
cfg["memory_mode"] = "hybrid"
json.dump(cfg, open(path, "w"), indent=2)
print("wrote", path, "bank", bank, "tags", cfg["retain_tags"])
PY

# 3. Read it back. The provider must say hindsight and available.
hermes -p "$BOT" memory status

# Rollback for one bot: hermes -p <bot> memory off   (built-in MEMORY.md and USER.md keep working)
