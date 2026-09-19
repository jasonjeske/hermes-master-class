# Build 6: Plugin Workshop II, the Prompt Library

![Build 6](../assets/art/part-03.webp)

### What you are building

A full page in the app, reachable from the sidebar, the palette and a keybind, that stores the prompts you paste most: search them, copy one to the clipboard, or open a fresh chat in the current profile with the prompt ready to paste. State persists per plugin through the SDK's storage. It ships with three starter prompts from this masterclass so it is useful the second it loads.

### What the docs say

Checked against the Desktop Plugin SDK page: Pages and sidebar nav, Palette commands and keybinds, Host API, the `ctx.os` door, Settings and storage, the UI kit.

| Fact | Detail |
|---|---|
| A page | `ROUTES_AREA` with `data: { path }` mounts a full page in the workspace; pair it with `SIDEBAR_NAV_AREA` (`path`, `label`, `codicon`) and navigate with `host.navigate(path)` |
| Storage | `ctx.storage.get(key, fallback)`, `.set`, `.remove`, namespaced under `hermes.plugin.<id>.*`. Renaming the plugin loses its stored state |
| The OS door | `ctx.os.writeClipboard(text)` resolves false when unavailable; `ctx.os.openExternal(url)`, `ctx.os.revealPath(path)`, `ctx.os.notify` for native notifications |
| New chats | `host.newChat(profile)` opens a fresh chat, optionally in another profile |
| The UI kit | Import the app's own components (`Button`, `Input`, `Textarea`, `ScrollArea`, `EmptyState` and the rest) so the page is native by default |
| State in React | Subscribe with `useValue(atom)` only in the component that renders the value; read atoms with `.get()` in handlers |

### The file

*`~/.hermes/desktop-plugins/prompt-library/plugin.js`*

