"""JSON schemas for the ledger tools. The description is how the model decides to call them."""

from __future__ import annotations

LEDGER_ADD = {
    "name": "ledger_add",
    "description": (
        "Record one money entry in the personal ledger: an expense or an income, "
        "with an amount, a category, an optional note and an optional date. "
        "Use it whenever the user mentions spending, paying, earning, or receiving money."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "amount": {"type": "number", "description": "Positive amount in the ledger currency, e.g. 42.50"},
            "kind": {"type": "string", "enum": ["expense", "income"], "description": "expense or income"},
            "category": {
                "type": "string",
                "description": "Short category such as groceries, rent, software, transport, salary, client",
            },
            "note": {"type": "string", "description": "What it was, in a few words"},
            "date": {"type": "string", "description": "ISO date YYYY-MM-DD; today when omitted"},
        },
        "required": ["amount", "kind", "category"],
    },
}

LEDGER_REPORT = {
    "name": "ledger_report",
    "description": (
        "Summarize the personal ledger for a month: totals for income and expenses, "
        "the net, and expenses grouped by category. Use it when the user asks how much "
        "they spent or earned, where the money went, or for a monthly budget check."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "month": {"type": "string", "description": "Month as YYYY-MM; the current month when omitted"},
            "limit": {"type": "integer", "description": "How many recent entries to include, default 10"},
        },
        "required": [],
    },
}
