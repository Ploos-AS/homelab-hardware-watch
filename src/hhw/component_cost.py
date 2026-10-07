from __future__ import annotations

from dataclasses import dataclass

from hhw.price_signal import raw_price_signal
from hhw.models import Candidate


KNOWN_COMPONENTS = {
    "memory", "hba", "nic", "rails", "caddies", "psu", "gpu", "kvm_interface_module",
}


@dataclass(frozen=True)
class MissingComponent:
    component: str
    required: bool = True
    cost_nok: float | None = None
    quantity: int = 1
    note: str | None = None
    evidence_key: str | None = None

    @classmethod
    def from_dict(cls, value: dict) -> "MissingComponent":
        component = str(value["component"]).lower()
        if component not in KNOWN_COMPONENTS:
            raise ValueError(f"unknown missing component: {component}")
        quantity = int(value.get("quantity", 1))
        if quantity < 1:
            raise ValueError("component quantity must be >= 1")
        cost = value.get("cost_nok")
        if cost is not None and float(cost) < 0:
            raise ValueError("component cost must be >= 0")
        return cls(
            component=component,
            required=bool(value.get("required", True)),
            cost_nok=None if cost is None else float(cost),
            quantity=quantity,
            note=value.get("note"),
            evidence_key=value.get("evidence_key"),
        )


def missing_components(candidate: Candidate) -> list[MissingComponent]:
    raw = (candidate.metadata or {}).get("missing_components") or []
    return [MissingComponent.from_dict(x) for x in raw]


def ready_cost(candidate: Candidate) -> dict:
    """Cost to make a listing usable for its intended role.

    Only required missing components affect comparability. Optional upgrades are
    retained as evidence but do not block or inflate the ready cost.
    """
    base_price, confidence = raw_price_signal(candidate)
    components = missing_components(candidate)
    required = [x for x in components if x.required]
    unknown = [x.component for x in required if x.cost_nok is None]

    if base_price is None:
        return {
            "comparable": False,
            "reason": "base_price_not_nok_comparable",
            "base_price_nok": None,
            "component_cost_nok": None,
            "ready_cost_nok": None,
            "price_confidence": confidence,
            "missing_components": components,
            "unknown_required_costs": unknown,
        }

    if unknown:
        return {
            "comparable": False,
            "reason": "required_component_cost_unknown",
            "base_price_nok": base_price,
            "component_cost_nok": None,
            "ready_cost_nok": None,
            "price_confidence": confidence,
            "missing_components": components,
            "unknown_required_costs": sorted(set(unknown)),
        }

    component_cost = sum((x.cost_nok or 0.0) * x.quantity for x in required)
    return {
        "comparable": True,
        "reason": None,
        "base_price_nok": base_price,
        "component_cost_nok": component_cost,
        "ready_cost_nok": base_price + component_cost,
        "price_confidence": confidence,
        "missing_components": components,
        "unknown_required_costs": [],
    }
