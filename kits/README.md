# Kits

Real files the volumes install. Each was validated with Hermes's own tooling before it went in: desktop plugins with the loader's contract (ESM default export, id equals folder, the three allowed imports, no JSX, theme variables only), the ledger with `hermes plugins doctor --ci`, every shell script with `sh -n`, every YAML and JSON parsed.

| Folder | Volume | What it is | How it installs |
|---|---|---|---|
| `desktop-plugins/hello-hermes` | 2, Build 5 | The smallest complete desktop plugin: a pane, a status chip, a palette command, a keybind | copy the folder to `~/.hermes/desktop-plugins/` |
| `desktop-plugins/prompt-library` | 2, Build 6 | A page that stores your prompts, copies them, and opens a chat with one | same |
| `desktop-plugins/fleet-board` | 2, Build 9 | A roster pane over `profiles.list` | same |
| `agent-plugins/ledger` | 2, Build 7 | One package, both SDKs: `ledger_add` and `ledger_report` tools, a `/ledger` command, dashboard routes, and a desktop page. Its `desktop/plugin.js` is copied to `~/.hermes/desktop-plugins/ledger/` on install, which is why the folder-name check passes only there | `hermes plugins install <path or owner/repo>` then `hermes plugins enable ledger` |
| `bot-team/<name>` | 3 | Six bots: `SOUL.md`, `config.yaml` (model pin placeholder, effort, and for atlas the disabled toolsets), `distribution.yaml`, `routines.sh` (kept outside `cron/`, which Hermes owns for job state), README | `hermes profile install ./bot-team/<name> --alias <name>`, then sign in providers per bot |
| `bot-team/memory` | 3, Build 7 | A shared Hindsight bank config and setup script, and a Mnemosyne setup script for a bot whose memory stays on the machine | `sh hindsight-setup.sh <bot> [bank]`, `sh mnemosyne-setup.sh <bot>` |
| `company/` | 4 | `COMPANY.md`, `ORG.yaml`, `POLICIES.md`, `ATLAS-PROTOCOL.md`, `SKILLS-LEDGER.md`, `life/routines.sh`, `cadence/routines.sh`, `scripts/backup.sh`, `production/LINE-TEMPLATE.md`, `clients/CLIENT-TEMPLATE.md` and `OFFER-TEMPLATE.md`, `corrections/README.md` | copy to your company folder; replace `<company folder>` in the cadence routines; run each routines file once with `sh` |

Placeholders to replace before use: every `model.default` in `bot-team/*/config.yaml`, `<company folder>` in the cadence routines, and the angle-bracket fields in the company templates. Nothing here holds a secret, and nothing here should: keys live in each profile's `.env`.

License: MIT, see [LICENSE-CODE](../LICENSE-CODE).
