# Tier 6: Sessions, Files and Sharing

Finding old work, forking it, moving it to your phone, and getting text and images in and out.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 49 | `/title` | Names the current session | Right after you start work you will want to find again | CLI and chat |
| 50 | `/sessions`, TUI `/switch` `/session` | Browses previous sessions and resumes one. In chat, `search` filters and `all` lists every origin (admins only). In the TUI it switches between the sessions open right now | You know the work exists but not what you called it | CLI and chat |
| 51 | `/branch` `/fork` | Copies the session into an independent branch. On Discord, Telegram, Slack and Matrix the branch opens in a new thread, and `--here` moves this chat onto it instead | You want to try a different approach without losing the current one | CLI and chat |
| 52 | `/handoff` | Moves the session to a messaging platform. The gateway picks it up there with the full transcript, and the CLI exits | You leave the desk and want to keep going from your phone. Needs the gateway running and a home channel set | CLI |
| 53 | `/save` | Exports the conversation as `json`, `md` or `html`. `redact` strips secrets from messages and tool output. In chat the file arrives as a document | You need a record to share, file or feed into something else | CLI and chat |
| 54 | `/history` | Prints the conversation so far | You want to reread what was said without scrolling | CLI |
| 55 | `/copy` | Copies the last response, or the Nth from last, to the clipboard | You want the answer in another app without terminal formatting | CLI |
| 56 | `/prompt` `/compose` | Opens your text editor to write the next prompt in markdown, then sends it (also `Ctrl+G`) | Long, structured prompts you want to edit properly | CLI |
| 57 | `/paste` | Attaches the image on your clipboard to the next prompt | You copied a screenshot and want Hermes to see it | CLI |
| 58 | `/image` | Attaches a local image file to the next prompt | The picture is on disk, not on the clipboard | CLI |
| 59 | `/export` | Packs a profile (skills, memory, persona, crons, plugins, settings) into a `.tar.gz`, with credentials stripped | Backing up a profile, or giving it to someone | CLI |
| 60 | `/import` | Installs a profile archive as a new profile. It never overwrites one you have | Setting up a profile someone exported | CLI |
| 61 | `/clear` | Clears the screen and starts a new session | You want a clean screen and a clean context together | CLI |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
