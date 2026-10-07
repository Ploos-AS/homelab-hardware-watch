from hhw.component_cost import ready_cost
from hhw.ip_kvm_ready_cost import add_missing_kvm_modules, kvm_module_evidence_key
from hhw.models import Candidate


def c(price=1000):
    return Candidate("x", "KVM", "https://example.invalid/kvm", item_price=price)


def test_model_specific_evidence_key():
    assert kvm_module_evidence_key("raritan_dominion_kx", "D2CIM-DVUSB") == "kvm_module:d2cim_dvusb"


def test_family_key_is_fallback_not_generic_cim_bucket():
    assert kvm_module_evidence_key("aten_kn", None) == "kvm_module_family:aten_kn"


def test_missing_module_unit_cost_multiplies_once():
    x = c(1000)
    add_missing_kvm_modules(
        x, family="raritan_dominion_kx", missing_count=4,
        model="D2CIM-DVUSB", unit_cost_nok=350,
    )
    result = ready_cost(x)
    assert result["component_cost_nok"] == 1400
    assert result["ready_cost_nok"] == 2400


def test_unknown_module_cost_blocks_ready_cost():
    x = c()
    add_missing_kvm_modules(
        x, family="raritan_dominion_kx", missing_count=4,
        model="D2CIM-DVUSB",
    )
    result = ready_cost(x)
    assert result["comparable"] is False
    assert result["unknown_required_costs"] == ["kvm_interface_module"]
