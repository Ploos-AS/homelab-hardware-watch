from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date
import hashlib

from hhw.families import bargain_family_key
from hhw.models import Candidate


def listing_id(candidate: Candidate) -> str:
    """Stable identity for one vendor listing across collection runs."""
    raw = f"{candidate.vendor_id}\0{candidate.url}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:20]


@dataclass(frozen=True)
class PriceObservation:
    listing_id: str
    vendor_id: str
    url: str
    observed_on: date
    item_price: float | None
    currency: str
    delivered_nok: float | None = None
    family_key: str | None = None

    @classmethod
    def from_candidate(cls, candidate: Candidate, observed_on: date) -> "PriceObservation":
        cost = (candidate.metadata or {}).get("delivered_cost") or {}
        delivered = (
            cost.get("import_confirmed_delivered_nok")
            if cost.get("cost_status") == "import_confirmed"
            else cost.get("estimated_delivered_nok")
        )
        return cls(
            listing_id=listing_id(candidate),
            vendor_id=candidate.vendor_id,
            url=candidate.url,
            observed_on=observed_on,
            item_price=candidate.item_price,
            currency=candidate.currency,
            delivered_nok=None if delivered is None else float(delivered),
            family_key=bargain_family_key(candidate.title),
        )

    def to_dict(self) -> dict:
        value = asdict(self)
        value["observed_on"] = self.observed_on.isoformat()
        return value
