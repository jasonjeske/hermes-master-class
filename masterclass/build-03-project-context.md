# Build 3: Project Context

![Build 3](../assets/art/part-05.webp)

### What you are building

One AGENTS.md at the root of each repository you work in, so the agent stops re-learning your project every session, plus a personal override file for the instructions that should not be committed.

### What the docs say

Checked against the Context Files page.

| Fact | Detail |
|---|---|
| Priority | One project context type loads per session, first match wins: `.hermes.md`, then `AGENTS.override.md`, then `AGENTS.md`, then `CLAUDE.md`, then `.cursorrules`. SOUL.md always loads separately as the identity |
| The override | If `AGENTS.override.md` sits next to `AGENTS.md`, the override loads instead of the committed file. Keep it gitignored for personal instructions |
| The chain | Inside a git repository, Hermes merges the git-root AGENTS.md with every AGENTS.md between the root and your working directory, in order |
| Progressive discovery | As the agent reads or runs things in subdirectories, it loads any AGENTS.md it finds there, once per directory, walking up to five parents. Nothing bloats the prompt until it is needed |
| Scanning | Context files are scanned for prompt-injection patterns before they load. A file that trips a pattern is blocked, which is the right outcome for a cloned repo you have not read |
| Cron | Cron jobs load no context file at all unless the job carries a `--workdir`. Build 8 covers this |

### Prompts

*`prompt-03-write-agents-md.md`*

```markdown
We are going to give this repository an AGENTS.md. Do these in order.

1. Read https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files
   and tell me in four lines which file wins when several exist, how the
   directory chain works, and what a personal AGENTS.override.md is for.
2. Explore this repository: the README, the package or build manifest,
   the test command, the folder layout, and any existing context files.
   Do not read secrets or .env files.
3. Draft AGENTS.md at the git root with exactly these sections:
   - What this project is, in three sentences.
   - How to run it, test it, and build it. Real commands, verified by
     running the read-only ones.
   - Conventions: language, formatter, naming, branch and commit rules.
   - Where things live: the five or six folders that matter and what is
     in each.
   - What never to do in this repo.
   Keep it under 120 lines. Facts only, no praise for the codebase.
4. If any subfolder works differently enough to need its own file,
   propose a nested AGENTS.md for it and say why.
5. Show me the file before writing it. After I say go, write it, then
   start a fresh session in this directory and tell me what you know
   about the project and where that knowledge came from.
```

*`prompt-03-override.md`*

```markdown
Create AGENTS.override.md next to the committed AGENTS.md in this
repository, containing only my personal instructions for working here:
my scratch folder, the branch prefix I use, and that I want a diff before
any file write in src/. Add it to .gitignore. Confirm from the Context
Files doc that the override replaces the committed file rather than
adding to it, and warn me if anything in AGENTS.md would therefore stop
applying to me.
```

### A template to start from

*`AGENTS.md`*

```markdown
# Project

One paragraph: what this is, who uses it, what "working" means.

# Run, test, build

- Run: `<command>`
- Test: `<command>` (must pass before any commit)
- Build: `<command>`

# Conventions

- Language and version, formatter, lint command.
- Naming rules that a reader would not guess.
- Branch prefix and commit message shape.

# Where things live

- `src/`: ...
- `tests/`: ...
- `scripts/`: ...

# Never

- Never edit generated files under `<path>`.
- Never run the migration command against anything but the local database.
- Never commit `.env` or anything under `secrets/`.
```

### Verify

- [ ] A fresh session in the repo names AGENTS.md as where it learned the project
- [ ] The override file is gitignored and the agent confirms it replaces the committed file
- [ ] hermes prompt-size in that directory shows the context file bytes

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
