from hhw.models import Candidate
from hhw.opportunity_report import markdown_opportunities


def test_report_contains_enterprise_and_ci_roles():
    c = Candidate(
        vendor_id="x",
        title="Dell R740xd",
        url="https://example.invalid/r740",
        currency="EUR",
        item_price=500,
        hardware={
            "memory_gb": 128,
            "drive_bays": {"count": 12, "size_in": 3.5},
            "storage_controller": "HBA330",
            "network_max_gbps": 25,
        },
    )
    report = markdown_opportunities([c])
    assert "## proxmox_compute" in report
    assert "## storage" in report
    assert "## linux_ci" in report
    assert "price_not_nok_comparable" in report
    assert "Dell R740xd" in report


def test_enterprise_report_shows_estimated_delivered_confidence():
    from hhw.models import Candidate
    c = Candidate("eu", "EU server", "https://example.invalid", currency="EUR", item_price=500,
                  hardware={"memory_gb": 64})
    c.metadata["delivered_cost"] = {
        "cost_status": "estimate",
        "estimated_delivered_nok": 4500,
    }
    report = markdown_opportunities([c], roles=["proxmox_compute"])
    assert "4500 NOK" in report
    assert "| estimate |" in report
