from datetime import date

from hhw.component_cost import ready_cost
from hhw.component_enrich import enrich_component_costs
from hhw.component_evidence import ComponentCostEvidence
from hhw.models import Candidate
from hhw.normalize import normalize_title


def test_listing_to_historical_evidence_to_ready_cost():
    candidate = Candidate(
        vendor_id="test",
        title="Dell R730 64GB RAM without rails",
        url="https://example.invalid/r730",
        currency="NOK",
        item_price=2500,
        condition="used",
    )
    candidate = normalize_title(candidate)

    evidence = [
        ComponentCostEvidence(
            component="rails",
            evidence_key="dell_r730_rails",
            cost_nok=700,
            observed_on=date(2026, 10, 1),
            source="vendor quote",
        ),
        ComponentCostEvidence(
            component="rails",
            evidence_key="dell_r730_rails",
            cost_nok=900,
            observed_on=date(2026, 10, 10),
            source="future quote",
        ),
    ]

    candidate = enrich_component_costs(candidate, evidence, date(2026, 10, 5))
    missing = candidate.metadata["missing_components"][0]
    cost = ready_cost(candidate)

    assert missing["evidence_key"] == "dell_r730_rails"
    assert missing["cost_nok"] == 700
    assert missing["cost_evidence_source"] == "vendor quote"
    assert cost["comparable"] is True
    assert cost["base_price_nok"] == 2500
    assert cost["component_cost_nok"] == 700
    assert cost["ready_cost_nok"] == 3200


def test_listing_without_compatible_model_stays_fail_closed():
    candidate = Candidate(
        vendor_id="test",
        title="Dell server without rails",
        url="https://example.invalid/server",
        currency="NOK",
        item_price=2500,
    )
    candidate = normalize_title(candidate)
    candidate = enrich_component_costs(
        candidate,
        [
            ComponentCostEvidence(
                component="rails",
                evidence_key="dell_r730_rails",
                cost_nok=700,
                observed_on=date(2026, 10, 1),
                source="vendor quote",
            )
        ],
        date(2026, 10, 5),
    )

    cost = ready_cost(candidate)
    assert cost["comparable"] is False
    assert cost["reason"] == "required_component_cost_unknown"
    assert cost["unknown_required_costs"] == ["rails"]
