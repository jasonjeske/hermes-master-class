## Build 4: Routines

![Build 4](assets/art/part-06.webp)

### What you are building

Recurring work attached to the bot that owns it: a morning standup from atlas, a health brief and a nightly backup from ops, a source watch from scout. Each one silent when nothing happened, each one landing in that bot's own chat where you would have asked anyway.

### What the docs say

Checked against the Bot Mode page (Routines) and the Cron page.

```table
| Fact | Detail |
| The pane | The Routines pane docks beside the chat while the Bots tab is active; a structured schedule picker builds the schedule, with an Advanced field for the raw Hermes schedule string |
| What a routine is | A plain Hermes cron job namespaced `[bot:<name>] <routine>`. It shows in `hermes cron list` and the core Cron page. Runs land in the Bot's own chat history |
| The CLI twin | `hermes -p <bot> cron create "<schedule>" "<prompt>" --name "<routine>"`, run under that bot's profile so the job belongs to it |
| Fresh session, every run | No chat history, no context file unless the job carries `--workdir`. The prompt plus the attached skills are the whole briefing |
| Silence | A final response containing `[SILENT]` delivers nothing and is still saved for audit. Failed runs always deliver |
| Per-job pins | A routine can pin its own model, provider and reasoning effort |
| Health | `hermes cron doctor` is the read-only check across every job; `hermes cron runs <id>` shows attempts; `hermes pause` is the global stop |
```

### The routines the kit ships

```code lang=bash file=kits/bot-team/ops/routines.sh
OPS_ROUTINES_SH
```

```code lang=bash file=kits/bot-team/atlas/routines.sh
ATLAS_ROUTINES_SH
```

```code lang=bash file=kits/bot-team/scout/routines.sh
SCOUT_ROUTINES_SH
```

```callout kind=warn title="Three things a routine cannot do, and the flag that fixes two of them"
A routine runs in a fresh headless session. It has no chat history, it has no message_agent (that tool exists only in canonical Bot Chat sessions), and @user means nothing to it, because a routine's output goes wherever its delivery target says. So a routine never "messages a teammate"; it gathers and reports. The kit's answer is --deliver bot-chat:<profile>: the output lands in that bot's Bot Chat as a message the bot answers, and in that reply the bot does have message_agent. That is why ops runs the board sweep and delivers it to atlas, and why the schedule strings read every day at 07:30 and every sunday 18:00: the parser accepts those, a cron expression, and plain intervals such as every 2h, and rejects every 1d at 07:30 even though an older docs example shows it.
```

```callout kind=info title="Who gets a routine"
Workers do not, by default. forge, quill and sentinel receive work as cards and messages; a routine on a worker is usually a sign that the planner should be sending it a card instead. The three bots with standing routines are the ones whose job is to look: the operator at the machines, the chief of staff at the board, the researcher at the sources.
```

### Prompts

```code lang=markdown file=prompt-b4-add-a-routine.md
You are <bot>. Add a routine for yourself. Read
https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode section
"Routines" and the "[SILENT]" and "delivery" sections of
https://hermes-agent.nousresearch.com/docs/user-guide/features/cron. The
routine: <what, when, and what counts as nothing to report>. Write the
prompt for a stranger with no history: every path absolute, every check
explicit, the silent condition stated, the report shape stated. Show me the
exact cronjob tool call or hermes cron create command, then create it after
I say go, run it once, and show me the output in this chat.
```

### Verify

```checklist
[ ] hermes -p ops cron list, hermes -p atlas cron list and hermes -p scout cron list each show the jobs by name (the Routines pane adds its own [bot:<name>] prefix only to jobs it creates)
[ ] hermes -p ops cron run board-sweep either ends in [SILENT] or lands in atlas's Bot Chat, where atlas answers it
[ ] hermes cron doctor reports every routine healthy
[ ] The Routines pane in the app lists the same jobs the CLI does
```

## Build 5: Bots Talking to Each Other

![Message paths between the six](assets/art/v3-message-paths.webp)

### What you are building

The habit and the mechanics of handing work between bots: an @mention in any chat, a `message_agent` call from inside a Bot Chat, the roster every bot carries in its prompt, and the delivery contract that tells you what "queued" means and what happens when a turn fails.

### What the docs say

Checked against the Bot Mode page: Bot-to-bot messaging, What actually makes a chat a Bot Chat, Failed turns retry safely, When a delivery fails.

