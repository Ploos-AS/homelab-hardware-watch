from datetime import date
from hhw.fx import FxObservation, rate_to_nok


def test_latest_rate_not_after_observation_date():
    rates = [
        FxObservation("EUR", "NOK", 11.0, date(2026, 1, 1), "test"),
        FxObservation("EUR", "NOK", 12.0, date(2026, 2, 1), "test"),
    ]
    assert rate_to_nok("EUR", rates, date(2026, 1, 15)).rate == 11.0
