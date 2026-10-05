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
