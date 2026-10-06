from __future__ import annotations

from hhw.decision_price import decision_price_signal
from hhw.models import Candidate


def score_managed_switch(candidate: Candidate) -> dict:
    hw = candidate.hardware or {}
    score = 0
    reasons: list[str] = []

    if hw.get("managed") is True:
        score += 15; reasons.append("managed")
    if hw.get("vlan") is True:
        score += 10; reasons.append("vlan")
    if hw.get("lacp") is True:
        score += 10; reasons.append("lacp")

    uplink = hw.get("uplink_max_gbps")
    if uplink is not None:
        if uplink >= 25:
            score += 30; reasons.append("uplink>=25gbe")
        elif uplink >= 10:
            score += 20; reasons.append("uplink>=10gbe")
        elif uplink >= 2.5:
            score += 5; reasons.append("uplink>=2.5gbe")

    ports_10g = hw.get("ports_10gbe", 0) or 0
    ports_25g = hw.get("ports_25gbe", 0) or 0
    if ports_25g >= 4:
        score += 15; reasons.append("ports_25gbe>=4")
    elif ports_10g >= 4:
        score += 10; reasons.append("ports_10gbe>=4")

    access_ports = hw.get("access_ports")
    if access_ports is not None and access_ports >= 24:
        score += 5; reasons.append("access_ports>=24")

    if hw.get("fanless") is True:
        score += 10; reasons.append("fanless")
    elif hw.get("noise_class") == "high":
        score -= 15; reasons.append("high_noise")

    idle = hw.get("idle_power_watts")
    if idle is not None:
        if idle <= 30:
            score += 5; reasons.append("idle_power<=30w")
        elif idle >= 100:
            score -= 10; reasons.append("idle_power>=100w")

    price, confidence, ready = decision_price_signal(candidate)
    if price is not None:
        if price <= 1500:
            points = 25
        elif price <= 2500:
            points = 15
        elif price <= 4000:
            points = 5
        else:
            points = 0
        if confidence == "estimate" and points:
            points = max(0, points - 5)
            reasons.append("estimated_delivered_price_penalty")
        score += points
        if points:
            reasons.append("switch_price_value")
        reasons.append(f"price_confidence:{confidence}")
    else:
        reasons.append("price_not_nok_comparable")

    return {
        "role": "managed_switch",
        "score": score,
        "reasons": reasons,
        "price_scored": price is not None,
        "price_nok": price,
        "price_confidence": confidence,
        "ready_cost": ready,
        "managed": hw.get("managed"),
        "uplink_max_gbps": uplink,
    }


def managed_switch_action(result: dict) -> str:
    score = result["score"]
    confidence = result.get("price_confidence", "unknown")
    # BUY requires the two core target facts to be explicit, not inferred.
    if (score >= 60 and confidence in {"domestic", "import_confirmed"}
            and result.get("managed") is True
            and (result.get("uplink_max_gbps") or 0) >= 10):
        return "BUY"
    if score >= 30:
        return "WATCH"
    return "PASS"
