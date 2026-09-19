# ops, the Operator

Runs the routines: briefs, sweeps, health checks, backups, weekly numbers. Silent when nothing needs a human.

## Files

- `SOUL.md`: the role, how it works, its voice, and what it never does.
- `config.yaml`: the model pin and effort. Toolsets to enable when creating the bot: terminal, file, memory, session_search, cronjob.
- `distribution.yaml`: makes this folder installable with `hermes profile install <path-or-repo> --alias`.
- `routines.sh`: the routines this bot runs, as `hermes -p ops cron create` commands; run the file once with `sh` from a clone of the kit. It lives outside `cron/`, which Hermes owns for job state.

## Install this bot alone

```bash
hermes profile install ./ops --alias          # from a clone of the kit
# then in Hermes Desktop: Bots, the new row appears; right-click, Edit Profile, tick the toolsets above
```

## Or create it by hand (the CLI twin of the New Agent dialog)

```bash
hermes profile create ops --description "Runs the routines: briefs, sweeps, health checks, backups, weekly numbers. Silent when nothing needs a human."
cp ./ops/SOUL.md ~/.hermes/profiles/ops/SOUL.md
hermes -p ops config set model.default "your-inexpensive-model"
```
