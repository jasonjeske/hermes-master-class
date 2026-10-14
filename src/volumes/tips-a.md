---
title: Hermes Expert Tips
subtitle: Volume 5 of the Hermes Agent Masterclass. Two habits that change how Hermes works for you, steering a running turn and queueing the next ones, and running real work through the kanban board instead of one long chat
why: Most people use Hermes like a chat window. Type, wait, read, type again. The commands and the board that turn it into an operator are already installed, and almost nobody uses them. This volume shows both, on one real project, checked against the source.
date: 2026-10-14
eyebrow: HERMES EXPERT TIPS · VOLUME 5
---

![Hermes Expert Tips](assets/art/v5-hero.webp)

## Orientation

The first four volumes built the agent, the app, the team and the company. This one is about how you work with all of it from hour to hour, and it is short on purpose: two tips, each one a habit that changes what a session with Hermes feels like.

Tip 1 is about the moment a turn is already running. Most people either wait for it to finish or kill it and start over. `/steer` changes direction mid-turn without stopping anything, and `/queue` lines up the next asks behind it, so you never sit and wait to type. Tip 2 is about the moment before a big ask. Most people paste the whole project into one chat and babysit it. The kanban board turns the same ask into cards with owners, parallel workers, handoffs, a review lane and a record, and leaves you only the decisions that are yours.

One project runs through both tips, so you see the difference on the same work: a comparison page for your product against three competitors. Tip 1 does it in the chat, steered and queued. Tip 2 does it on the board.

```callout kind=note title="What this volume rests on"
Every command, subcommand, flag and config key was checked against the installed source of Hermes Agent v0.21.7 (commit 3f2abce, October 12, 2026) and against the official documentation, and the board commands were run against a throwaway Hermes home where running them was safe. Where the docs and the code disagree, the text says so and follows the code. The profile names are the ones from Volume 1, Build 7: the planner is your default profile, and the workers are coder, researcher and writer.
```

```table
| Tip | You end up with | Checked against | Time |
| 1 | A running turn redirected without stopping it, and the next three asks queued behind it, edited and reordered while you wait | Slash Commands reference, CLI guide, the source | 20 minutes |
| 2 | A goal turned into cards with real owners, parallel workers on inexpensive models, handoffs between cards, a review lane, and a board you drive from the terminal, any chat, the dashboard or the app | Kanban page, the source | 60 minutes |
```

### How to use a tip

The same shape as the builds in the other volumes. **What you are building**, then **What the source says** with the facts in one table, then the tip worked on the shared project, then **Prompts** to paste into a Hermes chat and **Commands** for the terminal, then a **Verify** list.

## Tip 1: Steer It, Queue It

![One turn, a steer that lands mid-turn, and the queue behind it](assets/art/v5-steer-queue.webp)

### What you are building

The habit of never waiting on Hermes and never killing a turn to fix it. A turn that is already running has two doors most people do not know about. `/steer` slips a correction into the turn after the tool call it is on finishes, so the agent changes course without starting over and without losing what it already did. `/queue` lines up the next ask behind the current turn, so you type the follow-up the moment you think of it instead of holding it in your head until the turn ends. Together they turn one long wait into a session you keep feeding.

### What the source says

Checked against the Slash Commands reference, the CLI guide's Redirecting the Agent Mid-Turn and Busy Input Mode sections, the messaging guide, and the installed source (Hermes Agent v0.21.7, commit 3f2abce, October 12, 2026).

