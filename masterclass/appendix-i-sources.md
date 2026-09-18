# Appendix I: Sources

All twelve parts by Tony Simons (@tonysimons_), published on X between July 5 and July 20, 2026. Retrieved and compiled September 16, 2026.

| Part | Title | Published | Link |
|---|---|---|---|
| Index | Hermes Agent Masterclass: The Whole Damn Thing | Jul 20, 2026 | x.com/tonysimons_/status/2079066422211117218 |
| 1 | How Hermes Agent Actually Processes Work | Jul 5, 2026 | x.com/tonysimons_/status/2073880068657471523 |
| 2 | The Choices That Compound | Jul 7, 2026 | x.com/tonysimons_/status/2074253518224109718 |
| 3 | The Learning System | Jul 8, 2026 | x.com/tonysimons_/status/2074634038007001223 |
| 4 | Skills as Executable SOPs | Jul 9, 2026 | x.com/tonysimons_/status/2075010900247843018 |
| 5 | Tools and Toolsets | Jul 10, 2026 | x.com/tonysimons_/status/2075526192476631476 |
| 6 | Cron Makes Hermes Infrastructure | Jul 11, 2026 | x.com/tonysimons_/status/2076011080229552207 |
| 7 | Messaging Gateways Make Hermes Ambient | Jul 14, 2026 | x.com/tonysimons_/status/2076838692828684573 |
| 8 | Delegation and Subagents | Jul 15, 2026 | x.com/tonysimons_/status/2077219246178718068 |
| 9 | Browser and Computer Use | Jul 17, 2026 | x.com/tonysimons_/status/2077923978249724073 |
| 10 | Kanban as a Coordination Model | Jul 18, 2026 | x.com/tonysimons_/status/2078279982845980737 |
| 11 | The Admin Layer | Jul 19, 2026 | x.com/tonysimons_/status/2078641430562492927 |
| 12 | What to Skip, What Breaks, and How to Stay Sane | Jul 20, 2026 | x.com/tonysimons_/status/2078972949483454619 |

The author also references two companion pieces worth reading alongside the series: a guide to your first two weeks with Hermes Agent, and an earlier deep dive on kanban from May 2026. Official installation documentation lives at `hermes-agent.nousresearch.com/docs/getting-started/installation`.

### Sources for the Build Track

Every prompt, template and config block in the Build Track was checked against these, in September 2026. The documentation is the authority; when it and this document disagree, the documentation has moved and this document is behind.

| Build | Documentation pages (hermes-agent.nousresearch.com/docs/...) |
|---|---|
| 0 | getting-started/quickstart · getting-started/installation · reference/cli-commands |
| 1 | user-guide/features/personality · the default SOUL.md in the Hermes repository |
| 2 | user-guide/features/memory · user-guide/import-from-other-agents · user-guide/sessions |
| 3 | user-guide/features/context-files |
| 4 | user-guide/features/skills · developer-guide/creating-skills · user-guide/features/curator |
| 5 | user-guide/features/plugins · user-guide/features/built-in-plugins |
| 6 | user-guide/features/memory-providers · user-guide/features/honcho · skills/note-taking/obsidian/SKILL.md in the Hermes repository |
| 7 | user-guide/profiles · the cost-strategy section of user-guide/features/kanban |
| 8 | user-guide/features/cron |
| 9 | user-guide/features/delegation · user-guide/features/kanban |
| 10 | user-guide/configuration · user-guide/security · reference/cli-commands |

Community material that shaped the prompt pattern and the worked patterns, all public:

| Source | What it contributed |
|---|---|
| Hermes Wingtips, a numbered tip series by @witcheer on X, 75 tips as of September 2026 | The "hand this to your agent: read the docs section, set the key, show me the diff before you save" pattern that every Build Track prompt follows |
| Hermes Release Watch (@HermesWatcher on X), the one-page command cheat sheet | The daily command set in Build 0 was checked against it |
| Tonbi's AI Garage, the eleven-video Hermes Agent Masterclass on YouTube | The memory-layer framing in Build 6, the cron prompt discipline in Build 8, and the delegation cost notes in Build 9 |
| The Hermes user stories page on the official site | The nightly consolidation job in Build 6 follows a pattern one operator described publicly; the profile roster shape in Build 7 echoes several |

> 📝 **What this document added**
>
> The prose substance, and every mechanism, threshold and command above, come from the source articles. Added while compiling: twenty-six diagram plates, fourteen illustrations, the consolidated constant and triage tables, the vocabulary table, the operator drills, the cross-references between parts, the 30/60/90 path in Appendix E, the configuration and prompt guidance in Appendices F, G and H, and the whole of the Build Track. Nothing was invented about how Hermes behaves; every number, path, key and command came from the source series or from the official documentation named above.

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
