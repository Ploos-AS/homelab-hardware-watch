from hhw.ip_kvm_score import ip_kvm_action, score_ip_kvm
from hhw.models import Candidate


def kvm(price=1500, hardware=None):
    return Candidate(vendor_id="x", title="enterprise IP KVM", url="https://example.invalid",
                     currency="NOK", item_price=price, hardware=hardware or {})


def test_complete_16_port_enterprise_kvm_is_buy():
    x = kvm(hardware={
        "kvm_ports": 16, "kvm_over_ip": True, "bios_level_access": True,
        "virtual_media": True, "dual_psu": True, "dual_lan": True,
        "required_interface_modules": 16, "included_interface_modules": 16,
        "interface_module_vendor": "raritan",
        "interface_module_compatible_families": ["raritan_dominion_kx"],
    })
    x.title = "Raritan Dominion KX III DKX3-216"
    result = score_ip_kvm(x)
    assert result["score"] >= 60
    assert result["missing_interface_modules"] == 0
    assert ip_kvm_action(result) == "BUY"


def test_missing_cims_with_unknown_cost_cannot_auto_buy():
    result = score_ip_kvm(kvm(hardware={
        "kvm_ports": 16, "kvm_over_ip": True, "bios_level_access": True,
        "virtual_media": True, "required_interface_modules": 16,
        "included_interface_modules": 0,
    }))
    assert result["effective_cost_nok"] is None
    assert "missing_interface_module_cost_unknown" in result["reasons"]
    assert ip_kvm_action(result) == "WATCH"


def test_known_missing_module_cost_is_added():
    result = score_ip_kvm(kvm(1000, {
        "kvm_ports": 8, "kvm_over_ip": True, "bios_level_access": True,
        "required_interface_modules": 8, "included_interface_modules": 4,
        "missing_interface_modules_cost_nok": 2000,
    }))
    assert result["missing_interface_modules"] == 4
    assert result["effective_cost_nok"] == 3000


def test_non_ip_kvm_cannot_auto_buy():
    result = score_ip_kvm(kvm(hardware={
        "kvm_ports": 16, "kvm_over_ip": False, "bios_level_access": True,
        "virtual_media": True,
    }))
    assert ip_kvm_action(result) != "BUY"



def test_complete_count_without_compatibility_evidence_gets_no_complete_bonus():
    x = kvm(hardware={
        "kvm_ports": 16, "kvm_over_ip": True, "bios_level_access": True,
        "required_interface_modules": 16, "included_interface_modules": 16,
        "interface_module_vendor": "raritan",
    })
    x.title = "Raritan Dominion KX III DKX3-216"
    result = score_ip_kvm(x)
    assert result["interface_module_compatibility"] == "unknown"
    assert "interface_modules_complete" not in result["reasons"]



def test_rack_kvm_derives_required_modules_from_ports():
    x = kvm(hardware={})
    x.title = "Raritan Dominion KX III DKX3-216 with 12x D2CIM-DVUSB"
    result = score_ip_kvm(x)
    assert result["kvm_ports"] == 16
    assert result["missing_interface_modules"] == 4
    assert "required_interface_modules_from_port_count" in result["reasons"]


def test_single_node_kvm_does_not_invent_separate_module_requirement():
    x = kvm(hardware={"kvm_ports": 1, "kvm_over_ip": True, "bios_level_access": True})
    x.title = "Lantronix Spider KVM over IP"
    result = score_ip_kvm(x)
    assert result["ip_kvm_profile"] == "single_node"
    assert result["missing_interface_modules"] is None
    assert "required_interface_modules_from_port_count" not in result["reasons"]



def test_missing_cim_unit_cost_is_multiplied_by_missing_count_once():
    x = kvm(1000, {
        "missing_interface_modules_cost_nok": 350,
    })
    x.title = "Raritan Dominion KX III DKX3-216 with 12x D2CIM-DVUSB"
    result = score_ip_kvm(x)
    assert result["missing_interface_modules"] == 4
    assert result["effective_cost_nok"] == 2400
    assert result["ready_cost"]["component_cost_nok"] == 1400
