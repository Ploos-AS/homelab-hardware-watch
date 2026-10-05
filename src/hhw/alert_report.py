from __future__ import annotations

from hhw.monitor_run import MonitorEvent


def markdown_alerts(events: list[MonitorEvent]) -> str:
    lines = ["# Hardware watch alerts", ""]
    if not events:
        return "\n".join(lines + ["No actionable hardware changes.", ""])

    lines += ["| Action | Event | Vendor | Delivered | Listing |",
              "|---|---|---|---:|---|"]
    for event in events:
        price = f"{event.delivered_nok:.0f} NOK" if event.delivered_nok is not None else "—"
        lines.append(
            f"| {event.action or '—'} | {event.event} | {event.vendor_id} | "
            f"{price} | [open]({event.url}) |"
        )
    lines.append("")
    return "\n".join(lines)
