from hhw.models import Candidate
from hhw.opportunity_report import markdown_opportunities


def test_report_contains_all_decision_roles():
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
    for role in (
        "proxmox_compute", "storage", "linux_ci", "linux_arm64_ci",
        "macos_ci", "ai_server", "managed_switch", "ups",
    ):
        assert f"## {role}" in report
    assert "price_not_nok_comparable" in report
    assert "Dell R740xd" in report


def test_enterprise_report_shows_estimated_delivered_confidence():
    c = Candidate("eu", "EU server", "https://example.invalid", currency="EUR", item_price=500,
                  hardware={"memory_gb": 64})
    c.metadata["delivered_cost"] = {
        "cost_status": "estimate",
        "estimated_delivered_nok": 4500,
    }
    report = markdown_opportunities([c], roles=["proxmox_compute"])
    assert "4500 NOK" in report
    assert "| estimate |" in report


def test_ci_report_now_shows_real_action():
    c = Candidate(
        "no", "Tiny", "https://example.invalid", item_price=1400,
        hardware={"memory_gb": 16},
        metadata={
            "runner_family": "generic_tiny",
            "configuration_parity": {"comparable": True, "adjusted_price_nok": 1400},
        },
    )
    report = markdown_opportunities([c], roles=["linux_ci"])
    assert "| BUY |" in report
    assert "| domestic |" in report


def test_special_roles_use_unified_decisions():
    switch = Candidate(
        "no", "25GbE switch", "https://example.invalid/switch", item_price=1500,
        hardware={
            "managed": True, "vlan": True, "lacp": True,
            "uplink_max_gbps": 25, "ports_25gbe": 4,
        },
    )
    report = markdown_opportunities([switch], roles=["managed_switch"])
    assert "| BUY |" in report
    assert "uplink>=25gbe" in report
