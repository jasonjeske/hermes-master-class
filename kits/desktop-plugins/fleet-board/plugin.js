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