```table
| Fact | Detail |
| /steer | `/steer <text>`, alias `/s`. The help text: "Inject a message after the next tool call without interrupting." The running tool is never cut; your note waits for the current tool batch to finish, then reaches the model before its next step |
| How the model sees a steer | Since v0.21.2 (September 2026), as its own user message wrapped in an out-of-band marker, which the system prompt tells the model to treat with the same authority as your original request. It is saved in the session like any other message |
| Several steers | Two or three steers sent during one tool call arrive together, one per line |
| Nothing to land on | Sent while no turn is running, a steer is queued as the next turn. If the model finishes without calling another tool, a steer still waiting runs as the next turn instead of being lost |
| /queue | `/queue <text>`, alias `/q`. Each queued prompt runs as its own full turn after the current one, first in, first out, never merged with the others |
| Managing the queue | Classic CLI only: `/queue` or `/queue list` shows it numbered from 1; `/queue edit N <text>` replaces item N; `/queue rm N` removes it; `/queue move A B` moves item A to position B; `/queue clear` empties it; `/queue add <text>` queues text that happens to start with one of those words |
| Words that look like verbs | A verb only counts when its arguments fit: `/queue clear the logs` queues the sentence "clear the logs" |
| Typing while it works | `display.busy_input_mode` decides what plain typing does during a turn: `interrupt` (the default), `queue` or `steer`. `/busy steer`, `/busy queue`, `/busy interrupt` and `/busy status` change and show it in a session, and the CLI saves the choice to config |
| What interrupt really does | During a model request it cancels that request and your text becomes a real user message. During a tool call it acts as a steer and asks a foreground terminal command to move to the background |
| Images | An image never rides a steer; it is queued instead. On messaging platforms a voice note is transcribed and then steered |
| Since when | `/queue` 0.4.0 (March 2026), `/steer` 0.11.0 (April), steer as a busy mode 0.12.0 (April), queue list, edit and move 0.21.3 (September) |
```

### Where each one works

```table
| Surface | /steer | /queue |
| Classic CLI (`hermes chat`) | Yes, acts immediately mid-turn | Yes, with every management verb |
| The TUI | Yes, `/steer` and `/s` | Adds a prompt or shows the count. Edit queued items with the arrow keys; Ctrl+X deletes the highlighted one, Esc cancels the edit |
| Telegram, Discord, Slack and the other gateways | Yes, and it reaches the agent and every subagent it has running | Adds a prompt only. `/queue list` there queues the word "list" as a prompt |
| Hermes Desktop | Steer now on a queued entry in the queue panel; plain typing during a turn redirects it | A queue panel per session: Edit, Steer now, Send next, delete. Stop or Esc with turns queued pauses the queue and opens it above the composer |
| The API server | `POST /v1/runs/{run_id}/steer` with the text as `input`, `message` or `text`; 409 when the run is not running | |
```

Slack blocks native slash commands inside threads, so type `!steer` and `!queue` there; on Matrix, `!queue` works where a client swallows a leading slash.

### The neighbors

Four commands sit next to these two, and mixing them up is the commonest mistake.

```table
| Command | What it does |
| `Ctrl+C` in the CLI | With an empty prompt, interrupts the turn (twice within two seconds forces exit). It also drops a steer that has not landed yet |
| `/stop` | In the CLI, kills background processes and background delegations, not the turn. On messaging platforms it is the hard stop, and it discards the next queued follow-up |
| `/btw <question>` | A side question answered from a read-only snapshot of the conversation, without touching the running turn |
| `/bg <prompt>` | Runs the prompt in a separate background session. There is no `/background` alias |
```

### Steer, queue or interrupt

```table
| The moment | Use | Why |
| It is doing the right task the wrong way | `/steer` | The work so far stays; the correction lands after the current tool call |
| It needs a fact you just remembered | `/steer` | Same turn, same context, no restart |
| It is about to burn ten minutes on the wrong command | `Ctrl+C`, or `/stop` on a chat app, then ask again | A steer would wait for that command to finish |
| You thought of the next task | `/queue` | It runs as its own turn with everything this one learned already in the conversation |
| You want an answer about the work without changing it | `/btw` | Read-only, no interruption |
| A long side job that should not hold up the conversation | `/bg` | Its own session, in parallel |
| You are attaching a screenshot | `/queue` | Images never steer |
```

### Worked on a real project

The comparison page from the orientation, in the classic CLI, on your default profile. You kick it off with a prompt that gives the agent tools to call, because a steer only lands between tool calls:

```code lang=markdown file=prompt-t1-kickoff.md
Research the public pricing of Acme, Globex and Initech for a comparison
page about <your product>. For each one, open the vendor's own pricing
page, record every tier with its name, price and the source URL, and save
the findings to research/pricing.md. Then draft pages/compare.md: a table
of all tiers side by side, and three short paragraphs on where we win.
Mark anything you could not confirm as unconfirmed. Tell me when the
research file is written, before you start the draft.
```

It starts opening pricing pages. This is what the rest of the session looks like, typed while it works:

