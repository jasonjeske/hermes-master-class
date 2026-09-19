# Build 8: Plugin Workshop IV, let Hermes build the next one

![Build 8](../assets/art/part-11.webp)

### What you are building

The habit that turns Hermes Desktop into your own toolbox: you describe a pane, Hermes writes it against the documented contract, validates it, and you switch it on. The worked example is the Fleet Board, a pane that lists every profile on the gateway with its last activity, built from a documented gateway call and nothing else. Then the shape of a sharing link, so the plugins you make can be installed by anyone with one click.

### What the docs say

Checked against the Desktop Plugin SDK page (Host API, the agents section, distributing with an install link) and the Plugins page.

| Fact | Detail |
|---|---|
| The agent's own checklist | When an agent writes a desktop plugin it should load the bundled `hermes-desktop-plugins` skill, which carries the contract in agent-facing form and a ready `templates/plugin.js` |
| The gateway door | `host.request(method, params)` is the same JSON-RPC the app uses. `profiles.list` returns every profile with its most recent conversation as `last_session`; `profiles.create` creates one with `name`, `description`, `clone_from`, `soul` and a model pin |
| Data layer | `useQuery` from the SDK shares the app's query client: cache, dedupe, `refetchInterval`. Do not poll faster than a few seconds |
| Install links | `<a href="hermes://plugin/install?repo=owner/repo&enable=1">` opens a confirmation dialog that lists what the repo ships; deep links never auto-install |
| Where to look | Capabilities, Plugins, Installed shows one row per plugin with Desktop and Agent switches; Browse is the public catalog; Install from Git takes any repo and can pin a commit |

### The file

*`~/.hermes/desktop-plugins/fleet-board/plugin.js`*

```javascript
// Fleet Board, a Hermes Desktop plugin: every profile (every Bot) at a glance, with its last activity.
// Reads the gateway through host.request('profiles.list'), the same RPC the app uses. No backend needed.
import {
  queryClient,
  host, useValue, useQuery, relativeTime, Button, ScrollArea, EmptyState, StatusDot,
  PANES_AREA, PALETTE_AREA, STATUSBAR_AREAS
} from '@hermes/plugin-sdk'
import { jsx, jsxs } from 'react/jsx-runtime'

const ID = 'fleet-board'

function useFleet() {
  return useQuery({
    queryKey: [ID, 'profiles'],
    queryFn: () => host.request('profiles.list', { include_sessions: true }),
    refetchInterval: 30000
  })
}

function rowsOf(data) {
  const list = Array.isArray(data) ? data : (data && Array.isArray(data.profiles) ? data.profiles : [])
  return list.map(p => {
    const name = p.name || p.profile || String(p)
    const last = p.last_session || null
    const when = last && (last.updated_at || last.last_active || last.created_at) || null
    return { name, title: p.title || p.description || '', when, model: p.model || '' }
  })
}

function FleetPane() {
  const { data, isLoading, error, refetch } = useFleet()
  const busy = useValue(host.state.busy)
  const rows = rowsOf(data)
  return jsxs('div', {
    className: 'flex h-full flex-col gap-2 p-3 text-sm',
    children: [
      jsxs('div', { className: 'flex items-center justify-between', children: [
        jsx('div', { className: 'font-medium', children: 'Fleet' }),
        jsx(Button, { size: 'sm', variant: 'ghost', onClick: () => refetch(), children: 'Refresh' })
      ]}),
      error ? jsx('div', { className: 'text-(--ui-text-tertiary)', children: 'Could not read profiles: ' + String(error.message || error) }) : null,
      isLoading ? jsx('div', { className: 'text-(--ui-text-tertiary)', children: 'Loading the roster' }) : null,
      jsx(ScrollArea, { className: 'min-h-0 flex-1', children:
        rows.length
          ? jsx('div', { className: 'flex flex-col gap-1', children: rows.map(r => jsxs('button', {
              type: 'button',
              key: r.name,
              className: 'flex items-center justify-between gap-2 rounded px-2 py-1 text-left hover:bg-(--ui-accent)/10',
              onClick: () => host.newChat(r.name),
              children: [
                jsxs('div', { className: 'flex items-center gap-2', children: [
                  jsx(StatusDot, { status: r.when ? 'ok' : 'idle' }),
                  jsxs('div', { children: [
                    jsx('div', { children: r.name }),
                    r.title ? jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-tertiary)', children: r.title }) : null
                  ]})
                ]}),
                jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-quaternary)', children: r.when ? relativeTime(r.when) : 'no sessions yet' })
              ]
            })) })
          : (!isLoading && !error ? jsx(EmptyState, { title: 'No profiles', description: 'Create a Bot in the Bots tab and it appears here.' }) : null)
      }),
      jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-quaternary)', children: busy ? 'focused chat is working' : 'idle' })
    ]
  })
}

function FleetChip() {
  const { data } = useFleet()
  const n = rowsOf(data).length
  return jsx('button', {
    type: 'button',
    className: 'px-1.5 text-[0.6875rem] text-(--ui-text-tertiary)',
    onClick: () => host.notify({ kind: 'info', message: String(n) + ' profiles on this gateway. The Fleet pane lists them.' }),
    children: 'fleet ' + String(n)
  })
}

export default {
  id: 'fleet-board',
  name: 'Fleet Board',
  defaultEnabled: false,
  register(ctx) {
    ctx.registerMany([
      { id: 'pane', area: PANES_AREA, title: 'Fleet', data: { placement: 'right', width: '300px' }, render: () => jsx(FleetPane, {}) },
      { id: 'chip', area: STATUSBAR_AREAS.right, order: 128, render: () => jsx(FleetChip, {}) },
      { id: 'open', area: PALETTE_AREA, data: { id: 'fleet-board.open', label: 'Fleet Board: refresh roster', keywords: ['fleet', 'bots', 'profiles'], run: () => { queryClient.invalidateQueries({ queryKey: ['fleet-board', 'profiles'] }); host.notify({ kind: 'info', message: 'Fleet roster refreshed.' }) } } }
    ])
  }
}
```

