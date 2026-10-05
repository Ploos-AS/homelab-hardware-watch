from datetime import date
from hhw.cost_enrich import enrich_delivered_cost
from hhw.fx import FxObservation
from hhw.models import Candidate


def test_complete_eu_cost_becomes_comparable():
    c = Candidate(vendor_id="x", title="server", url="https://example.invalid",
        currency="EUR", item_price=119.0, metadata={
            "foreign_vat_rate": 0.19,
            "foreign_vat_included": True,
            "foreign_vat_removed_for_export": True,
            "shipping_eur": 20.0,
            "handling_nok": 100.0,
        })
    enrich_delivered_cost(c, [FxObservation("EUR","NOK",10.0,date(2026,1,1),"test")], date(2026,1,2))
    assert c.metadata["delivered_cost"]["comparable"] is True
    assert c.metadata["delivered_cost"]["delivered_nok"] == 1600.0


def test_missing_shipping_stays_noncomparable():
    c = Candidate(vendor_id="x", title="server", url="https://example.invalid",
        currency="EUR", item_price=100.0, metadata={"handling_nok": 100.0})
    enrich_delivered_cost(c, [FxObservation("EUR","NOK",10.0,date(2026,1,1),"test")], date(2026,1,2))
    assert c.metadata["delivered_cost"]["comparable"] is False