```code lang=text file=t1-session.txt
# 1. A correction the current work needs: steer it in.
/steer Use annual billing in USD for every price, and skip any tier that has no public price.

# 2. Something you just remembered, also for this turn.
/s Initech changed its pricing page last month; use the page, not the announcement.

# 3. The next three asks, lined up behind this turn.
/queue Add a FAQ to pages/compare.md: five questions a buyer comparing these four products would ask, answered from research/pricing.md only.
/queue Write a launch post for the page, under 200 words, linking to it.
/queue Check every number in pages/compare.md against research/pricing.md and list any mismatch.

# 4. Look at the queue and fix it before it fires.
/queue list
/queue edit 2 Write a LinkedIn post for the page, under 150 words, no hashtags.
/queue move 3 1
/queue rm 3

# 5. A question about the work that must not touch it.
/btw Which of the three has the cheapest entry tier so far?

# 6. A side job that should run in parallel.
/bg Check every link under pages/ and list the broken ones.
```

What happens, step by step. Each steer is acknowledged the moment you send it, and both land after the tool call the agent is on (if you sent them during the same call, they arrive together, one per line); the research file it writes uses annual USD prices. The queue runs after the turn ends, as separate turns, in the order you left it: the number check first, because you moved it to the top, then the FAQ. The launch post never runs. The move pushed it from item 2 to item 3, so `rm 3` removed it, not the number check you meant. Indexes shift every time you move or remove something, which is why `/queue list` comes before every `edit`, `move` and `rm`. The side question gets its answer without the main turn noticing, and the link check reports from its own background session.

### Make typing do what you mean

If you are the kind of person who types corrections while the agent works, change the default. `interrupt` cancels a model request mid-thought; `steer` lets the turn finish its step and take your note on board.

```code lang=bash file=t1-busy-mode.sh
hermes config set display.busy_input_mode steer   # plain typing during a turn now steers

# or, inside any chat session:
#   /busy steer       typing while busy steers the turn
#   /busy queue       typing while busy queues the next turn
#   /busy interrupt   the default
#   /busy status      show the current mode
```

```code lang=markdown file=prompt-t1-busy-audit.md
Read https://hermes-agent.nousresearch.com/docs/user-guide/cli sections
"Redirecting the Agent Mid-Turn" and "Busy Input Mode". Then tell me what
display.busy_input_mode is set to for this profile and for every other
profile in hermes profile list, and recommend a mode for each from how I
use it: CLI work where I correct as I go, a Telegram bot I message from my
phone, or a cron-only profile. Change nothing until I say go.
```

```callout kind=warn title="Gotchas worth knowing before you rely on it"
A steer waits for the whole tool: behind a ten-minute build it lands in ten minutes, so interrupt instead when the tool itself is the mistake. `Ctrl+C` and messaging `/stop` drop a steer that has not landed yet. A queued prompt runs against whatever the turn before it changed, so read `/queue list` and edit before it fires. In the CLI and the TUI, `/steer` reaches only the main agent; to steer one subagent, open the live work monitor with `Ctrl+T` and press `s` in the CLI (`e` in the TUI). On messaging platforms, `/new` and `/reset` empty the queue, and `/model` keeps it. Hermes Desktop ignores `display.busy_input_mode`: typing during a turn there redirects it, attachments queue, and an empty composer stops.
```

```callout kind=note title="Where the docs and the code disagree"
The Slash Commands reference still says a steer is appended to the last tool result's content; since v0.21.2 it is a separate user message, which is what this tip describes. The CLI guide says `/stop` cancels the turn; in v0.21.7 that is `Ctrl+C`, and `/stop` stops background work. The TUI guide says the TUI matches the CLI; for `/queue` it does not, because the management verbs are only in the classic CLI. And no doc page lists the `/s` alias, which is in the command registry.
```

### Verify

```checklist
[ ] A /steer typed during a tool-heavy turn was acknowledged at once, and the agent's next step followed it without the turn restarting
[ ] A /steer typed with no turn running was queued as the next turn instead
[ ] Three /queue prompts ran after the turn, as three separate turns, in order
[ ] /queue list numbered them from 1, and edit, move and rm changed what ran
[ ] /btw answered without changing the running turn
[ ] /busy status reports the mode you chose for this profile
```
