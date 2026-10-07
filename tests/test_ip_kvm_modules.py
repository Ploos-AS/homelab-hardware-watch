from hhw.ip_kvm_modules import interface_module_compatibility, interface_module_model_compatibility


def test_explicit_family_match_is_compatible():
    assert interface_module_compatibility(
        "raritan_dominion_kx", "raritan", ["raritan_dominion_kx"]
    ) == "compatible"


def test_explicit_wrong_family_is_incompatible():
    assert interface_module_compatibility(
        "raritan_dominion_lx", "raritan", ["raritan_dominion_kx"]
    ) == "incompatible"


def test_cross_vendor_module_is_incompatible():
    assert interface_module_compatibility("aten_kn", "raritan") == "incompatible"


def test_same_vendor_without_family_evidence_is_unknown():
    assert interface_module_compatibility("raritan_dominion_kx", "raritan") == "unknown"


def test_unknown_kvm_family_is_unknown():
    assert interface_module_compatibility(None, "raritan") == "unknown"



def test_known_d2cim_dvusb_resolves_compatible_with_bios_media():
    result = interface_module_model_compatibility("raritan_dominion_kx", "D2CIM-DVUSB")
    assert result["status"] == "compatible"
    assert result["virtual_media"] is True
    assert result["bios_virtual_media"] is True


def test_basic_dcim_usbg2_has_no_virtual_media():
    result = interface_module_model_compatibility("raritan_dominion_kx", "DCIM-USBG2")
    assert result["status"] == "compatible"
    assert result["virtual_media"] is False


def test_known_raritan_cim_is_incompatible_with_aten():
    assert interface_module_model_compatibility("aten_kn", "D2CIM-DVUSB")["status"] == "incompatible"


def test_unknown_model_stays_unknown():
    assert interface_module_model_compatibility("raritan_dominion_kx", "MYSTERY-CIM")["status"] == "unknown"
