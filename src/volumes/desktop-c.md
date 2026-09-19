## Build 9: Care and Feeding

![Build 9](assets/art/part-12.webp)

### What you are building

The maintenance you understand before you need it: how updates work across the app and its backends, what to do when permissions or credentials get asked for again, where every log lives, how to recover a stuck backend, and the three levels of uninstall.

### What the docs say

Checked against the Desktop page: Updating, Uninstalling, Troubleshooting, macOS permissions and local rebuilds.

```table
| Fact | Detail |
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
```

### Commands

```code lang=bash file=care.sh
hermes update --check                       # preview
hermes backup --quick --label "pre-update"  # snapshot the home first
hermes update --backup                      # then update
hermes desktop --setup-tcc-identity         # re-anchor the signing identity after the update
hermes logs gui -f                          # the app's boot log
hermes doctor                               # health, including Full Disk Access
```

### Prompts

```code lang=markdown file=prompt-d9-before-i-update.md
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

```code lang=markdown file=prompt-d9-after-the-update.md
The update finished. Verify it: hermes --version, hermes doctor, the last
thirty lines of ~/.hermes/logs/desktop.log summarized, hermes plugins list
compared with the list from before the update, and whether Full Disk
Access still reads as granted. If anything regressed, quote the exact line
and name the documented fix from the Desktop page's Troubleshooting
section. Do not apply a fix until I say so.
```

### Verify

```checklist
[ ] You know the path of a backup taken before your last update
[ ] After an update the app reports its own version matches the backend, and no permission prompt reappears
[ ] You can find desktop.log and update.log without searching
[ ] You know which of the three uninstall levels you would pick, and that two of them keep your data
```

## The Desktop Ledger

Ten builds, one line each, with the proof.

```table
| Build | Proof |
| 0 Install | hermes doctor clean with Full Disk Access granted; a message sent in the app appears in the CLI's session list |
| 1 The window | A Last turn diff in the review pane showed exactly one intended change |
| 2 Settings | hermes config show reads back your default model and cheaper auxiliary models |
| 3 Capabilities | security-guidance and disk-cleanup enabled for your profile |
| 4 Gateways | Test reports Reachable for a remote gateway, and its sessions live on that machine |
| 5 Hello Hermes | The pane, the chip, the palette command and the keybind all work after a hot reload |
| 6 Prompt Library | A saved prompt survives a restart; Copy and New chat both work |
| 7 Ledger | The doctor passes, /ledger prints a summary, and the page shows what the agent recorded |
| 8 Fleet Board | Every profile listed with its last activity; your own prompt produced a plugin that loaded |
| 9 Care | A pre-update backup exists and the post-update check came back clean |
```

```callout kind=success title="What you have now"
The app is no longer a nicer chat window. It is your own workbench: a page for your prompts, your money in a plugin you can read the source of, a board of your agents, and a habit of asking Hermes to build the next tool against a documented contract. Volume 3 turns the profiles you see in the Fleet Board into a team.
```
