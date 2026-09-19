## Build 5: Plugin Workshop I, Hello Hermes

![Build 5](assets/art/v2-plugin-anatomy.webp)

### What you are building

Your first desktop plugin: a pane in the right dock, a chip in the status bar, a palette command and a keybind, in one file of about eighty lines, loaded live into the running app without a build step. It does nothing useful yet. It proves the loop: write a file, watch the app pick it up, see it in Capabilities, and learn the six rules every plugin after this one obeys.

### What the docs say

Checked against the Desktop Plugin SDK page and the Extending section of the Desktop page.

```table
| Fact | Detail |
| One file | `~/.hermes/desktop-plugins/<id>/plugin.js`, plain ESM, loaded uncompiled. The folder name must equal the plugin's `id` |
| Three imports only | `@hermes/plugin-sdk`, `react`, `react/jsx-runtime`. Anything else fails to resolve on purpose |
| No JSX syntax | The file is not compiled, so write `jsx()` and `jsxs()` calls from `react/jsx-runtime` |
| The contract | Default-export `{ id, name, defaultEnabled, register(ctx) }`. `register` receives a scoped context and calls `ctx.register` or `ctx.registerMany` with contributions `{ id, area, title, order, when, render, data }` |
| Where things can go | Panes (`placement` main, left, right, top, bottom, optional `dock`), full pages (`ROUTES_AREA`), sidebar nav, status bar left or right, title bar, palette commands, keybinds, themes, composer slots, transcript directives |
| Styling | Theme variables only, in the `text-(--ui-text-tertiary)` form. Never a literal color. Leave the background alone |
| Hot reload | The app watches the folder, loads a new file within seconds, and reloads on every save. `Cmd+K`, Reload desktop plugins, forces it. Errors show as a toast and in `hermes logs gui -f` |
| App level | A desktop plugin is the same on every profile, gateway and remote machine the window connects to |
| Authority | A loaded plugin runs in the renderer with the app's full authority; the loader isolates errors, not intent. Load only files you or your agent wrote |
```

```callout kind=note title="From the field: form follows the job"
Tonbi's plugin guide counts twenty-five places a contribution can land and sorts them into four forms: compact (a status-bar item, "one factor, one action that should always be nearby"), anchored (a popover for detail and quick control without leaving the chat), expansive (a route with a sidebar entry, for real applications and dense data) and declarative (structured data the host decides how to show). His rule: decide the form from what the plugin is for before writing a line. His limits are worth pinning too: a plugin's storage is small JSON state, not a database; a plugin only runs while the app is open; it can only occupy areas the app itself consumes; and "a renderer-only plugin is strong for UI. A plugin plus a Python backend can become a real product." Builds 5, 6 and 7 walk that ladder in order.
```

### The file

```code lang=javascript file=~/.hermes/desktop-plugins/hello-hermes/plugin.js
// Hello Hermes - a Hermes Desktop plugin. Folder name must equal the id.
// Loaded uncompiled: no JSX syntax, and only these specifiers resolve.
import { host, haptic, useValue, STATUSBAR_AREAS, PALETTE_AREA, KEYBINDS_AREA } from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'

function HelloHermesPane() {
  const gateway = useValue(host.state.gateway)
  const profile = useValue(host.state.profile)

  return jsxs('div', {
    className: 'flex h-full flex-col gap-2 p-3 text-sm',
    children: [
      jsx('div', { className: 'font-medium', children: "Hello Hermes" }),
      jsx('div', {
        className: 'text-(--ui-text-tertiary)',
        children: 'gateway: ' + String(gateway)
      }),
      jsx('div', {
        className: 'text-(--ui-text-tertiary)',
        children: 'profile: ' + String(profile)
      })
    ]
  })
}

function HelloHermesChip() {
  return jsx('button', {
    type: 'button',
    className: 'px-1.5 text-[0.6875rem] text-(--ui-text-tertiary)',
    onClick: () => {
      haptic('tap')
      host.notify({ kind: 'info', message: "Hello Hermes is loaded." })
    },
    children: "hello-hermes"
  })
}

export default {
  id: "hello-hermes",
  name: "Hello Hermes",
  defaultEnabled: false,
  register(ctx) {
    ctx.register({
      id: 'pane',
      area: 'panes',
      title: "Hello Hermes",
      data: { placement: "right", width: "280px" },
      render: () => jsx(HelloHermesPane, {})
    })

    ctx.register({
      id: 'chip',
      area: STATUSBAR_AREAS.right,
      order: 130,
      render: () => jsx(HelloHermesChip, {})
    })

    ctx.register({
      id: 'open',
      area: PALETTE_AREA,
      data: {
        id: "hello-hermes.open",
        label: "Open Hello Hermes",
        keywords: ["hello-hermes", 'hermes', 'pane'],
        run: () => host.notify({ kind: 'info', message: "Hello Hermes pane is in the right dock." })
      }
    })

    ctx.register({
      id: 'keybind',
      area: KEYBINDS_AREA,
      data: {
        id: "hello-hermes.focus",
        label: "Focus Hello Hermes",
        category: "Hello Hermes",
        defaults: ['mod+alt+h'],
        run: () => host.notify({ kind: 'info', message: "Hello Hermes focused." })
      }
    })
  }
}
```

