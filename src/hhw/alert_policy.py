from __future__ import annotations

from hhw.monitor_run import MonitorEvent


def alert_worthy(event: MonitorEvent) -> bool:
    """Return True only for events worth surfacing to an operator."""
    if event.event == "new_candidate":
        return event.action in {"BUY", "WATCH"}
    if event.event == "became_buy":
        return True
    if event.event == "became_watch":
        return True
    if event.event in {"delivered_price_down", "item_price_down", "became_bargain", "became_exceptional"}:
        return event.action in {"BUY", "WATCH"}
    return False


def filter_alerts(events: list[MonitorEvent]) -> list[MonitorEvent]:
    return [event for event in events if alert_worthy(event)]
