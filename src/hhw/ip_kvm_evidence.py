from __future__ import annotations

import re
from datetime import date

from hhw.component_evidence import ComponentCostEvidence
from hhw.decision_price import decision_price_signal
from hhw.ip_kvm_module_catalog import MODULE_CATALOG
from hhw.ip_kvm_ready_cost import kvm_module_evidence_key


def observe_kvm_module_cost(candidate, observed_on: date) -> ComponentCostEvidence | None:
    """Turn a loose interface-module listing into unit-cost evidence."""
    text = " ".join(filter(None, [
        candidate.title,
        str((candidate.metadata or {}).get("description") or ""),
    ]))
    matches = []
    for model in sorted(MODULE_CATALOG, key=len, reverse=True):
        pattern = rf"(?:(\d+)\s*(?:x|×|stk\.?|pcs?\.?|pieces?)\s*)?\b{re.escape(model)}(?![-A-Z0-9])"
        match = re.search(pattern, text, re.I)
        if match:
            matches.append((model, int(match.group(1) or 1)))
    if len(matches) != 1:
        return None

    model, quantity = matches[0]
    # A bare model is only safely a single-unit observation when the listing
    # does not advertise an ambiguous lot/bundle.
    if quantity == 1 and re.search(r"\b(?:lot|bundle|pakke|sett|flere)\b", text, re.I):
        return None

    price, confidence, _ = decision_price_signal(candidate)
    if price is None or confidence not in {"domestic", "import_confirmed"}:
        return None

    key = kvm_module_evidence_key(None, model)
    return ComponentCostEvidence(
        component="kvm_interface_module",
        evidence_key=key,
        cost_nok=float(price) / quantity,
        observed_on=observed_on,
        source=candidate.url,
        note=f"{quantity}x {model}; {confidence}",
    )
