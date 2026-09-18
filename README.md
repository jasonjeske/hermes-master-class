![Hermes Agent Masterclass](assets/art/hero.webp)

# Hermes Agent Masterclass

### ➡️ [**Read the whole masterclass in one page**](masterclass/FULL-MASTERCLASS.md)

*37 sections top to bottom with every illustration inline and a linked table of contents. 12 parts, a 10-build track of copy-paste prompts, 9 appendices, 40 original images, 150+ reference tables.*

---

Two halves, one document.

**The first half** is Tony Simons' twelve-part **Hermes Agent Master Class**, published on X between July 5 and July 20, 2026, combined into one navigable reference. Every part carries an illustrated plate, the scattered constants pulled into tables, and a concrete exercise so the material can be practiced rather than only read.

**The second half is the Build Track.** Ten builds, in the order the pieces depend on each other, that take you from a fresh install to a Hermes with a real identity, seeded memory, project context, skills, plugins, a four-layer memory stack (built-in files, session search, one of Honcho, Mem0 or Hindsight, and an Obsidian vault), a profile roster, cron jobs, delegation, a kanban board, and the tuning and safety settings that decide cost and blast radius. Every prompt is written to be pasted as it is. Every path, key, command and tool name was checked against the official Hermes documentation, and each build names the page it was checked against.

The prompts share one shape, borrowed from the people who run Hermes hardest: tell the agent which documentation page to read, name the exact file and key, and require the diff before anything is saved. Hermes ships often and a model's memory of the project is always a version behind; that shape is why the prompts keep working after the next release.

The original article artwork is not reproduced here. Every illustration and plate in this repository was generated for it.

