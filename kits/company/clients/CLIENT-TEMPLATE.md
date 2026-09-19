# Client: <name>

One folder per client, one profile per client when their data must stay apart. Copy to <company folder>/clients/<slug>/CLIENT.md.

## Boundary
- Profile: <slug> (hermes profile create <slug> --description "..."), or "shared" when nothing here is confidential
- Data lives in: <absolute path to the client folder>; nothing about this client is stored anywhere else
- Tools this client's profile has: <the smallest list that does the work>
- Never: send on the client's behalf, log in as the client, store their credentials in a chat

## What we do for them
- Offer: <the service in one sentence>
- Cadence: <weekly, monthly, on request>
- Price and terms: <amount, currency, billing day, what is included>
- The number they care about: <what they will judge us on>

## Before every call
- scout: what changed for them since last time (their site, their news, their market), five lines with sources
- atlas: open items from the last notes, promises we made, questions to ask
- Delivered to the human 30 minutes before the call, in one message

## After every call
- Notes in <client folder>/notes/<date>.md within the hour: decisions, promises, dates
- Follow-up draft written by quill, sent by the human only
- New work becomes cards with this client's tenant on the board

## Money
- Every invoice and every payment is a ledger_add entry with category client:<slug>
- Invoices are drafted by quill from the ledger and this file; the human sends them
- Model spend for this client's profile is read from hermes insights and compared with the price monthly

## Notes on compliance
- Whose data protection rules apply: <country and law>
- What we told the client about where their data is processed: <the sentence, dated>
- Who is responsible for the security of the install: <written down, agreed, signed>
