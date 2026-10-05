from __future__ import annotations

from hhw.monitor_run import MonitorEvent


def markdown_alerts(events: list[MonitorEvent]) -> str:
    lines = ["# Hardware watch alerts", ""]
    if not events:
        return "\n".join(lines + ["No actionable hardware changes.", ""])

    lines += ["| Action | Event | Vendor | Delivered | Change | Listing |",
              "|---|---|---|---:|---:|---|"]
    for event in events:
        price = f"{event.delivered_nok:.0f} NOK" if event.delivered_nok is not None else "—"
        change = "—"
        if event.previous_delivered_nok is not None and event.delivered_nok is not None:
            delta = event.delivered_nok - event.previous_delivered_nok
            pct = (delta / event.previous_delivered_nok * 100) if event.previous_delivered_nok else None
            if pct is not None:
                change = f"{event.previous_delivered_nok:.0f} → {event.delivered_nok:.0f} NOK ({delta:+.0f}, {pct:+.1f}%)"
        elif event.previous_item_price is not None and event.item_price is not None:
            delta = event.item_price - event.previous_item_price
            pct = (delta / event.previous_item_price * 100) if event.previous_item_price else None
            if pct is not None:
                change = f"{event.previous_item_price:.2f} → {event.item_price:.2f} {event.currency or ''} ({delta:+.2f}, {pct:+.1f}%)".replace("  ", " ")
        lines.append(
            f"| {event.action or '—'} | {event.event} | {event.vendor_id} | "
            f"{price} | {change} | [open]({event.url}) |"
        )
    lines.append("")
    return "\n".join(lines)
