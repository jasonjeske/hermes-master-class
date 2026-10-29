# The Bonus Ledger

### Prompts

*`prompt-bonus-audit.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/reference/slash-commands.
Then search my last 20 sessions and find five moments where one slash
command would have saved me time or tokens: a turn I restarted instead of
steering, a follow-up I waited to type instead of queueing, a session that
ran long without /compress or /new, a model left on a frontier tier for
routine work. For each, quote the moment, name the command, and say what it
would have saved. Change nothing.
```

*`prompt-bonus-setup.md`*

```markdown
Set up three things for this profile and show me each change before you
make it: display.busy_input_mode set to steer, a quick command /deploy of
type exec that runs scripts/deploy.sh, and a model alias "fast" for the
cheapest model I already have configured. Then run /busy status and show
me the quick command and the alias in config.yaml.
```

### Verify

- [ ] `/help` lists the commands this class ranks, and `/help skills` lists your skill commands
- [ ] A `/steer` changed a running turn, and a `/queue` prompt ran after it as its own turn
- [ ] `/undo` put your last prompt back in the box
- [ ] `/context` listed your `AGENTS.md` as loaded
- [ ] `/debug local` printed a report and uploaded nothing
- [ ] `Ctrl+P` found a command from part of its name

> ✅ **What you have now**
>
> Every command Hermes has, in the order that pays. You steer and queue instead of waiting, you start fresh and compress instead of dragging a stale context, you undo a bad prompt instead of arguing with its answer, and you hand long work to a goal, a loop or the board while you do something else. The rest of the list is there when the moment comes, one row away.

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
