# Build 9: Delegation and Kanban

![Build 9](../assets/art/part-10.webp)

### What you are building

Delegation that hands well-specified work to a cheap child fleet without leaking your context window, and a kanban board that lets the profiles from Build 7 work a queue without you relaying between them.

### What the docs say

Checked against the Delegation page and the Kanban page.

| Fact | Detail |
|---|---|
| The tool | `delegate_task(goal=..., context=...)` for one child; `delegate_task(tasks=[{goal, context}, ...])` for a parallel batch, ten at a time by default via `delegation.max_concurrent_children` |
| The child knows nothing | No chat history, no memory of the parent's turn. Everything the child needs goes in `goal` and `context`. Its toolsets are the intersection with the parent's, never wider |
| One model for the fleet | `delegation.model` and `delegation.provider` in config.yaml route every child to one inexpensive model. There is no per-task model on the tool, so quality-sensitive work stays with the parent |
| Depth | `delegation.max_spawn_depth` defaults to 1: children cannot spawn children unless you raise it. Every level multiplies spend |
| The board | `hermes kanban init` creates `~/.hermes/kanban.db`. You drive it with `hermes kanban ...`, `/kanban ...`, or the dashboard tab from the bundled plugin. Workers drive it with the `kanban_*` tools, never by shelling out |
| Cards | `hermes kanban create "<title>" --assignee <profile> --workspace dir:<path> --priority N [--model <m> --provider <p>] [--skill <name>]`. `--triage` parks it for decomposition |
| Decomposition | Triage cards are fanned out by the decomposer, automatically when `kanban.auto_decompose` is true, or by `hermes kanban decompose <id>` in manual mode. It routes children to profiles by their descriptions from Build 7 |
| Decide before you fan out | Workers cannot see sibling cards. Any decision two cards would both have to make, a schema, a name, a format, the planner makes once and stamps into both bodies |
| Health | `hermes kanban dispatch --dry-run` says why a ready card is or is not spawning; `hermes kanban diagnostics` is the board snapshot |

### Delegation

*`~/.hermes/config.yaml`*

```yaml
model:
  default: "your-frontier-model"       # the parent plans on this
delegation:
  model: "your-inexpensive-model"      # every delegate_task child runs on this
  provider: "openrouter"               # optional, if the child model lives elsewhere
```

*`prompt-09-delegate.md`*

```markdown
Read the sections on the child's context, toolsets, and the delegation
model at
https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation
Then set delegation.model to the cheapest capable model I have configured
and show me the diff before saving.

After I say go, delegate this in parallel, one child per item, and write
each child's brief so a stranger could do it: the goal in one sentence,
every fact and path it needs in the context, and the exact output shape
you want back.

<the three or four independent items>

When the children return, do not paste their raw output. Give me one
merged result and tell me which child's answer you trusted least and why.
```

### Kanban

*`kanban.sh`*

```bash
hermes kanban init
hermes dashboard                      # the Kanban tab appears after Skills

hermes kanban create "Add rate limiting to the public API" \
  --assignee coder \
  --workspace dir:/absolute/path/to/your/repo \
  --priority 2

hermes kanban create "Research how three competitors price their API tiers" \
  --assignee researcher \
  --priority 3

hermes kanban create "Ship the Q4 pricing page" --triage     # let the decomposer fan it out
hermes kanban decompose <id>                                 # in manual mode

hermes kanban list
hermes kanban dispatch --dry-run
hermes kanban diagnostics
```

*`prompt-09-board.md`*

```markdown
Set up my kanban board and put the first real work on it. Do these in
order.

1. Read https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
   sections on the two surfaces, auto versus manual orchestration, and
   the cost strategy. Tell me in five lines how a card reaches a worker
   and what the worker uses to report back.
2. Run hermes profile list and confirm the workers and their descriptions
   from Build 7 exist. If a description is vague, propose a better one.
3. Here is the goal: <one project-sized goal>. Break it into cards. For
   every decision two cards would both have to make, make it once and
   put it in both bodies. Each card body carries: goal, context, files it
   may touch, definition of done.
4. Show me the cards as hermes kanban create commands with assignee,
   workspace, and priority. Do not create them until I say go.
5. After go: create them, run hermes kanban dispatch --dry-run, and tell
   me what would spawn and what is guarded and why.
```

> ⚠️ **Restrict the planner**
>
> The docs recommend pairing the orchestrator profile with toolsets restricted to board operations, so it cannot execute implementation work even if it tries. `hermes tools` in that profile is where you take the terminal away from it.

### Verify

- [ ] hermes config show reports delegation.model as the inexpensive model
- [ ] A parallel delegate_task returns one merged answer, and the children ran on the cheap model (hermes insights)
- [ ] hermes kanban list shows the cards with the right assignees
- [ ] The dashboard Kanban tab renders the board and a card's drawer shows its body

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
