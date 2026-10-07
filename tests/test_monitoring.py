from hhw.models import Candidate
from hhw.monitoring import candidate_id, changes, snapshot


def c(price=500, delivered=None, status="estimate"):
    x = Candidate("vendor", "server", "https://example.invalid/item/1", currency="EUR",
                  item_price=price, hardware={"memory_gb": 64})
    if delivered is not None:
        key = "import_confirmed_delivered_nok" if status == "import_confirmed" else "estimated_delivered_nok"
        x.metadata["delivered_cost"] = {"cost_status": status, key: delivered}
    return x


def test_candidate_id_is_stable_across_price_changes():
    assert candidate_id(c(500)) == candidate_id(c(450))


def test_new_candidate_event():
    assert changes(None, snapshot(c())) == ["new_candidate"]


def test_unchanged_candidate_is_silent():
    s = snapshot(c())
    assert changes(s, s) == []


def test_delivered_price_drop_is_detected():
    old = snapshot(c(delivered=6000))
    new = snapshot(c(delivered=5000))
    assert "delivered_price_down" in changes(old, new)


def test_item_price_drop_fallback_is_detected():
    assert "item_price_down" in changes(snapshot(c(500)), snapshot(c(450)))


def test_becoming_buy_is_explicit():
    old = snapshot(c(delivered=8000, status="import_confirmed"), "proxmox_compute")
    buy = c(delivered=2500, status="import_confirmed")
    buy.hardware.update({"cpu_threads": 32, "memory_gb": 128})
    new = snapshot(buy, "proxmox_compute")
    events = changes(old, new)
    assert "action_changed" in events
    assert "became_buy" in events


def test_runner_watch_to_buy_transition_is_explicit():
    old = Candidate(
        "vendor", "Tiny", "https://example.invalid/tiny", currency="NOK",
        item_price=1900, hardware={"memory_gb": 16},
        metadata={
            "runner_family": "generic_tiny",
            "configuration_parity": {"comparable": True, "adjusted_price_nok": 1900},
        },
    )
    new = Candidate(
        "vendor", "Tiny", "https://example.invalid/tiny", currency="NOK",
        item_price=1400, hardware={"memory_gb": 16},
        metadata={
            "runner_family": "generic_tiny",
            "configuration_parity": {"comparable": True, "adjusted_price_nok": 1400},
        },
    )
    before = snapshot(old, "linux_ci")
    after = snapshot(new, "linux_ci")
    assert before.action == "WATCH"
    assert after.action == "BUY"
    assert "became_buy" in changes(before, after)


def test_switch_decision_is_available_to_monitor():
    switch = Candidate(
        "vendor", "Switch", "https://example.invalid/switch", currency="NOK",
        item_price=1500,
        hardware={
            "managed": True, "vlan": True, "lacp": True,
            "uplink_max_gbps": 25, "ports_25gbe": 4,
        },
    )
    assert snapshot(switch, "managed_switch").action == "BUY"


def test_ups_decision_is_available_to_monitor():
    ups = Candidate(
        "vendor", "UPS", "https://example.invalid/ups", currency="NOK",
        item_price=1000,
        hardware={
            "output_watts": 1500,
            "ups_topology": "line_interactive",
            "replaceable_battery": True,
            "management_interfaces": ["usb", "snmp"],
            "nut_compatible": True,
        },
    )
    assert snapshot(ups, "ups").action == "BUY"



def test_bargain_transition_is_explicit():
    old = c(500)
    old.metadata["bargain"] = {"signal": "normal"}
    new = c(400)
    new.metadata["bargain"] = {"signal": "bargain"}
    assert "became_bargain" in changes(snapshot(old), snapshot(new))


def test_exceptional_transition_is_explicit():
    old = c(400)
    old.metadata["bargain"] = {"signal": "bargain"}
    new = c(300)
    new.metadata["bargain"] = {"signal": "exceptional"}
    assert "became_exceptional" in changes(snapshot(old), snapshot(new))
