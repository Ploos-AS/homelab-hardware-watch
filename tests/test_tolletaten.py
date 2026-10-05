from datetime import date

from hhw.providers.tolletaten import parse_current


PAYLOAD = {"omregningskurser": [
    {"valutakode": "EUR", "valutakurs": "10,767", "omregningsenhet": 1,
     "fomdato": "2026-10-01", "tomdato": "2026-10-14"},
    {"valutakode": "EUR", "valutakurs": "10,817", "omregningsenhet": 1,
     "fomdato": "2026-10-15", "tomdato": "2026-10-28"},
    {"valutakode": "SEK", "valutakurs": "95,440", "omregningsenhet": 100,
     "fomdato": "2026-10-01", "tomdato": "2026-10-14"},
]}


def test_current_eur_customs_rate():
    x = parse_current(PAYLOAD, "EUR", date(2026, 10, 5))
    assert x.rate == 10.767
    assert x.source == "tolletaten"


def test_future_period_not_used_early():
    x = parse_current(PAYLOAD, "EUR", date(2026, 10, 15))
    assert x.rate == 10.817


def test_conversion_unit_is_applied():
    x = parse_current(PAYLOAD, "SEK", date(2026, 10, 5))
    assert x.rate == 0.9544


def test_outside_published_period_is_unknown():
    assert parse_current(PAYLOAD, "EUR", date(2026, 11, 1)) is None
