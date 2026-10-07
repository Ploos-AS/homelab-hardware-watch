from datetime import date

import pytest

from hhw.price_history import PriceObservation
from hhw.price_stats import price_series


def obs(day, price, currency="NOK", delivered=None, listing="abc"):
    return PriceObservation(
        listing_id=listing,
        vendor_id="vendor",
        url="https://example.invalid/item",
        observed_on=date(2026, 10, day),
        item_price=price,
        currency=currency,
        delivered_nok=delivered,
    )


def test_item_price_median_low_high_latest():
    result = price_series(
        [obs(1, 3000), obs(2, 2000), obs(3, 2500)],
        "abc", date(2026, 10, 3),
    )
    assert result["basis"] == "item_price"
    assert result["median"] == 2500
    assert result["low"] == 2000
    assert result["high"] == 3000
    assert result["latest"] == 2500
    assert result["observations"] == 3


def test_delivered_nok_is_preferred_when_complete():
    result = price_series(
        [obs(1, 100, "EUR", 1400), obs(2, 90, "EUR", 1300)],
        "abc", date(2026, 10, 2),
    )
    assert result["basis"] == "delivered_nok"
    assert result["currency"] == "NOK"
    assert result["median"] == 1350


def test_mixed_currency_without_complete_delivered_history_fails_closed():
    result = price_series(
        [obs(1, 100, "EUR"), obs(2, 1000, "NOK")],
        "abc", date(2026, 10, 2),
    )
    assert result["comparable"] is False
    assert result["reason"] == "mixed_currency"


def test_missing_price_fails_closed():
    result = price_series(
        [obs(1, 1000), obs(2, None)],
        "abc", date(2026, 10, 2),
    )
    assert result["comparable"] is False
    assert result["reason"] == "price_missing"


def test_future_observations_are_excluded():
    result = price_series(
        [obs(1, 3000), obs(5, 1000)],
        "abc", date(2026, 10, 2),
    )
    assert result["observations"] == 1
    assert result["low"] == 3000


def test_window_limits_history():
    result = price_series(
        [obs(1, 3000), obs(5, 2500), obs(10, 2000)],
        "abc", date(2026, 10, 10), window_days=6,
    )
    assert result["observations"] == 2
    assert result["median"] == 2250
    assert result["low"] == 2000


def test_other_listing_is_ignored():
    result = price_series(
        [obs(1, 3000), obs(2, 100, listing="other")],
        "abc", date(2026, 10, 2),
    )
    assert result["observations"] == 1
    assert result["latest"] == 3000


def test_empty_history_is_not_comparable():
    result = price_series([], "abc", date(2026, 10, 2))
    assert result == {"comparable": False, "reason": "no_history", "observations": 0}


def test_invalid_window_rejected():
    with pytest.raises(ValueError):
        price_series([obs(1, 1000)], "abc", date(2026, 10, 2), window_days=0)
