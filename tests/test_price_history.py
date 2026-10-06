from datetime import date

from hhw.models import Candidate
from hhw.price_history import PriceObservation, listing_id
from hhw.price_history_store import load_price_history, merge_price_history, save_price_history


def candidate(price=1000, delivered=None):
    c = Candidate(
        vendor_id="vendor",
        title="server",
        url="https://example.invalid/listing/42",
        currency="NOK",
        item_price=price,
    )
    if delivered is not None:
        c.metadata["delivered_cost"] = {
            "cost_status": "import_confirmed",
            "import_confirmed_delivered_nok": delivered,
        }
    return c


def test_listing_id_is_stable_for_vendor_and_url():
    a = candidate(1000)
    b = candidate(900)
    b.title = "renamed listing"
    assert listing_id(a) == listing_id(b)


def test_observation_captures_candidate_price():
    observation = PriceObservation.from_candidate(candidate(1000, 1250), date(2026, 10, 6))
    assert observation.item_price == 1000
    assert observation.delivered_nok == 1250
    assert observation.observed_on == date(2026, 10, 6)


def test_store_roundtrip(tmp_path):
    path = tmp_path / "history.json"
    original = [PriceObservation.from_candidate(candidate(), date(2026, 10, 6))]
    save_price_history(path, original)
    assert load_price_history(path) == original


def test_missing_store_loads_empty(tmp_path):
    assert load_price_history(tmp_path / "missing.json") == []


def test_merge_preserves_different_days():
    first = PriceObservation.from_candidate(candidate(1000), date(2026, 10, 5))
    second = PriceObservation.from_candidate(candidate(900), date(2026, 10, 6))
    merged = merge_price_history([first], [second])
    assert [x.item_price for x in merged] == [1000, 900]


def test_same_listing_and_day_is_replaced_by_incoming():
    old = PriceObservation.from_candidate(candidate(1000), date(2026, 10, 6))
    new = PriceObservation.from_candidate(candidate(900), date(2026, 10, 6))
    merged = merge_price_history([old], [new])
    assert len(merged) == 1
    assert merged[0].item_price == 900


def test_different_listings_same_day_are_preserved():
    a = candidate(1000)
    b = Candidate("vendor", "other", "https://example.invalid/listing/99", item_price=800)
    day = date(2026, 10, 6)
    merged = merge_price_history(
        [PriceObservation.from_candidate(a, day)],
        [PriceObservation.from_candidate(b, day)],
    )
    assert len(merged) == 2
