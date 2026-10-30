# Attribution

## The source material

The substance and the structure of the twelve parts are the work of **Tony
Simons**, published as the twelve-part *Hermes Agent Master Class* on X between
July 5 and July 20, 2026.

**The original article artwork is deliberately not reproduced here.** Every
plate and every illustration in this repository was produced for this
compilation. To see the author's own figures, read the source articles.

- Author: [@tonysimons_](https://x.com/tonysimons_)
- Series index: https://x.com/tonysimons_/status/2079066422211117218
- Every individual part is linked in [Appendix I](masterclass/appendix-i-sources.md)

If you find this material useful, read the originals and follow the author.
He published the whole series free, with no paywall and no email wall.

## The documentation behind the Build Track

The Build Track was written from the official Hermes Agent documentation at
hermes-agent.nousresearch.com and from two bundled files in the Hermes Agent
repository (the default SOUL.md and the Obsidian skill). Every build names the
pages it was checked against, and Appendix I lists all of them. Hermes Agent
is published by Nous Research under the MIT License.

Community material that shaped the prompt pattern is credited in Appendix I:
the Hermes Wingtips tip series by @witcheer on X, the command cheat sheet by
Hermes Release Watch (@HermesWatcher) on X, Tonbi's AI Garage eleven-video
Hermes Agent Masterclass on YouTube, and the user stories page on the official
Hermes site.

## Volumes 2, 3 and 4

The Desktop, Bots and Company volumes were written from the official Hermes
Agent documentation (the Desktop, Desktop Plugin SDK, Plugins, Bot Mode,
Profiles, Profile Distributions, Multi-connection, Memory Providers, Kanban and
Cron pages, at the version installed while writing) and from the bundled
example plugins in the Hermes Agent repository. Two memory providers are
described from their own READMEs: Hindsight by Vectorize, and Mnemosyne by
mnemosyne-oss (MIT).

Two operators published field experience detailed enough to learn from, and
they are quoted by name wherever their experience adds something the docs do
not:

- **Tonbi's AI Garage** on YouTube: the eleven-video Hermes Agent Masterclass,
  the Bot Mode racing-game run, and the brainstorming skill his agent wrote
- **Wanderloots** (Callum) on YouTube: the Bot Mode best-practices and team
  upgrade videos, and the two agentic-memory videos on Mnemosyne and Hindsight

Volume 4 is grounded in the official Hermes user stories corpus (326 stories
shipped with the documentation site) and in the operators' own posts on
Reddit, X, GitHub and blogs. Every quotation names its author by handle and
links the source; where a post has since been removed, the text says so and
quotes only the Hermes team's curated excerpt. The operators quoted include
HolmeBengt, SquishyData, stan_frbd, kenmazaika, riceinmybelly, Godzillaton,
the RUDR9 and Jinn authors, the Hermes Swarm author, Gumroad's @scotty529,
@mvanhorn, @IBuzovskyi, @witcheer, @cyrilXBT, @shannholmberg, @code_rams,
@ogiberstein, @aakashgupta and Metics Media. None of them reviewed or endorsed
this volume; their words are quoted, their conclusions are theirs, and the
volume's own design decisions are the compilation's.

## The bonus class

The bonus class, Hermes Power User, was written from the installed source of
Hermes Agent v0.22.5: the slash command registry every surface reads, the
TUI's own command files, and the handlers behind the commands whose help line
leaves something out. The official Slash Commands reference was read alongside
it, and every place the two disagree is listed in the class. No third-party
cheat sheet was used. The ranking is the compilation's own judgment.

## Volume 6

The Tuning Masterclass was measured in a sealed, throwaway install of Hermes
Agent v0.22.5 (commit bf0203a) with Hermes's own context breakdown, and every
key, command and default it teaches was checked against that version's source
and the official documentation. The GitHub issues and release notes of
NousResearch/hermes-agent supplied the history it cites: how the fixed budget
grew and shrank between releases, and which changes moved it.

Every community technique the volume adopts was checked against the v0.22.5
source first, and each is credited by author and link on its community page,
[The Community, Credited](tune/99-the-community-credited.md), and most of them
also where the volume uses them:

- **witcheer**, through the Hermes Wingtips on X and the Hermes Autopilot prompts:
  - [the audit prompt shape](https://notwitcheer.github.io/hermes-recipes/prompts/):
    read first, propose, and change nothing without a yes
  - [the setup audit](https://notwitcheer.github.io/hermes-recipes/prompts/03-audit-my-setup/)
    that proposes a few one line changes, also
    [posted on X](https://x.com/witcheer/status/2098769643599020208)
  - measuring the fixed budget offline with `hermes prompt-size`, before and after
    a change, at no token cost
    ([Wingtip #31](https://x.com/witcheer/status/2081381590488568218))
  - reading the live window with `/context` and `/context all`
    ([Wingtip #88](https://x.com/witcheer/status/2105552884670550343))
  - reading spend by model, tool and platform from `hermes insights`
    ([Wingtip #32](https://x.com/witcheer/status/2081822725325435386))
  - a smaller toolset for each platform
    ([Wingtip #48](https://x.com/witcheer/status/2089706892993941840),
    [Wingtip #79](https://x.com/witcheer/status/2101910495888392672))
  - skill descriptions of 60 characters or less
    ([Wingtip #5](https://x.com/witcheer/status/2069828190197973337))
  - the project rule file order
    ([Wingtip #4](https://x.com/witcheer/status/2069385776756895880))
  - a personal AGENTS.override.md per folder
    ([Wingtip #64](https://x.com/witcheer/status/2096481734388858931))
  - memory as a snapshot per session
    ([Wingtip #3](https://x.com/witcheer/status/2069020659829608570),
    [Wingtip #19](https://x.com/witcheer/status/2076670836891689174)), also
    reported by Vectorize
  - one model for the whole session
    ([Wingtip #14](https://x.com/witcheer/status/2074153526222114974)), also
    noted by Matheus Battisti
  - compaction summaries on a cheaper model
    ([Wingtip #42](https://x.com/witcheer/status/2086745372521591061))
  - lower reasoning effort for side tasks
    ([Wingtip #75](https://x.com/witcheer/status/2100460797239415168))
  - a cheaper model for scheduled jobs
    ([Wingtip #62](https://x.com/witcheer/status/2095722000907923465))
  - the loop guardrails and the approval denial breaker
    ([Wingtip #69](https://x.com/witcheer/status/2098290534758408306),
    [Wingtip #83](https://x.com/witcheer/status/2103395194963980527))
  - pruning old sessions by hand, a dry run first
    ([Wingtip #66](https://x.com/witcheer/status/2097201422844436642))
  - script-only cron jobs that never call a model
    ([witcheer's Almanac](https://x.com/witcheer/status/2108903932797796580)),
    reporting an r/hermesagent poster
  - checking what an update would do before taking it
    ([witcheer's Almanac](https://x.com/witcheer/status/2108564754893582428))
- **Matheus Battisti**: [reading the cost of each task from `hermes insights`](https://horadecodar.com.br/hermes-agent-custo-tarefa/)
- **Khuyen Tran** (CodeCut): [previewing a curator run before it changes anything](https://codecut.ai/hermes-autonomous-skills-curator/)
- **Shabnam Katoch** (BetterClaw): [pruning old sessions with a dry run first](https://www.betterclaw.io/blog/hermes-agent-bugs-fixes),
  and checking an update before taking it
- **Ryan Underdown**: [measuring the skills index](https://bobatron.com/blog/hermes-system-prompt)
  as a share of the stable prompt
- **Mervin Praison**: [memory kept to durable facts](https://mer.vin/2026/05/soul-md-for-ai-agents-30-80-line-identity-blueprint-before-memory-or-tools/),
  with procedures left to skills
- **Azamat Safarov**: [every side task pinned to a model](https://dev.to/azamat_safarov/hermes-agent-burned-603m-tokens-behind-my-back-i-cut-background-costs-by-up-to-125x-43oi)
- **Tonbi's AI Garage** on YouTube: [the compression summarizer set under the auxiliary block](https://www.youtube.com/watch?v=NoF-YajElIM),
  with a written recap by
  [Jan Peter Alexander](https://ai-suka.pages.dev/2026/04/44-hermes-agent-auxiliary-model-routing-token-costs/)
- **Vincent Forat** (Preuve AI): [a cheaper model for scheduled jobs](https://preuve.ai/blog/hermes-agent-review),
  summarizing r/hermesagent

None of them reviewed or endorsed this volume. No community figure is quoted:
the volume's measurements are its own, and advice that no longer holds on
v0.22.5 is described without naming who gave it. The prices on the community
page are each seller's own, read from the seller's page.

## What this compilation added

Everything below was written while assembling this reference and is not part of
the original series:

- The whole Build Track: an introduction, ten builds, and a ledger, with every
  prompt, template, config block and table in them
- Twenty-six diagram plates, all produced for this compilation
- Fourteen illustrations, a hero, one per part, and the Build Track plate
- Forty original images in total, none taken from the source articles
- The consolidated constants table (Appendix C) and failure-triage table (Appendix D)
- The front-loaded vocabulary table
- Twelve operator drills, one per part
- The cross-references between parts
- The 30/60/90 adoption path (Appendix E)
- The configuration and prompt guidance in Appendices F, G and H, including the
  SOUL.md and USER.md examples and both worked build prompts
- Volumes 2, 3 and 4 in full: thirty builds, three ledgers, sixteen further
  plates and three further illustrations, and every prompt in them
- Volume 5 in full: two tips, the ledger, two further plates and one further
  illustration, and every prompt and command in them
- The bonus class in full: the ranking of all 119 slash commands in twelve
  tiers, the keys, shortcuts and docs-versus-code tables, the ledger, one
  further illustration, and every prompt in it
- Volume 6 in full: nine stages, three closing pages, four charts rendered from measured results, the hermes-tune skill with its five profile files, and every prompt in them
- The kits: three desktop plugins, the unified ledger plugin, six bot
  profiles with SOULs, configs, distributions and routines, the memory kit,
  and the company files (charter, org, policies, protocol, production line
  and client templates, life and cadence routines)

Nothing was invented about how Hermes Agent behaves. Where a number, threshold,
command, key or file path appears, it came from the source series, from the
official documentation named in Appendix I and in each build, or from a named
operator's own published words. The bonus class and Volume 6 also rest on
the Hermes Agent source code at the version they name, and every token count
in Volume 6 was measured with Hermes's own counters in a sealed, throwaway
install.

## The software

Hermes Agent is a project of [Nous Research](https://hermes-agent.nousresearch.com/).
This repository is an unofficial study reference and is not affiliated with,
endorsed by, or maintained by Nous Research or the author of the series.
For anything authoritative, use the
[official documentation](https://hermes-agent.nousresearch.com/docs/getting-started/installation).

## Licensing

This compilation's own contributions are CC BY 4.0, and the code under
`kits/`, `skills/` and `tools/` is MIT. The underlying source material of Volume 1 is not
relicensed here and remains the author's. See [LICENSE](LICENSE) for the exact
split.
