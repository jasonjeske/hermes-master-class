# forge, the Engineer

Implements well-specified changes in a repository, runs the tests, reports what changed and what was verified.

## Files

- `SOUL.md`: the role, how it works, its voice, and what it never does.
- `config.yaml`: the model pin and effort. Toolsets to enable when creating the bot: terminal, file, code_execution, memory.
- `distribution.yaml`: makes this folder installable with `hermes profile install <path-or-repo> --alias`.
- `routines.sh`: the routines this bot runs, as `hermes -p forge cron create` commands; run the file once with `sh` from a clone of the kit. It lives outside `cron/`, which Hermes owns for job state.

## Install this bot alone

```bash
hermes profile install ./forge --alias          # from a clone of the kit
# then in Hermes Desktop: Bots, the new row appears; right-click, Edit Profile, tick the toolsets above
```

## Or create it by hand (the CLI twin of the New Agent dialog)

```bash
hermes profile create forge --description "Implements well-specified changes in a repository, runs the tests, reports what changed and what was verified."
cp ./forge/SOUL.md ~/.hermes/profiles/forge/SOUL.md
hermes -p forge config set model.default "your-inexpensive-coding-model"
```
