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


def test_estimated_delivered_price_scores_with_penalty():
    x = c(hardware={"memory_gb": 64})
    x.metadata["delivered_cost"] = {
        "cost_status": "estimate",
        "estimated_delivered_nok": 4500,
    }
    result = score_enterprise(x, "proxmox_compute")
    assert result["price_scored"] is True
    assert result["price_confidence"] == "estimate"
    assert "estimated_delivered_price_penalty" in result["reasons"]
    assert result["score"] == 35  # 20 RAM + (20 price - 5 estimate penalty)


def test_import_confirmed_price_gets_full_price_points():
    x = c(hardware={"memory_gb": 64})
    x.metadata["delivered_cost"] = {
        "cost_status": "import_confirmed",
        "import_confirmed_delivered_nok": 4500,
    }
    result = score_enterprise(x, "proxmox_compute")
    assert result["price_confidence"] == "import_confirmed"
    assert "estimated_delivered_price_penalty" not in result["reasons"]
    assert result["score"] == 40


def test_expensive_import_confirmed_server_gets_cost_penalty():
    x = c(hardware={"memory_gb": 64})
    x.metadata["delivered_cost"] = {
        "cost_status": "import_confirmed",
        "import_confirmed_delivered_nok": 11465,
    }
    result = score_enterprise(x, "proxmox_compute")
    assert result["price_confidence"] == "import_confirmed"
    assert "delivered_nok>9000_penalty" in result["reasons"]
    assert result["score"] == 5  # 20 RAM - 15 delivered-cost penalty


def test_very_expensive_server_gets_stronger_penalty():
    x = c(hardware={"memory_gb": 64})
    x.metadata["delivered_cost"] = {
        "cost_status": "import_confirmed",
        "import_confirmed_delivered_nok": 13000,
    }
    result = score_enterprise(x, "proxmox_compute")
    assert "delivered_nok>12000_penalty" in result["reasons"]
    assert result["score"] == 0
