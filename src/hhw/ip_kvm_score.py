from __future__ import annotations

from hhw.decision_price import decision_price_signal
from hhw.models import Candidate
from hhw.ip_kvm_families import detect_ip_kvm_family, ip_kvm_profile
from hhw.ip_kvm_modules import interface_module_compatibility


def score_ip_kvm(candidate: Candidate) -> dict:
    hw = candidate.hardware or {}
    score = 0
    reasons: list[str] = []
    family = candidate.metadata.get("ip_kvm_family") or detect_ip_kvm_family(candidate.title)
    profile = ip_kvm_profile(family)

    ports = hw.get("kvm_ports")
    if ports is not None:
        if ports >= 32:
            score += 25; reasons.append("ports>=32")
        elif ports >= 16:
            score += 20; reasons.append("ports>=16")
        elif ports >= 8:
            score += 15; reasons.append("ports>=8")
        elif ports >= 1:
            score += 5; reasons.append("ports>=1")

    if hw.get("kvm_over_ip") is True:
        score += 20; reasons.append("kvm_over_ip")
    if hw.get("bios_level_access") is True:
        score += 15; reasons.append("bios_level_access")
    if hw.get("virtual_media") is True:
        score += 15; reasons.append("virtual_media")
    if hw.get("dual_psu") is True:
        score += 5; reasons.append("dual_psu")
    if hw.get("dual_lan") is True:
        score += 5; reasons.append("dual_lan")

    required = hw.get("required_interface_modules")
    included = hw.get("included_interface_modules")
    module_compatibility = interface_module_compatibility(
        family,
        hw.get("interface_module_vendor"),
        hw.get("interface_module_compatible_families"),
    )
    module_cost = hw.get("missing_interface_modules_cost_nok")
    missing = None
    if isinstance(required, int) and isinstance(included, int):
        missing = max(0, required - included)
        if missing == 0 and module_compatibility == "compatible":
            score += 15; reasons.append("interface_modules_complete")
        elif missing == 0:
            reasons.append(f"interface_module_compatibility:{module_compatibility}")
        else:
            reasons.append(f"missing_interface_modules:{missing}")

    price, confidence, ready = decision_price_signal(candidate)
    effective = price
    if effective is not None and missing and module_cost is None:
        effective = None
        reasons.append("missing_interface_module_cost_unknown")
    elif effective is not None and module_cost is not None:
        effective += float(module_cost)

    if effective is not None:
        if effective <= 2000:
            points = 25
        elif effective <= 4000:
            points = 15
        elif effective <= 7000:
            points = 5
        else:
            points = 0
        if confidence == "estimate" and points:
            points = max(0, points - 5)
            reasons.append("estimated_delivered_price_penalty")
        score += points
        if points:
            reasons.append("effective_ip_kvm_cost_value")
        reasons.append(f"price_confidence:{confidence}")
    else:
        reasons.append("effective_cost_not_comparable")

    return {
        "role": "ip_kvm", "score": score, "reasons": reasons,
        "price_scored": effective is not None, "price_nok": price,
        "effective_cost_nok": effective, "price_confidence": confidence,
        "ready_cost": ready, "kvm_ports": ports,
        "kvm_over_ip": hw.get("kvm_over_ip"),
        "bios_level_access": hw.get("bios_level_access"),
        "missing_interface_modules": missing,
        "ip_kvm_family": family, "ip_kvm_profile": profile,
        "interface_module_compatibility": module_compatibility,
    }


def ip_kvm_action(result: dict) -> str:
    if (result["score"] >= 60
            and result.get("price_confidence") in {"domestic", "import_confirmed"}
            and result.get("kvm_over_ip") is True
            and result.get("bios_level_access") is True
            and result.get("effective_cost_nok") is not None):
        return "BUY"
    if result["score"] >= 30:
        return "WATCH"
    return "PASS"