```callout kind=info title="Why defaultEnabled is false"
A plugin with `defaultEnabled: false` inventories in Capabilities, Plugins and stays dark until you flip it on. That is the right default for anything you are still writing: the app loads the file, you enable it when you want to see it, and a broken save never surprises you mid-conversation. Ship it that way too; the person installing it decides.
```

### Commands

```code lang=bash file=hello.sh
mkdir -p ~/.hermes/desktop-plugins/hello-hermes
# paste the file above as ~/.hermes/desktop-plugins/hello-hermes/plugin.js
# then in the app: Cmd+K, "Reload desktop plugins", then Capabilities, Plugins, switch Hello Hermes on
hermes logs gui -f            # the load line, or the error toast's cause
```

### Prompts

```code lang=markdown file=prompt-d5-explain-my-plugin.md
Read https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk
sections "Mental model", "The plugin contract" and "Pitfalls". Then read the
file ~/.hermes/desktop-plugins/hello-hermes/plugin.js and explain it to me
contribution by contribution: what each register call adds, which area it
lands in, and which host door it uses. Finish with the three rules from the
Pitfalls section that this file already obeys and the one thing I would
break first if I edited it carelessly.
```

```code lang=markdown file=prompt-d5-change-one-thing.md
Change the Hello Hermes plugin so the pane also shows the active model
(host.state.model) and the chip shows the gateway state instead of the
word hello-hermes. Keep every rule of the format: only the three imports,
jsx() calls, theme variables, folder name equal to id. Show me the diff
before you write it. After I say go, save it and tell me what I should see
after the hot reload, then tail hermes logs gui for ten seconds and report
any error.
```

### Verify

```checklist
[ ] Capabilities, Plugins lists Hello Hermes with a Desktop switch; flipping it on adds the pane to the right dock
[ ] The status bar shows the hello-hermes chip and clicking it toasts
[ ] Cmd+K finds "Open Hello Hermes"; Cmd+Option+H fires the keybind (Cmd+Shift+H is taken: it toggles the HUD)
[ ] hermes logs gui -f shows the load with no error line
```

## Build 6: Plugin Workshop II, the Prompt Library

![Build 6](assets/art/part-03.webp)

### What you are building

A full page in the app, reachable from the sidebar, the palette and a keybind, that stores the prompts you paste most: search them, copy one to the clipboard, or open a fresh chat in the current profile with the prompt ready to paste. State persists per plugin through the SDK's storage. It ships with three starter prompts from this masterclass so it is useful the second it loads.

### What the docs say

Checked against the Desktop Plugin SDK page: Pages and sidebar nav, Palette commands and keybinds, Host API, the `ctx.os` door, Settings and storage, the UI kit.

```table
| Fact | Detail |
| A page | `ROUTES_AREA` with `data: { path }` mounts a full page in the workspace; pair it with `SIDEBAR_NAV_AREA` (`path`, `label`, `codicon`) and navigate with `host.navigate(path)` |
| Storage | `ctx.storage.get(key, fallback)`, `.set`, `.remove`, namespaced under `hermes.plugin.<id>.*`. Renaming the plugin loses its stored state |
| The OS door | `ctx.os.writeClipboard(text)` resolves false when unavailable; `ctx.os.openExternal(url)`, `ctx.os.revealPath(path)`, `ctx.os.notify` for native notifications |
| New chats | `host.newChat(profile)` opens a fresh chat, optionally in another profile |
| The UI kit | Import the app's own components (`Button`, `Input`, `Textarea`, `ScrollArea`, `EmptyState` and the rest) so the page is native by default |
| State in React | Subscribe with `useValue(atom)` only in the component that renders the value; read atoms with `.get()` in handlers |
```

### The file

```code lang=javascript file=~/.hermes/desktop-plugins/prompt-library/plugin.js
PROMPT_LIBRARY_PLUGIN_JS
```

