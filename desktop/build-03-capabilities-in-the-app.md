# Build 3: Capabilities in the App

![Build 3](../assets/art/part-04.webp)

### What you are building

The management surface used from the app instead of the terminal: skills and plugins with an Installed view and a Browse view of the public catalogs, tools and MCP servers per agent, messaging setup with a QR code, and the two bundled safety plugins switched on for every profile you run.

### What the docs say

Checked against the Desktop page (Management panes, Where Browse gets its data, Extending the desktop app) and the Plugins and Plugin Catalog pages.

| Fact | Detail |
|---|---|
| Skills | Capabilities, Skills. Installed shows the selected profile's real skills and enable state; Browse searches the same published catalog as the public Skills Hub |
| Plugins | Capabilities, Plugins, same layout. Installed shows one row per plugin with a Desktop switch and an Agent switch; a plugin that ships both halves is one row. Browse shows the public Plugin Catalog. Install from Git takes any repo and can pin a commit |
| Where Browse reads | Native views over the same CDN snapshots the website uses (`/docs/api/skills.json`, `/docs/api/plugins.json`); no live GitHub calls |
| Install links | Hub pages carry `hermes://skill/install` and `hermes://plugin/install` links; the app always shows a review dialog before installing |
| The two switches | Desktop is app-level, one value everywhere. Agent is per profile, with the profile selector in that column's header |
| Tools and MCP | The Capabilities page has a Configuring selector that lists every agent on every connected machine; picking one edits that machine's toolsets and MCP servers |
| Messaging | The Messaging pane sets up gateway channels; Telegram has a Quick setup card that creates the bot from a QR code, detects your user id, saves credentials and restarts the gateway |
| Cron, Profiles, Agents, Command Center | Scheduled jobs, profile switching, and the orchestration surfaces, all reachable from the sidebar |

> 📝 **From the field: where plugins moved**
>
> Tonbi's part 3 flags a change that trips people following older videos: plugins used to live in Settings and now live under Capabilities beside Skills, Tools and MCP, with the desktop switch app-wide and the profile selector living only in the agent column's header. He also names the plugins he wrote for himself, a trading pane, a weather pane, a slide presenter, a YouTube planner, which is the best argument for Builds 5 to 8: the app becomes whatever panes you need.

### Commands

*`capabilities.sh`*

```bash
# The terminal twins of what Build 3 does in the app
hermes plugins list                      # every plugin and its state
hermes plugins enable security-guidance  # pattern-matches dangerous writes and warns or blocks
hermes plugins enable disk-cleanup       # tracks temp and test files the agent creates and cleans them
hermes skills list
hermes skills browse
```

> 📝 **From the field: the board decides who works**
>
> The Kanban board is a bundled desktop plugin and, in Tonbi's words, "the flagship plugin of Hermes desktop." His demonstration is the cleanest public example of the decomposer at work: a one-line idea dropped into triage fanned out into research, write and verify cards, each claimed by a different profile he had never assigned, because the Orchestration settings pane knows what each profile is good at from its description. The verifier card waited, blocked, until the writer card finished, then promoted itself to ready. His two tips: the Estimate effort button makes a real model call and tells you the token cost before you commit, and if you do not name a workspace the output lands in the board's attachments directory. Volume 3, Build 7 uses this board as the team's queue.

### Prompts

*`prompt-d3-capabilities-audit.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/user-guide/features/built-in-plugins
and https://hermes-agent.nousresearch.com/docs/user-guide/features/plugin-catalog
then run hermes plugins list and hermes skills list and tell me:

1. Which bundled plugins are enabled, and which of security-guidance and
   disk-cleanup are not.
2. Which catalog plugins would help the way I actually use you (read my
   last ten session titles first), three at most, with one line of why and
   the risk each one carries.
3. Which skills I have installed but have not loaded in the last thirty
   days (hermes curator status).

Then enable security-guidance and disk-cleanup with the config diff shown
first. Do not install anything from the catalog until I pick.
```

*`prompt-d3-telegram-from-the-app.md`*

```markdown
I am going to set up Telegram from Capabilities, Messaging with the QR
card. Before I do, read
https://hermes-agent.nousresearch.com/docs/user-guide/messaging and tell me
in five lines what the quick setup will write (which keys, which file),
what "allowlist" means for my user id, and what the Restart now banner is
waiting for. After I finish, verify from the terminal that the gateway is
running and the Telegram adapter connected, quoting the log line.
```

### Verify

- [ ] Capabilities, Plugins, Installed shows security-guidance and disk-cleanup with the Agent switch on for your profile
- [ ] Browse loads the catalog with cards, and opening a card shows an Install button, not a website
- [ ] The Configuring selector on Capabilities lists every profile you have
- [ ] If you set up Telegram, a message from your phone reaches the app and the reply comes back

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-DESKTOP.md)
