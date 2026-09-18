# Build 0: Day One

![Build 0](../assets/art/part-02.webp)

### What you are building

A Hermes install that answers, a provider you chose on purpose, a backup you took before touching anything, and the short list of commands you will actually type every day.

### What the docs say

Checked against the Quickstart and the CLI command reference.

| Fact | Detail |
|---|---|
| Install | One command on Linux and macOS. The installer page carries the Windows PowerShell command |
| Setup modes | `hermes setup` offers Quick Setup (Nous Portal, OAuth, no keys to manage), Full Setup (every provider and option, bring your own keys), and Blank Slate (only provider, file operations and terminal; nothing else loads until you enable it) |
| Provider choice | `hermes model` walks the choice interactively and can be rerun any time; there is no lock-in |
| Where things go | Secrets and tokens in `~/.hermes/.env`. Non-secret settings in `~/.hermes/config.yaml`. `hermes config set` writes either one for you |
| Two terminal UIs | `hermes --tui` is the modern one; the classic prompt UI is `hermes chat`. Both share sessions and slash commands |
| Resume | `hermes --continue` resumes the most recent session |
| Health | `hermes doctor` diagnoses config and dependencies (`--fix` repairs what it can). `hermes status` shows agent, auth and platform state |
| Backup | `hermes backup` zips the whole home directory; `--quick --label <name>` takes a state-only snapshot |
| Prompt cost | `hermes prompt-size` shows a byte breakdown of the system prompt: skills index, memory, profile, tool schemas. It runs offline |

### Commands

*`day-one.sh`*

```bash
# 1. Install (Linux and macOS)
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 2. Choose your setup mode and provider
hermes setup            # Quick Setup, Full Setup, or Blank Slate
hermes model            # pick or change the provider at any time

# 3. Prove it answers
hermes --tui

# 4. Health, then a backup before you change anything
hermes doctor
hermes status
hermes backup --quick --label "day-one"

# 5. See what every prompt is already costing you
hermes prompt-size
```

> 📝 **Which setup mode**
>
> Quick Setup is the fastest way to a working agent if you are happy to bill through Nous Portal. Full Setup is right if you already hold provider keys. Blank Slate is the choice for people who want to add every capability deliberately, and it is the safest starting point on a machine you care about, because nothing you did not choose ever loads, even after `hermes update`. Every build in this track works from any of the three; Blank Slate users re-enable toolsets with `hermes tools` as each build needs them.

### Prompts

The first prompt exists to test tools, not conversation. Part 2 makes the case: an agent that can chat but cannot act is a chatbot, and you find that out on day one or on the day it matters.

*`prompt-00-prove-the-loop.md`*

```markdown
Before we build anything, prove your tool surface works. Do these in order
and report each result on its own line, with the tool you used:

1. Run a terminal command that prints the current directory, the OS, and
   the shell.
2. Read the file ~/.hermes/config.yaml and tell me the model and provider
   currently set. Do not print any keys or tokens.
3. Write a small file at ~/hermes-day-one.txt containing today's date and
   the model name, then read it back to prove it landed.
4. Fetch the page https://hermes-agent.nousresearch.com/docs/getting-started/quickstart
   and tell me the three setup modes it lists.
5. List the toolsets you currently have and name any that are gated off,
   with the reason if you can tell.

If any step fails, say which one and why. Do not work around a failure
silently; a missing tool is exactly what I need to know today.
```

*`prompt-00-daily-commands.md`*

```markdown
Read the CLI command reference at
https://hermes-agent.nousresearch.com/docs/reference/cli-commands
and give me a two-column table of the twenty commands and slash commands a
person running you every day would actually use, grouped as: start and
resume, models and tools, memory and skills, sessions, and maintenance.
One line per command, what it does in under twelve words, nothing else.
```

### The daily set

You will get your own table from the prompt above. This is the one this masterclass would hand you.

| Intent | Command |
|---|---|
| Start the modern UI | `hermes --tui` |
| Resume the last session | `hermes --continue` |
| Fresh thread, optional name | `/new` or `/new payments-refactor` |
| Change model or provider | `hermes model` or `/model` |
| See and tune tool access | `hermes tools` and `/tools` |
| Switch a personality overlay | `/personality technical` |
| Teach a skill from a source | `/learn <url, path, or description>` |
| Browse and install skills | `hermes skills browse`, `hermes skills install <name>` |
| Turn a bundled plugin on | `hermes plugins enable <name>` |
| Health and state | `hermes doctor`, `hermes status` |
| Read and change settings | `hermes config show`, `hermes config set <key> <value>` |
| Prompt cost | `hermes prompt-size` |
| Token and cost analytics | `hermes insights` |
| Snapshot before changes | `hermes backup --quick --label <name>` |
| Update, with a preview first | `hermes update --check`, then `hermes update --backup` |

### Verify

- [ ] hermes doctor reports no errors
- [ ] The five-step tool prompt passed all five steps, or you know exactly which failed
- [ ] A backup exists from before your first change
- [ ] hermes prompt-size ran and you noted the total, so Build 2 and Build 4 have a baseline

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
