from __future__ import annotations

from hhw.component_cost import ready_cost
from hhw.models import Candidate


def decision_price_signal(candidate: Candidate) -> tuple[float | None, str, dict]:
    """Return role-ready NOK price, confidence and cost evidence.

    Required missing components are part of the decision price. If any required
    component cost is unknown, price scoring fails closed.
    """
    cost = ready_cost(candidate)
    if not cost["comparable"]:
        return None, cost["price_confidence"], cost
    return float(cost["ready_cost_nok"]), cost["price_confidence"], cost
