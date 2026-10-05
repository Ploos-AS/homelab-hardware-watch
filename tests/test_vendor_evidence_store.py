from datetime import date

from hhw.vendor_evidence import VendorEvidence
from hhw.vendor_evidence_store import load_vendor_evidence, save_vendor_evidence


def test_roundtrip(tmp_path):
    p = tmp_path / "evidence.json"
    source = [VendorEvidence("vendor", date(2026, 10, 5), "shipping", "checkout", {"shipping_eur": 19.9})]
    save_vendor_evidence(p, source)
    loaded = load_vendor_evidence(p)
    assert loaded == source
