# Stage 4: Memory and Context Files

### What this stage changes

The text Hermes adds to the system prompt from files: your memory (MEMORY.md and USER.md), the project rule file it finds in your working folder, and SOUL.md. Each of them rides every call, so this stage makes each one earn its place. It turns nothing off unless you choose to.

### Memory

Memory is two small stores: MEMORY.md for what the agent learns, USER.md for what it knows about you. Both go into the system prompt of every call. Their caps are `memory.memory_char_limit` (2,200 characters) and `memory.user_char_limit` (1,375), and a write past a cap is refused. We filled both toward their caps, 1,340 and 710 characters, and measured:

| Setup | Tokens before your first word | Change |
|---|---|---|
| Fresh install, empty memory | 13,769 |  |
| Memory filled toward its caps | 14,456 | plus 686 in the memory row |
| Same, with the memory toolset off | 13,374 | the memory row stays at 686 |
| Same, with both memory flags set to false | 12,687 | minus 1,769 from full memory |

Turning the memory toolset off removes the memory tool (821 tokens of schema in `/context all`) and its guidance, 1,082 tokens in all, but MEMORY.md and USER.md stay in the prompt. Only the two flags take them out:

*`memory-off.sh`*

```bash
hermes config set memory.memory_enabled false
hermes config set memory.user_profile_enabled false
```

That also ends memory across sessions, so most people should keep memory and keep it lean. A rule from [Mervin Praison](https://mer.vin/2026/05/soul-md-for-ai-agents-30-80-line-identity-blueprint-before-memory-or-tools/) is a good one to adopt: memory holds durable facts, procedures belong in skills, task logs stay out, and stale entries go at a monthly review. A task log in MEMORY.md is paid on every call. To cut an entry, edit MEMORY.md or USER.md in the memories folder beside config.yaml: a line holding only a section sign separates entries, so remove one of those lines with the entry.

Watch the caps too. A store at nine tenths of its cap or more is close to refusing writes, and it is the line the weekly audit in [Stage 8](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-08-keep-it-tuned.md) reports on. Count a store with `wc -m` on its file: the cap counts characters, while `hermes prompt-size` reports each store in bytes with about 335 bytes of header around it.

Memory is also a frozen snapshot, as [witcheer](https://x.com/witcheer/status/2069020659829608570) points out. A save during a session reaches the file at once but reaches the prompt only in your next session, which keeps the prompt cache warm. So trim memory, then start a new session to see the saving.

### Context files

Hermes adds the project rule file it finds for your working folder to the system prompt, and the file costs more than its own size. In our install a 2,406-byte AGENTS.md, about 602 tokens on its own, cost 1,401 tokens: 15,170 against 13,769. Nearly all the rest is what the file switches on. An AGENTS.md marks the folder as a code project (`agent/coding_context.py:35`), so Hermes adds its coding brief to the system prompt and a short workspace snapshot after the file. `/context` shows 876 tokens in the rules row and 525 more in the system prompt.

Only one kind of rule file loads: the first one Hermes finds with content, in this order ([witcheer](https://x.com/witcheer/status/2069385776756895880) flagged the trap):

| Order | File | Where Hermes looks |
|---|---|---|
| 1 | `.hermes.md` or `HERMES.md` | The working folder, then each parent up to the git root |
| 2 | The `AGENTS.md` chain | Every folder from the git root down to the working folder; in each one, `AGENTS.override.md` wins over `AGENTS.md` |
| 3 | `CLAUDE.md` | The working folder only |
| 4 | `.cursorrules` and `.cursor/rules/*.mdc` | The working folder only; every one of these files with content loads |

So a stray `.hermes.md` silently replaces your AGENTS.md, and a CLAUDE.md next to an AGENTS.md never loads. Keep one rule file per project, and keep it short. For a personal version of a team's AGENTS.md, put an `AGENTS.override.md` beside it and keep it out of git ([witcheer](https://x.com/witcheer/status/2096481734388858931)); in that folder it loads instead of the shared file.

Three more costs hide in these files. Every subagent reads the AGENTS.md chain again (not SOUL.md), so a long rule file is paid once more by each child. A context file that takes more than 5 seconds to read, such as a cloud-synced file that is only stored online, is skipped with only a line in agent.log. And each file is capped, by default at a slice of the model's window and never below 20,000 characters; Hermes keeps the start and the end of a longer one and marks what it cut.

SOUL.md is the agent's identity. It loads from your Hermes home in every session, never from the working folder, and it rides every call. Hermes builds the system prompt once per session, so an edit to SOUL.md applies in your next session, whatever the comment in the seeded file says.

### Coding context

`agent.coding_context` decides how much coding help rides along. The default, `auto`, adds a coding brief and a live git snapshot when you work interactively in a code project. `focus` goes further once Hermes detects a coding project: it narrows the toolsets to the coding set and shows the non-coding skill categories as names only, without descriptions. In an empty folder it changed nothing in our install, because there was no project to detect. If you code in one repository all day, try it there and measure it with the stage prompt:

*`coding-focus.sh`*

```bash
hermes config set agent.coding_context focus
```

### The stage prompt

Paste it into a Hermes session that has its terminal tool, started in the project folder you work in.

*`prompt-stage-4-memory.md`*

```markdown
Tune Hermes, stage 4: Memory and Context Files. Work in five steps, one change at a time.
MEASURE: Read my memory caps with `hermes config get memory.memory_char_limit` and `hermes config get memory.user_char_limit`, and count MEMORY.md and USER.md in the memories folder beside config.yaml with `wc -m`, the counts only, never their text. Then review the memory, user profile and project rule file in your system prompt, and mark every entry that is a task log, out of date or said twice. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: The one change that saves the most: memory cut down to durable facts, a shorter project rule file, or `hermes config set memory.memory_enabled false` and `hermes config set memory.user_profile_enabled false` if I do not use memory. For a memory or rule file, quote the exact entries or lines to cut and give me the `cp -p` command that keeps a dated copy beside the file, because I make the copy and the cut myself. Show the exact command and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: For a memory or rule file, change nothing and wait until I tell you the cut is made. For the config change, run `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in the folder `hermes config path` points to, with the current date and time and never over an existing backup, then run only the commands I approved. Never edit config.yaml with write_file or patch.
VERIFY: Count MEMORY.md and USER.md again with `wc -m` and compare them with the first counts and with their caps. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

- [ ] `hermes prompt-size --json` shows the size you trimmed smaller than before this stage
- [ ] `wc -m` counts MEMORY.md and USER.md under nine tenths of `memory.memory_char_limit` and `memory.user_char_limit`
- [ ] Every memory entry left is a durable fact, with no task logs and nothing said twice
- [ ] Exactly one project rule file loads in your working folder, and a new session's `/context` lists it
- [ ] A dated copy of every file this stage changed sits next to it, config.yaml as `config-YYYY-MM-DD-HHMMSS.yaml`

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-TUNING.md)
