from hhw.models import Candidate
from hhw.ups_score import score_ups, ups_action


def c(price=1000, hardware=None, currency="NOK"):
    return Candidate(
        vendor_id="x", title="UPS", url="https://example.invalid",
        currency=currency, item_price=price, hardware=hardware or {},
    )


GOOD = {
    "output_watts": 1500,
    "ups_topology": "line_interactive",
    "replaceable_battery": True,
    "management_interfaces": ["usb", "snmp"],
    "nut_compatible": True,
}


def test_good_enterprise_ups_at_low_price_is_buy():
    result = score_ups(c(1000, GOOD))
    assert result["effective_cost_nok"] == 1000
    assert ups_action(result) == "BUY"


def test_dead_battery_is_costed_not_automatically_rejected():
    hw = {**GOOD, "battery_replacement_required": True, "required_battery_replacement_nok": 1800}
    result = score_ups(c(500, hw))
    assert result["effective_cost_nok"] == 2300
    assert ups_action(result) == "BUY"


def test_unknown_required_battery_cost_blocks_price_decision():
    hw = {**GOOD, "battery_replacement_required": True}
    result = score_ups(c(500, hw))
    assert result["price_scored"] is False
    assert result["effective_cost_nok"] is None
    assert "battery_replacement_cost_unknown" in result["reasons"]
    assert ups_action(result) == "WATCH"


def test_non_serviceable_battery_is_penalized():
    hw = {**GOOD, "replaceable_battery": False}
    result = score_ups(c(1000, hw))
    assert "battery_not_serviceable" in result["reasons"]
    assert ups_action(result) != "BUY"


def test_expensive_replacement_battery_can_remove_bargain():
    hw = {**GOOD, "battery_replacement_required": True, "required_battery_replacement_nok": 5000}
    result = score_ups(c(500, hw))
    assert result["effective_cost_nok"] == 5500
    assert ups_action(result) == "WATCH"


def test_estimated_import_cannot_auto_buy():
    x = c(100, GOOD, currency="EUR")
    x.metadata["delivered_cost"] = {"cost_status": "estimate", "estimated_delivered_nok": 1000}
    result = score_ups(x)
    assert result["score"] >= 60
    assert ups_action(result) == "WATCH"
