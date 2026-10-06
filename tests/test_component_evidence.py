from datetime import date

import pytest

from hhw.component_evidence import ComponentCostEvidence, latest_component_cost
from hhw.component_evidence_store import load_component_evidence, save_component_evidence


def ev(key: str, day: int, cost: float = 700) -> ComponentCostEvidence:
    return ComponentCostEvidence(
        component="rails",
        evidence_key=key,
        cost_nok=cost,
        observed_on=date(2026, 10, day),
        source="test",
    )


def test_latest_component_cost_uses_latest_not_after_candidate_date():
    observations = [ev("dell_r730_rails", 1, 600), ev("dell_r730_rails", 5, 800)]
    found = latest_component_cost(observations, "rails", "dell_r730_rails", date(2026, 10, 3))
    assert found is not None
    assert found.cost_nok == 600


def test_future_evidence_is_never_used():
    assert latest_component_cost([ev("dell_r730_rails", 5)], "rails", "dell_r730_rails", date(2026, 10, 3)) is None


def test_component_and_key_must_both_match():
    observations = [ev("dell_r730_rails", 1)]
    assert latest_component_cost(observations, "caddies", "dell_r730_rails", date(2026, 10, 5)) is None
    assert latest_component_cost(observations, "rails", "dell_r740_rails", date(2026, 10, 5)) is None


def test_store_roundtrip(tmp_path):
    path = tmp_path / "components.json"
    original = [ev("dell_r730_rails", 1, 650)]
    save_component_evidence(path, original)
    assert load_component_evidence(path) == original


def test_negative_cost_rejected():
    with pytest.raises(ValueError):
        ev("dell_r730_rails", 1, -1)


def test_empty_key_rejected():
    with pytest.raises(ValueError):
        ev(" ", 1, 100)
