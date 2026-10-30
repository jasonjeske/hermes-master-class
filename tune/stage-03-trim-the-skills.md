# Stage 3: Trim the Skills

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

| What you change | Saves | What you give up |
|---|---|---|
| Opt out to the one essential skill, `hermes-agent` (12,388 left) | 1,381 | The other bundled skills, until you opt back in |
| Turn the skills toolset off, as the lean chat profile in Stage 2 does | 3,111 | Every skill: the index, the three skill tools (1,241 in `/context all`) and their guidance |
| Disable the skills you never use | One index row each | Only those skills |

No skills toolset means no index at all, so the second row is everything skills cost before the first load. Opting out keeps the skill tools and one skill. Disabling keeps everything you still use, which is why the stage prompt starts there.

### The levers

| Lever | What it does | Use it when |
|---|---|---|
| `hermes skills config` | An interactive checklist of your skills, for every platform or one. It takes no argument and writes `skills.disabled` or `skills.platform_disabled.<platform>` | You want to pick by hand |
| `skills.disabled` | Takes the named skills out of the index, the skill list and slash commands, and refuses a load of them. `hermes-agent` can never be disabled. Set it with `hermes config set` and a JSON list | You know the names, as the stage prompt does |
| `skills.platform_disabled.<platform>` | The same, on one platform only | A skill belongs in the terminal but not on Telegram |
| `hermes skills opt-out` | Stops seeding the bundled skills into this profile. Alone it changes nothing you can see: the copies stay on disk and in the index until you add `--remove`, which asks before it deletes the unmodified ones. `hermes skills opt-in --sync` brings them back | You use none of the bundled skills |
| `skills.auto_load` | Pins whole skills into the stable part of every session's system prompt | Almost never: every pinned SKILL.md rides every call in full |
| `-s` or `--skills` at launch | Preloads a skill for that one launch | You want a skill in one session without pinning it |

Set each disable key with one command, the list written as JSON with no spaces. A set replaces the whole list, so keep every name already in it. The names are three of the largest bundled skills; use names from your own list.

*`skills-disabled.sh`*

```bash
hermes config set skills.disabled '["p5js","humanizer"]'
hermes config set skills.platform_disabled.telegram '["claude-code"]'
```

By hand, the same two keys look like this in config.yaml:

*`skills-disabled.yaml`*

```yaml
skills:
  disabled:
    - p5js
    - humanizer
  platform_disabled:
    telegram:
      - claude-code
```

> ⚠️ **Why the stage prompt uses config set**
>
> Hermes refuses `write_file` and `patch` on the config.yaml it runs with (`tools/file_tools_write_guards.py:168`), so the stage prompt changes config only with `hermes config set`, which turns a quoted JSON list into a real list (`hermes_cli/config.py:3207`). For `skills.disabled` it then warns that the key is not a recognized config key. That notice is expected: Hermes reads the key anyway (`agent/skill_utils.py:286`).

### The curator

The curator keeps the skills the agent writes for itself from piling up. By default it runs at most once every 168 hours, after two hours without activity, marks a skill stale after 14 days without use and archives it after 30, and an archived skill can be restored. It never touches hub skills, and by default it leaves bundled skills alone too, so it will not trim the 58 above unless you set `curator.prune_builtins: true`. Its default run spends no tokens: only `curator.consolidate: true` adds a model pass. `hermes curator run --dry-run` reports what a run would do and changes nothing.

The 152 optional skills that ship with Hermes stay out of the index until you install one. An install reaches the prompt in your next session unless `/skills install` gets `--now`, and a session that is already running keeps its index and gets a short note listing what changed.

### The stage prompt

Paste it into a Hermes session that has its terminal tool.

*`prompt-stage-3-skills.md`*

```markdown
Tune Hermes, stage 3: Trim the Skills. Work in five steps, one change at a time.
MEASURE: Read my enabled skills with `hermes skills list --enabled-only`, how often each one has been used with `hermes curator usage`, the skills already turned off with `hermes config get skills.disabled` (not set means none, and its notice that the key is not recognized is expected), and any pinned skills with `hermes config get skills.auto_load`. Run `hermes prompt-size --json` and show the system prompt bytes, the tool schema bytes and their sum divided by four as estimated tokens.
PROPOSE: One `hermes config set skills.disabled '<JSON list>'` command, the JSON with no spaces, that keeps every name already in the list, adds the skills I have never used, largest SKILL.md first, and leaves hermes-agent on. If I use none of the bundled skills, give me `hermes skills opt-out --remove` to run myself instead, and say that it asks before it deletes their unmodified copies and that `hermes skills opt-in --sync` brings them back. Show the exact command and say in one line what it saves and what it costs me. Never put a key, token or password into config.
WAIT: Change nothing until I reply yes.
APPLY: If I chose the opt-out, wait until I tell you I ran it. Otherwise run `cp -p config.yaml config-YYYY-MM-DD-HHMMSS.yaml` in the folder `hermes config path` points to, with the current date and time and never over an existing backup, then run only the command I approved. Never edit config.yaml with write_file or patch.
VERIFY: Run `hermes skills list --enabled-only` again and show that the skills I turned off are gone and hermes-agent is still there. Run `hermes prompt-size --json` again and show a table with before, after and the difference. Remind me that this session keeps its old prompt and that a new session shows the change with /context all.
If you have no terminal tool in this session, give me each command to run and wait for my output.
```

### Verify

- [ ] `hermes prompt-size --json` shows fewer system prompt bytes than before this stage
- [ ] `hermes skills list --enabled-only` no longer shows the skills you turned off, and still shows `hermes-agent`
- [ ] `hermes config get skills.auto_load` prints an empty list, or only skills you use in every session
- [ ] A new session's `/context all` no longer lists the skills you turned off
- [ ] A `config-YYYY-MM-DD-HHMMSS.yaml` backup from this stage sits beside config.yaml, unless you only opted out

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-TUNING.md)
