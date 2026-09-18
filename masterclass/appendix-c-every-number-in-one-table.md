# Appendix C: Every Number in One Table

The series scatters its constants across twelve articles. Here they are together.

| Constant | Value | Where it applies |
|---|---|---|
| Registered tools | 70+ | Across ~28 toolsets, excluding your MCP servers |
| Providers supported | 18+ | With OAuth flows and credential pools |
| API execution modes | 3 | OpenAI chat completions, OpenAI Codex/Responses, native Anthropic Messages |
| Terminal backends | 6 | local, Docker, SSH, Singularity, Modal, Daytona |
| Browser backends | 5 | Browserbase, Browser Use, Firecrawl, local CDP, managed Chromium |
| Messaging platforms | 20+ | One gateway process serves all of them |
| Main iteration budget | 90 turns | Each tool call is one turn |
| Subagent iteration budget | 50 turns | Per child, independent of the parent |
| Default concurrent children | 3 | Per delegation batch |
| Default orchestration depth | 1 (flat) | Depth 3 at width 3 means 27 leaf agents |
| Preflight compression | 50% of context | Before the API call |
| Gateway auto-compression | 85% of context | During a gateway session |
| Messages preserved on compression | Last 20 | Middle turns are summarized |
| Memory budget | ~1,300 tokens | MEMORY.md plus USER.md combined |
| MEMORY.md hard limit | 2,200 characters | Returns an error with current entries, never a silent drop |
| Skill index cost | ~3,000 tokens | For a library of dozens of skills |
| Curator tick | Every 7 days | After at least 2 hours idle |
| Skill goes stale | 30 days unused | Deterministic phase |
| Skill archived | 90 days unused | Recoverable, never deleted |
| Cron tick | Every 60 seconds | Gateway-hosted scheduler |
| Screenshot cost | ~1,500 tokens | Flat rate on Anthropic regardless of base64 length |
| Screenshots kept in context | 3 most recent | Older become placeholder text |
| Computer-use session cost | ~30K tokens | Versus ~600K unoptimized |
| Removed child timeout | Formerly 300s | Now heartbeat staleness detection; hard timeout is opt-in |

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
