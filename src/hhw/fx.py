from __future__ import annotations
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class FxObservation:
    base: str
    quote: str
    rate: float
    observed_on: date
    source: str


def rate_to_nok(currency: str, observations: list[FxObservation], on_date: date) -> FxObservation | None:
    if currency == "NOK":
        return FxObservation("NOK", "NOK", 1.0, on_date, "identity")

    matches = [
        x for x in observations
        if x.base == currency and x.quote == "NOK" and x.observed_on <= on_date
    ]
    if not matches:
        return None
    source_priority = {
        "tolletaten": 100,
        "norges_bank": 50,
    }
    return max(
        matches,
        key=lambda x: (x.observed_on, source_priority.get(x.source.lower(), 0)),
    )
