from __future__ import annotations

from dataclasses import replace
from datetime import date

from hhw.component_cost import MissingComponent, missing_components
from hhw.component_evidence import ComponentCostEvidence, latest_component_cost
from hhw.models import Candidate


def enrich_component_costs(
    candidate: Candidate,
    observations: list[ComponentCostEvidence],
    observed_on: date,
) -> Candidate:
    """Fill unknown component costs from exact, historical evidence.

    Direct candidate cost evidence always wins. Components without an explicit
    evidence_key remain unknown; no generic component-price fallback is used.
    """
    enriched: list[dict] = []
    for component in missing_components(candidate):
        cost = component.cost_nok
        source = None
        evidence_date = None

        if cost is None and component.evidence_key:
            evidence = latest_component_cost(
                observations,
                component.component,
                component.evidence_key,
                observed_on,
            )
            if evidence is not None:
                cost = evidence.cost_nok
                source = evidence.source
                evidence_date = evidence.observed_on.isoformat()

        value = {
            "component": component.component,
            "required": component.required,
            "cost_nok": cost,
            "quantity": component.quantity,
        }
        if component.note is not None:
            value["note"] = component.note
        if component.evidence_key is not None:
            value["evidence_key"] = component.evidence_key
        if source is not None:
            value["cost_evidence_source"] = source
            value["cost_evidence_observed_on"] = evidence_date
        enriched.append(value)

    metadata = dict(candidate.metadata or {})
    if enriched:
        metadata["missing_components"] = enriched
    return replace(candidate, metadata=metadata)
