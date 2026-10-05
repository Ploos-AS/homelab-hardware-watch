from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date


@dataclass(frozen=True)
class ComponentCostEvidence:
    component: str
    evidence_key: str
    cost_nok: float
    observed_on: date
    source: str
    note: str = ""

    def __post_init__(self) -> None:
        if self.cost_nok < 0:
            raise ValueError("component evidence cost must be >= 0")
        if not self.evidence_key.strip():
            raise ValueError("component evidence key must not be empty")

    def to_dict(self) -> dict:
        out = asdict(self)
        out["observed_on"] = self.observed_on.isoformat()
        return out


def latest_component_cost(
    observations: list[ComponentCostEvidence],
    component: str,
    evidence_key: str,
    on_date: date,
) -> ComponentCostEvidence | None:
    matches = [
        x for x in observations
        if x.component == component
        and x.evidence_key == evidence_key
        and x.observed_on <= on_date
    ]
    return max(matches, key=lambda x: x.observed_on) if matches else None
