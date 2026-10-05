from hhw.models import Candidate
from hhw.switch_score import managed_switch_action, score_managed_switch


def c(price=2000, hardware=None, currency="NOK"):
    return Candidate(
        vendor_id="x", title="managed switch", url="https://example.invalid",
        currency=currency, item_price=price, hardware=hardware or {},
    )


CORE = {
    "managed": True,
    "vlan": True,
    "lacp": True,
    "uplink_max_gbps": 10,
    "ports_10gbe": 4,
    "access_ports": 24,
}


def test_good_10gbe_managed_switch_can_be_buy():
    result = score_managed_switch(c(2000, CORE))
    assert result["score"] >= 60
    assert managed_switch_action(result) == "BUY"


def test_25gbe_gets_stronger_network_value():
    fast = score_managed_switch(c(2000, {**CORE, "uplink_max_gbps": 25, "ports_25gbe": 4}))
    ten = score_managed_switch(c(2000, CORE))
    assert fast["score"] > ten["score"]


def test_model_name_alone_does_not_create_buy():
    result = score_managed_switch(c(1000, {}))
    assert managed_switch_action(result) == "PASS"


def test_no_10gbe_cannot_auto_buy():
    result = score_managed_switch(c(1000, {
        "managed": True, "vlan": True, "lacp": True,
        "uplink_max_gbps": 2.5, "access_ports": 48, "fanless": True,
    }))
    assert managed_switch_action(result) != "BUY"


def test_noisy_power_hungry_enterprise_switch_is_penalized():
    quiet = score_managed_switch(c(2000, CORE))
    noisy = score_managed_switch(c(2000, {**CORE, "noise_class": "high", "idle_power_watts": 120}))
    assert noisy["score"] == quiet["score"] - 25


def test_estimated_import_cannot_auto_buy():
    x = c(100, CORE, currency="EUR")
    x.metadata["delivered_cost"] = {"cost_status": "estimate", "estimated_delivered_nok": 1500}
    result = score_managed_switch(x)
    assert result["score"] >= 60
    assert managed_switch_action(result) == "WATCH"
