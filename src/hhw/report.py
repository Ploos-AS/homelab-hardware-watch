from __future__ import annotations
from datetime import datetime, timezone
from hhw.models import Candidate


def markdown_report(candidates: list[Candidate]) -> str:
    now = datetime.now(timezone.utc).isoformat()
    rows = sorted(candidates, key=lambda x: (x.item_price is None, x.item_price or 0))
    lines = [
        "# Norway current candidates",
        "",
        f"Generated: {now}",
        "",
        "| Vendor | Product | Price | Stock | Categories |",
        "|---|---|---:|---|---|",
    ]
    for c in rows:
        price = f"{c.item_price:,.0f} {c.currency}" if c.item_price is not None else "unknown"
        cats = ", ".join(c.categories)
        lines.append(f"| {c.vendor_id} | [{c.title}]({c.url}) | {price} | {c.stock_status} | {cats} |")
    return "\n".join(lines) + "\n"
