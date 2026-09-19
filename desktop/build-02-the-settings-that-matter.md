# Build 2: The Settings That Matter

![Build 2](../assets/art/part-05.webp)

### What you are building

The handful of settings that decide what the app costs and how it behaves, set deliberately, plus an audit prompt that reads the rest back to you from the docs so nothing is left at a default you never chose.

### What the docs say

Checked against the Desktop page (Choosing a model, Settings and onboarding, Per-profile settings, Fonts, Repository discovery) and the Configuration reference.

| Setting | Where | What it really does |
|---|---|---|
| The composer model picker | left of the microphone in the composer | Sticky per device and per chat; it never writes your default. Mid-chat switches reset the prompt cache, so on a long chat a fresh chat on the new model is often cheaper |
| The default model | Settings, Model | The per-profile default that new chats, crons, subagents and auxiliary tasks start from. The only place that writes it |
| Auxiliary models and effort | Settings, Model, Auxiliary models | Each side task (compression, titling, vision, background review) gets its own provider, model and reasoning effort; saved as `auxiliary.<task>.reasoning_effort`, the same key `hermes model` writes |
| Applies to | top of the config-backed settings pages when you have two or more profiles | Selects which profile your edits target; it follows the active profile by default and resets when you switch |
| Reasoning blocks | Settings, Chat, or `/reasoning show` | `display.show_reasoning`; whether the model's thinking is shown in the transcript |
| Reopen last chat | Settings, Appearance | `display.resume_last_session`; off means every cold start begins fresh |
| Keep computer awake | Settings, Advanced | Stops sleep during long or overnight runs; per computer |
| Fonts | Settings, Appearance | `desktop.font_family` for the UI, `terminal.font_family` for the terminal pane, per profile |
| Repository discovery | Settings, Workspace | `desktop.repo_scan_enabled`, `desktop.repo_scan_roots`, `desktop.repo_scan_exclude_paths`: where the Projects sidebar looks |
| Quick Entry | Settings, Advanced | The global hotkey composer; needs at least one modifier |
| Themes | Settings, Appearance | Built-in presets plus any VS Code Marketplace theme, converted and installed |

*`~/.hermes/config.yaml`*

```yaml
display:
  show_reasoning: false           # Settings, Chat, Reasoning Blocks
  resume_last_session: true       # Settings, Appearance, Reopen Last Chat on Launch
desktop:
  font_family: ""                 # blank means the theme's font
  repo_scan_enabled: true
  repo_scan_roots: []             # empty means the default home scan
  repo_scan_exclude_paths: []
terminal:
  font_family: ""                 # blank means the bundled JetBrains Mono
auxiliary:
  compression:
    reasoning_effort: "low"       # summaries do not need deep thinking
  title_generation:
    reasoning_effort: "none"
```

> 📝 **From the field: read the prompt before you tune the model**
>
> Tonbi's habit when the agent "is not performing as well": run `hermes prompt-size` and look at what every new session is already carrying, skills index, memory, tool schemas, before touching the model. Too many enabled skills is the usual answer, and the Skills pane in Build 3 is where you trim them.

### Prompts

*`prompt-d2-audit-my-settings.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/user-guide/desktop sections
"Choosing a model" and "Settings & onboarding", then read my config.yaml and
answer, one line each:

1. My default model per profile (model.default) and which composer picks I
   have made that are NOT my default (say which is which).
2. Every auxiliary task that runs on my main model instead of a cheaper one,
   and the auxiliary.<task> keys I would set to move each.
3. Whether reasoning blocks are shown, whether the last chat reopens on
   launch, and whether keep awake is on.
4. What repo_scan is scanning right now and whether that is more than I
   need.

Then propose the diff for the changes you recommend, and stop. Do not save.
```

*`prompt-d2-one-setting.md`*

```markdown
Set <key> to <value> in my config.yaml for the <profile> profile. Read the
matching row on https://hermes-agent.nousresearch.com/docs/user-guide/configuration
first and quote it. Show me the diff before you save. After I say go, save
it and tell me whether the running app picks it up live or needs a new
session.
```

### Verify

- [ ] Settings, Model shows the default you chose, and the composer picker shows the same unless you deliberately changed it for one chat
- [ ] The auxiliary rows show a cheaper model or a lower effort for compression and titles
- [ ] The Applies to chip row appears once you have two profiles and follows the active one
- [ ] hermes config show reads back every key from the block above

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-DESKTOP.md)
