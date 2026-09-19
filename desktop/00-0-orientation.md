# Orientation

![The Hermes Desktop Masterclass](../assets/art/v2-hero.webp)

Hermes Desktop is not a second product. It is the same agent you get from the CLI and the gateway, with the same config, keys, sessions, skills and memory, driven through a native window with panes, a terminal, a file browser, git review, voice, a HUD that floats over other apps, and a plugin system that lets one JavaScript file add a pane to the window. Everything you set up in Volume 1 is already here, and everything you do here shows up in the terminal.

This volume is a build track like Volume 1's second half. Ten builds, in dependency order, each ending with files you paste and prompts you run. The center of gravity is Builds 5 to 8: a plugin workshop that ends with three working plugins in the app and the prompt that makes Hermes write the fourth.

> 📝 **What this volume rests on**
>
> Every path, key, command, menu name and SDK call was checked against the official Hermes documentation for the version installed while writing (the Desktop page, the Desktop Plugin SDK page, Build a Hermes Plugin, the multi-connection guide, and the configuration reference) and against the bundled files in the Hermes repository. Where a tip comes from an operator's video or post rather than the docs, it says so. Where the docs do not cover something, the text says that too rather than guessing.

| Build | You end up with | Checked against | Time |
|---|---|---|---|
| 0 | The app installed, permissions settled once, the local backend understood | Installation, Desktop | 30 minutes |
| 1 | The window at your fingertips: sessions, panes, terminal, git review, HUD, palette, the keys you will actually use | Desktop | 45 minutes |
| 2 | The settings that decide cost and behavior, set on purpose, and an audit prompt for the rest | Desktop, Configuration | 30 minutes |
| 3 | Skills, plugins, tools and MCP managed from the app, the two safety plugins on | Desktop, Plugins | 20 minutes |
| 4 | The app talking to a Hermes on another machine, with the registry of every gateway you own | Desktop, Multi-connection | 45 minutes |
| 5 | Your first desktop plugin, loaded live | Desktop Plugin SDK | 30 minutes |
| 6 | A Prompt Library page with persistent storage | Desktop Plugin SDK | 30 minutes |
| 7 | A Ledger plugin with agent tools, a backend and a desktop page in one package | Build a Hermes Plugin, SDK | 60 minutes |
| 8 | The Fleet Board, and the prompt that makes Hermes write your next plugin | SDK, Plugins | 30 minutes |
| 9 | Updates, permissions after updates, logs, recovery and uninstall, all understood before you need them | Desktop | 20 minutes |

### How to use a build

Each build has four pieces. **What you are building** says what exists at the end. **What the docs say** is the short list of facts the build rests on, with the page named. **Prompts** are blocks marked with a file name like `prompt-d2-audit.md`: paste the whole block into a Hermes chat, in the app or anywhere else. **Commands** run in the app's own terminal pane or in your shell. Every build ends with a **verify** list, and a build is not done until that list passes.

> ℹ️ **The kits**
>
> Builds 5 to 8 ship their plugins as complete folders in the repository under `kits/`, validated against the loader's contract and, for the Python half, against `hermes plugins doctor --ci`. Copy a prompt and have Hermes type them, or clone the folder and drop it in place. Both roads end in the same file.

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-DESKTOP.md)
