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
        "macos_ci", "ai_server", "managed_switch", "ups", "ip_kvm",
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



def test_report_shows_bargain_signal_without_changing_action():
    c = Candidate(
        "no", "Apple Mac mini M1 16GB 256GB",
        "https://example.invalid/mac", item_price=3500,
        hardware={"memory_gb": 16},
        metadata={
            "runner_family": "mac_mini_apple_silicon",
            "bargain": {"signal": "exceptional", "discount_vs_median": 0.30},
        },
    )
    report = markdown_opportunities([c], roles=["macos_ci"])
    assert "| exceptional |" in report
    assert "## macos_ci" in report



def test_ip_kvm_report_uses_unified_decision_and_effective_cost_reasoning():
    kvm = Candidate(
        "no", "Raritan Dominion KX III DKX3-216",
        "https://example.invalid/kvm", item_price=1500,
        hardware={
            "kvm_ports": 16, "kvm_over_ip": True, "bios_level_access": True,
            "virtual_media": True, "dual_psu": True, "dual_lan": True,
            "required_interface_modules": 16, "included_interface_modules": 16,
            "interface_module_vendor": "raritan",
            "interface_module_compatible_families": ["raritan_dominion_kx"],
        },
    )
    report = markdown_opportunities([kvm], roles=["ip_kvm"])
    assert "## ip_kvm" in report
    assert "| BUY |" in report
    assert "interface_modules_complete" in report
    assert "effective_ip_kvm_cost_value" in report


def test_incomplete_ip_kvm_report_does_not_hide_unknown_cim_cost():
    kvm = Candidate(
        "no", "Raritan Dominion KX III DKX3-216 bare chassis",
        "https://example.invalid/kvm-bare", item_price=800,
        hardware={
            "kvm_ports": 16, "kvm_over_ip": True, "bios_level_access": True,
            "required_interface_modules": 16, "included_interface_modules": 0,
        },
    )
    report = markdown_opportunities([kvm], roles=["ip_kvm"])
    assert "missing_interface_module_cost_unknown" in report
    assert "| BUY |" not in report
