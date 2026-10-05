from __future__ import annotations
import json
from datetime import date
from pathlib import Path

from hhw.vendor_evidence import VendorEvidence


def load_vendor_evidence(path: str | Path) -> list[VendorEvidence]:
    p = Path(path)
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return [
        VendorEvidence(
            vendor_id=x["vendor_id"],
            observed_on=date.fromisoformat(x["observed_on"]),
            evidence_type=x["evidence_type"],
            source=x["source"],
            values=x.get("values", {}),
            note=x.get("note", ""),
        )
        for x in data.get("observations", [])
    ]


def save_vendor_evidence(path: str | Path, observations: list[VendorEvidence]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(
        observations,
        key=lambda x: (x.vendor_id, x.evidence_type, x.observed_on, x.source),
    )
    p.write_text(
        json.dumps({"observations": [x.to_dict() for x in ordered]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
