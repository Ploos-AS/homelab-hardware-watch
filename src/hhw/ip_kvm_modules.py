from __future__ import annotations


FAMILY_VENDOR = {
    "raritan_dominion_kx": "raritan",
    "raritan_dominion_lx": "raritan",
    "avocent_mergepoint": "avocent",
    "avocent_dsr": "avocent",
    "avocent_mpu": "avocent",
    "aten_kn": "aten",
    "lantronix_spider": "lantronix",
    "lantronix_spiderduo": "lantronix",
}


def interface_module_compatibility(
    kvm_family: str | None,
    module_vendor: str | None,
    compatible_families: list[str] | None = None,
) -> str:
    """Return compatible, incompatible, or unknown without guessing."""
    if not kvm_family:
        return "unknown"
    if compatible_families:
        return "compatible" if kvm_family in compatible_families else "incompatible"
    expected_vendor = FAMILY_VENDOR.get(kvm_family)
    if not expected_vendor or not module_vendor:
        return "unknown"
    if module_vendor.lower() != expected_vendor:
        return "incompatible"
    # Same vendor alone is insufficient: generations/features may differ.
    return "unknown"
