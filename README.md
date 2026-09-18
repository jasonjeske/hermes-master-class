![Hermes Agent Masterclass](assets/art/hero.webp)

# Hermes Agent Masterclass

### ➡️ [**Read the whole masterclass in one page**](masterclass/FULL-MASTERCLASS.md)

*All 24 sections top to bottom, with every illustration and diagram inline and a linked table of contents. 12 parts, 9 appendices, 24 diagrams, 40+ reference tables.*

---

A single, offline, deeply indexed reference built from Tony Simons' twelve-part **Hermes Agent Master Class**, published on X between July 5 and July 20, 2026.

The original series is excellent and it is serialized across twelve articles. This repository combines it into one navigable document, adds a workflow diagram to every part, pulls the scattered constants into reference tables, and attaches a concrete exercise to each section so the material can be practiced rather than only read.

The original article artwork is not reproduced here. The illustrations in this repository were generated for it, and every diagram was drawn for it. Read the source articles for the author's own figures.

> 📝 **Attribution**
>
> The substance and the structure of this material are the work of **[Tony Simons (@tonysimons_)](https://x.com/tonysimons_)**. Every source article is linked in [Appendix I](masterclass/appendix-i-sources.md), and the original figures live in those articles, not here.
>
> Added in this compilation: twenty-four workflow diagrams, the consolidated constant and failure-triage tables, the vocabulary table, twelve operator drills, the cross-references between parts, and the 30/60/90 adoption path. Nothing was invented about how Hermes behaves. Where a number appears, it came from the source.
>
> Hermes Agent is a project of [Nous Research](https://hermes-agent.nousresearch.com/docs/getting-started/installation).

---

## Read it your way

| Format | File | Best for |
|---|---|---|
| **Web page** | [`document/hermes-agent-masterclass.html`](document/hermes-agent-masterclass.html) | The full experience. Large-type reading layout, section illustrations, 21 live diagrams, fully offline, zero network calls |
| **PDF** | [`document/hermes-agent-masterclass.pdf`](document/hermes-agent-masterclass.pdf) | 110 pages, large type, selectable text, every diagram as vector art |
| **Markdown** | [`masterclass/`](masterclass/) | Reading on GitHub, diffing, quoting, or feeding to an agent |
| **One file** | [`masterclass/FULL-MASTERCLASS.md`](masterclass/FULL-MASTERCLASS.md) | The whole thing in a single markdown file |

The HTML is a single self-contained file, so it works with no internet connection and nothing to install. Download it and open it.

---

## Three ways through the material

The parts genuinely build on each other. Part 3 assumes Part 2's session persistence works. Part 6 assumes Part 4's skills exist. Part 10 assumes Part 11's profiles.

| Path | What you read | Time |
|---|---|---|
| **Foundation** | Parts 1, 2, 3, 5 and Appendix D | About 40 minutes |
| **Operator** | Foundation plus Parts 4, 6, 7, 12 | About 90 minutes |
| **Full stack** | All twelve parts and every appendix | Half a day |

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
- [The System in One Picture](masterclass/00-1-the-system-in-one-picture.md): nine subsystems in a single graph
- [The Twelve Parts, Indexed](masterclass/00-2-the-twelve-parts-indexed.md): the index and the front-loaded vocabulary

### Appendices

- [A: Complete Command Index](masterclass/appendix-a-complete-command-index.md): every command the series names, grouped by intent
- [B: Every Path and What Lives There](masterclass/appendix-b-every-path-and-what-lives-there.md): the `~/.hermes` tree annotated
- [C: Every Number in One Table](masterclass/appendix-c-every-number-in-one-table.md): every budget, threshold and timer in one place
- [D: Failure Triage](masterclass/appendix-d-failure-triage.md): symptom, likely cause, the check to run
- [E: A 30/60/90 Adoption Path](masterclass/appendix-e-a-30-60-90-adoption-path.md): the same material ordered by what to do first
- [F: Personality and Profile](masterclass/appendix-f-personality-and-profile-soul-md-and-user-md.md): what belongs in SOUL.md and USER.md, with complete worked files and an interview prompt that writes them for you
- [G: Skills and Plugins by Example](masterclass/appendix-g-skills-and-plugins-by-example.md): a full SKILL.md you can copy, bundles, safe hub installs, and when a plugin is actually warranted
- [H: Worked Build Prompts](masterclass/appendix-h-worked-build-prompts.md): two real prompts that produce working systems, why they work, and a reusable template
- [I: Sources](masterclass/appendix-i-sources.md): all twelve original articles, linked

---

## The one sentence version

A chatbot predicts the next token. Hermes runs a process: it assembles a layered prompt, resolves a provider, calls the model, dispatches whatever tools the model asked for, feeds the results back, and repeats until the model produces text instead of another tool call. Then it saves the session, updates its memory, and is ready to resume later.

Everything in the twelve parts is a consequence of that loop existing.

---

## What is in this repository

```text
README.md                         you are here
assets/art/                       13 original illustrations, hero plus one per part
document/
  hermes-agent-masterclass.html   the full document, self-contained and offline
  hermes-agent-masterclass.pdf    110 pages, large-type print layout
  source.md                       the authored source the HTML and PDF are built from
masterclass/
  00-*.md                         orientation, the system graph, the index
  part-01..12-*.md                the twelve parts
  appendix-a..i-*.md              the nine appendices
  FULL-MASTERCLASS.md             everything in one file
```

The markdown uses GitHub-flavored tables and fenced `mermaid` blocks, so every diagram renders natively here with nothing to install.

---

## Licensing

Two kinds of material, two different statuses. Full detail in [LICENSE](LICENSE).

| Layer | Status |
|---|---|
| The illustrations, all 24 diagrams, the reference tables, the operator drills, and Appendices E through H | **CC BY 4.0.** Share and adapt freely, including commercially, with credit |
| The substance of Parts 1 to 12 | **Tony Simons' work.** Published free by the author, reproduced here with credit, and not relicensed by this repository |
| The build tooling in `build/` | **MIT.** See [LICENSE-CODE](LICENSE-CODE) |
| Bundled Mermaid in the HTML | **MIT.** See [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md) |

The original article artwork is not reproduced anywhere here. To reuse the source material itself rather than this compilation's additions, the articles are linked per-part in [Appendix I](masterclass/appendix-i-sources.md) and the author is the person to ask.

## A note on scope

This is a study reference, not documentation for the Hermes project. For installation, the current API surface, and anything authoritative, go to the [official Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/getting-started/installation). Behavior described here reflects the series as published in July 2026 and a fast-moving project will have moved since.
