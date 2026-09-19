# scout, the Researcher

Reads source code and external docs, verifies claims against three sources, returns cited findings.

## Files

- `SOUL.md`: the role, how it works, its voice, and what it never does.
- `config.yaml`: the model pin and effort. Toolsets to enable when creating the bot: web, browser, file, memory.
- `distribution.yaml`: makes this folder installable with `hermes profile install <path-or-repo> --alias`.
- `routines.sh`: the routines this bot runs, as `hermes -p scout cron create` commands; run the file once with `sh` from a clone of the kit. It lives outside `cron/`, which Hermes owns for job state.

## Install this bot alone

```bash
hermes profile install ./scout --alias          # from a clone of the kit
# then in Hermes Desktop: Bots, the new row appears; right-click, Edit Profile, tick the toolsets above
```

## Or create it by hand (the CLI twin of the New Agent dialog)

```bash
hermes profile create scout --description "Reads source code and external docs, verifies claims against three sources, returns cited findings."
cp ./scout/SOUL.md ~/.hermes/profiles/scout/SOUL.md
hermes -p scout config set model.default "your-mid-model"
```
