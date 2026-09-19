# quill, the Writer

Turns findings and decisions into briefs, posts, docs and messages for a named reader.

## Files

- `SOUL.md`: the role, how it works, its voice, and what it never does.
- `config.yaml`: the model pin and effort. Toolsets to enable when creating the bot: file, memory, skills.
- `distribution.yaml`: makes this folder installable with `hermes profile install <path-or-repo> --alias`.
- `routines.sh`: the routines this bot runs, as `hermes -p quill cron create` commands; run the file once with `sh` from a clone of the kit. It lives outside `cron/`, which Hermes owns for job state.

## Install this bot alone

```bash
hermes profile install ./quill --alias          # from a clone of the kit
# then in Hermes Desktop: Bots, the new row appears; right-click, Edit Profile, tick the toolsets above
```

## Or create it by hand (the CLI twin of the New Agent dialog)

```bash
hermes profile create quill --description "Turns findings and decisions into briefs, posts, docs and messages for a named reader."
cp ./quill/SOUL.md ~/.hermes/profiles/quill/SOUL.md
hermes -p quill config set model.default "your-mid-model"
```
