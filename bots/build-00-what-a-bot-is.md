# Build 0: What a Bot Is

![Build 0](../assets/art/part-11.webp)

### What you are building

The model in your head that makes every later build obvious: what the roster shows, what a Bot Chat is, why `/new` does not work in it, what a routine and a room are, and the two markers that switch the whole machinery on.

### What the docs say

Checked against the Bot Mode page and the Profiles page.

| Term | What it is |
|---|---|
| Profile | The persistent home for one agent's config, memory, skills, credentials and chat history: `~/.hermes/profiles/<name>/` |
| Bot | A profile presented in the roster with a title, an avatar, a section and a pinned canonical chat. Every Bot is a profile; a profile you only drive from the CLI or a gateway stays a plain profile |
| Bot Chat | The canonical, persistent conversation created the moment a Bot is born. Clicking the row always opens it. Typing `/new` or `/reset` inside it is rerouted to `/compact`, fresh working context in the same conversation, because forking the relationship is the one thing Bot Mode promises never happens |
| Routine | A recurring task attached to the Bot that does it. Under the hood it is a Hermes cron job named `[bot:<name>] <routine>`, so it also appears in `hermes cron list`; runs land in the Bot's own chat history |
| Room | A group chat of 2 to 6 Bots with one visible conversation, up to three serial rounds of member turns per message, and a needs-you badge when a Bot escalates with `@user` |
| Messaging bot | Different thing: an account on Telegram, Discord or Slack connected through the gateway |
| Subagent | Different thing: a child spawned by `delegate_task` with a fresh conversation, same profile |
| Warm backends | One backend process per local Bot. The cap is Settings, Advanced, Warm Bot Backends (default 3, "~60 MB each" in the page's words); idle backends are reaped after the timeout next to it, 10 minutes by default |
| Off switch | Bot Mode is a bundled desktop plugin; Capabilities, Plugins, Bots, Desktop switch. Your profiles, sessions and cron jobs are untouched either way |

**The two markers.** The messaging protocol and the `message_agent` tool are injected only when two conditions hold, and the Bots pane satisfies both the moment it creates a Bot: the session is titled exactly `Bot Chat`, and at least one profile on the install carries a `ui_meta: { hermes-bots: … }` block in its `profile.yaml`. That is why a headless install with no desktop never sees `message_agent`, and Build 5 gives the two lines that switch it on by hand.

| In Bot Mode | From a shell |
|---|---|
| Chat with a Bot | `hermes -p <bot> chat` |
| A Bot's files, skills, memory | `~/.hermes/profiles/<bot>/` |
| Routines | `hermes cron list`, jobs named `[bot:<name>] …` |
| Create or inspect | `hermes profile create`, `hermes profile list` |

> 📝 **From the field: Tonbi's first-day guide**
>
> Tonbi's Bot Mode walkthrough, recorded the day after the feature shipped, says the same thing in one line: "Bots themselves are not necessarily new. They're just profiles. What has changed is how they can work together and communicate with one another." He calls the canonical chat the bot's "agent inbox", a dedicated session for agent-to-agent traffic. The docs call it the Bot Chat; it is the same thing.

### Prompts

*`prompt-b0-show-me-my-roster.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode sections
"The Bots pane", "What actually makes a chat a Bot Chat" and "CLI parity".
Then run hermes profile list and, for each profile, tell me: whether it is a
Bot (does its profile.yaml carry a ui_meta hermes-bots block), whether it has
a session titled exactly "Bot Chat", its model, and how many cron jobs are
named [bot:<name>]. One table. Change nothing.
```

### Verify

- [ ] You can say in one sentence why /new does nothing in a Bot Chat and what it does instead
- [ ] hermes cron list shows any routine you created in the app, named [bot:<name>]
- [ ] hermes profile list matches the roster in the Bots tab
- [ ] Settings, Advanced shows the Warm Bot Backends count and you know what happens when it is exceeded

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-BOTS.md)