```javascript
// Prompt Library, a Hermes Desktop plugin. Folder name must equal the id.
// One ESM file, loaded uncompiled: no JSX syntax, only the three allowed imports.
import {
  host, haptic, useValue, Button, Input, Textarea, ScrollArea, EmptyState,
  ROUTES_AREA, SIDEBAR_NAV_AREA, PALETTE_AREA, KEYBINDS_AREA, STATUSBAR_AREAS
} from '@hermes/plugin-sdk'
import { useState } from 'react'
import { jsx, jsxs } from 'react/jsx-runtime'

const ROUTE = '/prompt-library'

// Storage lives under hermes.plugin.prompt-library.* and is namespaced by the host.
function loadPrompts(ctx) {
  return ctx.storage.get('prompts', [])
}
function savePrompts(ctx, prompts) {
  ctx.storage.set('prompts', prompts)
}

const STARTERS = [
  {
    id: 'change-a-setting',
    title: 'Change one setting safely',
    tags: 'config docs diff',
    body: 'Read the "<section>" section of https://hermes-agent.nousresearch.com/docs/user-guide/configuration and set <key> to <value> in my config.yaml. Show me the diff before you save it. After I say go, save it and run hermes config show to confirm.'
  },
  {
    id: 'write-a-skill',
    title: 'Turn what we just did into a skill',
    tags: 'skill procedure',
    body: 'Turn the workflow we just completed into a skill under ~/.hermes/skills/<category>/<name>/SKILL.md with a description under sixty characters phrased as the request it answers, then When to Use, Procedure, Pitfalls and Verification. Show me the file before creating it with skill_manage.'
  },
  {
    id: 'build-a-desktop-plugin',
    title: 'Build me a desktop plugin',
    tags: 'plugin desktop sdk',
    body: 'Load the bundled hermes-desktop-plugins skill and write a Hermes Desktop plugin at ~/.hermes/desktop-plugins/<id>/plugin.js that <does one thing>. Only import from @hermes/plugin-sdk, react and react/jsx-runtime, no JSX syntax, theme variables only, folder name equal to the id. Show me the file, then tell me the exact palette command to reload plugins and what I should see.'
  }
]

function PromptCard({ prompt, onCopy, onChat, onDelete }) {
  return jsxs('div', {
    className: 'flex flex-col gap-1 rounded border border-(--ui-stroke-secondary) p-2',
    children: [
      jsxs('div', { className: 'flex items-center justify-between gap-2', children: [
        jsx('div', { className: 'font-medium', children: prompt.title }),
        jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-quaternary)', children: prompt.tags || '' })
      ]}),
      jsx('div', { className: 'whitespace-pre-wrap text-(--ui-text-secondary)', children: prompt.body }),
      jsxs('div', { className: 'flex gap-2 pt-1', children: [
        jsx(Button, { size: 'sm', onClick: () => onCopy(prompt), children: 'Copy' }),
        jsx(Button, { size: 'sm', variant: 'outline', onClick: () => onChat(prompt), children: 'New chat' }),
        jsx(Button, { size: 'sm', variant: 'ghost', onClick: () => onDelete(prompt), children: 'Delete' })
      ]})
    ]
  })
}

function PromptLibraryPage({ ctx }) {
  const [prompts, setPrompts] = useState(() => {
    const stored = ctx.storage.get(KEY, null)
    if (stored === null) { savePrompts(ctx, STARTERS); return STARTERS }
    return stored
  })
  const [query, setQuery] = useState('')
  const [title, setTitle] = useState('')
  const [tags, setTags] = useState('')
  const [body, setBody] = useState('')
  const profile = useValue(host.state.profile)

  const persist = (next) => { setPrompts(next); savePrompts(ctx, next) }
  const q = query.trim().toLowerCase()
  const visible = prompts.filter(p => !q || (p.title + ' ' + p.tags + ' ' + p.body).toLowerCase().includes(q))

  const copy = async (p) => {
    const ok = await ctx.os.writeClipboard(p.body)
    haptic('tap')
    host.notify({ kind: ok ? 'info' : 'warning', message: ok ? 'Prompt copied. Paste it into any chat.' : 'Clipboard is not available here.' })
  }
  const chat = async (p) => {
    await ctx.os.writeClipboard(p.body)
    host.newChat(profile)
    host.notify({ kind: 'info', message: 'New chat opened in ' + profile + '. The prompt is on your clipboard: paste and send.' })
  }
  const remove = (p) => persist(prompts.filter(x => x.id !== p.id))
  const add = () => {
    if (!title.trim() || !body.trim()) {
      host.notify({ kind: 'warning', message: 'A prompt needs a title and a body.' })
      return
    }
    const id = title.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') + '-' + Date.now().toString(36)
    persist([{ id, title: title.trim(), tags: tags.trim(), body: body.trim() }, ...prompts])
    setTitle(''); setTags(''); setBody('')
  }

  return jsxs('div', {
    className: 'flex h-full flex-col gap-3 p-4 text-sm',
    children: [
      jsxs('div', { className: 'flex items-center justify-between', children: [
        jsx('div', { className: 'text-base font-medium', children: 'Prompt Library' }),
        jsx('div', { className: 'text-(--ui-text-tertiary)', children: String(prompts.length) + ' prompts, profile ' + profile })
      ]}),
      jsx(Input, { value: query, placeholder: 'Search title, tags, text', onChange: (e) => setQuery(e.target.value) }),
      jsxs('div', { className: 'grid gap-2 rounded border border-(--ui-stroke-secondary) p-2', children: [
        jsx(Input, { value: title, placeholder: 'Title', onChange: (e) => setTitle(e.target.value) }),
        jsx(Input, { value: tags, placeholder: 'tags, space separated', onChange: (e) => setTags(e.target.value) }),
        jsx(Textarea, { value: body, rows: 5, placeholder: 'The prompt, exactly as you would paste it', onChange: (e) => setBody(e.target.value) }),
        jsx('div', { children: jsx(Button, { size: 'sm', onClick: add, children: 'Save prompt' }) })
      ]}),
      jsx(ScrollArea, { className: 'min-h-0 flex-1', children:
        visible.length
          ? jsx('div', { className: 'flex flex-col gap-2 pr-2', children: visible.map(p => jsx(PromptCard, { key: p.id, prompt: p, onCopy: copy, onChat: chat, onDelete: remove })) })
          : jsx(EmptyState, { title: 'No prompts match', description: 'Clear the search or save a new prompt above.' })
      })
    ]
  })
}

function CountChip({ ctx }) {
  return jsx('button', {
    type: 'button',
    className: 'px-1.5 text-[0.6875rem] text-(--ui-text-tertiary)',
    onClick: () => host.navigate(ROUTE),
    children: 'prompts ' + String(loadPrompts(ctx).length)
  })
}

export default {
  id: 'prompt-library',
  name: 'Prompt Library',
  defaultEnabled: false,
  register(ctx) {
    ctx.registerMany([
      { id: 'page', area: ROUTES_AREA, data: { path: ROUTE }, render: () => jsx(PromptLibraryPage, { ctx }) },
      { id: 'nav', area: SIDEBAR_NAV_AREA, data: { path: ROUTE, label: 'Prompts', codicon: 'book' } },
      { id: 'chip', area: STATUSBAR_AREAS.right, order: 125, render: () => jsx(CountChip, { ctx }) },
      { id: 'open', area: PALETTE_AREA, data: { id: 'prompt-library.open', label: 'Open Prompt Library', keywords: ['prompt', 'library', 'template'], run: () => host.navigate(ROUTE) } },
      { id: 'keybind', area: KEYBINDS_AREA, data: { id: 'prompt-library.open', label: 'Open Prompt Library', category: 'Prompt Library', defaults: ['mod+shift+p'], run: () => host.navigate(ROUTE) } }
    ])
  }
}
```

> 📝 **Why copy and paste, not inject**
>
> The SDK gives a plugin a curated set of doors and a composer middleware for transforming a draft on its way out, but no documented call that writes text into the composer of an existing chat. So the library does the honest thing: it puts the prompt on your clipboard and, if you ask, opens a fresh chat in the current profile for you to paste into. One keystroke more, zero reliance on an undocumented method that a release could remove.

### Prompts

*`prompt-d6-seed-my-library.md`*

```markdown
Open the Prompt Library page in the app is my job; yours is the content.
Read every prompt I have pasted into you in the last two weeks
(session_search across my sessions for messages that start with "Read
https://hermes-agent.nousresearch.com/docs" or with "Build me"), pick the
eight I reuse most, and give each a title under six words and three tags.
Return them as a JSON array of {title, tags, body} so I can paste them into
the library one by one. Do not rewrite the bodies.
```

*`prompt-d6-extend-it.md`*

```markdown
Read the Prompt Library plugin at
~/.hermes/desktop-plugins/prompt-library/plugin.js and add one feature:
an "Export" button that writes all prompts as JSON to the clipboard, and an
"Import" textarea that merges a pasted JSON array into storage without
duplicating ids. Keep the format rules. Show me the diff before saving.
```

### Verify

- [ ] The sidebar shows Prompts; the page opens with the three starter prompts
- [ ] Saving a prompt survives an app restart (storage is persisted)
- [ ] Copy puts the body on the clipboard; New chat opens a chat in the current profile
- [ ] Cmd+Shift+P opens the page

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-DESKTOP.md)
