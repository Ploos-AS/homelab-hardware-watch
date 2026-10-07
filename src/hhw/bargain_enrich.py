from __future__ import annotations

from datetime import date

from hhw.bargain import bargain_signal
from hhw.families import bargain_config_key, bargain_family_key
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

        config = bargain_config_key(candidate.title)
        comparison_history = history
        comparison_family = family
        precision = "family"
        if config:
            exact = [x for x in history if getattr(x, "config_key", None) == config]
            if len({x.listing_id for x in exact if x.listing_id != listing_id(candidate)}) >= 3:
                comparison_history = exact
                comparison_family = family
                precision = "exact_config"

        candidate.metadata["bargain"] = bargain_signal(
            comparison_history,
            comparison_family,
            listing_id(candidate),
            current_price,
            currency,
            observed_on,
        )
        candidate.metadata["bargain"]["comparison_precision"] = precision
        candidate.metadata["bargain"]["config_key"] = config
    return candidates
