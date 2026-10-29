# Tier 7: Tools and Integrations

What the agent can reach, and the commands that change it without a restart.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 62 | `/tools` | Lists tools, or turns tools off and on for this session. Changing them resets the session | A tool keeps getting called when it should not, or one you need is off | CLI |
| 63 | `/toolsets` | Lists the toolsets available | Checking what a profile can reach before you give it a job | CLI |
| 64 | `/plugins` | Lists installed plugins and whether each one is enabled | A plugin's tools are missing and you want to know why | CLI |
| 65 | `/reload-mcp` `/reload_mcp` | Reloads MCP servers from config and checks again which tools are available | You added an MCP server or a credential mid-session | CLI and chat |
| 66 | `/reload` | Reloads `.env` variables into the running session | You added an API key and do not want to restart | CLI |
| 67 | `/browser` | Connects the browser tools to your running Chrome, Brave, Chromium or Edge, or switches to Browser Use mode | The agent needs your logged-in browser, not a fresh headless one | CLI |
| 68 | `/cron` | Lists, adds, edits, pauses, resumes, runs and removes scheduled jobs | Jobs that must run without you (Volume 1, Build 8) | CLI |
| 69 | `/suggestions` `/suggest` | Lists automations Hermes has suggested. `accept` creates one, `dismiss` drops it, `catalog` adds curated starters | You want automations without writing cron jobs by hand | CLI and chat |
| 70 | `/blueprint` `/bp` | Sets up an automation from a template, step by step or in one line with `slot=value` | You want a known automation filled in for you | CLI and chat |
| 71 | `/egress` | Shows the Docker egress proxy: whether it runs, where its credentials come from, and the next fix | You run Hermes in Docker and a provider call is blocked | CLI and chat |
| 72 | `/codex-runtime` `/codex_runtime` | Hands eligible OpenAI and Codex turns to a `codex app-server` subprocess, or back. Takes effect next session | You want Codex's own shell and patch tools, and ChatGPT subscription sign-in, on OpenAI models | CLI and chat |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
