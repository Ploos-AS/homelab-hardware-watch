from hhw.ai_score import ai_host_action, score_ai_host
from hhw.models import Candidate


def c(price=5000, hardware=None, currency="NOK"):
    return Candidate(
        vendor_id="x", title="workstation", url="https://example.invalid",
        currency=currency, item_price=price, hardware=hardware or {},
    )


def test_24gb_gpu_dominates_ai_score():
    result = score_ai_host(c(8000, {"gpu_vram_gb": 24, "memory_gb": 64}))
    assert result["score"] >= 60
    assert ai_host_action(result) == "BUY"


def test_expandable_gpu_less_workstation_can_be_watch():
    result = score_ai_host(c(5000, {
        "pcie_full_length_slots": 2,
        "psu_watts": 1000,
        "gpu_power_connectors_suitable": True,
        "gpu_full_length_clearance": True,
        "memory_gb": 64,
    }))
    assert result["score"] >= 60
    assert ai_host_action(result) == "BUY"


def test_cpu_and_ram_alone_do_not_make_ai_host_attractive():
    result = score_ai_host(c(5000, {"cpu_count": 2, "memory_gb": 128}))
    assert result["score"] < 30
    assert ai_host_action(result) == "PASS"


def test_no_gpu_clearance_and_power_is_penalized():
    result = score_ai_host(c(4000, {
        "memory_gb": 64,
        "gpu_full_length_clearance": False,
        "gpu_power_connectors_suitable": False,
    }))
    assert result["score"] < 0
    assert ai_host_action(result) == "PASS"


def test_estimated_import_cannot_auto_buy():
    x = c(500, {
        "gpu_vram_gb": 24,
        "memory_gb": 64,
    }, currency="EUR")
    x.metadata["delivered_cost"] = {
        "cost_status": "estimate",
        "estimated_delivered_nok": 5000,
    }
    result = score_ai_host(x)
    assert result["score"] >= 60
    assert result["price_confidence"] == "estimate"
    assert ai_host_action(result) == "WATCH"


def test_import_confirmed_can_buy():
    x = c(500, {"gpu_vram_gb": 24, "memory_gb": 64}, currency="EUR")
    x.metadata["delivered_cost"] = {
        "cost_status": "import_confirmed",
        "import_confirmed_delivered_nok": 5000,
    }
    result = score_ai_host(x)
    assert ai_host_action(result) == "BUY"


def test_expensive_gpu_less_host_is_penalized():
    result = score_ai_host(c(16000, {
        "pcie_full_length_slots": 1,
        "psu_watts": 750,
        "memory_gb": 32,
    }))
    assert "expensive_gpu_less_host" in result["reasons"]
    assert ai_host_action(result) == "PASS"


def test_cheap_gpu_incapable_host_gets_no_price_bonus():
    result = score_ai_host(c(7000, {"memory_gb": 64}))
    assert result["score"] == 10
    assert ai_host_action(result) == "PASS"
