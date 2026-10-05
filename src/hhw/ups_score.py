from __future__ import annotations

from hhw.enterprise_score import _price_signal
from hhw.models import Candidate


def score_ups(candidate: Candidate) -> dict:
    hw = candidate.hardware or {}
    score = 0
    reasons: list[str] = []

    watts = hw.get("output_watts")
    if watts is not None:
        if watts >= 2000:
            score += 25; reasons.append("output>=2000w")
        elif watts >= 1000:
            score += 20; reasons.append("output>=1000w")
        elif watts >= 600:
            score += 10; reasons.append("output>=600w")

    topology = hw.get("ups_topology")
    if topology == "online_double_conversion":
        score += 20; reasons.append("online_double_conversion")
    elif topology == "line_interactive":
        score += 10; reasons.append("line_interactive")

    if hw.get("replaceable_battery") is True:
        score += 15; reasons.append("replaceable_battery")
    elif hw.get("replaceable_battery") is False:
        score -= 30; reasons.append("battery_not_serviceable")

    management = set(hw.get("management_interfaces") or [])
    if "snmp" in management:
        score += 15; reasons.append("snmp")
    if management.intersection({"usb", "serial"}):
        score += 5; reasons.append("local_management")

    if hw.get("nut_compatible") is True or hw.get("apcupsd_compatible") is True:
        score += 10; reasons.append("open_monitoring_compatible")

    noise = hw.get("noise_class")
    if noise == "high":
        score -= 10; reasons.append("high_noise")
    idle = hw.get("idle_power_watts")
    if idle is not None and idle >= 100:
        score -= 10; reasons.append("idle_power>=100w")

    price, confidence = _price_signal(candidate)
    battery_cost = hw.get("required_battery_replacement_nok")
    battery_required = hw.get("battery_replacement_required")

    effective = None
    if price is not None:
        if battery_required is True and battery_cost is None:
            reasons.append("battery_replacement_cost_unknown")
        else:
            effective = price + (float(battery_cost or 0) if battery_required else 0.0)
            if effective <= 1500:
                points = 30
            elif effective <= 3000:
                points = 20
            elif effective <= 5000:
                points = 10
            else:
                points = 0
            if confidence == "estimate" and points:
                points = max(0, points - 5)
                reasons.append("estimated_delivered_price_penalty")
            score += points
            if points:
                reasons.append("effective_ups_cost_value")
        reasons.append(f"price_confidence:{confidence}")
    else:
        reasons.append("price_not_nok_comparable")

    return {
        "role": "ups",
        "score": score,
        "reasons": reasons,
        "price_scored": effective is not None,
        "price_nok": price,
        "effective_cost_nok": effective,
        "battery_replacement_nok": battery_cost if battery_required else 0,
        "price_confidence": confidence,
        "replaceable_battery": hw.get("replaceable_battery"),
    }


def ups_action(result: dict) -> str:
    score = result["score"]
    confidence = result.get("price_confidence", "unknown")
    if not result.get("price_scored"):
        return "WATCH" if score >= 30 else "PASS"
    if (score >= 60 and confidence in {"domestic", "import_confirmed"}
            and result.get("replaceable_battery") is True
            and result.get("effective_cost_nok") is not None
            and result["effective_cost_nok"] <= 3000):
        return "BUY"
    if score >= 30:
        return "WATCH"
    return "PASS"
