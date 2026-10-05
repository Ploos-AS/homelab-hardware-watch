from hhw.models import Candidate
from hhw.parity import configuration_parity


def item(price, memory):
    return Candidate(
        vendor_id="x",
        title="Tiny",
        url="https://example.invalid",
        item_price=price,
        hardware={"memory_gb": memory},
    )


def test_8gb_gets_upgrade_cost():
    result = configuration_parity(item(1500, 8))
    assert result["adjusted_price_nok"] == 1900
    assert result["adjustments"][0]["to_gb"] == 16


def test_16gb_needs_no_memory_adjustment():
    result = configuration_parity(item(1600, 16))
    assert result["adjusted_price_nok"] == 1600
    assert result["adjustments"] == []


def test_unknown_memory_is_not_comparable():
    result = configuration_parity(item(1500, None))
    assert result["comparable"] is False
    assert result["reason"] == "memory_unknown"
