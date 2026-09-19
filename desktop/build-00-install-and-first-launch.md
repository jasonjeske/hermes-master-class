# Build 0: Install and First Launch

![Build 0](../assets/art/part-02.webp)

### What you are building

The app on your Mac, the local backend it manages, the one permission grant that stops macOS from asking about every folder, and a clear picture of what lives where.

### What the docs say

Checked against the Installation page, the Platform Support page, and the Desktop page.

| Fact | Detail |
|---|---|
| Two sanctioned installs | The Hermes Desktop installer from the website installs both the command line and the app, and is the recommended path on macOS. Or install the CLI first with the one-line installer, then run `hermes desktop`, which builds and launches the app against your existing config, keys, sessions and skills |
| Platform | macOS on Apple Silicon, Windows 10 and 11, and Linux or WSL2 all have a Desktop build; Intel Macs do not. This volume is written on macOS and says so where a step differs |
| The same home | On first launch the app can install the Hermes runtime into `~/.hermes`, the same layout a CLI install uses. That is why the two are interchangeable |
| What runs | The app launches a headless `hermes serve` backend for you and talks to it over JSON-RPC and WebSocket. It never needs the web dashboard |
| Folder prompts | macOS prompts per folder as Hermes touches Desktop, Downloads, Documents. One Full Disk Access grant for Hermes.app (and your terminal) covers all of them. `hermes doctor` reports whether the grant is present |
| Grants survive updates | Grants are remembered against the code-signing identity. Locally built and self-updated apps carry a stable identity, so grants persist. For a certificate-anchored identity run `hermes desktop --setup-tcc-identity` once, and re-run it after updates to re-sign |
| Stuck permission | `tccutil reset All com.nousresearch.hermes`, then re-grant and fully relaunch |
| Logs | Boot logs land in `~/.hermes/logs/desktop.log`; `hermes logs gui -f` tails them |

### Commands

*`day-one-desktop.sh`*

```bash
# A. Already have the CLI from Volume 1? Build and launch the app on top of it.
hermes desktop

# B. Fresh Mac: download the Hermes Desktop installer from hermes-agent.nousresearch.com and run it.
#    It installs the CLI and the app together. Then:
hermes doctor                 # includes the Full Disk Access check on macOS
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
#    enable Hermes.app and your terminal, then fully quit and relaunch both

# C. Anchor the signing identity so permission grants outlive every update
hermes desktop --setup-tcc-identity

# D. Know where things are
hermes status
hermes logs gui -f            # the app's boot log, live
```

> 📝 **If you run Omarchy**
>
> Hermes Desktop installs from Omarchy's own menu (Install, AI, Hermes Desktop), follows the system theme, and can be set as the default agent with `omarchy default agent hermes`. Tonbi's warning is the one line to remember: launched that way, the agent starts in YOLO mode, which bypasses the dangerous-command approvals, so treat the default-agent binding as a power tool and read Build 10 of Volume 1 before you leave it on.

> ⚠️ **Two prompts people report after updates**
>
> Operators on the Hermes forums and issue tracker describe two recurring prompts after an update: macOS asking again for folder or screen permissions, and a keychain prompt for the app's saved credentials. The documented cure for the first is the identity anchor above plus a `tccutil reset` and a fresh grant when a stale grant lingers. For the keychain prompt, the community advice is to allow it rather than delete the keychain item, since the item holds the app's stored credentials. Treat that second point as field advice, not a documented guarantee; the docs cover the permissions side in detail.

> 📝 **From the field: Tonbi's Desktop Masterclass, part 1**
>
> Tonbi's September 2026 rebuild of his desktop guide opens with the sentence this whole volume rests on: "It's a front end. It's not a separate agent." He also notes that his own June guide covered, by his count, about forty percent of the app after five major releases, which is the honest reason this volume names the documentation page for every fact instead of a video. When a video and the docs disagree, the docs are newer.

### Prompts

*`prompt-d0-what-did-the-app-install.md`*

```markdown
Read https://hermes-agent.nousresearch.com/docs/user-guide/desktop
sections "How it works" and "Connecting to a remote backend" (just the first
paragraphs). Then look at this machine and tell me, with paths:

1. Where the Hermes runtime the app uses lives, and whether it is the same
   ~/.hermes my terminal uses (compare hermes status from both).
2. Which process the app is talking to right now (name and port) and whether
   it is the local backend or a remote one.
3. Whether Full Disk Access is granted for the terminal and for Hermes.app,
   from hermes doctor.
4. The last twenty lines of ~/.hermes/logs/desktop.log, summarized in three
   lines, with any warning quoted.

Change nothing.
```

### Verify

- [ ] The app opens to a chat on your existing profile, with your sessions from the CLI visible
- [ ] hermes doctor shows Full Disk Access granted for the terminal, and the app no longer prompts per folder
- [ ] hermes logs gui -f shows a clean boot with the backend ready
- [ ] A message sent in the app appears in hermes sessions list from the terminal

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-DESKTOP.md)
