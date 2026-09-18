# Build 4: Skills

![Build 4](../assets/art/part-04.webp)

### What you are building

Your first skills, written from work you already did once; a bundle for the combination you run every week; and a curator configured so the library stays clean without you.

### What the docs say

Checked against the Skills page, the Creating Skills guide, the Curator page, and the Skills Hub reference.

| Fact | Detail |
|---|---|
| Where | `~/.hermes/skills/<category>/<name>/SKILL.md`. Agent-created skills land there too unless `skills.create_dir` points elsewhere. `skills.external_dirs` adds shared directories. Project skills beat local skills beat external ones when names collide |
| Frontmatter | `name`, `description`, `version`, optional `platforms`, and a `metadata.hermes` block with `tags`, `category`, `requires_toolsets`, `fallback_for_toolsets`, and `config` entries the skill needs |
| Loading | Progressive disclosure: the index of names and descriptions loads at session start, a body loads only on a match. The description is therefore the whole trigger |
| Teaching | `/learn <url>`, `/learn <path to a repo, a PDF, a document>`, or `/learn <a description of what we just did>` creates a skill from that source |
| The tool | The agent writes and edits its own skills with `skill_manage`. `skills.write_approval: true` makes every such write ask you first |
| Bundles | `~/.hermes/skill-bundles/<slug>.yaml` with `name`, `description`, a required `skills` list, and an optional `instruction` prepended to all of them. `hermes bundles create <slug> --skill a --skill b -d "..."` writes one. `/<slug> <task>` loads every skill in it |
| The hub | `hermes skills browse`, `search`, `inspect`, `install`, and `tap add <org/repo>` for a private skill repository. Installs pass a security scan; inspect before you install anyway |
| The curator | A background pass over agent-created skills. Prune-only by default: idle skills go stale after 14 days and archive after 30. `curator.consolidate: true` opts into the LLM merge pass. `hermes curator pin <skill>` exempts one; snapshots are taken before every real pass and `hermes curator rollback` restores |

### Prompts

*`learn.sh`*

```bash
# Teach from a source. Each of these is a documented /learn form.
/learn https://docs.example.com/api/quickstart
/learn the REST client in ~/projects/acme-sdk, focus on auth and pagination
/learn how I just deployed the staging server
/learn ~/books/some-reference.pdf
```

*`prompt-04-skill-from-work.md`*

```markdown
We just finished a workflow I will need again. Turn it into a skill. Do
these in order.

1. Read https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills
   and confirm the frontmatter fields and the sections a skill should have.
2. Reconstruct what we actually did from this conversation: every tool
   call that mattered, every correction I made, every dead end.
3. Draft SKILL.md for ~/.hermes/skills/<category>/<name>/ with:
   - A description under sixty characters, phrased as the request it
     answers, using the verbs I would actually say.
   - When to Use, and when not to.
   - Procedure, numbered, with the exact commands.
   - Pitfalls, including every correction I made today.
   - Verification: what proves it worked, stated so you can check it
     without me.
   - metadata.hermes tags and category, and requires_toolsets if the
     procedure needs the terminal, browser, or web.
4. Show me the file. After I say go, create it with skill_manage.
5. Then start a new session and trigger it with a natural request that
   matches the description, without naming the skill. Tell me whether it
   loaded. If it did not, the description is a summary, not a trigger;
   rewrite it and try again.
```

*`prompt-04-audit-library.md`*

```markdown
Audit my skill library. Run hermes curator status and read the index of
skills you have available. For each agent-created skill give me: name,
description, when it last loaded, and one of keep, merge, or archive with
a reason. Propose the merges as concrete new descriptions. Then tell me
which skills you would pin so the curator never touches them. Do not
change anything; this is a report.
```

### A complete skill file

*`~/.hermes/skills/ops/release-check/SKILL.md`*

```markdown
---
name: release-check
description: Check a release is live, healthy, and serving the right version
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [release, verification, ops]
    category: ops
    requires_toolsets: [terminal, web]
---

## When to Use
When I ask whether a release, deploy, or rollout is live, healthy, or
serving the right version. Not for deploying; that is a different skill.

## Procedure
1. Ask which environment if I did not say. Never assume production.
2. Fetch the health endpoint with a cache-busting query string and record
   the status code.
3. Fetch the version endpoint and compare it to the version I named.
4. Tail the error log for the last sixty seconds and count new entries.
5. Report all three results on three lines, then a one-word verdict.

## Pitfalls
- The deploy API returns 202 before the release is live. A 202 is not live.
- A CDN can serve a healthy cached page while the origin is down. The
  cache-busting parameter in step 2 is not optional.
- Two of three checks passing is a failed check. Say so.

## Verification
- Health returned 200 with the cache-busting parameter.
- The served version string matches the version I named.
- Zero new error-log entries in the window.
```

### A bundle for the weekly combination

*`bundle.sh`*

```bash
hermes bundles create ship-it \
  --skill github-code-review \
  --skill test-driven-development \
  --skill release-check \
  -d "Review, test, and verify a release end to end"

/ship-it verify the 2.4.1 release on staging
```

*`~/.hermes/skill-bundles/ship-it.yaml`*

```yaml
name: ship-it
description: Review, test, and verify a release end to end
skills:
  - github-code-review
  - test-driven-development
  - release-check
instruction: |
  Run the review first. Do not start the release check until the tests
  pass. Report each skill's verdict on its own line.
```

### The curator, configured

*`~/.hermes/config.yaml`*

```yaml
curator:
  enabled: true
  interval_hours: 168          # weekly
  stale_after_days: 14
  archive_after_days: 30
  consolidate: false           # prune only; opt in to the LLM merge pass later
  prune_builtins: true
```

*`curator.sh`*

```bash
hermes curator status              # last run, counts, pinned list
hermes curator run --dry-run       # what it would do, no mutations
hermes curator pin release-check   # never auto-transition this one
hermes curator rollback --list     # every snapshot, with reason and size
```

### Verify

- [ ] A natural request that matches the description loads the skill in a fresh session
- [ ] /ship-it <task> loads all three skills (the agent names them in its first reply)
- [ ] hermes curator status lists the skill you pinned
- [ ] hermes prompt-size shows the skills index grew by roughly one line per skill, not by the bodies

---

[← Back to the index](../README.md) · [Whole masterclass in one file](FULL-MASTERCLASS.md)
