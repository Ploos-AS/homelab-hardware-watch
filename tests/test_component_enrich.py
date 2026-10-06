from datetime import date

from hhw.component_enrich import enrich_component_costs
from hhw.component_evidence import ComponentCostEvidence
from hhw.models import Candidate


def candidate(missing):
    return Candidate(
        vendor_id="test",
        title="Dell R730",
        url="https://example.invalid/item",
        currency="NOK",
        item_price=2500,
        stock_status="in_stock",
        condition="used",
        metadata={"missing_components": missing},
    )


def evidence(day=1, cost=700):
    return ComponentCostEvidence(
        component="rails",
        evidence_key="dell_r730_rails",
        cost_nok=cost,
        observed_on=date(2026, 10, day),
        source="test-source",
    )


def test_exact_evidence_key_fills_unknown_cost():
    c = candidate([{"component": "rails", "evidence_key": "dell_r730_rails"}])
    out = enrich_component_costs(c, [evidence()], date(2026, 10, 2))
    item = out.metadata["missing_components"][0]
    assert item["cost_nok"] == 700
    assert item["cost_evidence_source"] == "test-source"


def test_direct_candidate_cost_wins_over_store():
    c = candidate([{"component": "rails", "evidence_key": "dell_r730_rails", "cost_nok": 500}])
    out = enrich_component_costs(c, [evidence(cost=900)], date(2026, 10, 2))
    item = out.metadata["missing_components"][0]
    assert item["cost_nok"] == 500
    assert "cost_evidence_source" not in item


def test_future_evidence_does_not_fill_cost():
    c = candidate([{"component": "rails", "evidence_key": "dell_r730_rails"}])
    out = enrich_component_costs(c, [evidence(day=5)], date(2026, 10, 2))
    assert out.metadata["missing_components"][0]["cost_nok"] is None


def test_unmatched_key_remains_unknown():
    c = candidate([{"component": "rails", "evidence_key": "dell_r740_rails"}])
    out = enrich_component_costs(c, [evidence()], date(2026, 10, 2))
    assert out.metadata["missing_components"][0]["cost_nok"] is None


def test_no_key_remains_unknown():
    c = candidate([{"component": "rails"}])
    out = enrich_component_costs(c, [evidence()], date(2026, 10, 2))
    assert out.metadata["missing_components"][0]["cost_nok"] is None


def test_quantity_is_preserved():
    c = candidate([{"component": "caddies", "quantity": 4, "cost_nok": 100}])
    out = enrich_component_costs(c, [], date(2026, 10, 2))
    assert out.metadata["missing_components"][0]["quantity"] == 4
