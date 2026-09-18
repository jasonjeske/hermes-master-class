# Build 10: Tuning and Safety

![Build 10](../assets/art/part-12.webp)

### What you are building

The handful of config keys that decide cost, effort and blast radius, set on purpose; the one prompt that changes any setting safely; and a weekly maintenance habit that keeps the whole setup healthy.

### What the docs say

Checked against the Configuration page, the Security page, and the CLI reference.

| Fact | Detail |
|---|---|
| Approvals | `approvals.mode` is `smart` (dangerous commands ask, safe ones run), `manual` (everything asks), or `off`. `approvals.deny` is a list of patterns that are always refused. `approvals.cron_mode` governs unattended runs. `/yolo` toggles approvals in a session |
| Always on | A hard blocklist of destructive commands, prompt-injection scanning of every context file including SOUL.md, and SSRF protection on outbound requests, regardless of mode |
| Docker | With `terminal.backend: docker`, the dangerous-command check is skipped because the host is not reachable; the worst case is a wrecked container |
| Effort | `agent.reasoning_effort` sets the global thinking level: none, minimal, low, medium, high, xhigh, max, ultra. Empty means medium |
| Side tasks | Every auxiliary task takes its own `provider`, `model` and `reasoning_effort`: `auxiliary.compression`, `auxiliary.vision`, `auxiliary.title_generation`, `auxiliary.background_review`, `auxiliary.kanban_decomposer`. `provider: main` means "whatever the main agent uses" |
| Compression | `compression.threshold` defaults to 0.50 of the context window; `/compress` forces it |
| Turn caps | `agent.max_turns` is unlimited by default; `agent.budget_warning_ratio` adds a one-time warning. `goals.max_turns` (default 20) auto-pauses a `/goal` |
| Verify on stop | `agent.verify_on_stop: true` refuses a final answer on a turn that edited code but produced no fresh verification evidence |
| Watching cost | `hermes prompt-size` for the per-prompt baseline, `hermes insights` for token, cost and activity analytics |
| Sessions | `hermes sessions export <file> --redact` scrubs secrets from anything you share; `hermes sessions prune` deletes old ended sessions |
| Updates | `hermes update --check` previews, `hermes update --backup` snapshots the home directory before pulling |

### The config, annotated

*`~/.hermes/config.yaml`*

```yaml
agent:
  reasoning_effort: "medium"       # raise per task, not globally
  verify_on_stop: true             # no "done" without evidence on coding turns
  budget_warning_ratio: 0.75       # one warning before a long task runs out

approvals:
  mode: smart                      # dangerous commands ask, safe ones run
  deny:
    - "rm -rf /"
    - "git push --force*"
    - "*DROP TABLE*"

auxiliary:
  compression:
    reasoning_effort: "low"        # summaries do not need deep thinking
  vision:
    reasoning_effort: "none"
  background_review:
    provider: openrouter
    model: your-inexpensive-model
  kanban_decomposer:
    provider: main                 # decomposition deserves the frontier model

compression:
  threshold: 0.50
```

### The one prompt for any setting

This is the shape the strongest community material converges on, and it works for every key in the configuration reference.

*`prompt-10-change-a-setting.md`*

```markdown
Read the "<section name>" section of
https://hermes-agent.nousresearch.com/docs/user-guide/configuration
Then set <key> to <value> in my config.yaml. Show me the diff before you
save it, and tell me in one line what will change in my next session.
After I say go, save it, run hermes config show, and confirm the key
reads back as set.
```

### Prompts

*`prompt-10-safety-review.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/user-guide/security
sections on approvals, the deny list, and unattended runs. Then show me
my current approvals block from config.yaml and answer:

1. Which mode am I in, and what does that mean for a command like
   rm -rf on a project folder?
2. What does a cron job do when it hits a dangerous command under my
   current cron_mode?
3. Propose an approvals.deny list for this machine: the five commands
   that would hurt most if run by mistake, as patterns.

Show me the diff. Do not save until I say go.
```

*`prompt-10-cost-audit.md`*

```markdown
Run hermes prompt-size and hermes insights. Tell me:

1. The three largest pieces of my system prompt in bytes and what each
   one is (skills index, memory, tool schemas, context file).
2. Which of them I could shrink without losing anything I use weekly,
   with the exact change.
3. Which side tasks (compression, vision, background review, titles) run
   on my main model and what auxiliary.<task>.model I could point each
   at instead.

Then propose the config diff for the changes you recommend and stop.
```

### Weekly maintenance

*`weekly.sh`*

```bash
hermes doctor
hermes cron doctor
hermes curator status
hermes prompt-size
hermes insights
hermes backup --quick --label "weekly"
hermes update --check
```

- [ ] hermes doctor and hermes cron doctor report nothing broken
- [ ] The prompt-size total has not crept up without a reason you can name
- [ ] Skills the curator marked stale are ones you actually stopped using
- [ ] A backup from this week exists
- [ ] hermes update --check was read before any update ran, and the update ran with --backup

### Verify

- [ ] hermes config show reads back every key from the annotated config
- [ ] A dangerous command in a chat asks for approval; a denied pattern is refused outright
- [ ] A coding turn with no test run is refused a final answer while verify_on_stop is on
- [ ] hermes insights shows the side tasks on the cheaper models

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
