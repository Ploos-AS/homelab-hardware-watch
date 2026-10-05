from datetime import date

from hhw.cost_enrich import enrich_delivered_cost
from hhw.fx import FxObservation
from hhw.models import Candidate
from hhw.vendor_evidence import VendorEvidence


DAY = date(2026, 10, 5)
FX = [FxObservation("EUR", "NOK", 10.0, DAY, "test")]


def test_vendor_evidence_fills_missing_cost_inputs():
    c = Candidate("vendor", "server", "https://example.invalid", currency="EUR", item_price=119)
    evidence = [
        VendorEvidence("vendor", DAY, "shipping", "checkout", {"shipping_eur": 20}),
        VendorEvidence("vendor", DAY, "vat", "terms", {
            "foreign_vat_included": True,
            "foreign_vat_rate": 0.19,
            "foreign_vat_removed_for_export": True,
        }),
        VendorEvidence("vendor", DAY, "handling", "policy", {"handling_nok": 100}),
    ]
    enrich_delivered_cost(c, FX, DAY, evidence)
    assert c.metadata["delivered_cost"]["comparable"] is True
    assert c.metadata["delivered_cost"]["delivered_nok"] == 1600.0
    assert len(c.metadata["delivered_cost"]["vendor_evidence"]) == 3


def test_candidate_specific_value_overrides_vendor_evidence():
    c = Candidate("vendor", "server", "https://example.invalid", currency="EUR", item_price=119,
                  metadata={"shipping_eur": 30, "handling_nok": 100,
                            "foreign_vat_included": True, "foreign_vat_rate": 0.19,
                            "foreign_vat_removed_for_export": True})
    evidence = [VendorEvidence("vendor", DAY, "shipping", "old checkout", {"shipping_eur": 20})]
    enrich_delivered_cost(c, FX, DAY, evidence)
    assert c.metadata["delivered_cost"]["shipping_nok"] == 300.0


def test_unknown_item_price_never_becomes_zero_price():
    c = Candidate("vendor", "RFQ server", "https://example.invalid", currency="EUR", item_price=None)
    evidence = [VendorEvidence("vendor", DAY, "shipping", "quote", {"shipping_eur": 20})]
    enrich_delivered_cost(c, FX, DAY, evidence)
    assert c.metadata["delivered_cost"] == {
        "comparable": False,
        "reason": "item_price_unknown",
        "delivered_nok": None,
    }
