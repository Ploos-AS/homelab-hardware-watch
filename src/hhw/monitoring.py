from __future__ import annotations

from dataclasses import dataclass
import hashlib

from hhw.enterprise_score import enterprise_action, score_enterprise
from hhw.models import Candidate


def candidate_id(candidate: Candidate) -> str:
    """Stable identity for one vendor listing across collection runs."""
    raw = f"{candidate.vendor_id}\0{candidate.url}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:20]


@dataclass(frozen=True)
class Snapshot:
    candidate_id: str
    vendor_id: str
    url: str
    item_price: float | None
    currency: str
    delivered_nok: float | None
    action: str | None

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def snapshot(candidate: Candidate, role: str | None = None) -> Snapshot:
    cost = (candidate.metadata or {}).get("delivered_cost") or {}
    delivered = (
        cost.get("import_confirmed_delivered_nok")
        if cost.get("cost_status") == "import_confirmed"
        else cost.get("estimated_delivered_nok")
    )
    action = None
    if role in {"proxmox_compute", "storage"}:
        action = enterprise_action(score_enterprise(candidate, role))
    return Snapshot(
        candidate_id=candidate_id(candidate),
        vendor_id=candidate.vendor_id,
        url=candidate.url,
        item_price=candidate.item_price,
        currency=candidate.currency,
        delivered_nok=delivered,
        action=action,
    )


def changes(previous: Snapshot | None, current: Snapshot) -> list[str]:
    if previous is None:
        return ["new_candidate"]

    events = []
    if (
        previous.delivered_nok is not None
        and current.delivered_nok is not None
        and current.delivered_nok < previous.delivered_nok
    ):
        events.append("delivered_price_down")
    elif (
        previous.item_price is not None
        and current.item_price is not None
        and current.currency == previous.currency
        and current.item_price < previous.item_price
    ):
        events.append("item_price_down")

    if previous.action != current.action:
        events.append("action_changed")
        if current.action == "BUY":
            events.append("became_buy")
        elif current.action == "WATCH":
            events.append("became_watch")
    return events
