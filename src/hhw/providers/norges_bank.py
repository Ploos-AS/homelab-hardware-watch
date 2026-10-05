from __future__ import annotations

import csv
import io
from datetime import date

import requests

from hhw.fx import FxObservation


API = "https://data.norges-bank.no/api/data/EXR/B.{currency}.NOK.SP"


def fetch_daily(currency: str, start: date, end: date) -> list[FxObservation]:
    currency = currency.upper()
    url = API.format(currency=currency)
    r = requests.get(url, params={
        "format": "csv",
        "startPeriod": start.isoformat(),
        "endPeriod": end.isoformat(),
        "locale": "en",
    }, timeout=30, headers={"User-Agent": "homelab-hardware-watch/0.3"})
    r.raise_for_status()
    return parse_csv(r.text, currency)


def parse_csv(text: str, currency: str) -> list[FxObservation]:
    rows = csv.DictReader(io.StringIO(text), delimiter=";")
    out = []
    for row in rows:
        period = row.get("TIME_PERIOD") or row.get("Time period")
        value = row.get("OBS_VALUE") or row.get("Observation value")
        if not period or not value:
            continue
        try:
            rate = float(value.replace(",", "."))
            observed = date.fromisoformat(period[:10])
        except (ValueError, TypeError):
            continue
        out.append(FxObservation(
            base=currency.upper(),
            quote="NOK",
            rate=rate,
            observed_on=observed,
            source="norges_bank",
        ))
    return out
