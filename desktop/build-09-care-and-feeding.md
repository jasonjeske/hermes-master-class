# Build 9: Care and Feeding

![Build 9](../assets/art/part-12.webp)

### What you are building

The maintenance you understand before you need it: how updates work across the app and its backends, what to do when permissions or credentials get asked for again, where every log lives, how to recover a stuck backend, and the three levels of uninstall.

### What the docs say

Checked against the Desktop page: Updating, Uninstalling, Troubleshooting, macOS permissions and local rebuilds.

| Fact | Detail |
|---|---|
| Updates | The app checks in the background and offers a one-click update. With several gateways registered, Update now updates the connected backend first, then every other eligible gateway, then the app itself last. After a backend update the app re-checks its own version |
| Rate limits on the check | Anonymous GitHub requests are capped per network address; the check uses `GITHUB_TOKEN`, then `GH_TOKEN`, then the GitHub CLI's login, then anonymous |
| Update logs | Detailed build output streams to the profile's `logs/update.log` |
| Permissions after updates | Grants follow the signing identity; `hermes desktop --setup-tcc-identity` anchors it, re-run after updates. A stuck grant: `tccutil reset All com.nousresearch.hermes`, re-grant, fully relaunch |
| Reconnect | If a chat stops responding while Connected, the status bar's gateway menu has Reconnect gateway, which redials without restarting the app |
| Backend crashed | The app restarts a local backend that exits and shows a notice; `~/.hermes/logs/desktop.log` records the exit code and the last output lines |
| Failed turns | The error card names the failing layer (provider, endpoint, streaming, auth, billing, gateway, runtime, disk) and offers Retry, Switch provider, Open logs, Send diagnostics (redacted, consented) and Copy error details |
| Resets | Force a clean first launch by removing `~/.hermes/hermes-agent/.hermes-bootstrap-complete`; rebuild a broken venv by removing `~/.hermes/hermes-agent/venv`; reset a stuck microphone prompt with `tccutil reset Microphone com.nousresearch.hermes` |
| SSH host key changed | The app fails closed; `ssh-keygen -R <host>` then Retry |
| Uninstall | Settings, About, Danger zone: app only (`hermes uninstall --gui`), app and agent keeping data (`hermes uninstall`), or everything (`hermes uninstall --full`) |

### Commands

*`care.sh`*

```bash
hermes update --check                       # preview
hermes backup --quick --label "pre-update"  # snapshot the home first
hermes update --backup                      # then update
hermes desktop --setup-tcc-identity         # re-anchor the signing identity after the update
hermes logs gui -f                          # the app's boot log
hermes doctor                               # health, including Full Disk Access
```

### Prompts

*`prompt-d9-before-i-update.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/user-guide/desktop section
"Updating" and https://hermes-agent.nousresearch.com/docs/getting-started/updating
then tell me, before I press Update:

1. What hermes update --check says is waiting.
2. Whether I have more than one gateway registered and therefore what will
   be updated in which order.
3. Take hermes backup --quick --label pre-update and show me the path.
4. Whether any local source edits exist in ~/.hermes/hermes-agent that an
   update would stash (git status there).

Then stop. I will press Update myself and ask you to verify afterwards.
```

*`prompt-d9-after-the-update.md`*

```markdown
The update finished. Verify it: hermes --version, hermes doctor, the last
thirty lines of ~/.hermes/logs/desktop.log summarized, hermes plugins list
compared with the list from before the update, and whether Full Disk
Access still reads as granted. If anything regressed, quote the exact line
and name the documented fix from the Desktop page's Troubleshooting
section. Do not apply a fix until I say so.
```

### Verify

- [ ] You know the path of a backup taken before your last update
- [ ] After an update the app reports its own version matches the backend, and no permission prompt reappears
- [ ] You can find desktop.log and update.log without searching
- [ ] You know which of the three uninstall levels you would pick, and that two of them keep your data

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-DESKTOP.md)
