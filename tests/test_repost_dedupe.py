from datetime import date
from hhw.price_history import PriceObservation
from hhw.price_stats import family_price_series


def observation(identifier, vendor, price, config="mac_mini_m1_16gb_512gb"):
    return PriceObservation(
        listing_id=identifier, vendor_id=vendor,
        url=f"https://example.invalid/{identifier}",
        observed_on=date(2026, 10, 8), item_price=price,
        currency="NOK", family_key="mac_mini_m1",
        config_key=config, price_confidence="domestic",
    )


def test_reposted_same_vendor_same_configuration_and_price_counts_once():
    rows = [observation("old", "seller1", 4000),
            observation("new", "seller1", 4000),
            observation("other", "seller2", 4500)]
    stats = family_price_series(rows, "mac_mini_m1", date(2026, 10, 8))
    assert stats["listings"] == 2


def test_different_sellers_are_not_collapsed():
    rows = [observation("a", "seller1", 4000),
            observation("b", "seller2", 4000),
            observation("c", "seller3", 4000)]
    assert family_price_series(rows, "mac_mini_m1", date(2026, 10, 8))["listings"] == 3


def test_same_seller_different_configuration_not_collapsed():
    rows = [observation("a", "seller1", 4000),
            observation("b", "seller1", 4000, "mac_mini_m1_8gb_256gb")]
    assert family_price_series(rows, "mac_mini_m1", date(2026, 10, 8))["listings"] == 2
