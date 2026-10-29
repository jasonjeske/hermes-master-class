# Shortcuts Hiding in Plain Sight

### Short prefixes, and the ones that surprise you

The classic CLI runs a command from the first few letters. An exact name or alias always wins. Otherwise, when one command starts with what you typed, it runs; when several do, the one shortest name wins; when they tie, Hermes lists them and runs nothing. Installed skills join the race, so a skill name can change the result. On v0.22.5 with no skill sharing the letters:

| You type | It runs | Watch out |
|---|---|---|
| `/h` | `/hb`, the heartbeat | Not `/help`. Type `/he` |
| `/res` | `/reset`, a new session | Not `/resume`. The confirmation catches it, but type `/resu` |
| `/st` | `/stop` | Not `/status` or `/steer`. Use `/ste` or `/s` for steer |
| `/sk` | `/skin` | Not `/skills`. Type `/ski` |
| `/co` | `/copy` | Not `/compress` or `/context`. Use `/ctx` |
| `/qu` | `/quit` | It exits. Use `/q` for queue |
| `/mod`, `/u`, `/g`, `/k`, `/l` | `/model`, `/undo`, `/goal`, `/kanban`, `/loop` | Safe |

### Your skills are commands

Every installed skill is also a command: `/github-pr-workflow`, `/excalidraw`, whatever you have. When a skill's name matches a built-in command or alias, the built-in wins and the skill gets no command of its own, so give your skills names no command uses. A bundle (`/bundles`) is one command that loads several skills.

### Commands you make yourself

`quick_commands` in `config.yaml` adds your own: `type: exec` runs a shell command (30 seconds at most, with a cleaned environment) and `type: alias` points at another slash command. Built-in commands are resolved first, so a quick command named like a built-in never runs in the CLI. `model_aliases` gives `/model` short names: `hermes config set model.aliases.fav anthropic/claude-opus-4.6`, then `/model fav`.

### Commands that ask first

`/clear`, `/new`, `/reset`, `/undo` and `/quit --delete` open a confirmation in the CLI because they throw away history. Add `now`, `--yes` or `-y` to skip it once (`/new -y`), or set `approvals.destructive_slash_confirm: false` to turn it off.

### In Slack threads

Slack does not deliver slash commands inside threads. Use `!` instead (`!stop`, `!status`), or `/hermes <command>` anywhere.

### Who may run what in chat

On platforms with an allowlist, admins get every command and everyone else gets the names in `user_allowed_commands`, plus `/help` and `/whoami`. Set `allow_admin_from` and `user_allowed_commands` in the platform's `extra:` block.

> ⚠️ **Gotchas worth knowing before you rely on them**
>
> `/debug` with no argument posts your last 200 log lines to a public paste service and the act of typing it is the consent: read `/debug local` first. `/model` resets the prompt cache, so the next turn rereads the whole conversation at full input price, and `/tools` resets the session: change them between tasks, not inside one. `/yolo` lasts for the whole session, and resuming that session brings it back. `/goal` keeps spending turns until its judge says done, so give it a finish line a reviewer could check. In chat, setting a goal while a turn is running needs `/stop` first.

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
