from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from hhw.component_evidence import ComponentCostEvidence


def load_component_evidence(path: str | Path) -> list[ComponentCostEvidence]:
    p = Path(path)
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return [
        ComponentCostEvidence(
            component=x["component"],
            evidence_key=x["evidence_key"],
            cost_nok=float(x["cost_nok"]),
            observed_on=date.fromisoformat(x["observed_on"]),
            source=x["source"],
            note=x.get("note", ""),
        )
        for x in data.get("observations", [])
    ]


def save_component_evidence(path: str | Path, observations: list[ComponentCostEvidence]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(
        observations,
        key=lambda x: (x.component, x.evidence_key, x.observed_on, x.source),
    )
    p.write_text(
        json.dumps({"observations": [x.to_dict() for x in ordered]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def merge_component_evidence(existing, incoming):
    """Deterministically deduplicate observations without losing history."""
    by_key = {
        (x.component, x.evidence_key, x.observed_on, x.source): x
        for x in [*existing, *incoming]
    }
    return sorted(
        by_key.values(),
        key=lambda x: (x.component, x.evidence_key, x.observed_on, x.source),
    )
