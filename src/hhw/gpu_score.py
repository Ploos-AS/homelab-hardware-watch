from __future__ import annotations

from hhw.decision_price import decision_price_signal
from hhw.models import Candidate


def score_gpu(candidate: Candidate) -> dict:
    hw = candidate.hardware or {}
    score = 0
    reasons = []
    vram = hw.get("gpu_vram_gb")
    price, confidence, ready = decision_price_signal(candidate)
    if vram is not None:
        if vram >= 48: score += 50; reasons.append("vram>=48gb")
        elif vram >= 32: score += 40; reasons.append("vram>=32gb")
        elif vram >= 24: score += 35; reasons.append("vram>=24gb")
        elif vram >= 16: score += 20; reasons.append("vram>=16gb")
        elif vram >= 12: score += 8; reasons.append("vram>=12gb")
    if price is not None and vram:
        vram_per_1000 = vram * 1000.0 / price if price > 0 else 999.0
        if vram_per_1000 >= 8: score += 35; reasons.append("vram_value>=8gb_per_1000nok")
        elif vram_per_1000 >= 5: score += 25; reasons.append("vram_value>=5gb_per_1000nok")
        elif vram_per_1000 >= 3: score += 15; reasons.append("vram_value>=3gb_per_1000nok")
        if confidence == "estimate": score -= 5; reasons.append("estimated_delivered_price_penalty")
    if hw.get("compute_supported") is False: score -= 40; reasons.append("compute_support_risk")
    if hw.get("passive_cooling") is True and hw.get("airflow_ready") is not True:
        score -= 15; reasons.append("passive_cooling_requires_host_airflow")
    return {"role":"gpu","score":score,"reasons":reasons,"vram_gb":vram,
            "price_scored":price is not None,"price_nok":price,
            "price_confidence":confidence,"ready_cost":ready}


def gpu_action(result: dict) -> str:
    if result["score"] >= 65 and result.get("price_confidence") in {"domestic","import_confirmed"}:
        return "BUY"
    return "WATCH" if result["score"] >= 30 else "PASS"
