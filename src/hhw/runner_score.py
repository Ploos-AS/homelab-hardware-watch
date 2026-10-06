from __future__ import annotations

from hhw.decision_price import decision_price_signal
from hhw.models import Candidate
from hhw.opportunities import ROLE_FAMILY_BONUS


VALID_ROLES = {"linux_ci", "linux_arm64_ci", "macos_ci"}


def score_runner(candidate: Candidate, role: str) -> dict:
    """Decision-quality score for Tiny/CI runner candidates."""
    if role not in VALID_ROLES:
        raise ValueError(f"unknown runner role: {role}")

    hw = candidate.hardware or {}
    metadata = candidate.metadata or {}
    family = metadata.get("runner_family")
    parity = metadata.get("configuration_parity") or {}
    score = 0
    reasons: list[str] = []

    family_bonus = ROLE_FAMILY_BONUS.get(role, {}).get(family, 0)
    if family_bonus:
        score += family_bonus
        reasons.append(f"family_fit:{family}")

    arm_families = {"arm64_rk3588", "raspberry_pi_5", "arm64_other"}
    incompatible = (
        role == "linux_ci"
        and (family in arm_families or str(family).startswith("mac_mini"))
    ) or (
        role == "macos_ci" and not str(family).startswith("mac_mini")
    ) or (
        role == "linux_arm64_ci"
        and family not in arm_families
    )
    if incompatible:
        score -= 100
        reasons.append("architecture_mismatch")

    memory = hw.get("memory_gb")
    if memory is not None:
        if memory >= 16:
            score += 15
            reasons.append("ram>=16gb")
        elif memory >= 8:
            score += 5
            reasons.append("ram>=8gb")

    # Configuration parity is preferred for domestic Tiny/CI comparisons because
    # it accounts for the working cost of bringing a candidate to 16 GB.
    price, confidence, ready = decision_price_signal(candidate)
    parity_price = parity.get("adjusted_price_nok")
    if confidence == "domestic" and parity.get("comparable") and parity_price is not None:
        price = float(parity_price)

    if price is not None:
        if price <= 1500:
            points = 30
        elif price <= 2000:
            points = 20
        elif price <= 2500:
            points = 10
        else:
            points = 0

        if confidence == "estimate" and points:
            points = max(0, points - 5)
            reasons.append("estimated_delivered_price_penalty")
        score += points
        if points:
            reasons.append("runner_price_value")
        reasons.append(f"price_confidence:{confidence}")
    else:
        reasons.append("price_not_nok_comparable")

    return {
        "role": role,
        "score": score,
        "reasons": reasons,
        "price_scored": price is not None,
        "price_nok": price,
        "price_confidence": confidence,
        "ready_cost": ready,
        "runner_family": family,
    }


def runner_action(result: dict) -> str:
    score = result["score"]
    confidence = result.get("price_confidence", "unknown")
    if score >= 60 and confidence in {"domestic", "import_confirmed"}:
        return "BUY"
    if score >= 30:
        return "WATCH"
    return "PASS"
