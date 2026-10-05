from hhw.enterprise_score import score_enterprise
from hhw.models import Candidate


def c(currency="EUR", price=500, hardware=None):
    return Candidate(vendor_id="x", title="x", url="https://example.invalid", currency=currency,
                     item_price=price, hardware=hardware or {})


def test_eur_never_gets_nok_price_bonus():
    x = score_enterprise(c(hardware={"memory_gb": 64}), "proxmox_compute")
    assert x["price_scored"] is False
    assert "price_not_nok_comparable" in x["reasons"]


def test_storage_lff_hba_25gbe_is_strong():
    x = score_enterprise(c(hardware={
        "memory_gb": 64,
        "drive_bays": {"count": 12, "size_in": 3.5},
        "storage_controller": "HBA330",
        "network_max_gbps": 25,
    }), "storage")
    assert x["score"] >= 95


def test_nok_price_can_score():
    x = score_enterprise(c(currency="NOK", price=4500, hardware={"memory_gb": 64}), "proxmox_compute")
    assert x["price_scored"] is True
    assert "nok<=5000" in x["reasons"]
