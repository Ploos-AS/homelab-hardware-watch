from datetime import date
from hhw.fx import FxObservation, rate_to_nok


def test_latest_rate_not_after_observation_date():
    rates = [
        FxObservation("EUR", "NOK", 11.0, date(2026, 1, 1), "test"),
        FxObservation("EUR", "NOK", 12.0, date(2026, 2, 1), "test"),
    ]
    assert rate_to_nok("EUR", rates, date(2026, 1, 15)).rate == 11.0


def test_tolletaten_wins_equal_date_for_import_costing():
    rates = [
        FxObservation("EUR", "NOK", 10.5, date(2026, 10, 1), "norges_bank"),
        FxObservation("EUR", "NOK", 10.7, date(2026, 10, 1), "tolletaten"),
    ]
    chosen = rate_to_nok("EUR", rates, date(2026, 10, 1))
    assert chosen.source == "tolletaten"
    assert chosen.rate == 10.7


def test_newer_market_rate_still_beats_older_customs_rate():
    rates = [
        FxObservation("EUR", "NOK", 10.7, date(2026, 10, 1), "tolletaten"),
        FxObservation("EUR", "NOK", 10.6, date(2026, 10, 2), "norges_bank"),
    ]
    chosen = rate_to_nok("EUR", rates, date(2026, 10, 2))
    assert chosen.source == "norges_bank"
