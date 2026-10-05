from __future__ import annotations

from hhw.models import Candidate


def _nok_price(candidate: Candidate) -> float | None:
    if candidate.currency != "NOK" or candidate.item_price is None:
        return None
    return float(candidate.item_price)


def score_enterprise(candidate: Candidate, role: str) -> dict:
    hw = candidate.hardware or {}
    score = 0
    reasons = []

    memory = hw.get("memory_gb")
    network = hw.get("network_max_gbps", 0)
    bays = hw.get("drive_bays") or {}
    controller = str(hw.get("storage_controller", "")).upper()

    if role == "proxmox_compute":
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

    price = _nok_price(candidate)
    if price is not None:
        if price <= 3000:
            score += 30; reasons.append("nok<=3000")
        elif price <= 5000:
            score += 20; reasons.append("nok<=5000")
        elif price <= 7000:
            score += 10; reasons.append("nok<=7000")
    else:
        reasons.append("price_not_nok_comparable")

    return {"role": role, "score": score, "reasons": reasons, "price_scored": price is not None}
