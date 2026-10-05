from __future__ import annotations
from hhw.models import Candidate

REFERENCE_MEMORY_GB = 16

# Working assumptions for comparison only. These are deliberately separate
# from observed listing prices and can later be replaced by component watches.
UPGRADE_ASSUMPTIONS_NOK = {
    "memory_to_16gb": 400,
}


def configuration_parity(candidate: Candidate) -> dict:
    memory = candidate.hardware.get("memory_gb")
    adjustments = []
    adjusted = candidate.item_price

    if memory is None:
        return {
            "comparable": False,
            "reason": "memory_unknown",
            "observed_price_nok": candidate.item_price,
            "adjusted_price_nok": None,
            "adjustments": [],
        }

    if memory < REFERENCE_MEMORY_GB:
        cost = UPGRADE_ASSUMPTIONS_NOK["memory_to_16gb"]
        adjustments.append({
            "type": "memory",
            "from_gb": memory,
            "to_gb": REFERENCE_MEMORY_GB,
            "estimated_cost_nok": cost,
        })
        if adjusted is not None:
            adjusted += cost

    return {
        "comparable": adjusted is not None,
        "reason": None if adjusted is not None else "price_unknown",
        "observed_price_nok": candidate.item_price,
        "adjusted_price_nok": adjusted,
        "adjustments": adjustments,
    }
