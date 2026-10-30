## Stage 3: Trim the Skills

### What this stage changes

The skills index: the list of every installed skill that rides in the system prompt of every call. This stage turns off the skills you never use, so their rows leave the index and the model stops being told to consider them. Every skill you keep works as before, and no skill file is edited.

Keep the skills you use. The ones you never call cost you twice: once in the index on every call, and again whenever the model loads one it did not need.

### What the skills block costs

On a fresh install the system prompt is 3,433 tokens, and about 1,720 of them are the skills block: a short header, one row per skill with its description cut to 60 characters, and a line for each category. The 58 bundled skills render about 6,871 characters, and every skill you install adds a row. `/context` counts the whole block as System prompt, not as Skills, for the reason [Stage 0](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-00-measure-before-you-change-anything.md) explains.

The second bill comes from the header. It tells the model to load any skill that is even partially relevant to the task, so a long index also means more loads. A load (`skill_view`) puts the whole SKILL.md into the conversation, where it stays for the rest of the session. The largest bundled skills are `claude-code` at 35,175 bytes, `humanizer` at 34,463 and `p5js` at 27,534. `hermes prompt-size --json` lists every skill with the size of its SKILL.md, which is what a load costs, so the expensive ones are easy to find.

A description longer than 60 characters shows in the index as its first 57 characters and three dots. Whatever comes later, often the part that says when to use the skill, never reaches the model. [witcheer](https://x.com/witcheer/status/2069828190197973337) caught `/learn` drafting descriptions past that limit. Keep every description you write to one sentence of 60 characters or fewer.

[Ryan Underdown](https://bobatron.com/blog/hermes-system-prompt) traced how Hermes builds its system prompt and measured how much of it the skills index takes, the same question this stage starts from. His fix was a patched `agent/prompt_builder.py`. `hermes update` replaces that file, and v0.22.5 has no plugin seam for the index, so this stage uses the levers Hermes ships.

### What we measured

A sealed install of v0.22.5 with the 58 bundled skills sends 13,769 tokens before your first word.

```table
| What you change | Saves | What you give up |
| Opt out to the one essential skill, `hermes-agent` (12,388 left) | 1,381 | The other bundled skills, until you opt back in |
| Turn the skills toolset off, as the lean chat profile in Stage 2 does | 3,111 | Every skill: the index, the three skill tools (1,241 in `/context all`) and their guidance |
| Disable the skills you never use | One index row each | Only those skills |
```

No skills toolset means no index at all, so the second row is everything skills cost before the first load. Opting out keeps the skill tools and one skill. Disabling keeps everything you still use, which is why the stage prompt starts there.

### The levers

```table
| Lever | What it does | Use it when |
| `hermes skills config` | An interactive checklist of your skills, for every platform or one. It takes no argument and writes `skills.disabled` or `skills.platform_disabled.<platform>` | You want to pick by hand |
| `skills.disabled` | Takes the named skills out of the index, the skill list and slash commands, and refuses a load of them. `hermes-agent` can never be disabled. Set it with `hermes config set` and a JSON list | You know the names, as the stage prompt does |
| `skills.platform_disabled.<platform>` | The same, on one platform only | A skill belongs in the terminal but not on Telegram |
| `hermes skills opt-out` | Stops seeding the bundled skills into this profile. Alone it changes nothing you can see: the copies stay on disk and in the index until you add `--remove`, which asks before it deletes the unmodified ones. `hermes skills opt-in --sync` brings them back | You use none of the bundled skills |
| `skills.auto_load` | Pins whole skills into the stable part of every session's system prompt | Almost never: every pinned SKILL.md rides every call in full |
| `-s` or `--skills` at launch | Preloads a skill for that one launch | You want a skill in one session without pinning it |
```

Set each disable key with one command, the list written as JSON with no spaces. A set replaces the whole list, so keep every name already in it. The names are three of the largest bundled skills; use names from your own list.

```code lang=bash file=skills-disabled.sh
hermes config set skills.disabled '["p5js","humanizer"]'
hermes config set skills.platform_disabled.telegram '["claude-code"]'
```

By hand, the same two keys look like this in config.yaml:

```code lang=yaml file=skills-disabled.yaml
skills:
  disabled:
    - p5js
    - humanizer
  platform_disabled:
    telegram:
      - claude-code
```

```callout kind=warn title="Why the stage prompt uses config set"
Hermes refuses `write_file` and `patch` on the config.yaml it runs with (`tools/file_tools_write_guards.py:168`), so the stage prompt changes config only with `hermes config set`, which turns a quoted JSON list into a real list (`hermes_cli/config.py:3207`). For `skills.disabled` it then warns that the key is not a recognized config key. That notice is expected: Hermes reads the key anyway (`agent/skill_utils.py:286`).
```

### The curator

The curator keeps the skills the agent writes for itself from piling up. By default it runs at most once every 168 hours, after two hours without activity, marks a skill stale after 14 days without use and archives it after 30, and an archived skill can be restored. It never touches hub skills, and by default it leaves bundled skills alone too, so it will not trim the 58 above unless you set `curator.prune_builtins: true`. Its default run spends no tokens: only `curator.consolidate: true` adds a model pass. `hermes curator run --dry-run` reports what a run would do and changes nothing.

The 152 optional skills that ship with Hermes stay out of the index until you install one. An install reaches the prompt in your next session unless `/skills install` gets `--now`, and a session that is already running keeps its index and gets a short note listing what changed.

### The stage prompt

Paste it into a Hermes session that has its terminal tool.

```code lang=markdown file=prompt-stage-3-skills.md
Tune Hermes, stage 3: Trim the Skills. Work in five steps, one change at a time.
MEASURE: Read my enabled skills with `hermes skills list --enabled-only`, how often each one has been used with `hermes curator usage`, the skills already turned off with `hermes config get skills.disabled` (not set means none, and its notice that the key is not recognized is expected), and any pinned skills with `hermes config get skills.auto_load`. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: One `hermes config set skills.disabled '<JSON list>'` command, the JSON with no spaces, that keeps every name already in the list, adds the skills I have never used, largest SKILL.md first, and leaves hermes-agent on. If I use none of the bundled skills, give me `hermes skills opt-out --remove` to run myself instead, and say that it asks before it deletes their unmodified copies and that `hermes skills opt-in --sync` brings them back. Show the exact command and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: If I chose the opt-out, wait until I tell you I ran it. Otherwise run `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in the folder `hermes config path` points to, with the current date and time and never over an existing backup, then run only the command I approved. Never edit config.yaml with write_file or patch.
VERIFY: Run `hermes skills list --enabled-only` again and show that the skills I turned off are gone and hermes-agent is still there. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

```checklist
[ ] `hermes prompt-size --json` shows fewer system prompt bytes than before this stage
[ ] `hermes skills list --enabled-only` no longer shows the skills you turned off, and still shows `hermes-agent`
[ ] `hermes config get skills.auto_load` prints an empty list, or only skills you use in every session
[ ] A new session's `/context all` no longer lists the skills you turned off
[ ] A `config-YYYY-MM-DD-HHMMSS.yaml` backup from this stage sits beside config.yaml, unless you only opted out
```

## Stage 4: Memory and Context Files

### What this stage changes

The text Hermes adds to the system prompt from files: your memory (MEMORY.md and USER.md), the project rule file it finds in your working folder, and SOUL.md. Each of them rides every call, so this stage makes each one earn its place. It turns nothing off unless you choose to.

### Memory

Memory is two small stores: MEMORY.md for what the agent learns, USER.md for what it knows about you. Both go into the system prompt of every call. Their caps are `memory.memory_char_limit` (2,200 characters) and `memory.user_char_limit` (1,375), and a write past a cap is refused. We filled both toward their caps, 1,340 and 710 characters, and measured:

```table
| Setup | Tokens before your first word | Change |
| Fresh install, empty memory | 13,769 | |
| Memory filled toward its caps | 14,456 | plus 686 in the memory row |
| Same, with the memory toolset off | 13,374 | the memory row stays at 686 |
| Same, with both memory flags set to false | 12,687 | minus 1,769 from full memory |
```

Turning the memory toolset off removes the memory tool (821 tokens of schema in `/context all`) and its guidance, 1,082 tokens in all, but MEMORY.md and USER.md stay in the prompt. Only the two flags take them out:

```code lang=bash file=memory-off.sh
hermes config set memory.memory_enabled false
hermes config set memory.user_profile_enabled false
```

That also ends memory across sessions, so most people should keep memory and keep it lean. A rule from [Mervin Praison](https://mer.vin/2026/05/soul-md-for-ai-agents-30-80-line-identity-blueprint-before-memory-or-tools/) is a good one to adopt: memory holds durable facts, procedures belong in skills, task logs stay out, and stale entries go at a monthly review. A task log in MEMORY.md is paid on every call. To cut an entry, edit MEMORY.md or USER.md in the memories folder beside config.yaml: a line holding only a section sign separates entries, so remove one of those lines with the entry.

Watch the caps too. A store at nine tenths of its cap or more is close to refusing writes, and it is the line the weekly audit in [Stage 8](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-08-keep-it-tuned.md) reports on. Count a store with `wc -m` on its file: the cap counts characters, while `hermes prompt-size` reports each store in bytes with about 335 bytes of header around it.

Memory is also a frozen snapshot, as [witcheer](https://x.com/witcheer/status/2069020659829608570) points out. A save during a session reaches the file at once but reaches the prompt only in your next session, which keeps the prompt cache warm. So trim memory, then start a new session to see the saving.

### Context files

Hermes adds the project rule file it finds for your working folder to the system prompt, and the file costs more than its own size. In our install a 2,406-byte AGENTS.md, about 602 tokens on its own, cost 1,401 tokens: 15,170 against 13,769. Nearly all the rest is what the file switches on. An AGENTS.md marks the folder as a code project (`agent/coding_context.py:35`), so Hermes adds its coding brief to the system prompt and a short workspace snapshot after the file. `/context` shows 876 tokens in the rules row and 525 more in the system prompt.

Only one kind of rule file loads: the first one Hermes finds with content, in this order ([witcheer](https://x.com/witcheer/status/2069385776756895880) flagged the trap):

```table
| Order | File | Where Hermes looks |
| 1 | `.hermes.md` or `HERMES.md` | The working folder, then each parent up to the git root |
| 2 | The `AGENTS.md` chain | Every folder from the git root down to the working folder; in each one, `AGENTS.override.md` wins over `AGENTS.md` |
| 3 | `CLAUDE.md` | The working folder only |
| 4 | `.cursorrules` and `.cursor/rules/*.mdc` | The working folder only; every one of these files with content loads |
```

So a stray `.hermes.md` silently replaces your AGENTS.md, and a CLAUDE.md next to an AGENTS.md never loads. Keep one rule file per project, and keep it short. For a personal version of a team's AGENTS.md, put an `AGENTS.override.md` beside it and keep it out of git ([witcheer](https://x.com/witcheer/status/2096481734388858931)); in that folder it loads instead of the shared file.

Three more costs hide in these files. Every subagent reads the AGENTS.md chain again (not SOUL.md), so a long rule file is paid once more by each child. A context file that takes more than 5 seconds to read, such as a cloud-synced file that is only stored online, is skipped with only a line in agent.log. And each file is capped, by default at a slice of the model's window and never below 20,000 characters; Hermes keeps the start and the end of a longer one and marks what it cut.

SOUL.md is the agent's identity. It loads from your Hermes home in every session, never from the working folder, and it rides every call. Hermes builds the system prompt once per session, so an edit to SOUL.md applies in your next session, whatever the comment in the seeded file says.

### Coding context

`agent.coding_context` decides how much coding help rides along. The default, `auto`, adds a coding brief and a live git snapshot when you work interactively in a code project. `focus` goes further once Hermes detects a coding project: it narrows the toolsets to the coding set and shows the non-coding skill categories as names only, without descriptions. In an empty folder it changed nothing in our install, because there was no project to detect. If you code in one repository all day, try it there and measure it with the stage prompt:

```code lang=bash file=coding-focus.sh
hermes config set agent.coding_context focus
```

### The stage prompt

Paste it into a Hermes session that has its terminal tool, started in the project folder you work in.

```code lang=markdown file=prompt-stage-4-memory.md
Tune Hermes, stage 4: Memory and Context Files. Work in five steps, one change at a time.
MEASURE: Read my memory caps with `hermes config get memory.memory_char_limit` and `hermes config get memory.user_char_limit`, and count MEMORY.md and USER.md in the memories folder beside config.yaml with `wc -m`, the counts only, never their text. Then review the memory, user profile and project rule file in your system prompt, and mark every entry that is a task log, out of date or said twice. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: The one change that saves the most: memory cut down to durable facts, a shorter project rule file, or `hermes config set memory.memory_enabled false` and `hermes config set memory.user_profile_enabled false` if I do not use memory. For a memory or rule file, quote the exact entries or lines to cut and give me the `cp -p` command that keeps a dated copy beside the file, because I make the copy and the cut myself. Show the exact command and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: For a memory or rule file, change nothing and wait until I tell you the cut is made. For the config change, run `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in the folder `hermes config path` points to, with the current date and time and never over an existing backup, then run only the commands I approved. Never edit config.yaml with write_file or patch.
VERIFY: Count MEMORY.md and USER.md again with `wc -m` and compare them with the first counts and with their caps. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

```checklist
[ ] `hermes prompt-size --json` shows the size you trimmed smaller than before this stage
[ ] `wc -m` counts MEMORY.md and USER.md under nine tenths of `memory.memory_char_limit` and `memory.user_char_limit`
[ ] Every memory entry left is a durable fact, with no task logs and nothing said twice
[ ] Exactly one project rule file loads in your working folder, and a new session's `/context` lists it
[ ] A dated copy of every file this stage changed sits next to it, config.yaml as `config-YYYY-MM-DD-HHMMSS.yaml`
```

## Stage 5: MCP Servers

### What this stage changes

Which MCP tools each server puts in front of the model. With tool search on, an MCP server is cheap, and this stage makes it cheaper: each server keeps only the tools you use, and a server you stopped using stops riding along. It changes a server's tools setting or its enabled flag, never its command, arguments or credentials.

### How MCP tools are billed

With tool search on, as it is by default, Hermes defers every MCP tool. Its schema leaves the request, and the tool becomes one line, a name and a short first sentence, in the listing that the three bridge tools carry ([Stage 1](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-01-defer-what-you-rarely-call.md) explains the bridge). `/context` reports MCP as 0 and bills that listing in the (unknown) row of `/context all`: 3 tools and 745 tokens on a fresh install.

The listing has a ceiling: the smaller of `tools.tool_search.listing_max_tokens` (4,000 tokens) and `tools.tool_search.threshold_pct` (5 percent) of the model's window. Past it, Hermes shortens the listing to names only, then to one line per server, starting with the largest server. Turn tool search off and every MCP schema rides every call in full, with no ceiling, so leave it on.

### What we measured

The official filesystem MCP server, 14 tools, added to a fresh install:

```table
| Setup | Tokens before your first word | Change |
| Fresh install | 13,769 | |
| Plus the filesystem server, all 14 tools deferred | 14,095 | plus 326 |
| Same server, with an include list of 2 tools | 13,823 | plus 54 |
```

The server is cheap because tool search defers it. The include list still cut its listing from 326 tokens to 54, and the tools it leaves out are not registered at all.

### Trim each server

Name the tools you use, one command per server, the list written as JSON with no spaces:

```code lang=bash file=mcp-tools.sh
hermes config set mcp_servers.filesystem.tools.include '["read_text_file","list_directory"]'
```

By hand in config.yaml, this is the whole block to change; the server's own lines stay as they are:

```code lang=yaml file=mcp-tools.yaml
mcp_servers:
  filesystem:
    tools:
      include: [read_text_file, list_directory]
```

`mcp_servers.<name>.tools.include` takes exact names or shell-style wildcards, and it wins over `mcp_servers.<name>.tools.exclude` when a server has both; an empty include list registers nothing. `mcp_servers.<name>.tools.resources: false` and `mcp_servers.<name>.tools.prompts: false` drop the four utility tools a server gets when it offers resources or prompts. `mcp_servers.<name>.enabled: false` turns a server off everywhere and keeps its settings for later. To pick from a list instead of typing names, `hermes mcp configure <name>` toggles a server's tool selection.

### Startup and subagents

`mcp_servers.<name>.lazy: true` defers a server's connection until it is needed, which speeds up startup. Two other settings decide where a server's listing is paid again. `delegation.inherit_mcp_toolsets` is true by default, so a subagent given a narrower toolset list still keeps the parent's MCP servers. If your subagents never need MCP tools, turn it off:

```code lang=bash file=mcp-subagents.sh
hermes config set delegation.inherit_mcp_toolsets false
```

To keep MCP off one platform, put `no_mcp` in that platform's list under `platform_toolsets`, the lists [Stage 2](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-02-pick-a-toolset-profile.md) builds. A cron job that sets its own toolsets also gets every enabled server unless its list has `no_mcp`.

### The stage prompt

Paste it into a Hermes session that has its terminal tool. Measure MCP with `/context all`: the (unknown) row is where its listing is billed. `hermes prompt-size` cannot show it: that command never starts your MCP servers, so its tool bytes leave every MCP tool out (`hermes_cli/main.py:2866` starts MCP in the background only for chat sessions). Read a server's settings one key at a time, never with `hermes config show` or a bare `hermes config get mcp_servers`: both print launch commands, arguments and URLs unmasked, and those can carry tokens.

```code lang=markdown file=prompt-stage-5-mcp.md
Tune Hermes, stage 5: MCP Servers. Work in five steps, one change at a time.
MEASURE: List my MCP servers with `hermes mcp list` and show me only its Name, Tools and Status columns, then read each server's tools setting with `hermes config get mcp_servers.<name>.tools`. Never run `hermes config show` or a bare `hermes config get mcp_servers`: they print launch commands, arguments and URLs unmasked. Ask me which of each server's tools I use. Ask me to run /context all and paste its (unknown) row, where the listing that carries MCP tools is billed. That row is this stage's measure, because `hermes prompt-size` never starts MCP servers. Also run `hermes prompt-size --json` and note its estimated tokens, the fixed budget without MCP.
PROPOSE: For one server, either `hermes config set mcp_servers.<name>.tools.include '<JSON list>'` with only the tools I use, the JSON with no spaces, or `hermes config set mcp_servers.<name>.enabled false` for a server I no longer use. Never show or change its launch command, arguments, env or headers. Show the exact command and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: Run `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in the folder `hermes config path` points to, with the current date and time and never over an existing backup, then run only the command I approved. Never edit config.yaml with write_file or patch.
VERIFY: Read the server's setting again with `hermes config get mcp_servers.<name>.tools` or the Status column of `hermes mcp list`, then ask me to open a new session, run /context all and paste the (unknown) row. Run `hermes prompt-size --json` again and confirm its estimated tokens did not move, since it never counts MCP tools. Show a table of the (unknown) row with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

```checklist
[ ] `hermes config get mcp_servers.<name>.tools` prints the include list you approved
[ ] A new session's `/context all` shows a smaller (unknown) row than before this stage
[ ] Every server you no longer use shows as disabled in the Status column of `hermes mcp list`
[ ] `hermes config get tools.tool_search.enabled` prints auto or on, never off
[ ] A `config-YYYY-MM-DD-HHMMSS.yaml` backup from this stage sits beside config.yaml
```
