from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from hhw.price_history import PriceObservation


def load_price_history(path: str | Path) -> list[PriceObservation]:
    path = Path(path)
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        PriceObservation(
            listing_id=x["listing_id"],
            vendor_id=x["vendor_id"],
            url=x["url"],
            observed_on=date.fromisoformat(x["observed_on"]),
            item_price=x.get("item_price"),
            currency=x["currency"],
            delivered_nok=x.get("delivered_nok"),
        )
        for x in payload.get("observations", [])
    ]


def merge_price_history(
    existing: list[PriceObservation],
    incoming: list[PriceObservation],
) -> list[PriceObservation]:
    """Merge observations, replacing the same listing/day with the newest input."""
    merged = {(x.listing_id, x.observed_on): x for x in existing}
    for observation in incoming:
        merged[(observation.listing_id, observation.observed_on)] = observation
    return sorted(
        merged.values(),
        key=lambda x: (x.observed_on, x.vendor_id, x.listing_id),
    )


def save_price_history(path: str | Path, observations: list[PriceObservation]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(
        observations,
        key=lambda x: (x.observed_on, x.vendor_id, x.listing_id),
    )
    payload = {"observations": [x.to_dict() for x in ordered]}
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
