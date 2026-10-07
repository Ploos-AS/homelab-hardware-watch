from hhw.ip_kvm_bundle import enrich_ip_kvm_bundle
from hhw.models import Candidate


def c(title, description=None):
    x = Candidate("x", title, "https://example.invalid", item_price=1000)
    if description:
        x.metadata["description"] = description
    return x


def test_explicit_raritan_model_bundle_sets_count_and_compatibility():
    x = enrich_ip_kvm_bundle(c("Raritan KX III with 16x D2CIM-DVUSB"))
    assert x.hardware["included_interface_modules"] == 16
    assert x.hardware["interface_module_vendor"] == "raritan"
    assert "raritan_dominion_kx" in x.hardware["interface_module_compatible_families"]
    assert x.metadata["interface_modules"][0]["virtual_media"] is True


def test_model_can_be_found_in_description():
    x = enrich_ip_kvm_bundle(c("Raritan KVM bundle", "8 stk D2CIM-DVUSB-HDMI følger med"))
    assert x.hardware["included_interface_modules"] == 8
    assert x.metadata["interface_modules"][0]["video"] == "hdmi"


def test_multiple_known_models_are_summed():
    x = enrich_ip_kvm_bundle(c("8x D2CIM-DVUSB + 4x D2CIM-DVUSB-DP"))
    assert x.hardware["included_interface_modules"] == 12
    assert len(x.metadata["interface_modules"]) == 2


def test_generic_cim_count_is_not_compatibility_evidence():
    x = enrich_ip_kvm_bundle(c("Raritan KVM med 12 CIM inkludert"))
    assert x.hardware["included_interface_modules"] == 12
    assert "interface_module_compatible_families" not in x.hardware
    assert x.metadata["interface_module_count_source"] == "generic_text"


def test_unknown_model_does_not_become_known_module():
    x = enrich_ip_kvm_bundle(c("16x MYSTERY-CIM"))
    assert "interface_modules" not in x.metadata