> 📝 **Attribution**
>
> The substance and the structure of the twelve parts are the work of **[Tony Simons (@tonysimons_)](https://x.com/tonysimons_)**. Every source article is linked in [Appendix I](masterclass/appendix-i-sources.md), and the original figures live in those articles, not here.
>
> Added in this compilation: the whole Build Track, forty original images, the consolidated constant and failure-triage tables, the vocabulary table, twelve operator drills, the cross-references between parts, the 30/60/90 adoption path, and Appendices F through H. Nothing was invented about how Hermes behaves. Where a number, path, key or command appears, it came from the source series or from the official documentation named in Appendix I.
>
> Hermes Agent is a project of [Nous Research](https://hermes-agent.nousresearch.com/docs/getting-started/installation).

---

## Start here

| If you want to | Read |
|---|---|
| Understand how Hermes works, end to end | [Part 1](masterclass/part-01-how-hermes-actually-processes-work.md) onward, in order |
| Build a Hermes setup this weekend with prompts you paste | [The Build Track](masterclass/build-00-0-the-build-track.md), Builds 0 to 10, in order |
| Fix a specific thing | [Appendix D: Failure Triage](masterclass/appendix-d-failure-triage.md) |
| Look something up | [Appendix A: Commands](masterclass/appendix-a-complete-command-index.md) · [B: Paths](masterclass/appendix-b-every-path-and-what-lives-there.md) · [C: Numbers](masterclass/appendix-c-every-number-in-one-table.md) |

---

## The Build Track

| Build | You end up with | Checked against |
|---|---|---|
| [0 Day One](masterclass/build-00-day-one.md) | A working install, a chosen provider, and the daily command set | Quickstart, CLI reference |
| [1 SOUL.md](masterclass/build-01-soul-md.md) | A SOUL.md that shapes behavior, three complete files to start from, and personality overlays | Personality doc |
| [2 USER.md and MEMORY.md](masterclass/build-02-user-md-and-memory-md.md) | Both memory files seeded from an interview and from your machine, plus the cheap-model review | Memory doc, import doc |
| [3 Project Context](masterclass/build-03-project-context.md) | An AGENTS.md per project and a personal override file | Context Files doc |
| [4 Skills](masterclass/build-04-skills.md) | Skills written from work you already did, a bundle, and a configured curator | Skills docs, Creating Skills guide |
| [5 Plugins](masterclass/build-05-plugins.md) | The bundled safety plugins on, and a minimal plugin written to the documented shape | Plugins docs |
| [6 The Memory Stack](masterclass/build-06-the-memory-stack.md) | Four layers: built-in, session search, Honcho or Mem0 or Hindsight, and an Obsidian vault, plus a nightly consolidation job | Memory Providers, Honcho docs |
| [7 Profiles](masterclass/build-07-profiles.md) | A roster with a frontier planner and inexpensive workers | Profiles doc |
| [8 Cron](masterclass/build-08-cron.md) | Jobs that brief themselves, stay silent when healthy, and cost nothing when no reasoning is needed | Cron doc |
| [9 Delegation and Kanban](masterclass/build-09-delegation-and-kanban.md) | A cheap child fleet and a board the profiles work from | Delegation and Kanban docs |
| [10 Tuning and Safety](masterclass/build-10-tuning-and-safety.md) | Approvals, model routing, effort levels, and a weekly maintenance habit | Configuration and Security docs |
| [The Build Ledger](masterclass/build-11-the-build-ledger.md) | One proof line per build | |

---

## The twelve parts

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

### Front matter

- [Orientation](masterclass/00-0-orientation.md): how to read this, and the one-sentence version
- [The System in One Picture](masterclass/00-1-the-system-in-one-picture.md): nine subsystems in a single plate
- [The Twelve Parts, Indexed](masterclass/00-2-the-twelve-parts-indexed.md): the index and the front-loaded vocabulary

### Appendices

- [A: Complete Command Index](masterclass/appendix-a-complete-command-index.md): every command the series names, grouped by intent
- [B: Every Path and What Lives There](masterclass/appendix-b-every-path-and-what-lives-there.md): the `~/.hermes` tree annotated, including the memories, bundles, plugins and profiles directories
- [C: Every Number in One Table](masterclass/appendix-c-every-number-in-one-table.md): every budget, threshold and timer in one place
- [D: Failure Triage](masterclass/appendix-d-failure-triage.md): symptom, likely cause, the check to run
- [E: A 30/60/90 Adoption Path](masterclass/appendix-e-a-30-60-90-adoption-path.md): the same material ordered by what to do first
- [F: Personality and Profile](masterclass/appendix-f-personality-and-profile-soul-md-and-user-md.md): what belongs in SOUL.md and USER.md, with complete worked files and an interview prompt that writes them for you
- [G: Skills and Plugins by Example](masterclass/appendix-g-skills-and-plugins-by-example.md): a full SKILL.md you can copy, bundles, safe hub installs, and when a plugin is actually warranted
- [H: Worked Build Prompts](masterclass/appendix-h-worked-build-prompts.md): two real prompts that produce working systems, why they work, and a reusable template
- [I: Sources](masterclass/appendix-i-sources.md): all twelve original articles, plus every documentation page the Build Track was checked against

---

## The one sentence version

A chatbot predicts the next token. Hermes runs a process: it assembles a layered prompt, resolves a provider, calls the model, dispatches whatever tools the model asked for, feeds the results back, and repeats until the model produces text instead of another tool call. Then it saves the session, updates its memory, and is ready to resume later.

Everything in the twelve parts is a consequence of that loop existing. Everything in the Build Track is a file or a config block that shapes it.

---

## What is in this repository

```text
README.md                         you are here
assets/art/                       40 original images: hero, one per part, the Build Track plate, and 26 diagram plates
masterclass/
  00-*.md                         orientation, the system plate, the index
  part-01..12-*.md                the twelve parts
  build-00..11-*.md               the Build Track: introduction, ten builds, the ledger
  appendix-a..i-*.md              the nine appendices
  FULL-MASTERCLASS.md             everything in one file
src/source.md                     the authored source every markdown file is generated from
tools/                            the two scripts that turn the source into the masterclass/ files
```

Pure GitHub Markdown. Tables and images render here with nothing to install, and the whole thing can be cloned and read offline or fed to an agent.

To rebuild the `masterclass/` files after editing `src/source.md`:

```bash
cp src/source.md /tmp/mc-source.md
python3 tools/convert.py      # typed blocks in the source to GitHub markdown
python3 tools/split.py        # one file per section, plus FULL-MASTERCLASS.md
```

---

## Licensing

Two kinds of material, two different statuses. Full detail in [LICENSE](LICENSE).

| Layer | Status |
|---|---|
| All 40 illustrations and plates, the reference tables, the operator drills, Appendices E through H, and the whole Build Track | **CC BY 4.0.** Share and adapt freely, including commercially, with credit |
| The substance of Parts 1 to 12 | **Tony Simons' work.** Published free by the author, reproduced here with credit, and not relicensed by this repository |
| The scripts in `tools/` | **MIT.** See [LICENSE-CODE](LICENSE-CODE) |

The original article artwork is not reproduced anywhere here. To reuse the source material itself rather than this compilation's additions, the articles are linked per-part in [Appendix I](masterclass/appendix-i-sources.md) and the author is the person to ask.

## A note on scope

This is a study reference, not documentation for the Hermes project. For installation, the current API surface, and anything authoritative, go to the [official Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/getting-started/installation). The twelve parts reflect the series as published in July 2026; the Build Track was checked against the documentation in September 2026. A fast-moving project will have moved since, which is exactly why every prompt in the Build Track reads the docs before it writes.
