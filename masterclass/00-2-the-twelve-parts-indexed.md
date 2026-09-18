# The Twelve Parts, Indexed

| # | Part | The one thing it teaches | Drill in this doc |
|---|---|---|---|
| 1 | How Hermes Actually Processes Work | The turn is a five-stage loop, not a single inference | Trace one turn end to end |
| 2 | The Choices That Compound | Deployment home, session persistence and tool reach are the only day-one decisions that matter | The three-tool smoke test |
| 3 | The Learning System | Memory holds facts, skills hold procedures, the background review writes both | Force a memory write and verify it survives |
| 4 | Skills as Executable SOPs | A skill is a markdown file with a trigger, a procedure, pitfalls and a verification | Write one real skill |
| 5 | Tools and Toolsets | Capability is dynamic and gated by check_fn, not fixed at install | Audit your live tool surface |
| 6 | Cron as Infrastructure | A scheduled job runs in a fresh session, so the prompt must be self-contained | Ship a zero-token watchdog |
| 7 | Messaging Gateways | One gateway process, 20+ platforms, portable sessions | Cross-surface a single session |
| 8 | Delegation and Subagents | Children get isolated context and their own budget; only the summary returns | Run a three-way parallel research fan-out |
| 9 | Browser and Computer Use | The agent acts on interfaces that were never built for APIs | Hybrid-route a local and a public page |
| 10 | Kanban as a Coordination Model | A durable board is how multiple profiles coordinate without talking | Stand up a three-profile pipeline |
| 11 | The Admin Layer | A profile is a whole independent agent, not a config preset | Clone a profile and prove isolation |
| 12 | What Breaks and What to Skip | Context is the first wall; integrations fail silently | Build the weekly tool-surface canary |

### Vocabulary, front-loaded

The series uses these terms from Part 1 onward. Knowing them before you start saves rereading.

| Term | What it actually means |
|---|---|
| Agent loop | The five-stage cycle run per turn: assemble, resolve, compress, call, parse. Repeats while the model returns tool calls |
| Turn | One pass through the loop. A tool call costs a turn, so one user message can cost many |
| Iteration budget | The cap on turns in a single task. 90 for the main agent, 50 for a subagent |
| Toolset | A named bundle of tools granted to a surface. The CLI gets a broad one, a phone bot a narrow one |
| check_fn | A per-tool availability test run at schema build time. Fails, and the model never sees the tool exists |
| Progressive disclosure | Loading a skill index at session start and the skill body only on demand |
| Profile | A fully independent agent: its own config, memory, skills, sessions, cron, gateway and credentials |
| Stable / context / volatile | The three ordered prompt tiers. Stable is cacheable identity, volatile is memory and timestamp |
| Session lineage | The chain linking a compressed session to the one it came from |
| Background review | A forked agent that inspects each finished turn and proposes memory and skill writes |
| Curator | The scheduled garbage collector that ages, archives and consolidates skills |
| No-agent mode | A cron job that runs a script and delivers stdout, with no LLM call at all |

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