```callout kind=note title="Why copy and paste, not inject"
The SDK gives a plugin a curated set of doors and a composer middleware for transforming a draft on its way out, but no documented call that writes text into the composer of an existing chat. So the library does the honest thing: it puts the prompt on your clipboard and, if you ask, opens a fresh chat in the current profile for you to paste into. One keystroke more, zero reliance on an undocumented method that a release could remove.
```

### Prompts

```code lang=markdown file=prompt-d6-seed-my-library.md
Open the Prompt Library page in the app is my job; yours is the content.
Read every prompt I have pasted into you in the last two weeks
(session_search across my sessions for messages that start with "Read
https://hermes-agent.nousresearch.com/docs" or with "Build me"), pick the
eight I reuse most, and give each a title under six words and three tags.
Return them as a JSON array of {title, tags, body} so I can paste them into
the library one by one. Do not rewrite the bodies.
```

```code lang=markdown file=prompt-d6-extend-it.md
Read the Prompt Library plugin at
~/.hermes/desktop-plugins/prompt-library/plugin.js and add one feature:
an "Export" button that writes all prompts as JSON to the clipboard, and an
"Import" textarea that merges a pasted JSON array into storage without
duplicating ids. Keep the format rules. Show me the diff before saving.
```

### Verify

```checklist
[ ] The sidebar shows Prompts; the page opens with the three starter prompts
[ ] Saving a prompt survives an app restart (storage is persisted)
[ ] Copy puts the body on the clipboard; New chat opens a chat in the current profile
[ ] Cmd+Shift+P opens the page
```

## Build 7: Plugin Workshop III, the Ledger (agent and desktop in one package)

![Build 7](assets/art/v2-unified-package.webp)

### What you are building

The first plugin with two halves in one folder. The agent gets two tools, `ledger_add` and `ledger_report`, and a `/ledger` slash command, so telling Hermes "I paid 42.50 for groceries" records it and "how much did I spend this month" answers from real numbers. The desktop gets a Ledger page that reads the same database through the plugin's own backend routes, with a form and bars by category. Money lands in a SQLite file under the plugin data directory, never in the plugin folder, so updates cannot erase it.

### What the docs say

Checked against Build a Hermes Plugin, the Desktop Plugin SDK's "One package, both SDKs" and "The Python side", and Extending the Dashboard.

```table
| Fact | Detail |
| Layout | `~/.hermes/plugins/<id>/` with `plugin.yaml`, `__init__.py` (`register(ctx)`), `schemas.py`, `tools.py`, `dashboard/manifest.json` plus `dashboard/plugin_api.py`, and `desktop/plugin.js`. One installable folder |
| Manifest v2 | `manifest_version: 2`, `api_version: 1`, `name`, `version`, `description`, `license`, `tags`, `provides_tools`; optional `requires_env`, `python_dependencies` or a `pyproject.toml`, `config_schema` |
| Handlers | `def handler(args: dict, **kwargs) -> str`: always a JSON string, never raise. The schema description is what makes the model call the tool |
| Slash commands | `ctx.register_command("ledger", handler, description=...)` gives `/ledger` on every surface |
| Durable state | `from plugins.plugin_storage import plugin_db` returns a SQLite connection at `<home>/plugin-data/<id>/data.db`, WAL mode. Never write into the plugin directory |
| The backend | `dashboard/manifest.json` is `{"name": "<id>", "api": "plugin_api.py"}`; `plugin_api.py` exports a FastAPI `router`; routes mount under `/api/plugins/<id>/` inside the gateway, at startup, only when the plugin is in `plugins.enabled` |
| The desktop half | `desktop/plugin.js` is an ordinary disk plugin; the app copies it to `~/.hermes/desktop-plugins/<id>/` when the package is installed and reaches the backend with `ctx.rest('/summary')` |
| Two switches | The Python half is gated by `plugins.enabled` in config.yaml; the desktop half by its own switch in Capabilities, Plugins. Both default to off |
| Doctor | `hermes plugins doctor ~/.hermes/plugins/ledger --ci` runs real discovery, manifest parsing, import and registration |
```

### The files

```code lang=yaml file=~/.hermes/plugins/ledger/plugin.yaml
LEDGER_PLUGIN_YAML
```

```code lang=python file=~/.hermes/plugins/ledger/schemas.py
LEDGER_SCHEMAS_PY
```

```code lang=python file=~/.hermes/plugins/ledger/ledger_core.py
LEDGER_CORE_PY
```

```code lang=python file=~/.hermes/plugins/ledger/tools.py
LEDGER_TOOLS_PY
```

```code lang=python file=~/.hermes/plugins/ledger/__init__.py
LEDGER_INIT_PY
```

