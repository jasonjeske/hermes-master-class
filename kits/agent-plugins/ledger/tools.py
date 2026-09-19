"""Handlers for the ledger tools.

Rules Hermes holds every handler to: take the parsed args dict, return a JSON
string, never raise.
"""

from __future__ import annotations

import json
from typing import Any

from . import ledger_core as core


def ledger_add(args: dict, **kwargs: Any) -> str:
    try:
        amount = float(args.get("amount", 0))
        kind = str(args.get("kind", "expense")).lower()
        category = str(args.get("category", "")).strip()
        if amount <= 0 or kind not in ("expense", "income") or not category:
            return json.dumps({"error": "need a positive amount, a kind of expense or income, and a category"})
        entry = core.add_entry(amount, kind, category, str(args.get("note", "")), args.get("date") or None)
        return json.dumps({"ok": True, "entry": entry})
    except Exception as exc:  # a handler never raises
        return json.dumps({"error": str(exc)})


def ledger_report(args: dict, **kwargs: Any) -> str:
    try:
        return json.dumps(core.month_report(args.get("month"), int(args.get("limit", 10) or 10)))
    except Exception as exc:
        return json.dumps({"error": str(exc)})
