"""Ledger core: the SQLite store and the two operations. No Hermes imports at module level,
so both the agent tools and the dashboard API can load this file.

Durable state lives under <hermes home>/plugin-data/ledger/ through plugins.plugin_storage,
never inside the plugin folder (updates and removals wipe the folder).
"""

from __future__ import annotations

import datetime as dt

_SCHEMA = """
CREATE TABLE IF NOT EXISTS entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT NOT NULL,
  kind TEXT NOT NULL CHECK (kind IN ('expense', 'income')),
  category TEXT NOT NULL,
  amount REAL NOT NULL CHECK (amount > 0),
  note TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS entries_date ON entries(date);
"""


def db():
    """Open the plugin's SQLite database (WAL mode, created on first use)."""
    from plugins.plugin_storage import plugin_db

    conn = plugin_db("ledger")
    conn.executescript(_SCHEMA)
    return conn


def _month(value: str | None) -> str:
    if value and len(value) == 7 and value[4] == "-":
        return value
    return dt.date.today().strftime("%Y-%m")


def add_entry(amount: float, kind: str, category: str, note: str = "", date: str | None = None) -> dict:
    day = date or dt.date.today().isoformat()
    dt.date.fromisoformat(day)  # raises on a bad date
    conn = db()
    with conn:
        cur = conn.execute(
            "INSERT INTO entries(date, kind, category, amount, note, created_at) VALUES (?,?,?,?,?,?)",
            (day, kind, category.strip().lower(), float(amount), note.strip(), dt.datetime.now().isoformat(timespec="seconds")),
        )
    return {"id": cur.lastrowid, "date": day, "kind": kind, "category": category.strip().lower(), "amount": float(amount), "note": note.strip()}


def month_report(month: str | None = None, limit: int = 10) -> dict:
    month = _month(month)
    conn = db()
    like = month + "-%"
    income = conn.execute("SELECT COALESCE(SUM(amount),0) FROM entries WHERE kind='income' AND date LIKE ?", (like,)).fetchone()[0]
    expense = conn.execute("SELECT COALESCE(SUM(amount),0) FROM entries WHERE kind='expense' AND date LIKE ?", (like,)).fetchone()[0]
    by_cat = conn.execute(
        "SELECT category, ROUND(SUM(amount),2) AS total, COUNT(*) AS n FROM entries "
        "WHERE kind='expense' AND date LIKE ? GROUP BY category ORDER BY total DESC",
        (like,),
    ).fetchall()
    recent = conn.execute(
        "SELECT id, date, kind, category, amount, note FROM entries WHERE date LIKE ? ORDER BY date DESC, id DESC LIMIT ?",
        (like, int(limit)),
    ).fetchall()
    return {
        "month": month,
        "income": round(income, 2),
        "expenses": round(expense, 2),
        "net": round(income - expense, 2),
        "by_category": [{"category": c, "total": t, "count": n} for c, t, n in by_cat],
        "recent": [
            {"id": i, "date": d, "kind": k, "category": c, "amount": a, "note": nt} for i, d, k, c, a, nt in recent
        ],
    }


