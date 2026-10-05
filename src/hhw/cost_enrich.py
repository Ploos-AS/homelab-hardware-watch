from __future__ import annotations
from datetime import date

from hhw.delivered_cost import DeliveredCostInput, calculate_delivered_nok
from hhw.fx import FxObservation, rate_to_nok


def enrich_delivered_cost(candidate, fx: list[FxObservation], observed_on: date):
    metadata = candidate.metadata
    obs = rate_to_nok(candidate.currency, fx, observed_on)

    shipping = metadata.get("shipping_eur") if candidate.currency == "EUR" else metadata.get("shipping_nok")
    handling = metadata.get("handling_nok")
    vat_rate = metadata.get("foreign_vat_rate")
    vat_included = bool(metadata.get("foreign_vat_included", False))
    vat_removed = metadata.get("foreign_vat_removed_for_export")

    result = calculate_delivered_nok(DeliveredCostInput(
        item_price=candidate.item_price or 0,
        currency=candidate.currency,
        exchange_rate_to_nok=obs.rate if obs else None,
        foreign_vat_rate=vat_rate,
        foreign_vat_included=vat_included,
        foreign_vat_removed_for_export=vat_removed,
        shipping=shipping,
        handling_nok=handling,
    ))
    result["fx_observed_on"] = obs.observed_on.isoformat() if obs else None
    result["fx_source"] = obs.source if obs else None
    metadata["delivered_cost"] = result
    return candidate
