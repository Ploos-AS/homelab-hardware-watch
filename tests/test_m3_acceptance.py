from datetime import date

from hhw.cost_enrich import enrich_delivered_cost
from hhw.enterprise_score import score_enterprise
from hhw.fx import FxObservation
from hhw.models import Candidate
from hhw.vendor_evidence import VendorEvidence


DAY = date(2026, 10, 5)


def test_servershop24_r640_acceptance():
    candidate = Candidate(
        vendor_id="servershop24_de",
        title="Dell EMC PowerEdge R640 2x Xeon Gold 6138 HBA330",
        url="https://www.servershop24.de/en/dell-emc-r640-rack-server/a-136650/",
        currency="EUR",
        item_price=747.89,
        hardware={
            "weight_kg": 18,
            "memory_gb": 32,
            "cpu_count": 2,
            "storage_controller": "HBA330",
        },
        metadata={},
    )
    evidence = [
        VendorEvidence(
            vendor_id="servershop24_de",
            observed_on=DAY,
            evidence_type="handling",
            source="acceptance fixture: zero placeholder excluded from production evidence",
            values={"handling_nok": 0.0},
        )
    ]
    fx = [FxObservation("EUR", "NOK", 11.50, DAY, "norges_bank")]

    enrich_delivered_cost(candidate, fx, DAY, evidence)
    cost = candidate.metadata["delivered_cost"]

    # 747.89 + 103.99 shipping, converted at the fixture FX rate, then 25% Norwegian VAT.
    assert cost["cost_status"] == "estimate"
    assert cost["estimated_delivered_nok"] == 12245.78
    assert cost["vendor_evidence"][-1]["method"] == "dhl_express"

    scored = score_enterprise(candidate, "proxmox_compute")
    assert scored["price_confidence"] == "estimate"
    assert scored["price_nok"] == 12245.78
    assert scored["price_scored"] is True
