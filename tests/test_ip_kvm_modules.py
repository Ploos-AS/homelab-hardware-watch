from hhw.ip_kvm_modules import interface_module_compatibility


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
