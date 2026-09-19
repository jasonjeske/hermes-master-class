![Hermes Agent Masterclass](assets/art/hero.webp)

# Hermes Agent Masterclass

Four volumes, one repository, pure GitHub Markdown. Every prompt pastes as it is, every file installs as it is, and every path, key and command was checked against the official Hermes Agent documentation for the version installed while writing.

| Volume | Read it in one page | What it gives you |
|---|---|---|
| **1. The Agent** | [FULL-MASTERCLASS.md](masterclass/FULL-MASTERCLASS.md) | Tony Simons' twelve-part series, indexed and illustrated, plus a ten-build track from a fresh install to a tuned, remembering, scheduled agent |
| **2. Hermes Desktop** | [FULL-HERMES-DESKTOP.md](desktop/FULL-HERMES-DESKTOP.md) | The app, made yours: the window, the settings that matter, gateways and other machines, and a four-part plugin workshop that ships three desktop plugins and one unified agent-plus-desktop package |
| **3. Hermes Bots** | [FULL-HERMES-BOTS.md](bots/FULL-HERMES-BOTS.md) | Bot Mode as a team: six bots with every SOUL.md, model pin and routine, how they message and meet, one shared memory, one shared board, one roster across machines, shipped as installable distributions |
| **4. The Hermes Company** | [FULL-HERMES-COMPANY.md](company/FULL-HERMES-COMPANY.md) | Your life, then your business, on those bots: an org of bots with human gates, production lines, clients, money, the cadence, the learning loop, and the whole company as one repository, grounded in named operators |

The kits the volumes install live in [`kits/`](kits/): three desktop plugins, a unified ledger plugin, six bot profiles with a memory kit, and the company files. Each is real code or a real config, validated with Hermes's own tooling before it went in.

