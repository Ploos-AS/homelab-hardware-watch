from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class VendorEvidence:
    vendor_id: str
    observed_on: date
    evidence_type: str
    source: str
    values: dict[str, Any]
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        out = asdict(self)
        out["observed_on"] = self.observed_on.isoformat()
        return out


def latest_evidence(
    observations: list[VendorEvidence],
    vendor_id: str,
    evidence_type: str,
    on_date: date,
) -> VendorEvidence | None:
    matches = [
        x for x in observations
        if x.vendor_id == vendor_id
        and x.evidence_type == evidence_type
        and x.observed_on <= on_date
    ]
    return max(matches, key=lambda x: x.observed_on) if matches else None
