# Orientation

![Hermes Agent Masterclass](../assets/art/hero.webp)

This document is the whole of Tony Simons' twelve-part **Hermes Agent Master Class**, published on X between July 5 and July 20, 2026, combined into one offline reference and drilled deeper at every part.

Nothing from the original is dropped. Every mechanism the series names is here, every figure the author drew is here, and on top of that each part carries three additions that the serialized format could not give you:

- **A mechanism diagram.** The series describes the agent loop, the cron tick, the delegation tree and the profile boundary in prose. Here each one is also a real graph you can read in five seconds.
- **Reference tables.** Numbers scattered across a paragraph (iteration budgets, compression thresholds, curator timers, token costs) are pulled into tables you can look up later without rereading the prose.
- **An operator drill.** One concrete exercise per part. Reading about the agent loop teaches you nothing you can use on Tuesday. Running a command that proves the loop behaved the way the article said it would is what makes it yours.

> 📝 **Whose words are whose**
>
> The substance and the structure are Tony Simons' work, sourced from the articles linked in Appendix I. The original article artwork is not reproduced; every illustration and diagram here was produced for this compilation, as were the tables, the operator drills, the cross-references and the three configuration appendices. Where an addition makes a claim the series did not, it is marked as an addition rather than blended into the source material.

### How to read this

There are three honest ways through this document and they suit different weeks.

| Path | What you read | Time | Who it is for |
|---|---|---|---|
| Foundation | Parts 1, 2, 3, 5, and Appendix D | About 40 minutes | Anyone who wants the agent working correctly before adding anything |
| Operator | Foundation plus Parts 4, 6, 7, 12 and Appendix F | About 90 minutes | Someone running Hermes daily who wants it running without them |
| Full stack | All twelve parts plus every appendix | Half a day | Someone building multi-agent infrastructure on Hermes |
| Configure it | Appendices F, G and H on their own | About 25 minutes | Someone who wants the identity files, a first skill, and a prompt that produces a working system |

The parts genuinely build. Part 3 assumes Part 2's session persistence actually works. Part 6 assumes Part 4's skills exist. Part 10 assumes Part 11's profiles. Reading out of order is possible but each part will quietly reference a foundation you have not laid.

### The one sentence version

A chatbot predicts the next token. Hermes runs a process: it assembles a layered prompt, resolves a provider, calls the model, dispatches whatever tools the model asked for, feeds the results back, and repeats until the model produces text instead of another tool call. Then it saves the session, updates its memory, and is ready to resume later. Everything else in these twelve parts is a consequence of that loop existing.

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
