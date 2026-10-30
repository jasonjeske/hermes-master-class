# Stage 5: MCP Servers

### What this stage changes

Which MCP tools each server puts in front of the model. With tool search on, an MCP server is cheap, and this stage makes it cheaper: each server keeps only the tools you use, and a server you stopped using stops riding along. It changes a server's tools setting or its enabled flag, never its command, arguments or credentials.

### How MCP tools are billed

With tool search on, as it is by default, Hermes defers every MCP tool. Its schema leaves the request, and the tool becomes one line, a name and a short first sentence, in the listing that the three bridge tools carry ([Stage 1](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-01-defer-what-you-rarely-call.md) explains the bridge). `/context` reports MCP as 0 and bills that listing in the (unknown) row of `/context all`: 3 tools and 745 tokens on a fresh install.

The listing has a ceiling: the smaller of `tools.tool_search.listing_max_tokens` (4,000 tokens) and `tools.tool_search.threshold_pct` (5 percent) of the model's window. Past it, Hermes shortens the listing to names only, then to one line per server, starting with the largest server. Turn tool search off and every MCP schema rides every call in full, with no ceiling, so leave it on.

### What we measured

The official filesystem MCP server, 14 tools, added to a fresh install:

| Setup | Tokens before your first word | Change |
|---|---|---|
| Fresh install | 13,769 |  |
| Plus the filesystem server, all 14 tools deferred | 14,095 | plus 326 |
| Same server, with an include list of 2 tools | 13,823 | plus 54 |

The server is cheap because tool search defers it. The include list still cut its listing from 326 tokens to 54, and the tools it leaves out are not registered at all.

### Trim each server

Name the tools you use, one command per server, the list written as JSON with no spaces:

*`mcp-tools.sh`*

```bash
hermes config set mcp_servers.filesystem.tools.include '["read_text_file","list_directory"]'
```

By hand in config.yaml, this is the whole block to change; the server's own lines stay as they are:

*`mcp-tools.yaml`*

```yaml
mcp_servers:
  filesystem:
    tools:
      include: [read_text_file, list_directory]
```

`mcp_servers.<name>.tools.include` takes exact names or shell-style wildcards, and it wins over `mcp_servers.<name>.tools.exclude` when a server has both; an empty include list registers nothing. `mcp_servers.<name>.tools.resources: false` and `mcp_servers.<name>.tools.prompts: false` drop the four utility tools a server gets when it offers resources or prompts. `mcp_servers.<name>.enabled: false` turns a server off everywhere and keeps its settings for later. To pick from a list instead of typing names, `hermes mcp configure <name>` toggles a server's tool selection.

### Startup and subagents

`mcp_servers.<name>.lazy: true` defers a server's connection until it is needed, which speeds up startup. Two other settings decide where a server's listing is paid again. `delegation.inherit_mcp_toolsets` is true by default, so a subagent given a narrower toolset list still keeps the parent's MCP servers. If your subagents never need MCP tools, turn it off:

*`mcp-subagents.sh`*

```bash
hermes config set delegation.inherit_mcp_toolsets false
```

To keep MCP off one platform, put `no_mcp` in that platform's list under `platform_toolsets`, the lists [Stage 2](https://github.com/jasonjeske/hermes-master-class/blob/main/tune/stage-02-pick-a-toolset-profile.md) builds. A cron job that sets its own toolsets also gets every enabled server unless its list has `no_mcp`.

### The stage prompt

Paste it into a Hermes session that has its terminal tool. Measure MCP with `/context all`: the (unknown) row is where its listing is billed. `hermes prompt-size` cannot show it: that command never starts your MCP servers, so its tool bytes leave every MCP tool out (`hermes_cli/main.py:2866` starts MCP in the background only for chat sessions). Read a server's settings one key at a time, never with `hermes config show` or a bare `hermes config get mcp_servers`: both print launch commands, arguments and URLs unmasked, and those can carry tokens.

*`prompt-stage-5-mcp.md`*

```markdown
Tune Hermes, stage 5: MCP Servers. Work in five steps, one change at a time.
MEASURE: List my MCP servers with `hermes mcp list` and show me only its Name, Tools and Status columns, then read each server's tools setting with `hermes config get mcp_servers.<name>.tools`. Never run `hermes config show` or a bare `hermes config get mcp_servers`: they print launch commands, arguments and URLs unmasked. Ask me which of each server's tools I use. Ask me to run /context all and paste its (unknown) row, where the listing that carries MCP tools is billed. That row is this stage's measure, because `hermes prompt-size` never starts MCP servers. Also run `hermes prompt-size --json` and note its estimated tokens, the fixed budget without MCP.
PROPOSE: For one server, either `hermes config set mcp_servers.<name>.tools.include '<JSON list>'` with only the tools I use, the JSON with no spaces, or `hermes config set mcp_servers.<name>.enabled false` for a server I no longer use. Never show or change its launch command, arguments, env or headers. Show the exact command and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: Run `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in the folder `hermes config path` points to, with the current date and time and never over an existing backup, then run only the command I approved. Never edit config.yaml with write_file or patch.
VERIFY: Read the server's setting again with `hermes config get mcp_servers.<name>.tools` or the Status column of `hermes mcp list`, then ask me to open a new session, run /context all and paste the (unknown) row. Run `hermes prompt-size --json` again and confirm its estimated tokens did not move, since it never counts MCP tools. Show a table of the (unknown) row with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

- [ ] `hermes config get mcp_servers.<name>.tools` prints the include list you approved
- [ ] A new session's `/context all` shows a smaller (unknown) row than before this stage
- [ ] Every server you no longer use shows as disabled in the Status column of `hermes mcp list`
- [ ] `hermes config get tools.tool_search.enabled` prints auto or on, never off
- [ ] A `config-YYYY-MM-DD-HHMMSS.yaml` backup from this stage sits beside config.yaml

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-TUNING.md)
