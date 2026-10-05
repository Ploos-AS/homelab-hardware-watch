from __future__ import annotations

from dataclasses import dataclass

from hhw.models import Candidate
from hhw.monitor_store import load_state, save_state
from hhw.monitoring import Snapshot, changes, snapshot


@dataclass(frozen=True)
class MonitorEvent:
    candidate_id: str
    vendor_id: str
    url: str
    event: str
    action: str | None
    delivered_nok: float | None


def run_monitor(candidates: list[Candidate], state_file: str, role: str | None = None) -> list[MonitorEvent]:
    previous = load_state(state_file)
    current: list[Snapshot] = []
    events: list[MonitorEvent] = []

    for candidate in candidates:
        now = snapshot(candidate, role)
        current.append(now)
        before = previous.get(now.candidate_id)
        for event in changes(before, now):
            events.append(MonitorEvent(
                candidate_id=now.candidate_id,
                vendor_id=now.vendor_id,
                url=now.url,
                event=event,
                action=now.action,
                delivered_nok=now.delivered_nok,
            ))

    save_state(state_file, current)
    return sorted(events, key=lambda x: (x.candidate_id, x.event))
