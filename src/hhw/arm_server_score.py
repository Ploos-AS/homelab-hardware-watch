from __future__ import annotations

from hhw.decision_price import decision_price_signal
from hhw.models import Candidate
from hhw.arm_server_enrich import enrich_arm_server


def score_arm_server(candidate: Candidate) -> dict:
    candidate = enrich_arm_server(candidate)
    hw = candidate.hardware or {}
    score = 0
    reasons = []
    if hw.get("architecture") not in {"arm64", "aarch64"}:
        score -= 100; reasons.append("not_arm64")
    cores = hw.get("cpu_cores")
    if cores is not None:
        if cores >= 80: score += 30; reasons.append("cores>=80")
        elif cores >= 32: score += 20; reasons.append("cores>=32")
        elif cores >= 16: score += 10; reasons.append("cores>=16")
    ram = hw.get("memory_gb")
    if ram is not None:
        if ram >= 128: score += 25; reasons.append("ram>=128gb")
        elif ram >= 64: score += 15; reasons.append("ram>=64gb")
        elif ram >= 32: score += 5; reasons.append("ram>=32gb")
    if hw.get("ecc") is True: score += 10; reasons.append("ecc")
    if (hw.get("network_gbps") or 0) >= 10: score += 10; reasons.append("network>=10gbe")
    if hw.get("pcie_expandable") is True: score += 5; reasons.append("pcie_expandable")
    if hw.get("linux_supported") is False: score -= 50; reasons.append("linux_support_risk")

    price, confidence, ready = decision_price_signal(candidate)
    if price is not None:
        # ARM servers are opportunistic: cheap enough to beat assembling many SBC runners.
        if price <= 3000: score += 40; reasons.append("exceptionally_cheap_arm_server")
        elif price <= 5000: score += 25; reasons.append("cheap_arm_server")
        elif price <= 8000: score += 10; reasons.append("arm_server_price_watch")
        if confidence == "estimate": score -= 5; reasons.append("estimated_delivered_price_penalty")
    else:
        reasons.append("price_not_nok_comparable")
    return {"role":"arm_server","score":score,"reasons":reasons,"price_scored":price is not None,
            "price_nok":price,"price_confidence":confidence,"ready_cost":ready}


def arm_server_action(result: dict) -> str:
    if result["score"] >= 65 and result.get("price_confidence") in {"domestic","import_confirmed"}:
        return "BUY"
    return "WATCH" if result["score"] >= 30 else "PASS"
