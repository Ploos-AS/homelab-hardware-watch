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


def test_explicit_missing_components_are_recorded_fail_closed():
    item = normalize_title(c("Dell R730 64GB RAM no HBA, rails not included, without caddies"))
    missing = {x["component"]: x for x in item.metadata["missing_components"]}
    assert set(missing) == {"hba", "rails", "caddies"}
    assert all(x["required"] is True for x in missing.values())
    assert all(x["cost_nok"] is None for x in missing.values())


def test_absence_of_component_word_does_not_mean_missing():
    item = normalize_title(c("Dell R730 64GB RAM"))
    assert "missing_components" not in item.metadata


def test_existing_component_cost_evidence_is_preserved():
    item = Candidate(
        vendor_id="test",
        title="Dell R730 without rails",
        url="https://example.invalid",
        metadata={"missing_components": [
            {"component": "rails", "required": True, "cost_nok": 700, "note": "vendor quote"}
        ]},
    )
    normalized = normalize_title(item)
    assert normalized.metadata["missing_components"] == item.metadata["missing_components"]
