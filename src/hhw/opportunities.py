from __future__ import annotations

from dataclasses import dataclass
from hhw.models import Candidate

ROLE_FAMILY_BONUS = {
    "linux_ci": {
        "generic_tiny": 20,
        "dell_optiplex_micro": 20,
        "hp_business_mini": 20,
        "lenovo_thinkcentre_tiny": 20,
        "fujitsu_esprimo_q": 17,
        "asus_expertcenter_pn": 17,
        "acer_veriton_mini": 17,
        "intel_nuc": 17,
        "asus_nuc": 17,
        "minisforum_mini": 12,
        "beelink_mini": 12,
        "gmktec_mini": 12,
    },
    "linux_arm64_ci": {
        "arm64_rk3588": 30,
        "raspberry_pi_5": 25,
        "arm64_other": 10,
    },
    "macos_ci": {
        "mac_mini_apple_silicon": 35,
        "mac_mini_intel": 15,
    },
}


@dataclass
class Opportunity:
    candidate: Candidate
    role: str
    score: float
    reasons: list[str]


def score_candidate(candidate: Candidate, role: str) -> Opportunity:
    score = 0.0
    reasons = []
    family = candidate.metadata.get("runner_family")
    parity = candidate.metadata.get("configuration_parity", {})
    adjusted = parity.get("adjusted_price_nok")

    family_bonus = ROLE_FAMILY_BONUS.get(role, {}).get(family, 0)
    if family_bonus:
        score += family_bonus
        reasons.append(f"family fits {role} (+{family_bonus})")

    memory = candidate.hardware.get("memory_gb")
    if memory is not None:
        if memory >= 16:
            score += 10
            reasons.append("16 GB+ memory (+10)")
        elif memory >= 8:
            score += 3
            reasons.append("8 GB memory (+3)")

    if adjusted is not None:
        if adjusted <= 1500:
            score += 30
            reasons.append("parity price <= NOK 1500 (+30)")
        elif adjusted <= 2000:
            score += 20
            reasons.append("parity price <= N150/16GB reference (+20)")
        elif adjusted <= 2500:
            score += 10
            reasons.append("parity price <= NOK 2500 (+10)")

    # Do not award architecture-specific role value to the wrong family.
    if role == "macos_ci" and not str(family).startswith("mac_mini"):
        score -= 100
        reasons.append("not a native Mac candidate (-100)")
    if role == "linux_arm64_ci" and family not in {"arm64_rk3588", "raspberry_pi_5", "arm64_other"}:
        score -= 100
        reasons.append("not an ARM64 Linux family (-100)")

    return Opportunity(candidate, role, score, reasons)


def rank(candidates: list[Candidate], role: str) -> list[Opportunity]:
    return sorted(
        (score_candidate(c, role) for c in candidates),
        key=lambda x: (x.score, -(x.candidate.item_price or 10**9)),
        reverse=True,
    )
