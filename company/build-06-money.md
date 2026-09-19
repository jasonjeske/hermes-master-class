# Build 6: Money

![If the fleet costs more than it earns, you will know on Sunday](../assets/art/v4-money-loop.webp)

### What you are building

The books and the bill for the bots, in one loop: every dollar in and out goes through the ledger plugin from Volume 2, model spend comes from hermes insights per profile, and a Sunday routine puts both on one page with one recommended decision. The case file has the cheapest always-on setups on record and no cost figure for any multi-bot fleet. This build is how you become the first person who knows theirs.

### What the sources say

| Source | The number or the mechanism |
|---|---|
| HolmeBengt | Finance Review, Sunday at 18:00 and the 28th at 20:00: income, expenses, liquid assets, burn rate versus budget weekly; P&L, month-over-month variance, net worth trajectory and savings rate monthly. Total cost about USD 17 a month, agreed to in a comment rather than stated; DeepSeek's API "way cheaper than using an account" |
| witcheer | "I've been running a 24/7 AI agent on a Mac Mini for 2 months. 18 cron jobs, 35 scripts, 6 custom skills, a structured context system that makes every session smarter than the last. Total cost: $21/month." |
| SquishyData | Twenty signals on plain cron append to a ledger; one agentic job triages it. The cheap layer is deterministic, only the triage spends a model |
| Hermes Swarm | "track costs with daily budget caps" |
| stan_frbd | "For everyday usage, you don't need the biggest models. I use GPT-5.4-mini by default. I use GPT-5.5 for orchestrating multiple agents and for important tasks" |
| Wanderloots | "I can delegate specific tasks or bots to local models so that a more powerful cloud agent like the orchestrator can delegate to local models to do most of the work and still maintain the same level of quality but significantly reduce the cost." |
| Hermes docs | hermes insights --days N reports tokens, cost, tool patterns and activity per session source; hermes cron create --no-agent --script runs a deterministic watchdog with no model at all |

> 📝 **What the fleet costs is a routine, not a feeling**
>
> Nobody in the case file reports a multi-bot number because nobody made a bot report it. Volume 3 already gave ops a weekly-numbers routine over hermes insights. This build gives the team the Sunday page that joins that number to the ledger: ops gathers the figures with the shell and delivers them into atlas's Bot Chat, atlas writes the page and the decision it implies: a model down, a bot retired, a price up.

### Commands

*`c6-commands.sh`*

```bash
# The books: the ledger plugin from Volume 2, Build 8, enabled on the bots that record money.
hermes -p ops plugins enable ledger
hermes -p quill plugins enable ledger
# Record by voice or by chat; read back by month. --oneshot answers and exits; -q alone opens a session, and it never parses slash commands.
hermes -p ops chat --oneshot -q "Call ledger_add with amount 497.00, kind income, category client:acme, note September retainer, and confirm the id."
hermes -p ops chat --oneshot -q "Call ledger_report for this month and show me the table."
# The bill for the bots, per profile, last 7 days.
hermes insights --days 7
hermes -p forge insights --days 7
# A watchdog that costs nothing: a script under ~/.hermes/scripts/ that prints only when spend crosses a line.
hermes -p ops cron create "every day at 07:00" --no-agent --script spend-guard.sh --name "spend-guard"
```

### Prompts

*`prompt-c6-cost-per-bot.md`*

```markdown
You are @ops, because this needs the shell. Run hermes insights --days 30
for every profile in hermes profile list. Table: bot, model, sessions,
tokens, cost, cost per card completed (from hermes kanban stats). Then
three recommendations with the saving each: a bot that could drop one
model tier, a routine that could run --no-agent, a bot whose sessions are
mostly idle chatter. Change nothing; atlas decides.
```

*`prompt-c6-sunday-page.md`*

```markdown
You are @atlas. ops has posted this week's figures in your Bot Chat (or
I paste them here). Produce the Sunday page: money in and out this month
with the biggest three categories; fleet cost this week versus last;
cards shipped and blocked; the one number from COMPANY.md and its trend.
End with exactly one recommended decision and the number that would
change if I take it. One page. If nothing moved, say so in one line and
stop.
```

*`prompt-c6-spend-guard.md`*

```markdown
You are @ops. Write ~/.hermes/scripts/spend-guard.sh: a script with no
model call that reads the last 24 hours of cost from hermes insights
--days 1, compares it to a line in <company folder>/budget.txt, and
prints one line only when the cost is over the line, otherwise prints
nothing. Test it twice: once with the line above today's spend (silent)
and once below it (one line). Then show me the hermes cron create
--no-agent --script command and wait.
```

### Verify

- [ ] ledger_report for this month matches your bank to the dollar for the entries you recorded
- [ ] hermes insights gives you a number per bot, and the Sunday page shows it next to money in
- [ ] The spend guard printed nothing on a normal day and one line when you lowered the budget
- [ ] You made one decision from a Sunday page and wrote it into POLICIES.md or ORG.yaml

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-COMPANY.md)