### Prompts

The first prompt is the one you will reuse for every plugin after this. It names the skill, the contract, the validation and the proof, and leaves the idea to you.

*`prompt-d8-build-me-a-plugin.md`*

```markdown
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

*`prompt-d8-share-it.md`*

```markdown
Prepare the <id> plugin for sharing. Create a git repository containing
only the plugin folder and a README that explains what it does, what it
reads, and how to install it: an "Install in Hermes" link of the form
hermes://plugin/install?repo=<owner>/<repo>&enable=1 plus the manual copy
path. Confirm from
https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
what the install dialog will show for a desktop-only repo. Do not push;
show me the repository contents and the README first.
```

> 📝 **From the field: the two-minute plugin**
>
> In part 3 of his desktop masterclass Tonbi builds a plugin live from a single dictated prompt: a status-bar item that opens a popover with the latest AI news from a few RSS feeds and an update button. His verbatim ask, lightly cleaned: "make a Hermes desktop app plugin using the plugin SDK. I want to fetch the latest AI news from free RSS feeds. I want an update button that will update the news. It should have a popover style with the title on the status bar. I can click and then see three to four news items and the update button." It came back in a couple of minutes, missing the update button, which took seconds to fix. His own caveat is the useful part: "usually won't one shot these. You need to edit it a little bit." Write the spec anyway; the edit is smaller when the spec was bigger.

### Ideas that are one prompt away

| Pane | Reads | Why it earns its place |
|---|---|---|
| Cost today | `host.state.focusedUsage` and `hermes insights` through a Python half | The number you want in the corner of your eye, not in a report |
| Cron board | the cron JSON-RPC the Scheduled Jobs page uses | Every routine, its last run and next run, without leaving the chat |
| Kanban lane | the kanban RPC the Kanban page uses | Your three active cards beside the conversation that feeds them |
| Health log | a Python half with plugin_db | Sleep, training, supplements: a form and a week view, and the agent can write to it too |
| Reading list | `ctx.storage` and `ctx.os.openExternal` | Links you save from chats, one click to open, one to send to a Bot |

### Verify

- [ ] Fleet Board lists every profile hermes profile list knows about, with a last-activity time where one exists
- [ ] Clicking a row opens a new chat in that profile
- [ ] The build prompt produced a plugin that validated and loaded without an error toast
- [ ] Your README's install link opens the app's confirmation dialog rather than installing silently

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-DESKTOP.md)
