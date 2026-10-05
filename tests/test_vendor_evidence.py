from datetime import date

from hhw.vendor_evidence import VendorEvidence, latest_evidence


def test_latest_evidence_is_not_from_future():
    observations = [
        VendorEvidence("vendor", date(2026, 9, 1), "shipping", "checkout", {"shipping_eur": 20}),
        VendorEvidence("vendor", date(2026, 10, 1), "shipping", "checkout", {"shipping_eur": 25}),
    ]
    found = latest_evidence(observations, "vendor", "shipping", date(2026, 9, 15))
    assert found.values["shipping_eur"] == 20


def test_wrong_evidence_type_is_not_used():
    observations = [
        VendorEvidence("vendor", date(2026, 9, 1), "vat", "terms", {"foreign_vat_removed_for_export": True}),
    ]
    assert latest_evidence(observations, "vendor", "shipping", date(2026, 10, 1)) is None