> 📝 **Attribution**
>
> Volume 1's twelve parts are the work of **[Tony Simons (@tonysimons_)](https://x.com/tonysimons_)**; every source article is linked in [Appendix I](masterclass/appendix-i-sources.md). Volumes 2 to 4 were written from the official documentation and quote two operators who published detailed field experience, **Tonbi's AI Garage** and **Wanderloots**, by name where their experience adds something the docs do not; Volume 4 quotes the operators behind the official Hermes user stories by handle, with links. Nothing was invented about how Hermes behaves. Full credits in [ATTRIBUTION.md](ATTRIBUTION.md).
>
> Hermes Agent is a project of [Nous Research](https://hermes-agent.nousresearch.com/docs/getting-started/installation). This is an unofficial study reference.

---

## Start here

| If you want to | Read |
|---|---|
| Understand how Hermes works, end to end | Volume 1, [Part 1](masterclass/part-01-how-hermes-actually-processes-work.md) onward |
| Build a Hermes setup this weekend with prompts you paste | Volume 1, [the Build Track](masterclass/build-00-0-the-build-track.md), Builds 0 to 10 |
| Get the Desktop app right and write your first plugin | Volume 2, [Build 0](desktop/build-00-install-and-first-launch.md), then the [plugin workshop](desktop/build-05-plugin-workshop-i-hello-hermes.md) |
| Turn your profiles into a team that works while you sleep | Volume 3, [Build 0](bots/build-00-what-a-bot-is.md) onward |
| Run your week, then your company, on that team | Volume 4, [Build 0](company/build-00-the-case.md) onward |
| Set up the memory that makes all of it compound | Volume 1 [Build 6](masterclass/build-06-the-memory-stack.md) for one agent, Volume 3 [Build 7](bots/build-07-shared-memory-and-a-shared-board.md) for a team |
| Fix a specific thing | [Appendix D: Failure Triage](masterclass/appendix-d-failure-triage.md) |
| Look something up | [Commands](masterclass/appendix-a-complete-command-index.md) · [Paths](masterclass/appendix-b-every-path-and-what-lives-there.md) · [Numbers](masterclass/appendix-c-every-number-in-one-table.md) |

---

## Volume 2: The Hermes Desktop Masterclass

![The Hermes Desktop Masterclass](assets/art/v2-hero.webp)

The same agent as the CLI, in a window that adds panes, a HUD, git review, worktrees, a plugin surface and a roster of gateways. Builds 5 to 8 are a workshop: a hello-world pane, a prompt library page, a ledger that is an agent plugin and a desktop page in one folder, and the prompts that get Hermes to write the next plugin for you.

| Build | You end up with | Checked against |
|---|---|---|
| [0 Install and First Launch](desktop/build-00-install-and-first-launch.md) | The app installed, permissions settled once, the local backend understood | Installation, Desktop |
| [1 The Window](desktop/build-01-the-window.md) | The window at your fingertips: sessions, panes, terminal, git review, HUD, palette, the keys you will actually use | Desktop |
| [2 The Settings That Matter](desktop/build-02-the-settings-that-matter.md) | The settings that decide cost and behavior, set on purpose, and an audit prompt for the rest | Desktop, Configuration |
| [3 Capabilities in the App](desktop/build-03-capabilities-in-the-app.md) | Skills, plugins, tools and MCP managed from the app, the two safety plugins on | Desktop, Plugins |
| [4 Gateways and Other Machines](desktop/build-04-gateways-and-other-machines.md) | The app talking to a Hermes on another machine, with the registry of every gateway you own | Desktop, Multi-connection |
| [5 Plugin Workshop I, Hello Hermes](desktop/build-05-plugin-workshop-i-hello-hermes.md) | Your first desktop plugin, loaded live | Desktop Plugin SDK |
| [6 Plugin Workshop II, the Prompt Library](desktop/build-06-plugin-workshop-ii-the-prompt-library.md) | A Prompt Library page with persistent storage | Desktop Plugin SDK |
| [7 Plugin Workshop III, the Ledger (agent and desktop in one package)](desktop/build-07-plugin-workshop-iii-the-ledger-agent-and-desktop-in-one-package.md) | A Ledger plugin with agent tools, a backend and a desktop page in one package | Build a Hermes Plugin, SDK |
| [8 Plugin Workshop IV, let Hermes build the next one](desktop/build-08-plugin-workshop-iv-let-hermes-build-the-next-one.md) | The Fleet Board, and the prompt that makes Hermes write your next plugin | SDK, Plugins |
| [9 Care and Feeding](desktop/build-09-care-and-feeding.md) | Updates, permissions after updates, logs, recovery and uninstall, all understood before you need them | Desktop |

Kits: [`kits/desktop-plugins/hello-hermes`](kits/desktop-plugins/hello-hermes), [`kits/desktop-plugins/prompt-library`](kits/desktop-plugins/prompt-library), [`kits/desktop-plugins/fleet-board`](kits/desktop-plugins/fleet-board), [`kits/agent-plugins/ledger`](kits/agent-plugins/ledger).

---

## Volume 3: The Hermes Bots Masterclass

![The Hermes Bots Masterclass](assets/art/v3-hero.webp)

A Bot is a profile, so a team is a set of folders, and a set of folders can be written down, versioned and installed. This volume ships one: atlas, forge, scout, quill, sentinel and ops, with a model per bot and the reason, routines owned by the right bot, message paths, rooms that settle, a shared Hindsight bank with Mnemosyne as the local-only alternative, the kanban board as the queue, and the roster spread across a laptop, a Mac mini and a VPS.

| Build | You end up with | Checked against |
|---|---|---|
| [0 What a Bot Is](bots/build-00-what-a-bot-is.md) | The mental model: bot, profile, Bot Chat, routine, room, and the two markers that make it all work | Bot Mode, Profiles |
| [1 Design the Roster](bots/build-01-design-the-roster.md) | A roster designed from your real work, named so the tags work, sized so the machine keeps up | Bot Mode |
| [2 A Model per Bot](bots/build-02-a-model-per-bot.md) | A model per bot with a reason and a cost, and the credential rule that bites | Profiles, Kanban |
| [3 The Birth of a Bot](bots/build-03-the-birth-of-a-bot.md) | Your first three bots born, from the dialog or the CLI, with SOULs written for their roles | Bot Mode, Personality |
| [4 Routines](bots/build-04-routines.md) | Routines attached to the bots that own them, silent when nothing happened | Bot Mode, Cron |
| [5 Bots Talking to Each Other](bots/build-05-bots-talking-to-each-other.md) | Bots messaging each other, with the delivery contract understood | Bot Mode |
| [6 Rooms](bots/build-06-rooms.md) | Group chats that plan, review and escalate without spinning | Bot Mode |
| [7 Shared Memory and a Shared Board](bots/build-07-shared-memory-and-a-shared-board.md) | Shared memory and a shared board: Hindsight and Mnemosyne, and kanban as the queue | Memory Providers, Kanban |
| [8 Bots Across Machines](bots/build-08-bots-across-machines.md) | Bots across machines: the mini, the VPS, one roster | Bot Mode, Multi-connection |
| [9 Ship the Team, Grow It, Shrink It](bots/build-09-ship-the-team-grow-it-shrink-it.md) | The team shipped as an installable distribution, and the prompts that grow or shrink it | Profile Distributions |

Kit: [`kits/bot-team/`](kits/bot-team/), one folder per bot plus [`memory/`](kits/bot-team/memory/).

---

## Volume 4: The Hermes Company Masterclass

![The Hermes Company Masterclass](assets/art/v4-hero.webp)

Grounded in thirteen named cases from the official user stories corpus and the operators' own posts, with the limits stated first: no audited revenue, two source posts removed, no data-protection answer, no security review. What survives is the mechanisms, and this volume turns them into files: a charter, an org of bots, dated policy rules, production lines with a human gate, client folders, the books plus the bill for the bots, a cadence of routines, and the company as one installable repository.

| Build | You end up with | Grounded in |
|---|---|---|
| [0 The Case](company/build-00-the-case.md) | The case: what people actually run, what it costs, what nobody has proven | 13 named cases |
| [1 Life First](company/build-01-life-first.md) | Life first: inbox, calendar, health, money and the weekly review, as bots and routines | HolmeBengt, SquishyData, stan_frbd |
| [2 The Company Blueprint](company/build-02-the-company-blueprint.md) | The company blueprint: a charter, an org of bots, decision rights, human gates | Jinn, RUDR9, ogiberstein |
| [3 The Chief of Staff](company/build-03-the-chief-of-staff.md) | The chief of staff: your planner bot owning the board and the cadence | RUDR9, Hermes Swarm |
| [4 Production Lines](company/build-04-production-lines.md) | Production lines: content, products, education, from research to a publish gate | cyrilXBT, Metics, kenmazaika |
| [5 Clients](company/build-05-clients.md) | Clients: research before calls, proposals, notes, invoices behind a gate | mvanhorn, IBuzovskyi, pacmanpill |
| [6 Money](company/build-06-money.md) | Money: the ledger as the books, a weekly P&L routine, what the fleet costs | HolmeBengt, witcheer, Volume 2's ledger |
| [7 The Cadence](company/build-07-the-cadence.md) | The cadence: standup room, weekly review, monthly retro, the dashboard | Hermes Swarm, Gumroad |
| [8 Learn While You Run](company/build-08-learn-while-you-run.md) | Learn while you run: corrections become files, skills become SOPs | Gumroad, HolmeBengt, riceinmybelly |
| [9 Ship the Company](company/build-09-ship-the-company.md) | Ship the company: one repo installs the whole roster; backups, security, the always-on box | RUDR9, stan_frbd |

Kit: [`kits/company/`](kits/company/).

---

## Volume 1: The Hermes Agent Masterclass

Tony Simons' twelve parts, combined into one navigable reference with a plate per part, the scattered constants pulled into tables and an exercise per part, followed by the Build Track: ten builds from a fresh install to a Hermes with an identity, seeded memory, project context, skills, plugins, a four-layer memory stack, a profile roster, cron jobs, delegation, a kanban board, and the tuning and safety settings that decide cost and blast radius.

| Build | You end up with | Checked against |
|---|---|---|
| [0 Day One](masterclass/build-00-day-one.md) | A working install, a chosen provider, and the daily command set | Quickstart, CLI reference |
| [1 SOUL.md](masterclass/build-01-soul-md.md) | A SOUL.md that shapes behavior, three complete files to start from, and personality overlays | Personality doc |
| [2 USER.md and MEMORY.md](masterclass/build-02-user-md-and-memory-md.md) | Both memory files seeded from an interview and from your machine, plus the cheap-model review | Memory doc, import doc |
| [3 Project Context](masterclass/build-03-project-context.md) | An AGENTS.md per project and a personal override file | Context Files doc |
| [4 Skills](masterclass/build-04-skills.md) | Skills written from work you already did, a bundle, and a configured curator | Skills docs, Creating Skills guide |
| [5 Plugins](masterclass/build-05-plugins.md) | The bundled safety plugins on, and a minimal plugin written to the documented shape | Plugins docs |
| [6 The Memory Stack](masterclass/build-06-the-memory-stack.md) | Four layers: built-in, session search, Hindsight (or Mnemosyne, or Honcho), and an Obsidian vault, plus a nightly consolidation job | Memory Providers, provider READMEs |
| [7 Profiles](masterclass/build-07-profiles.md) | A roster with a frontier planner and inexpensive workers | Profiles doc |
| [8 Cron](masterclass/build-08-cron.md) | Jobs that brief themselves, stay silent when healthy, and cost nothing when no reasoning is needed | Cron doc |
| [9 Delegation and Kanban](masterclass/build-09-delegation-and-kanban.md) | A cheap child fleet and a board the profiles work from | Delegation and Kanban docs |
| [10 Tuning and Safety](masterclass/build-10-tuning-and-safety.md) | Approvals, model routing, effort levels, and a weekly maintenance habit | Configuration and Security docs |
| [The Build Ledger](masterclass/build-11-the-build-ledger.md) | One proof line per build | |

### The twelve parts

| # | Part | The one thing it teaches |
|---|---|---|
| 1 | [How Hermes Actually Processes Work](masterclass/part-01-how-hermes-actually-processes-work.md) | The turn is a five-stage loop, not a single inference |
| 2 | [The Choices That Compound](masterclass/part-02-the-choices-that-compound.md) | Deployment home, session persistence and tool reach are the only day-one decisions that matter |
| 3 | [The Learning System](masterclass/part-03-the-learning-system.md) | Memory holds facts, skills hold procedures, the background review writes both |
| 4 | [Skills as Executable SOPs](masterclass/part-04-skills-as-executable-sops.md) | A skill is a markdown file with a trigger, a procedure, pitfalls and a verification |
| 5 | [Tools and Toolsets](masterclass/part-05-tools-and-toolsets.md) | Capability is dynamic and gated by `check_fn`, not fixed at install |
| 6 | [Cron Makes Hermes Infrastructure](masterclass/part-06-cron-makes-hermes-infrastructure.md) | A scheduled job runs in a fresh session, so the prompt must be self-contained |
| 7 | [Messaging Gateways Make Hermes Ambient](masterclass/part-07-messaging-gateways-make-hermes-ambient.md) | One gateway process, 20+ platforms, portable sessions |
| 8 | [Delegation and Subagents](masterclass/part-08-delegation-and-subagents.md) | Children get isolated context and their own budget; only the summary returns |
| 9 | [Browser and Computer Use](masterclass/part-09-browser-and-computer-use.md) | The agent acts on interfaces that were never built for APIs |
| 10 | [Kanban as a Coordination Model](masterclass/part-10-kanban-as-a-coordination-model.md) | A durable board is how multiple profiles coordinate without talking |
| 11 | [The Admin Layer](masterclass/part-11-the-admin-layer.md) | A profile is a whole independent agent, not a config preset |
| 12 | [What Breaks, What to Skip, How to Stay Sane](masterclass/part-12-what-breaks-what-to-skip-how-to-stay-sane.md) | Context is the first wall; integrations fail silently |

Front matter: [Orientation](masterclass/00-0-orientation.md) · [The System in One Picture](masterclass/00-1-the-system-in-one-picture.md) · [The Twelve Parts, Indexed](masterclass/00-2-the-twelve-parts-indexed.md)

Appendices: [A Commands](masterclass/appendix-a-complete-command-index.md) · [B Paths](masterclass/appendix-b-every-path-and-what-lives-there.md) · [C Numbers](masterclass/appendix-c-every-number-in-one-table.md) · [D Failure Triage](masterclass/appendix-d-failure-triage.md) · [E 30/60/90](masterclass/appendix-e-a-30-60-90-adoption-path.md) · [F Personality and Profile](masterclass/appendix-f-personality-and-profile-soul-md-and-user-md.md) · [G Skills and Plugins by Example](masterclass/appendix-g-skills-and-plugins-by-example.md) · [H Worked Build Prompts](masterclass/appendix-h-worked-build-prompts.md) · [I Sources](masterclass/appendix-i-sources.md)

---

## The one sentence version

A chatbot predicts the next token. Hermes runs a process: it assembles a layered prompt, resolves a provider, calls the model, dispatches whatever tools the model asked for, feeds the results back, and repeats until the model produces text instead of another tool call. Then it saves the session, updates its memory, and is ready to resume later. Volume 1 is that loop. Volume 2 is the window on it. Volume 3 is several of them, talking. Volume 4 is what they are for.

---

## What is in this repository

```text
README.md                         you are here
assets/art/                       56 original images: heroes, one per part, and the diagram plates for all four volumes
masterclass/                      Volume 1: front matter, twelve parts, the Build Track, nine appendices, FULL-MASTERCLASS.md
desktop/                          Volume 2: ten builds, the ledger, FULL-HERMES-DESKTOP.md
bots/                             Volume 3: ten builds, the ledger, FULL-HERMES-BOTS.md
company/                          Volume 4: ten builds, the ledger, FULL-HERMES-COMPANY.md
kits/
  desktop-plugins/                hello-hermes, prompt-library, fleet-board (one plugin.js each)
  agent-plugins/ledger/           the unified package: plugin.yaml, tools, dashboard API, desktop page
  bot-team/                       atlas, forge, scout, quill, sentinel, ops, and memory/ (Hindsight and Mnemosyne setup)
  company/                        COMPANY.md, ORG.yaml, POLICIES.md, ATLAS-PROTOCOL.md, life/, cadence/, production/, clients/
src/source.md                     the authored source of Volume 1
src/volumes/                      the authored parts of Volumes 2 to 4; kit files are spliced in at build time
tools/                            the scripts that turn the sources into the volume folders
```

To rebuild Volume 1 after editing `src/source.md`:

```bash
cp src/source.md /tmp/mc-source.md
python3 tools/convert.py
python3 tools/split.py
```

To rebuild a later volume after editing `src/volumes/` or a kit file (bots shown; use `desktop` or `company` and the matching title):

```bash
python3 tools/assemble-volume.py bots /tmp/bots.md
python3 tools/convert-volume.py /tmp/bots.md /tmp/bots.converted.md
python3 tools/split-volume.py /tmp/bots.converted.md bots "The Hermes Bots Masterclass" FULL-HERMES-BOTS.md
```

---

## Licensing

Full detail in [LICENSE](LICENSE).

| Layer | Status |
|---|---|
| The text of Volumes 2, 3 and 4, the whole Build Track in Volume 1, all 56 images, the reference tables, the operator drills, and Appendices E through H | **CC BY 4.0.** Share and adapt freely, including commercially, with credit |
| The substance of Volume 1's Parts 1 to 12 | **Tony Simons' work.** Published free by the author, reproduced here with credit, and not relicensed by this repository |
| Everything under `kits/` and `tools/` | **MIT.** See [LICENSE-CODE](LICENSE-CODE) |

## A note on scope

This is a study reference, not documentation for the Hermes project. For installation, the current API surface, and anything authoritative, go to the [official Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/getting-started/installation). Volume 1's parts reflect the series as published in July 2026; every build in every volume was checked against the documentation in September 2026. A fast-moving project will have moved since, which is exactly why the prompts read the docs before they write.
