# Tier 9: Chat Platforms Only

Commands the terminal does not have, because they only make sense in a chat.

| # | Command | What it does | Use it when | Works in |
|---|---|---|---|---|
| 85 | `/sethome` `/set-home` | Marks this chat as the home channel, where cron and other deliveries land | Setting up a new bot chat, and before a `/handoff` to it | Chat |
| 86 | `/platform` | Lists every platform adapter with its state, pauses one, or resumes it and clears a tripped breaker | One platform is failing and you want to stop it without stopping the rest | Chat |
| 87 | `/restart` | Restarts the gateway once active runs drain, then confirms in this chat | A config change needs a restart and you are on your phone | Chat |
| 88 | `/topic` | Turns on Telegram DM topics, so each topic is its own session. `off` turns them off | You want several parallel conversations with one bot on Telegram | Chat |
| 89 | `/commands` | Pages through every command and skill | Your platform's command menu cuts the list short | Chat |
| 90 | `/start` | Acknowledges a platform's first-contact ping without a reply and without starting a turn | You want to check the gateway answers without spending a turn | Chat |

---

[← Back to the index](../README.md) · [Whole volume in one file](FULL-HERMES-SLASH-COMMANDS.md)
