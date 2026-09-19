// Desktop half of the ledger plugin: a page that reads /api/plugins/ledger/ through ctx.rest.
// Loaded uncompiled: no JSX syntax, only the three allowed imports, theme variables only.
import {
  host, useQuery, useQueryClient, Button, Input, ScrollArea, EmptyState,
  ROUTES_AREA, SIDEBAR_NAV_AREA, PALETTE_AREA
} from '@hermes/plugin-sdk'
import { useState } from 'react'
import { jsx, jsxs } from 'react/jsx-runtime'

const ID = 'ledger'
const ROUTE = '/ledger'

function thisMonth() {
  const d = new Date()
  return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0')
}

function money(n) {
  return (Math.round(Number(n) * 100) / 100).toFixed(2)
}

function Bar({ label, value, max, count }) {
  const pct = max > 0 ? Math.max(2, Math.round((value / max) * 100)) : 0
  return jsxs('div', { className: 'flex flex-col gap-0.5', children: [
    jsxs('div', { className: 'flex justify-between text-[0.75rem]', children: [
      jsx('span', { children: label + (count ? '  (' + count + ')' : '') }),
      jsx('span', { className: 'text-(--ui-text-tertiary)', children: money(value) })
    ]}),
    jsx('div', { className: 'h-1.5 w-full rounded bg-(--ui-stroke-secondary)', children:
      jsx('div', { className: 'h-1.5 rounded bg-(--ui-accent)', style: { width: pct + '%' } })
    })
  ]})
}

function LedgerPage({ ctx }) {
  const qc = useQueryClient()
  const [month, setMonth] = useState(thisMonth())
  const [amount, setAmount] = useState('')
  const [kind, setKind] = useState('expense')
  const [category, setCategory] = useState('')
  const [note, setNote] = useState('')
  const { data, isLoading, error } = useQuery({
    queryKey: [ID, 'summary', month],
    queryFn: () => ctx.rest('/summary?month=' + encodeURIComponent(month)),
    refetchInterval: 20000
  })
  const invalidate = () => qc.invalidateQueries({ queryKey: [ID, 'summary'] })

  const add = async () => {
    try {
      await ctx.rest('/entries', { method: 'POST', body: { amount: Number(amount), kind, category, note } })
      setAmount(''); setCategory(''); setNote('')
      invalidate()
      host.notify({ kind: 'info', message: 'Entry saved.' })
    } catch (e) {
      host.notifyError(e, 'Could not save the entry. Is the ledger plugin enabled in plugins.enabled?')
    }
  }
  const remove = async (id) => {
    try { await ctx.rest('/entries/' + id, { method: 'DELETE' }); invalidate() } catch (e) { host.notifyError(e, 'Could not delete.') }
  }

  const cats = (data && data.by_category) || []
  const max = cats.reduce((m, c) => Math.max(m, c.total), 0)

  return jsxs('div', { className: 'flex h-full flex-col gap-3 p-4 text-sm', children: [
    jsxs('div', { className: 'flex items-center justify-between', children: [
      jsx('div', { className: 'text-base font-medium', children: 'Ledger' }),
      jsx(Input, { value: month, className: 'w-28', onChange: (e) => setMonth(e.target.value), placeholder: 'YYYY-MM' })
    ]}),
    error ? jsx('div', { className: 'text-(--ui-text-tertiary)', children: 'Backend not reachable: ' + String(error.message || error) + '. Enable the ledger plugin and restart the gateway.' }) : null,
    data ? jsxs('div', { className: 'grid grid-cols-3 gap-2', children: [
      jsxs('div', { className: 'rounded border border-(--ui-stroke-secondary) p-2', children: [ jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-tertiary)', children: 'Income' }), jsx('div', { className: 'font-medium', children: money(data.income) }) ]}),
      jsxs('div', { className: 'rounded border border-(--ui-stroke-secondary) p-2', children: [ jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-tertiary)', children: 'Expenses' }), jsx('div', { className: 'font-medium', children: money(data.expenses) }) ]}),
      jsxs('div', { className: 'rounded border border-(--ui-stroke-secondary) p-2', children: [ jsx('div', { className: 'text-[0.6875rem] text-(--ui-text-tertiary)', children: 'Net' }), jsx('div', { className: 'font-medium', children: money(data.net) }) ]})
    ]}) : (isLoading ? jsx('div', { className: 'text-(--ui-text-tertiary)', children: 'Loading' }) : null),
    jsxs('div', { className: 'grid gap-2 rounded border border-(--ui-stroke-secondary) p-2', children: [
      jsxs('div', { className: 'grid grid-cols-4 gap-2', children: [
        jsx(Input, { value: amount, placeholder: 'Amount', onChange: (e) => setAmount(e.target.value) }),
        jsx('select', { value: kind, className: 'rounded border border-(--ui-stroke-secondary) bg-transparent px-2', onChange: (e) => setKind(e.target.value), children: [
          jsx('option', { value: 'expense', children: 'expense' }),
          jsx('option', { value: 'income', children: 'income' })
        ]}),
        jsx(Input, { value: category, placeholder: 'Category', onChange: (e) => setCategory(e.target.value) }),
        jsx(Input, { value: note, placeholder: 'Note', onChange: (e) => setNote(e.target.value) })
      ]}),
      jsx('div', { children: jsx(Button, { size: 'sm', onClick: add, children: 'Add entry' }) })
    ]}),
    jsx(ScrollArea, { className: 'min-h-0 flex-1', children: jsxs('div', { className: 'flex flex-col gap-3 pr-2', children: [
      cats.length ? jsx('div', { className: 'flex flex-col gap-2', children: cats.map(c => jsx(Bar, { key: c.category, label: c.category, value: c.total, max, count: c.count })) })
                  : (data ? jsx(EmptyState, { title: 'No expenses this month', description: 'Add one above, or tell Hermes what you spent.' }) : null),
      data && data.recent && data.recent.length ? jsx('div', { className: 'flex flex-col gap-1', children: data.recent.map(r => jsxs('div', { key: r.id, className: 'flex items-center justify-between gap-2 text-[0.75rem]', children: [
        jsx('span', { className: 'text-(--ui-text-tertiary)', children: r.date }),
        jsx('span', { className: 'flex-1', children: r.category + (r.note ? ', ' + r.note : '') }),
        jsx('span', { className: r.kind === 'income' ? '' : 'text-(--ui-text-secondary)', children: (r.kind === 'income' ? '+' : '-') + money(r.amount) }),
        jsx(Button, { size: 'sm', variant: 'ghost', onClick: () => remove(r.id), children: 'x' })
      ]})) }) : null
    ]}) })
  ]})
}

export default {
  id: 'ledger',
  name: 'Ledger',
  defaultEnabled: false,
  register(ctx) {
    ctx.registerMany([
      { id: 'page', area: ROUTES_AREA, data: { path: ROUTE }, render: () => jsx(LedgerPage, { ctx }) },
      { id: 'nav', area: SIDEBAR_NAV_AREA, data: { path: ROUTE, label: 'Ledger', codicon: 'graph' } },
      { id: 'open', area: PALETTE_AREA, data: { id: 'ledger.open', label: 'Open Ledger', keywords: ['ledger', 'money', 'budget'], run: () => host.navigate(ROUTE) } }
    ])
  }
}
