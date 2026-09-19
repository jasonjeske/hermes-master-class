"""Backend routes for the ledger desktop page. Mounted at /api/plugins/ledger/ inside the gateway.

The dashboard loads this file by path, not as part of the plugin package, so the core
module is loaded by path too (the same pattern the bundled examples use).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from fastapi import APIRouter, HTTPException

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("hermes_ledger_core", _HERE.parent / "ledger_core.py")
core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(core)

router = APIRouter()


@router.get("/summary")
async def summary(month: str | None = None) -> dict:
    return core.month_report(month, limit=20)


@router.post("/entries")
async def create(body: dict) -> dict:
    try:
        amount = float(body.get("amount", 0))
        kind = str(body.get("kind", "expense")).lower()
        category = str(body.get("category", "")).strip()
        if amount <= 0 or kind not in ("expense", "income") or not category:
            raise ValueError("need a positive amount, a kind, and a category")
        return {"ok": True, "entry": core.add_entry(amount, kind, category, str(body.get("note", "")), body.get("date") or None)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/entries/{entry_id}")
async def remove(entry_id: int) -> dict:
    conn = core.db()
    with conn:
        cur = conn.execute("DELETE FROM entries WHERE id = ?", (int(entry_id),))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="no such entry")
    return {"ok": True, "deleted": int(entry_id)}
