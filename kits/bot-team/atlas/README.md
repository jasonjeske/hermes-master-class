# atlas, the Chief of staff

Plans work, decides shared choices once, routes cards and messages to the right teammate, escalates real decisions to the human. Never implements.

## Files

- `SOUL.md`: the role, how it works, its voice, and what it never does.
- `config.yaml`: the model pin and effort. Toolsets to enable when creating the bot: kanban, memory, file, session_search (no terminal, no code execution).
- `distribution.yaml`: makes this folder installable with `hermes profile install <path-or-repo> --alias`.
- `routines.sh`: the routines this bot runs, as `hermes -p atlas cron create` commands; run the file once with `sh` from a clone of the kit. It lives outside `cron/`, which Hermes owns for job state.

## Install this bot alone

```bash
hermes profile install ./atlas --alias          # from a clone of the kit
# then in Hermes Desktop: Bots, the new row appears; right-click, Edit Profile, tick the toolsets above
```

## Or create it by hand (the CLI twin of the New Agent dialog)

```bash
hermes profile create atlas --description "Plans work, decides shared choices once, routes cards and messages to the right teammate, escalates real decisions to the human. Never implements."
cp ./atlas/SOUL.md ~/.hermes/profiles/atlas/SOUL.md
hermes -p atlas config set model.default "your-frontier-model"
```
