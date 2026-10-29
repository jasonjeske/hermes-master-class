# Tier 10: Account and Upkeep

Updates, versions, sign-in, and the housekeeping you do once a month.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 91 | `/update` | Updates Hermes Agent to the latest version | A fix or feature you need just shipped | CLI and chat |
| 92 | `/version` `/v` | Shows the version, build and environment | Before you report a bug, or follow a guide written for another version | CLI and chat |
| 93 | `/debug` | Uploads a debug report with the last 200 log lines to a public paste service and prints the links, with no confirmation step. `local` prints it here and uploads nothing | Run `/debug local` first and read it. Upload only when someone asks you for the links | CLI and chat |
| 94 | `/whoami` | Shows your command access in this chat: admin or user | A command is refused and you want to know why | CLI and chat |
| 95 | `/profile` | Shows the active profile name and its home folder | Making sure you are in the profile you think you are | CLI and chat |
| 96 | `/config` | Shows the current configuration | Checking a setting without leaving the session | CLI |
| 97 | `/platforms` `/gateway` | Shows the status of every messaging platform | A bot stopped answering | CLI |
| 98 | `/login` | Signs in with a Nous account. In chat, paired direct messages only | Setting up Nous Portal billing or tools | CLI and chat |
| 99 | `/topup` | Shows your Nous balance and opens billing | Your Nous credits are running low | CLI and chat |
| 100 | `/subscription` `/upgrade` | Shows your Nous plan and opens the page to change it | Changing your Nous plan | CLI |
| 101 | `/autoprune` | Turns automatic pruning of old ended sessions on or off. Hermes asks once when the disk runs low | The session database keeps growing and the disk is filling | CLI and chat |
| 102 | `/quit` `/exit` | Exits the CLI. `--delete` also deletes this session's history | You are done. Add `--delete` only for a session you never want back | CLI |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
