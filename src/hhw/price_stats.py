from __future__ import annotations

from datetime import date, timedelta
from statistics import median

from hhw.price_history import PriceObservation


def price_series(
    observations: list[PriceObservation],
    listing_id: str,
    as_of: date,
    window_days: int | None = None,
) -> dict:
    """Return one comparable historical price series for a listing.

    Delivered NOK is preferred when every selected observation has it.
    Otherwise raw item prices are used only when all priced observations share
    one currency. Mixed/non-comparable history fails closed.
    """
    selected = [
        x for x in observations
        if x.listing_id == listing_id and x.observed_on <= as_of
    ]
    if window_days is not None:
        if window_days < 1:
            raise ValueError("window_days must be >= 1")
        start = as_of - timedelta(days=window_days - 1)
        selected = [x for x in selected if x.observed_on >= start]

    selected.sort(key=lambda x: x.observed_on)
    if not selected:
        return {"comparable": False, "reason": "no_history", "observations": 0}

    delivered = [x.delivered_nok for x in selected]
    if all(value is not None for value in delivered):
        values = [float(value) for value in delivered]
        basis = "delivered_nok"
        currency = "NOK"
    else:
        priced = [x for x in selected if x.item_price is not None]
        currencies = {x.currency for x in priced}
        if len(priced) != len(selected):
            return {"comparable": False, "reason": "price_missing", "observations": len(selected)}
        if len(currencies) != 1:
            return {"comparable": False, "reason": "mixed_currency", "observations": len(selected)}
        values = [float(x.item_price) for x in selected]
        basis = "item_price"
        currency = next(iter(currencies))

    return {
        "comparable": True,
        "reason": None,
        "basis": basis,
        "currency": currency,
        "observations": len(values),
        "median": float(median(values)),
        "low": min(values),
        "high": max(values),
        "latest": values[-1],
        "first_observed_on": selected[0].observed_on,
        "last_observed_on": selected[-1].observed_on,
    }



def family_price_series(
    observations: list[PriceObservation],
    family_key: str,
    as_of: date,
    window_days: int | None = None,
) -> dict:
    """Cross-listing market statistics using the latest observation per listing.

    This prevents a long-lived listing from receiving more weight merely
    because it was collected on more days.
    """
    selected = [
        x for x in observations
        if x.family_key == family_key and x.observed_on <= as_of
    ]
    if window_days is not None:
        if window_days < 1:
            raise ValueError("window_days must be >= 1")
        start = as_of - timedelta(days=window_days - 1)
        selected = [x for x in selected if x.observed_on >= start]

    latest_by_listing: dict[str, PriceObservation] = {}
    for observation in sorted(selected, key=lambda x: x.observed_on):
        latest_by_listing[observation.listing_id] = observation
    selected = list(latest_by_listing.values())

    # Prefer evidence suitable for decisions. Estimated import totals may be
    # useful for discovery, but must not define a bargain market baseline when
    # enough domestic/import-confirmed observations exist.
    confirmed = [x for x in selected if x.price_confidence in {"domestic", "import_confirmed"}]
    confidence_basis = "confirmed" if len(confirmed) >= 3 else "mixed_or_legacy"
    if len(confirmed) >= 3:
        selected = confirmed

    if not selected:
        return {"comparable": False, "reason": "no_family_history", "listings": 0}

    delivered = [x.delivered_nok for x in selected]
    if all(value is not None for value in delivered):
        values = [float(value) for value in delivered]
        basis = "delivered_nok"
        currency = "NOK"
    else:
        if any(x.item_price is None for x in selected):
            return {"comparable": False, "reason": "price_missing", "listings": len(selected)}
        currencies = {x.currency for x in selected}
        if len(currencies) != 1:
            return {"comparable": False, "reason": "mixed_currency", "listings": len(selected)}
        values = [float(x.item_price) for x in selected]
        basis = "item_price"
        currency = next(iter(currencies))

    return {
        "comparable": True,
        "reason": None,
        "family_key": family_key,
        "basis": basis,
        "currency": currency,
        "listings": len(values),
        "confidence_basis": confidence_basis,
        "median": float(median(values)),
        "low": min(values),
        "high": max(values),
    }
