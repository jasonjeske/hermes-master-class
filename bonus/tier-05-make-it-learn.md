# Tier 5: Make It Learn

Hermes improves itself after turns on its own. These commands make it learn on purpose, and let you check what it kept.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 40 | `/refine` | Runs the memory and skill review now, instead of waiting for the automatic one after a turn. Focus text steers it | You just finished something worth keeping, for example `/refine save the deploy steps as a skill` | CLI and chat |
| 41 | `/learn` | Writes a reusable skill from anything you point at: a folder, a URL, this chat, pasted notes | You walked the agent through a procedure and never want to explain it again | CLI and chat |
| 42 | `/init` | Scans the repo and writes its `AGENTS.md`, or merges new findings into the one you have | The first session in a new project | CLI and chat |
| 43 | `/memory` | Shows memory writes waiting behind the approval gate, approves or rejects them, and turns the gate on or off | You want to see what Hermes will remember before it does | CLI and chat |
| 44 | `/skills` | Searches, browses, inspects, installs and audits skills. In chat, only the approval review (`pending`, `diff`, `approve`, `reject`) and only while the skill approval gate is on | Finding a skill someone already wrote, or reviewing one the agent wants to save | CLI, chat opt-in |
| 45 | `/curator` | Reports, runs, pauses and resumes the background skill maintenance. `pin` keeps a skill safe from its archiving pass | Your skill list is going stale, or a skill you rely on must never be archived | CLI and chat |
| 46 | `/bundles` | Lists skill bundles: one `/name` that loads several skills at once | You keep loading the same three skills together | CLI and chat |
| 47 | `/reload-skills` `/reload_skills` | Rescans the skills folder for skills you added or removed | You installed or edited a skill and the session cannot see it | CLI and chat |
| 48 | `/journey` `/learning` `/memory-graph` | Opens the timeline of what Hermes has learned, skills and memories, with `delete` and `edit` | You want to check, prune or fix what it learned | CLI |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
