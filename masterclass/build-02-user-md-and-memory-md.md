# Build 2: USER.md and MEMORY.md

![Build 2](../assets/art/part-03.webp)

### What you are building

The two built-in memory files, seeded on purpose instead of accumulating by accident: USER.md from a short interview, MEMORY.md from an inspection of the machine the agent actually runs on. Plus the habit that makes memory pay off, and the cheap-model setting that makes the background review affordable.

### What the docs say

Checked against the Memory page and the Import from Other Agents page.

| Fact | Detail |
|---|---|
| Where | Both files live in `~/.hermes/memories/`. MEMORY.md is the agent's notes about the environment and lessons. USER.md is your profile: preferences, communication style, expectations |
| Limits | MEMORY.md 2,200 characters, about 800 tokens. USER.md 1,375 characters, about 500 tokens. Exceeding a limit returns an error that shows the current entries so the agent can consolidate; nothing is silently dropped |
| Frozen snapshot | Both are rendered into the system prompt once, at session start, and never change mid-session. That preserves the prompt cache. Writes go to disk immediately and show up in the next session |
| The tool | The `memory` tool adds, replaces and removes entries. `replace` and `remove` match a short unique substring of the entry, not the whole text; an ambiguous substring is refused |
| The boundary | Memory is built around the moment a session ends. Run `/new` at natural boundaries: a finished task, a topic change, the start of a day. Each boundary re-reads the updated files |
| Recall | `session_search` searches every past conversation over full-text search in `~/.hermes/state.db`. It costs nothing until it is called, so the split is: memory for what should always be in context, session search for everything else |
| Config | `memory.memory_enabled`, `memory.user_profile_enabled`, `memory.memory_char_limit`, `memory.user_char_limit`, `memory.write_approval` (default false, writes freely) |
| Review cost | The background review that proposes memory and skill writes runs on the main model by default. `auxiliary.background_review.provider` and `.model` point it at a cheaper model; capture quality held in the project's own testing |
| Import | `hermes import-agent claude-code` or `hermes import-agent codex` maps global instruction files into MEMORY.md entries, permission rules into the command allowlist and `approvals.deny`, MCP servers into `mcp_servers`, and skills into their own category. Credentials are never read. `--dry-run` previews, `--sync` re-imports what changed |

### Prompts

*`prompt-02-seed-user.md`*

```markdown
We are going to seed USER.md, the file you keep about me. Do these in order.

1. Read https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
   and tell me in three lines what USER.md is for, its character limit,
   and how the memory tool's replace action matches an entry.
2. Show me what ~/.hermes/memories/USER.md contains right now.
3. Interview me in short rounds, one subject each, and start each round
   with what you already believe so I only correct you:
   - How to talk to me: length, tone, what annoys me.
   - Standing preferences: languages, package managers, spelling,
     formatting, anything I would otherwise repeat.
   - Things you must never ask me twice.
   - My environment in one line: time zone, working hours, main machine.
4. Write the entries with the memory tool, target "user", one fact per
   entry, shortest phrasing that still stands alone. Stay well under the
   1,375 character limit; leave room for what you learn on your own.
5. Show me the finished file. Tell me which things I said you deliberately
   left out because they belong in a project's AGENTS.md instead.
```

*`prompt-02-seed-memory.md`*

```markdown
Seed MEMORY.md, your own notes, from the machine you are running on rather
than from guesses. Do these in order.

1. Inspect the environment with the terminal: OS and version, shell,
   package managers present, language runtimes and versions, container
   tools, the folders under my home where projects live, and any CLI
   tools you can see that you will use often.
2. Read ~/.hermes/config.yaml and note the model, the provider, and which
   toolsets are enabled. Do not record any secret.
3. Write eight to twelve entries with the memory tool, target "memory".
   Each entry is a fact you would otherwise have to rediscover: a version,
   a path, a quirk, a convention. No opinions, no project details.
4. Show me the file and its usage count against the 2,200 character
   limit. Leave at least a third of the budget free.
```

*`prompt-02-consolidate.md`*

```markdown
Your memory is near its limit. Read every entry in MEMORY.md and USER.md,
then propose a consolidation: merge overlapping entries, drop anything a
session_search could recover in one query, and shorten what remains.
Show me the before and after side by side with the character counts.
Do not write anything until I say go.
```

*`prompt-02-import.md`*

```markdown
I used another coding agent before Hermes. Read
https://hermes-agent.nousresearch.com/docs/user-guide/import-from-other-agents
then run hermes import-agent --dry-run and walk me through the plan it
prints: what would land in MEMORY.md, what becomes an allowlist or deny
rule, which skills would be copied and where, and what was reported as
unmapped. Do not apply it. I will decide item by item and then say go.
```

### The cheap review

*`~/.hermes/config.yaml`*

```yaml
auxiliary:
  background_review:
    provider: openrouter                 # any configured provider
    model: your-inexpensive-model        # a fast model is enough for the review
```

*`prompt-02-cheap-review.md`*

```markdown
Read the "background review" section of
https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
Then set auxiliary.background_review.provider and
auxiliary.background_review.model in my config.yaml to the cheapest model
I have configured that you would trust to summarize a conversation. Show
me the diff before you save it. After I say go, run hermes config show
and confirm the keys took.
```

### Verify

- [ ] Both files exist under ~/.hermes/memories/ and each is under its limit with headroom
- [ ] After /new, the agent answers "what do you know about me" from USER.md without being told
- [ ] hermes prompt-size shows memory bytes close to the file sizes
- [ ] The background review runs on the model you chose (hermes config show)

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
