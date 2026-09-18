# Build 5: Plugins

![Build 5](../assets/art/part-11.webp)

### What you are building

The bundled plugins that should be on from day one, switched on. The judgment for when a plugin is the answer and when a skill or `execute_code` is. And, if you need one, a minimal plugin that registers a single tool, written against the documented shape.

### What the docs say

Checked against the Plugins page and the Built-in Plugins page.

| Fact | Detail |
|---|---|
| Four kinds | Tool plugins that register tools and hooks, memory providers, model providers, and dashboard plugins that add a tab |
| Opt-in | Bundled and third-party plugins ship disabled. `hermes plugins enable <name>` turns one on; `plugins.enabled` is the allow-list in config.yaml and `plugins.disabled` always wins if a name is in both. `hermes plugins list` shows all three states |
| Where user plugins live | `~/.hermes/plugins/<name>/` with a `plugin.yaml` (name, version, description) and an `__init__.py` whose `register(ctx)` calls `ctx.register_tool(...)` and `ctx.register_hook(...)` |
| Bundled, worth enabling early | `security-guidance` pattern-matches dangerous code on file writes and appends a warning or blocks. `disk-cleanup` tracks test and temp files the agent creates and cleans them on session end |
| Also bundled | `observability/langfuse` tracing, `spotify`, `google_meet`, `teams_pipeline`, image backends under `image_gen/`, `hermes-achievements`, and `kanban/dashboard` which Build 9 uses |
| Restart | A new or newly enabled plugin loads on the next start of Hermes |

### Prompts

*`prompt-05-enable-bundled.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins
then run hermes plugins list and tell me, for every bundled plugin, its
name, one line on what it does, and whether it is enabled.

Then enable security-guidance and disk-cleanup. Show me the diff to
config.yaml before you save it. After I say go, apply it, tell me I need
to restart, and after the restart prove both loaded by showing hermes
plugins list again.
```

*`prompt-05-skill-or-plugin.md`*

```markdown
I want the agent to be able to <capability>. Before building anything,
decide the extension point and show your reasoning against these three
questions, each answered yes or no with one line of evidence:

1. Does a built-in tool or an installed MCP server already do this? Check
   /tools and the mcp_servers section of my config.yaml.
2. Could execute_code do it as a script the agent writes and runs, with
   no code for me to maintain?
3. Does the model need to call this as a TOOL mid-reasoning, rather than
   follow it as a procedure?

If 1 is yes, use that. If 2 is yes and 3 is no, write a skill (Build 4).
Only if 3 is yes and 1 and 2 are no do we write a plugin. Tell me which
and why, then stop.
```

*`prompt-05-minimal-plugin.md`*

```markdown
We decided a plugin is right. Read the "Minimal working example" section of
https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
and follow its shape exactly.

Create ~/.hermes/plugins/<name>/ with plugin.yaml and __init__.py. The
plugin registers ONE tool named <tool_name> with a JSON schema that has
<parameters>, and a handler that <does the one thing>. No network calls,
no writes outside the agent's home, no secrets read from anywhere.

Show me both files before writing them. After I say go: write them, add
the plugin to plugins.enabled with a diff, tell me to restart, and after
the restart call the tool once with a real argument and show the result
and the /tools entry.
```

### The two files

*`~/.hermes/plugins/hello-world/plugin.yaml`*

```yaml
name: hello-world
version: "1.0"
description: A minimal example plugin
```

*`~/.hermes/plugins/hello-world/__init__.py`*

```python
"""Minimal Hermes plugin: registers one tool."""

def register(ctx):
    schema = {
        "name": "hello_world",
        "description": "Returns a friendly greeting for the given name.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Name to greet"}
            },
            "required": ["name"],
        },
    }

    def handler(args, **kwargs):
        return {"greeting": f"Hello, {args.get('name', 'world')}"}

    ctx.register_tool(schema=schema, handler=handler)
```

> ⚠️ **The docs example is the contract**
>
> The register call signature, the hook names and the way a handler returns its result are the parts that change between releases. The prompt above makes the agent read the current example before writing, and the minimal shape here is the one documented at the time of writing. If your version differs, the doc page wins.

### Verify

- [ ] hermes plugins list shows security-guidance and disk-cleanup enabled
- [ ] Writing a file with an obviously dangerous line gets the security warning appended
- [ ] If you wrote a plugin, /tools lists its tool and a real call returns the expected shape

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
