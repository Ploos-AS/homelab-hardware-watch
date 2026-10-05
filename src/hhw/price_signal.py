from __future__ import annotations

from hhw.models import Candidate


def raw_price_signal(candidate: Candidate) -> tuple[float | None, str]:
    cost = (candidate.metadata or {}).get("delivered_cost") or {}
    if cost.get("cost_status") == "import_confirmed":
        price = cost.get("import_confirmed_delivered_nok")
        if price is not None:
            return float(price), "import_confirmed"
    estimated = cost.get("estimated_delivered_nok")
    if estimated is not None:
        return float(estimated), "estimate"
    if candidate.currency == "NOK" and candidate.item_price is not None:
        return float(candidate.item_price), "domestic"
    return None, "unknown"
