from __future__ import annotations

import re

from hhw.ip_kvm_families import detect_ip_kvm_family


def enrich_ip_kvm(candidate):
    """Fill only high-confidence IP-KVM facts derivable from model/title."""
    title = candidate.title or ""
    hw = candidate.hardware
    family = detect_ip_kvm_family(title)
    if family:
        candidate.metadata.setdefault("ip_kvm_family", family)

    # Raritan Dominion KX III: DKX3-108/116/132/216/232/416/432/464.
    m = re.search(r"\bDKX3-(108|116|132|216|232|416|432|464)\b", title, re.I)
    if m:
        ports = int(m.group(1)[-2:])
        hw.setdefault("kvm_ports", ports)
        hw.setdefault("kvm_over_ip", True)
        hw.setdefault("bios_level_access", True)
        candidate.metadata["ip_kvm_model"] = f"DKX3-{m.group(1)}"
        return candidate

    # ATEN KN model names encode port count in the final two digits.
    m = re.search(r"\b(KN\d{2}(08|16|32|40|64)(?:VA|VB)?)\b", title, re.I)
    if m:
        hw.setdefault("kvm_ports", int(m.group(2)))
        hw.setdefault("kvm_over_ip", True)
        hw.setdefault("bios_level_access", True)
        candidate.metadata["ip_kvm_model"] = m.group(1).upper()
        return candidate

    # Avocent MergePoint Unity model names commonly expose 8/16/32 ports.
    m = re.search(r"\b(MPU\d*(08|16|32)[A-Z]*)\b", title, re.I)
    if m:
        hw.setdefault("kvm_ports", int(m.group(2)))
        hw.setdefault("kvm_over_ip", True)
        hw.setdefault("bios_level_access", True)
        candidate.metadata["ip_kvm_model"] = m.group(1).upper()

    return candidate