```code lang=json file=~/.hermes/plugins/ledger/dashboard/manifest.json
LEDGER_MANIFEST_JSON
```

```code lang=python file=~/.hermes/plugins/ledger/dashboard/plugin_api.py
LEDGER_API_PY
```

```code lang=javascript file=~/.hermes/plugins/ledger/desktop/plugin.js
LEDGER_DESKTOP_JS
```

### Commands

```code lang=bash file=ledger-install.sh
# 1. Put the folder in place (or clone it from the masterclass repo's kits/)
cp -R kits/agent-plugins/ledger ~/.hermes/plugins/ledger     # from a clone of the masterclass repo
/bin/ls ~/.hermes/plugins/ledger ~/.hermes/plugins/ledger/dashboard ~/.hermes/plugins/ledger/desktop

# 2. Prove the agent half before enabling it
hermes plugins doctor ~/.hermes/plugins/ledger --ci

# 3. Enable the Python half (this is the security gate for the backend routes too)
hermes plugins enable ledger
hermes plugins list | grep ledger

# 4. Restart the gateway so the routes mount, then make the app copy the desktop half and switch it on
hermes gateway restart
# In the app: Capabilities, Plugins, Rescan. That copies desktop/plugin.js to ~/.hermes/desktop-plugins/ledger/
# beside a .hermes-package.json marker (hermes plugins update does the same). Then: Ledger, Desktop switch on.
/bin/ls ~/.hermes/desktop-plugins/ledger/     # plugin.js and .hermes-package.json must both be there

# 5. Talk to it
hermes chat -q "I paid 42.50 for groceries today, record it in the ledger"
hermes chat -q "How much did I spend this month and on what?"
```

```callout kind=warn title="If the page says the backend is not reachable"
Four causes, in order: the desktop half was never copied because nothing triggered a Rescan (check for `~/.hermes/desktop-plugins/ledger/.hermes-package.json`), the plugin is not in `plugins.enabled` (the desktop switch alone never imports Python, by design), the gateway was not restarted after enabling (routes mount at startup), or the route failed to import. The last one leaves a line in `~/.hermes/logs/errors.log` reading `Failed to load plugin ledger API routes`.
```

### Prompts

```code lang=markdown file=prompt-d7-install-and-prove.md
Install the ledger plugin from the masterclass kit. Do these in order and
show me the output of each step:
1. Read https://hermes-agent.nousresearch.com/docs/developer-guide/plugins
   section "Store durable state" and tell me where the ledger's database
   will live on this machine.
2. Copy the kit folder to ~/.hermes/plugins/ledger and run
   hermes plugins doctor ~/.hermes/plugins/ledger --ci.
3. Show me the diff hermes plugins enable ledger would make to my
   config.yaml, then run it after I say go, then restart the gateway.
4. Record one expense and one income with the ledger tools, run
   ledger_report for this month, and show me the JSON.
5. Tell me exactly where to click in the app to switch the desktop half on.
```

```code lang=markdown file=prompt-d7-categorize-with-the-model.md
Extend the ledger plugin's Python half with one auxiliary task: when
ledger_add is called without a category, classify the note into one of my
categories with ctx.llm. Read
https://hermes-agent.nousresearch.com/docs/developer-guide/plugin-llm-access
first and register the task with ctx.register_auxiliary_task("ledger_classifier")
so I can pin it to a cheap model under auxiliary.ledger_classifier in
config.yaml. Keep the handler contract: JSON string back, never raise, the
classification failing must fall back to the category "uncategorized".
Show me the diff, then run the doctor.
```

### Verify

```checklist
[ ] hermes plugins doctor ~/.hermes/plugins/ledger --ci prints OK and registrations: 2 tool(s)
[ ] After enable and restart, hermes plugins list shows ledger enabled and the banner lists ledger_add, ledger_report
[ ] /ledger in any chat prints the month summary without a model call
[ ] The Ledger page shows the entry the agent recorded, and an entry added on the page shows up in ledger_report
[ ] ~/.hermes/plugin-data/ledger/data.db exists and the plugin folder holds no database
```

## Build 8: Plugin Workshop IV, let Hermes build the next one

![Build 8](assets/art/part-11.webp)

### What you are building

The habit that turns Hermes Desktop into your own toolbox: you describe a pane, Hermes writes it against the documented contract, validates it, and you switch it on. The worked example is the Fleet Board, a pane that lists every profile on the gateway with its last activity, built from a documented gateway call and nothing else. Then the shape of a sharing link, so the plugins you make can be installed by anyone with one click.

### What the docs say

