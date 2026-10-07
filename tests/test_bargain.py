from datetime import date

from hhw.bargain import bargain_signal
from hhw.price_history import PriceObservation


DAY = date(2026, 10, 7)


def obs(listing, price, family="mac_mini_m1", currency="NOK", confidence="unknown"):
    return PriceObservation(
        listing_id=listing, vendor_id="vendor",
        url=f"https://example.invalid/{listing}",
        observed_on=date(2026, 10, 1), item_price=price,
        currency=currency, family_key=family, price_confidence=confidence,
    )


def signal(price, history=None):
    history = history or [obs("a", 5000), obs("b", 5000), obs("c", 5000)]
    return bargain_signal(history, "mac_mini_m1", "current", price, "NOK", DAY)


def test_normal_price():
    assert signal(4600)["signal"] == "normal"


def test_good_price_at_ten_percent_below_median():
    assert signal(4500)["signal"] == "good_price"


def test_bargain_at_twenty_percent_below_median():
    result = signal(4000)
    assert result["signal"] == "bargain"
    assert result["discount_vs_median"] == 0.20


def test_exceptional_at_thirty_percent_below_median():
    assert signal(3500)["signal"] == "exceptional"


def test_requires_three_prior_listings():
    result = signal(3000, [obs("a", 5000), obs("b", 5000)])
    assert result["signal"] == "insufficient_history"
    assert result["reason"] == "too_few_listings"


def test_current_listing_is_excluded_from_baseline():
    history = [
        obs("current", 1000),
        obs("a", 5000), obs("b", 5000), obs("c", 5000),
    ]
    result = bargain_signal(history, "mac_mini_m1", "current", 4000, "NOK", DAY)
    assert result["stats"]["median"] == 5000
    assert result["signal"] == "bargain"


def test_other_generation_does_not_count():
    history = [
        obs("a", 5000), obs("b", 5000),
        obs("m4", 9000, family="mac_mini_m4"),
    ]
    result = signal(3000, history)
    assert result["signal"] == "insufficient_history"


def test_currency_mismatch_fails_closed():
    history = [obs("a", 500), obs("b", 500), obs("c", 500)]
    result = bargain_signal(history, "mac_mini_m1", "current", 400, "EUR", DAY)
    assert result["signal"] == "not_comparable"
    assert result["reason"] == "currency_mismatch"



def test_gpu_family_does_not_mix_with_other_gpu_model():
    history = [
        obs("a", 5000, "gpu_rtx_3090"),
        obs("b", 5200, "gpu_rtx_3090"),
        obs("c", 4800, "gpu_rtx_3090"),
        obs("p40", 1000, "gpu_tesla_p40"),
    ]
    result = bargain_signal(history, "gpu_rtx_3090", "current", 3500, "NOK", DAY)
    assert result["stats"]["median"] == 5000
    assert result["signal"] == "exceptional"


def test_arm_server_families_do_not_mix():
    history = [
        obs("a", 7000, "arm_server_ampere_altra"),
        obs("b", 7200, "arm_server_ampere_altra"),
        obs("c", 6800, "arm_server_ampere_altra"),
        obs("max", 12000, "arm_server_ampere_altra_max"),
    ]
    result = bargain_signal(history, "arm_server_ampere_altra", "current", 5000, "NOK", DAY)
    assert result["stats"]["median"] == 7000



def test_confirmed_market_excludes_estimated_import_when_enough_evidence():
    history = [
        obs("a", 5000, confidence="domestic"),
        obs("b", 5000, confidence="domestic"),
        obs("c", 5000, confidence="import_confirmed"),
        obs("estimate", 1000, confidence="estimate"),
    ]
    result = signal(3500, history)
    assert result["stats"]["median"] == 5000
    assert result["stats"]["listings"] == 3
    assert result["stats"]["confidence_basis"] == "confirmed"
    assert result["signal"] == "exceptional"



def test_reposts_share_one_vote_in_market_median():
    history = [
        PriceObservation("url-a", "vendor", "https://x/a", date(2026,10,1), 1000, "NOK",
                         family_key="mac_mini_m1", market_id="same-offer"),
        PriceObservation("url-b", "vendor", "https://x/b", date(2026,10,2), 1000, "NOK",
                         family_key="mac_mini_m1", market_id="same-offer"),
        obs("other-a", 5000),
        obs("other-b", 5000),
    ]
    result = signal(3000, history)
    assert result["signal"] == "insufficient_history"
    assert result["stats"]["listings"] == 3
