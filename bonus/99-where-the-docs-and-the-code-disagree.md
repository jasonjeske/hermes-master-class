# Where the Docs and the Code Disagree

Checked against the official Slash Commands reference on October 29, 2026. In every case the rows above follow the code.

| Topic | The docs say | v0.22.5 does |
|---|---|---|
| `/steer` | The note is appended to the last tool result | Saves the note as its own user message, the change Volume 5 described in v0.21.2 |
| Short prefixes | `/h` resolves to `/help`, and an ambiguous prefix takes the first match in registry order | The one shortest match wins, so `/h` runs `/hb`, and a tie runs nothing |
| `/save` | CLI only | Also works in chat, where the export arrives as a document |
| `/undo` | Removes the last exchange | Takes a count, `/undo 3`, and puts your prompt back in the box |
| Quick commands | The example names one `status` | Built-in `/status` wins in the CLI, so that quick command never runs there |
| TUI commands | Only `/connectors` is listed as TUI only | The TUI has fifteen commands of its own (Tier 12) and three extra aliases: `/background`, `/switch`, `/session` |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