Checked against the Desktop Plugin SDK page (Host API, the agents section, distributing with an install link) and the Plugins page.

```table
| Fact | Detail |
| The agent's own checklist | When an agent writes a desktop plugin it should load the bundled `hermes-desktop-plugins` skill, which carries the contract in agent-facing form and a ready `templates/plugin.js` |
| The gateway door | `host.request(method, params)` is the same JSON-RPC the app uses. `profiles.list` returns every profile with its most recent conversation as `last_session`; `profiles.create` creates one with `name`, `description`, `clone_from`, `soul` and a model pin |
| Data layer | `useQuery` from the SDK shares the app's query client: cache, dedupe, `refetchInterval`. Do not poll faster than a few seconds |
| Install links | `<a href="hermes://plugin/install?repo=owner/repo&enable=1">` opens a confirmation dialog that lists what the repo ships; deep links never auto-install |
| Where to look | Capabilities, Plugins, Installed shows one row per plugin with Desktop and Agent switches; Browse is the public catalog; Install from Git takes any repo and can pin a commit |
```

### The file

```code lang=javascript file=~/.hermes/desktop-plugins/fleet-board/plugin.js
FLEET_BOARD_PLUGIN_JS
```

### Prompts

The first prompt is the one you will reuse for every plugin after this. It names the skill, the contract, the validation and the proof, and leaves the idea to you.

```code lang=markdown file=prompt-d8-build-me-a-plugin.md
Build me a Hermes Desktop plugin. Do these in order.

1. Load the bundled hermes-desktop-plugins skill and read its template.
2. The plugin: <one sentence: what it shows or does, and where it lives:
   a right pane, a full page, or a status bar chip>. Its id is <id>.
3. Write ~/.hermes/desktop-plugins/<id>/plugin.js obeying the format:
   only @hermes/plugin-sdk, react and react/jsx-runtime imports; jsx()
   calls, no JSX syntax; theme variables only, no literal colors; folder
   name equal to id; defaultEnabled false; every identifier you use is in
   the import line; atoms read with .get() in handlers and useValue only
   in the component that renders them; no polling faster than ten seconds.
4. For data use host.request with a method that is documented on the
   Desktop Plugin SDK page or the web dashboard page; if the data needs a
   backend, stop and propose a unified package instead.
5. Show me the file before writing it. After I say go, write it, tell me
   the palette command to reload plugins, and watch hermes logs gui for
   fifteen seconds. Report the load line or the exact error.
```

```code lang=markdown file=prompt-d8-share-it.md
Prepare the <id> plugin for sharing. Create a git repository containing
only the plugin folder and a README that explains what it does, what it
reads, and how to install it: an "Install in Hermes" link of the form
hermes://plugin/install?repo=<owner>/<repo>&enable=1 plus the manual copy
path. Confirm from
https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
what the install dialog will show for a desktop-only repo. Do not push;
show me the repository contents and the README first.
```

```callout kind=note title="From the field: the two-minute plugin"
In part 3 of his desktop masterclass Tonbi builds a plugin live from a single dictated prompt: a status-bar item that opens a popover with the latest AI news from a few RSS feeds and an update button. His verbatim ask, lightly cleaned: "make a Hermes desktop app plugin using the plugin SDK. I want to fetch the latest AI news from free RSS feeds. I want an update button that will update the news. It should have a popover style with the title on the status bar. I can click and then see three to four news items and the update button." It came back in a couple of minutes, missing the update button, which took seconds to fix. His own caveat is the useful part: "usually won't one shot these. You need to edit it a little bit." Write the spec anyway; the edit is smaller when the spec was bigger.
```

### Ideas that are one prompt away

```table
| Pane | Reads | Why it earns its place |
| Cost today | `host.state.focusedUsage` and `hermes insights` through a Python half | The number you want in the corner of your eye, not in a report |
| Cron board | the cron JSON-RPC the Scheduled Jobs page uses | Every routine, its last run and next run, without leaving the chat |
| Kanban lane | the kanban RPC the Kanban page uses | Your three active cards beside the conversation that feeds them |
| Health log | a Python half with plugin_db | Sleep, training, supplements: a form and a week view, and the agent can write to it too |
| Reading list | `ctx.storage` and `ctx.os.openExternal` | Links you save from chats, one click to open, one to send to a Bot |
```

### Verify

```checklist
[ ] Fleet Board lists every profile hermes profile list knows about, with a last-activity time where one exists
[ ] Clicking a row opens a new chat in that profile
[ ] The build prompt produced a plugin that validated and loaded without an error toast
[ ] Your README's install link opens the app's confirmation dialog rather than installing silently
```
