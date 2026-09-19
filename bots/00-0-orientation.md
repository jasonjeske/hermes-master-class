# Orientation

![The Hermes Bots Masterclass](../assets/art/v3-hero.webp)

Bot Mode is the part of Hermes Desktop that turns your profiles into a roster of named Bots, each with its own chat, role, model, memory, skills and avatar. Bots run routines, deliberate in group chats, and message each other directly. It ships built in and on by default. And there is no new primitive underneath it: a Bot is a profile, the same `~/.hermes/profiles/<name>/` you met in Volume 1, so everything you do in the roster is visible from the terminal too.

That last sentence is the whole design of this volume. Because a Bot is a profile, a team is a set of folders, and a set of folders can be written down, versioned, shared and installed. So this volume does not describe a team. It ships one: six bots with every file, the routines they run, the way they talk, and the prompts that add a seventh or retire one. You can build it in the app one dialog at a time, or clone the kit and be done in a minute. Both roads end in the same folders.

> 📝 **What this volume rests on**
>
> Every mechanism was checked against the official Bot Mode page, the Profiles page, the Profile Distributions page, the multi-connection guide and the Kanban page for the version installed while writing, plus the bundled files in the Hermes repository. Two operators who published early and detailed Bot Mode walkthroughs, Tonbi's AI Garage and Wanderloots, are quoted where their field experience adds something the docs do not, and always by name.

| Build | You end up with | Checked against | Time |
|---|---|---|---|
| 0 | The mental model: bot, profile, Bot Chat, routine, room, and the two markers that make it all work | Bot Mode, Profiles | 20 minutes |
| 1 | A roster designed from your real work, named so the tags work, sized so the machine keeps up | Bot Mode | 30 minutes |
| 2 | A model per bot with a reason and a cost, and the credential rule that bites | Profiles, Kanban | 30 minutes |
| 3 | Your first three bots born, from the dialog or the CLI, with SOULs written for their roles | Bot Mode, Personality | 45 minutes |
| 4 | Routines attached to the bots that own them, silent when nothing happened | Bot Mode, Cron | 30 minutes |
| 5 | Bots messaging each other, with the delivery contract understood | Bot Mode | 30 minutes |
| 6 | Group chats that plan, review and escalate without spinning | Bot Mode | 45 minutes |
| 7 | Shared memory and a shared board: Hindsight and Mnemosyne, and kanban as the queue | Memory Providers, Kanban | 60 minutes |
| 8 | Bots across machines: the mini, the VPS, one roster | Bot Mode, Multi-connection | 45 minutes |
| 9 | The team shipped as an installable distribution, and the prompts that grow or shrink it | Profile Distributions | 45 minutes |

### How to use a build

Same shape as the other volumes. **What you are building**, then **What the docs say** with the page named, then **Prompts** to paste into a Hermes chat and **Commands** for the terminal, then a **verify** list. The kit under `kits/bot-team/` holds one folder per bot: `SOUL.md`, `config.yaml`, `distribution.yaml`, `routines.sh` and a README.

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-BOTS.md)
