from hhw.models import Candidate
from hhw.normalize import normalize_title
from hhw.reference import price_vs_n150


def c(title):
    return Candidate(vendor_id="test", title=title, url="https://example.invalid")


def test_intel_tiny_title():
    item = normalize_title(c("Lenovo ThinkCentre M920q Tiny i5-9500T 16GB RAM 256GB SSD"))
    assert item.hardware["cpu"]["model"].lower() == "i5-9500t"
    assert item.hardware["memory_gb"] == 16
    assert item.hardware["storage"][0]["capacity_gb"] == 256
    assert item.hardware["form_factor"] == "tiny"


def test_ryzen_title():
    item = normalize_title(c("HP EliteDesk Mini Ryzen 5 PRO 4650GE 16GB RAM 512GB NVMe"))
    assert "4650GE" in item.hardware["cpu"]["model"]
    assert item.hardware["memory_gb"] == 16
    assert item.hardware["storage"][0]["type"] == "NVME"


def test_n150_price_reference():
    assert price_vs_n150(1500)["delta_nok"] == -500
    assert price_vs_n150(2500)["ratio"] == 1.25
