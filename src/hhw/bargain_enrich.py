from __future__ import annotations

from datetime import date

from hhw.bargain import bargain_signal
from hhw.families import bargain_family_key
from hhw.price_history import PriceObservation, listing_id


def enrich_bargains(
    candidates,
    history: list[PriceObservation],
    observed_on: date,
):
    for candidate in candidates:
        family = bargain_family_key(candidate.title)
        if family is None or candidate.item_price is None:
            continue

        current_price = float(candidate.item_price)
        currency = candidate.currency
        cost = (candidate.metadata or {}).get("delivered_cost") or {}
        delivered = (
            cost.get("import_confirmed_delivered_nok")
            if cost.get("cost_status") == "import_confirmed"
            else cost.get("estimated_delivered_nok")
        )
        if delivered is not None:
            current_price = float(delivered)
            currency = "NOK"

        candidate.metadata["bargain"] = bargain_signal(
            history,
            family,
            listing_id(candidate),
            current_price,
            currency,
            observed_on,
        )
    return candidates
