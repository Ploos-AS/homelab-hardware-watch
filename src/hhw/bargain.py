from __future__ import annotations

from datetime import date

from hhw.price_history import PriceObservation
from hhw.price_stats import family_price_series


def bargain_signal(
    observations: list[PriceObservation],
    family_key: str,
    current_listing_id: str,
    current_price: float,
    currency: str,
    as_of: date,
    *,
    min_listings: int = 3,
    window_days: int | None = 90,
) -> dict:
    """Classify a price against prior comparable listings in its family.

    The current listing is excluded from the market baseline. This signal is
    informational and must not override compatibility or decision BUY gates.
    """
    prior = [
        x for x in observations
        if x.listing_id != current_listing_id
    ]
    stats = family_price_series(prior, family_key, as_of, window_days)
    if not stats["comparable"]:
        return {"signal": "insufficient_history", "reason": stats["reason"], "stats": stats}
    if stats["listings"] < min_listings:
        return {"signal": "insufficient_history", "reason": "too_few_listings", "stats": stats}
    if stats["currency"] != currency:
        return {"signal": "not_comparable", "reason": "currency_mismatch", "stats": stats}

    median_price = stats["median"]
    discount = (median_price - current_price) / median_price if median_price > 0 else 0.0

    if discount >= 0.30:
        signal = "exceptional"
    elif discount >= 0.20:
        signal = "bargain"
    elif discount >= 0.10:
        signal = "good_price"
    else:
        signal = "normal"

    return {
        "signal": signal,
        "reason": None,
        "discount_vs_median": discount,
        "current_price": float(current_price),
        "currency": currency,
        "stats": stats,
    }