```table
| Fact | Detail |
| @mentions | Type `@researcher have a look at this` in any chat; the composer resolves it against the live roster and the active Bot is told exactly who you mean. The Bot then composes its own message and sends it with `message_agent`. Your text is never forwarded verbatim |
| The tool | `message_agent(target="researcher", message="…")` from inside a canonical Bot Chat. The target is a profile name, a friendly name, or the `@` tag. The tool validates the target against the roster and prefixes `Message from 🤖 <name> (@<handle>):` automatically |
| Fire and forget | The sender gets `status: queued` plus a `delivery_id` and finishes its turn. The completion notification later carries the reply or the failure. Queued means handed off, not delivered |
| The roster in the prompt | Teammate names and roles, from each profile's title and description, are part of every Bot Chat's system prompt, so a bot knows who does what before choosing a recipient |
| Only in Bot Chats | `message_agent` exists only in canonical Bot Chat sessions on Bot-Mode-managed installs, never in regular chats, room member sessions or plain CLI sessions |
| Staying silent | A bot with nothing to add ends its turn with `[SILENT]` or `NO_REPLY`; the sender gets an empty reply instead of the token |
| Retries | A failed delivery turn is retried at most once and only when a retry can help: offline target, timeout, rate limit, server error, context overflow (compacted first). Auth, quota and configuration failures surface immediately |
| Reason codes | A failed turn carries a machine-readable reason: `provider_auth_or_access`, `provider_quota_limit`, `provider_rate_limit`, `provider_server_error`, `context_overflow`, `missing_config`, `model_unavailable`, `runtime_offline`, `queued_expired`, `delivery_timeout`, `target_busy`, `unknown` |
| The switch | `agent.bot_mode_protocol: true` in config.yaml (default on) injects the protocol into canonical Bot Chats only; your SOUL.md and regular sessions stay untouched |
| Headless | On a gateway-only install nothing writes the markers. To enable by hand: `hermes -p <bot> chat -c "Bot Chat" --create-if-missing` and an empty `ui_meta: { hermes-bots: {} }` block in one profile's profile.yaml |
```

```code lang=yaml file=~/.hermes/config.yaml (excerpt)
agent:
  bot_mode_protocol: true   # inject the bot-to-bot messaging protocol into canonical Bot Chats
```

```code lang=yaml file=~/.hermes/profiles/atlas/profile.yaml (headless installs only)
ui_meta:
  hermes-bots: {}
```

### The message paths

The plate above is the whole team's wiring. Read it as five standing paths:

```table
| From | To | Carries | Trigger |
| you | atlas | a goal | you type it in atlas's chat |
| atlas | forge, scout, quill | a card or a message with goal, context, files, definition of done | atlas's plan |
| forge, quill | sentinel | "review this" with the definition of done attached | the worker finishing |
| sentinel | forge, quill, atlas | findings ranked by severity, or a block | the review |
| anyone | you | `@user` with one specific question | a decision that is yours |
```

Everything else is noise. If a bot is messaging outside these paths, its SOUL is missing a line.

```callout kind=note title="From the field: the first message you should send"
Tonbi's very first test of bot-to-bot messaging is the right one to copy: he tells one bot, in plain language, "send a message to <other bot> asking to introduce itself, and then tell me the response." The exchange shows up in the receiver's Bot Chat, and the reply comes back to the sender. Do that once with every pair you expect to talk; it costs a minute and it proves the roster, the protocol and the routing in one go.
```

### Prompts

```code lang=markdown file=prompt-b5-handshake.md
Send a message to @<other bot> asking it to introduce itself in two lines
and to tell you which toolsets it has. Tell me the delivery status you got
back, then the reply when it arrives. If the reply does not arrive, tell me
the reason code from the completion notification and what the docs say it
means.
```

```code lang=markdown file=prompt-b5-handoff-shape.md
From now on, every handoff you send with message_agent carries four parts
in this order: the goal in one sentence; the context (paths, facts,
constraints) the recipient cannot see; the files it may touch; and the
definition of done, stated so the recipient can check it without you. Show
me the message you would send to @forge for this task before you send it:
<task>.
```

### Verify

```checklist
[ ] A handshake between every pair that should talk came back with a reply, and the exchange is visible in the receiver's Bot Chat
[ ] The sender's completion notification showed the reply, not just queued
[ ] A message to a bot that is signed out surfaced a provider_auth_or_access reason instead of hanging
[ ] Your handoffs carry goal, context, files and definition of done
```

## Build 6: Rooms

