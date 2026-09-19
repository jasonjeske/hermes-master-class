"""ledger plugin for Hermes Agent: two tools and one slash command.

register() runs once at load. A crash here disables only this plugin.
"""

from __future__ import annotations

import json
import logging

from . import ledger_core as core, schemas, tools

logger = logging.getLogger(__name__)

TOOLSET = "ledger"


def _slash_ledger(raw_args: str) -> str:
    """/ledger [YYYY-MM]: print the month summary without spending a model turn."""
    try:
        report = core.month_report(raw_args.strip() or None, limit=5)
    except Exception as exc:
        return f"ledger: {exc}"
    lines = [
        f"Ledger {report['month']}: income {report['income']:.2f}, expenses {report['expenses']:.2f}, net {report['net']:.2f}",
    ]
    for row in report["by_category"][:8]:
        lines.append(f"  {row['category']:<16} {row['total']:>10.2f}  ({row['count']})")
    return "\n".join(lines)


def register(ctx) -> None:
    ctx.register_tool(name="ledger_add", toolset=TOOLSET, schema=schemas.LEDGER_ADD, handler=tools.ledger_add)
    ctx.register_tool(name="ledger_report", toolset=TOOLSET, schema=schemas.LEDGER_REPORT, handler=tools.ledger_report)
    ctx.register_command("ledger", _slash_ledger, description="Month summary of the personal ledger, e.g. /ledger 2026-09")
    logger.debug("ledger registered: %s", json.dumps(["ledger_add", "ledger_report", "/ledger"]))
