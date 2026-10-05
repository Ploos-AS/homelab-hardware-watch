from __future__ import annotations

from datetime import date
import requests

from hhw.fx import FxObservation

URL = "https://data.toll.no/dataset/340b660f-acdd-4155-9909-dde72144d093/resource/4677ff8a-5fa7-47b8-be58-65418dd10fce/download/valutakurs.json"


def parse_current(payload: dict, currency: str, on_date: date) -> FxObservation | None:
    for row in payload.get("omregningskurser", []):
        if row.get("valutakode") != currency:
            continue
        start = date.fromisoformat(row["fomdato"])
        end_text = row.get("tomdato") or ""
        end = date.fromisoformat(end_text) if end_text else date.max
        if start <= on_date <= end:
            rate = float(row["valutakurs"].replace(",", ".")) / float(row["omregningsenhet"])
            return FxObservation(currency, "NOK", rate, on_date, "tolletaten")
    return None


def fetch_current(currency: str, on_date: date | None = None) -> FxObservation | None:
    day = on_date or date.today()
    response = requests.get(URL, timeout=30, headers={"User-Agent": "homelab-hardware-watch/0.3"})
    response.raise_for_status()
    return parse_current(response.json(), currency, day)
