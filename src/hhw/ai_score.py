from __future__ import annotations

from hhw.decision_price import decision_price_signal
from hhw.models import Candidate


def score_ai_host(candidate: Candidate) -> dict:
    """Score a complete AI machine or an expandable host for local GPU workloads."""
    hw = candidate.hardware or {}
    score = 0
    reasons: list[str] = []

    vram = hw.get("gpu_vram_gb")
    if vram is not None:
        if vram >= 48:
            score += 60; reasons.append("vram>=48gb")
        elif vram >= 24:
            score += 50; reasons.append("vram>=24gb")
        elif vram >= 16:
            score += 35; reasons.append("vram>=16gb")
        elif vram >= 12:
            score += 20; reasons.append("vram>=12gb")
        elif vram >= 8:
            score += 8; reasons.append("vram>=8gb")

    slots = hw.get("pcie_full_length_slots", 0) or 0
    if slots >= 2:
        score += 20; reasons.append("pcie_full_length_slots>=2")
    elif slots >= 1:
        score += 10; reasons.append("pcie_full_length_slots>=1")

    psu = hw.get("psu_watts")
    if psu is not None:
        if psu >= 1000:
            score += 15; reasons.append("psu>=1000w")
        elif psu >= 750:
            score += 10; reasons.append("psu>=750w")

    if hw.get("gpu_power_connectors_suitable") is True:
        score += 10; reasons.append("gpu_power_connectors_suitable")

    if hw.get("gpu_full_length_clearance") is True:
        score += 10; reasons.append("gpu_full_length_clearance")

    memory = hw.get("memory_gb")
    if memory is not None and memory >= 64:
        score += 10; reasons.append("ram>=64gb")
    elif memory is not None and memory >= 32:
        score += 5; reasons.append("ram>=32gb")

    # CPU is intentionally not a major positive signal: local AI value is
    # dominated by GPU/VRAM and the ability to power/fit useful accelerators.
    if hw.get("gpu_full_length_clearance") is False:
        score -= 25; reasons.append("no_full_length_gpu_clearance")
    if hw.get("gpu_power_connectors_suitable") is False:
        score -= 20; reasons.append("gpu_power_unsuitable")

    price, confidence, ready = decision_price_signal(candidate)
    gpu_capable = vram is not None or slots >= 1 or hw.get("gpu_full_length_clearance") is True
    if price is not None:
        if price <= 5000 and gpu_capable:
            points = 20
        elif price <= 8000:
            points = 10
        elif price > 15000 and vram is None:
            points = -20
            reasons.append("expensive_gpu_less_host")
        else:
            points = 0
        if confidence == "estimate" and points > 0:
            points = max(0, points - 5)
            reasons.append("estimated_delivered_price_penalty")
        score += points
        reasons.append(f"price_confidence:{confidence}")
    else:
        reasons.append("price_not_nok_comparable")

    return {
        "role": "ai_host",
        "score": score,
        "reasons": reasons,
        "price_scored": price is not None,
        "price_nok": price,
        "price_confidence": confidence,
        "ready_cost": ready,
    }


def ai_host_action(result: dict) -> str:
    score = result["score"]
    confidence = result.get("price_confidence", "unknown")
    if score >= 60 and confidence in {"domestic", "import_confirmed"}:
        return "BUY"
    if score >= 30:
        return "WATCH"
    return "PASS"
