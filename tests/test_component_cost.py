import pytest

from hhw.component_cost import MissingComponent, ready_cost
from hhw.models import Candidate


def c(price=2000, missing=None, currency="NOK"):
    return Candidate(
        "x", "hardware", "https://example.invalid",
        currency=currency, item_price=price,
        metadata={"missing_components": missing or []},
    )


def test_complete_candidate_ready_cost_equals_price():
    result = ready_cost(c())
    assert result["comparable"] is True
    assert result["component_cost_nok"] == 0
    assert result["ready_cost_nok"] == 2000


def test_required_components_are_added_with_quantity():
    result = ready_cost(c(missing=[
        {"component": "hba", "cost_nok": 500},
        {"component": "caddies", "cost_nok": 100, "quantity": 4},
        {"component": "rails", "cost_nok": 600},
    ]))
    assert result["component_cost_nok"] == 1500
    assert result["ready_cost_nok"] == 3500


def test_unknown_required_component_cost_fails_closed():
    result = ready_cost(c(missing=[
        {"component": "hba", "cost_nok": 500},
        {"component": "rails"},
    ]))
    assert result["comparable"] is False
    assert result["reason"] == "required_component_cost_unknown"
    assert result["ready_cost_nok"] is None
    assert result["unknown_required_costs"] == ["rails"]


def test_optional_unknown_upgrade_does_not_block_ready_cost():
    result = ready_cost(c(missing=[
        {"component": "gpu", "required": False},
    ]))
    assert result["comparable"] is True
    assert result["ready_cost_nok"] == 2000


def test_import_confirmed_price_is_valid_base():
    x = c(price=100, currency="EUR", missing=[{"component": "nic", "cost_nok": 500}])
    x.metadata["delivered_cost"] = {
        "cost_status": "import_confirmed",
        "import_confirmed_delivered_nok": 3000,
    }
    result = ready_cost(x)
    assert result["price_confidence"] == "import_confirmed"
    assert result["ready_cost_nok"] == 3500


def test_estimated_import_remains_estimated():
    x = c(price=100, currency="EUR")
    x.metadata["delivered_cost"] = {
        "cost_status": "estimate",
        "estimated_delivered_nok": 3000,
    }
    result = ready_cost(x)
    assert result["comparable"] is True
    assert result["price_confidence"] == "estimate"


def test_unknown_component_type_is_rejected():
    with pytest.raises(ValueError, match="unknown missing component"):
        ready_cost(c(missing=[{"component": "mystery", "cost_nok": 1}]))


def test_negative_cost_is_rejected():
    with pytest.raises(ValueError, match="component cost must be >= 0"):
        MissingComponent.from_dict({"component": "psu", "cost_nok": -1})


def test_required_parts_change_enterprise_decision_price():
    from hhw.enterprise_score import score_enterprise

    x = Candidate(
        "x", "server", "https://example.invalid/server",
        currency="NOK", item_price=2500,
        hardware={"memory_gb": 64, "cpu_count": 2},
        metadata={"missing_components": [
            {"component": "hba", "cost_nok": 1000},
            {"component": "rails", "cost_nok": 1500},
        ]},
    )
    result = score_enterprise(x, "proxmox_compute")
    assert result["price_nok"] == 5000
    assert result["ready_cost"]["component_cost_nok"] == 2500


def test_unknown_required_part_blocks_price_scoring():
    from hhw.enterprise_score import score_enterprise

    x = Candidate(
        "x", "server", "https://example.invalid/server",
        currency="NOK", item_price=2500,
        hardware={"memory_gb": 128, "cpu_count": 2},
        metadata={"missing_components": [{"component": "rails"}]},
    )
    result = score_enterprise(x, "proxmox_compute")
    assert result["price_scored"] is False
    assert result["price_nok"] is None
    assert result["ready_cost"]["reason"] == "required_component_cost_unknown"
