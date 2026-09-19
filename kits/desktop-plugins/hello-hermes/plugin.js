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
