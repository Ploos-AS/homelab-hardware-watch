from hhw.decision import decide
from hhw.models import Candidate


def c(price, hw):
    return Candidate("used", "hardware", "https://example.invalid/item", item_price=price, hardware=hw)


def test_very_cheap_large_arm_server_is_buy():
    r = decide(c(3000, {"architecture":"arm64","cpu_cores":80,"memory_gb":128,"ecc":True,
                        "network_gbps":10,"pcie_expandable":True,"linux_supported":True}), "arm_server")
    assert r["action"] == "BUY"


def test_expensive_arm_server_does_not_get_brand_style_bonus():
    r = decide(c(15000, {"architecture":"arm64","cpu_cores":32,"memory_gb":64,"ecc":True}), "arm_server")
    assert r["action"] != "BUY"


def test_cheap_24gb_gpu_is_buy():
    r = decide(c(3000, {"gpu_vram_gb":24,"compute_supported":True}), "gpu")
    assert r["action"] == "BUY"


def test_passive_datacenter_gpu_needs_airflow():
    r = decide(c(4000, {"gpu_vram_gb":24,"compute_supported":True,"passive_cooling":True}), "gpu")
    assert "passive_cooling_requires_host_airflow" in r["reasons"]
