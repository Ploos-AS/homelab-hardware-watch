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