![Three rounds, then the room settles](assets/art/v3-room-rounds.webp)

### What you are building

Group chats that do real deliberation without spinning: a planning room where atlas, forge and scout agree a phase plan; a review room where sentinel judges before you do; and the habits, three rounds, @user escalation, threads, that keep a room useful.

### What the docs say

Checked against the Bot Mode page: Groups and group chats.

```table
| Fact | Detail |
| Membership | 2 to 6 Bots per room. Right-click a Bot, Manage groups, or the room header's Manage members to edit the roster in place; a removed Bot takes no further turns, an added one reads recent history on its first turn |
| Rounds | In the page's words: "Your message triggers up to three serial rounds of member turns. @-mentioned Bots respond (everyone responds when nobody is mentioned); each Bot replies briefly or passes, and the room settles when a full round stays silent." Hard caps: 10 messages per send, 3 rounds |
| Not everyone speaks | Speaking is each member's choice; a Bot replies only when it has something new to add. Mentioning specific members scopes the round to them |
| Escalation | Bots pull each other in with `@name` and escalate to you with `@user`; the room row shows a needs-you badge, and command approvals in the room answer on the click |
| Threads | Reply in thread continues a topic without reordering the room; Activity is a status view, not the conversation |
| Handoff to the primary | `@hermes` reaches the primary Bot from any room |
| Keeps running | When every member lives on the same gateway, that gateway owns turn scheduling; closing the Desktop does not stop a room mid-discussion. Rooms are mirrored into every connected gateway's shared metadata |
| Cross-machine rooms | Members on other connections are seated with a device badge and a device-qualified handle such as `@reviewer-mini`; each member's turns run on its own machine |
| Holds | `stop @bot` holds a member; `@all resume` or any message addressing the room releases everyone |
```

### Two standing rooms

```table
| Room | Members | When you open it | What good looks like |
| planning | atlas, forge, scout | a new project or a change of direction | a numbered phase plan with owners, the shared decisions written out, and one @user question at most |
| review | sentinel, forge, quill | before anything ships | findings ranked by severity, a verdict per artifact, and a block that stays a block |
```

```callout kind=note title="From the field: plan first, then let the boss push"
Tonbi's racing-game run is the clearest public example of a room doing work. His kickoff to the group was two moves: "everyone introduce yourselves and your role, take a look at the spec," then "decide amongst yourselves the phases for this project and the roles. Just plan it, no coding yet." The bots negotiated phases, asked each other real interface questions (texture atlas dimensions, of all things) and marked phase one parallel. Only then: "start working on this project based on this plan. Please report back when you are done with the task or if you hit any blockers, need help from me." He added his orchestrator bot afterward and told it to check in every twenty minutes and push anyone who had not started. His honest note: with no tool calls visible in a room, he repeatedly doubted whether work was happening. Threads are the cure; talk to the orchestrator in a separate thread and let the workers alone.
```

### Prompts

```code lang=markdown file=prompt-b6-planning-room.md
@atlas @forge @scout Everyone introduce yourself in one line: your role and
what you own. Then read <the brief, attached or at this path> and decide
among yourselves the phases for this project and who owns each. Write the
shared decisions (names, formats, interfaces) into the plan so nobody has to
guess them later. Mark which phases can run in parallel. Plan only, no
work yet. When you agree, @atlas posts the plan as a numbered list and asks
me the one question you could not settle, if any.
```

```code lang=markdown file=prompt-b6-review-room.md
@sentinel review <the artifact: a path, a diff, a draft> against this
definition of done: <paste it>. Rank findings by severity with location and
failure scenario. @forge and @quill answer only findings addressed to you,
with the fix or a reason to disagree, no rewrites in the room. @sentinel
closes with one of approve, changes requested, or blocked, and @user only if
the block needs my decision.
```

```code lang=markdown file=prompt-b6-start-work.md
@atlas Start work on the plan we agreed. Hand each phase-one owner its card
or message with goal, context, files and definition of done. Check the room
every twenty minutes: nudge anyone who has not started, unblock what you can,
and post a standup line when a phase completes. Report to me in this thread
only when a phase is done or you are blocked on a decision that is mine.
```

### Verify

```checklist
[ ] The planning room produced a numbered plan with owners and settled at most three rounds after your kickoff
[ ] A review room ended with a verdict per artifact and a needs-you badge only when a decision was genuinely yours
[ ] Closing and reopening the Desktop found the room where it was
[ ] Reply in thread kept a side question from reordering the main conversation
```
