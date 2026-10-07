from __future__ import annotations

from hhw.models import Candidate
from hhw.decision_price import decision_price_signal
from hhw.price_signal import raw_price_signal as _price_signal


def score_enterprise(candidate: Candidate, role: str) -> dict:
    hw = candidate.hardware or {}
    score = 0
    reasons = []

    memory = hw.get("memory_gb")
    network = hw.get("network_max_gbps", 0)
    bays = hw.get("drive_bays") or {}
    controller = str(hw.get("storage_controller", "")).upper()

    if role in {"proxmox_compute", "proxmox_rack"}:
        if memory is not None:
            if memory >= 128:
                score += 30; reasons.append("ram>=128gb")
            elif memory >= 64:
                score += 20; reasons.append("ram>=64gb")
            elif memory >= 32:
                score += 10; reasons.append("ram>=32gb")
        if hw.get("cpu_count", 0) >= 2:
            score += 10; reasons.append("dual_cpu")
        if network >= 25:
            score += 15; reasons.append("network>=25gbe")
        elif network >= 10:
            score += 10; reasons.append("network>=10gbe")

    elif role == "storage":
        count = bays.get("count", 0)
        size = bays.get("size_in")
        if size == 3.5 and count >= 12:
            score += 40; reasons.append(">=12_lff")
        elif size == 3.5 and count >= 8:
            score += 30; reasons.append(">=8_lff")
        elif count >= 8:
            score += 15; reasons.append(">=8_bays")

        if "HBA" in controller:
            score += 25; reasons.append("hba")
        elif controller:
            score += 5; reasons.append("storage_controller_present")

        if network >= 25:
            score += 20; reasons.append("network>=25gbe")
        elif network >= 10:
            score += 12; reasons.append("network>=10gbe")

        if memory is not None and memory >= 64:
            score += 10; reasons.append("ram>=64gb")
        elif memory is not None and memory >= 32:
            score += 5; reasons.append("ram>=32gb")
    else:
        raise ValueError(f"unknown enterprise role: {role}")

    price, price_confidence, ready = decision_price_signal(candidate)
    if price is not None:
        if price <= 3000:
            price_points = 30
        elif price <= 5000:
            price_points = 20
        elif price <= 7000:
            price_points = 10
        else:
            price_points = 0
            if price > 12000:
                score -= 20
                reasons.append("delivered_nok>12000_penalty")
            elif price > 9000:
                score -= 15
                reasons.append("delivered_nok>9000_penalty")
            elif price > 7000:
                score -= 10
                reasons.append("delivered_nok>7000_penalty")
        if price_confidence == "estimate" and price_points:
            price_points = max(0, price_points - 5)
            reasons.append("estimated_delivered_price_penalty")
        score += price_points
        if price_points:
            threshold = 3000 if price <= 3000 else 5000 if price <= 5000 else 7000
            prefix = "nok" if price_confidence == "domestic" else "delivered_nok"
            reasons.append(f"{prefix}<={threshold}")
        reasons.append(f"price_confidence:{price_confidence}")
    else:
        reasons.append("price_not_nok_comparable")

    return {
        "role": role,
        "score": score,
        "reasons": reasons,
        "price_scored": price is not None,
        "price_nok": price,
        "price_confidence": price_confidence,
        "ready_cost": ready,
    }


def enterprise_action(result: dict) -> str:
    """Convert enterprise score/confidence into an actionable recommendation."""
    score = result["score"]
    confidence = result.get("price_confidence", "unknown")

    # BUY requires a trustworthy NOK price signal. Estimated imports remain WATCH
    # until checkout/customs assumptions are sufficiently confirmed.
    if score >= 60 and confidence in {"domestic", "import_confirmed"}:
        return "BUY"
    if score >= 30:
        return "WATCH"
    return "PASS"
