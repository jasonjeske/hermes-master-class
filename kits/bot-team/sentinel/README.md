# sentinel, the Reviewer

Reviews code, copy, plans and numbers against their definition of done; approves, requests changes, or blocks.

## Files

- `SOUL.md`: the role, how it works, its voice, and what it never does.
- `config.yaml`: the model pin and effort. Toolsets to enable when creating the bot: terminal, file, web, memory.
- `distribution.yaml`: makes this folder installable with `hermes profile install <path-or-repo> --alias`.
- `routines.sh`: the routines this bot runs, as `hermes -p sentinel cron create` commands; run the file once with `sh` from a clone of the kit. It lives outside `cron/`, which Hermes owns for job state.

## Install this bot alone

```bash
hermes profile install ./sentinel --alias          # from a clone of the kit
# then in Hermes Desktop: Bots, the new row appears; right-click, Edit Profile, tick the toolsets above
```

## Or create it by hand (the CLI twin of the New Agent dialog)

```bash
hermes profile create sentinel --description "Reviews code, copy, plans and numbers against their definition of done; approves, requests changes, or blocks."
cp ./sentinel/SOUL.md ~/.hermes/profiles/sentinel/SOUL.md
hermes -p sentinel config set model.default "your-frontier-model"
```
