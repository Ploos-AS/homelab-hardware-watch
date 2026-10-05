from __future__ import annotations
from datetime import date

from hhw.delivered_cost import DeliveredCostInput, calculate_delivered_nok
from hhw.fx import FxObservation, rate_to_nok
from hhw.vendor_evidence import VendorEvidence, latest_evidence
from hhw.shipping import SERVERSHOP24_NO_METHODS, cheapest_for_weight


def _evidence_values(evidence, vendor_id, observed_on):
    values = {}
    sources = []
    for kind in ("norway_checkout", "shipping", "vat", "handling"):
        obs = latest_evidence(evidence, vendor_id, kind, observed_on)
        if obs:
            values.update(obs.values)
            sources.append({
                "type": kind,
                "observed_on": obs.observed_on.isoformat(),
                "source": obs.source,
            })
    return values, sources


def enrich_delivered_cost(
    candidate,
    fx: list[FxObservation],
    observed_on: date,
    evidence: list[VendorEvidence] | None = None,
):
    metadata = candidate.metadata

    if candidate.item_price is None:
        metadata["delivered_cost"] = {
            "comparable": False,
            "reason": "item_price_unknown",
            "delivered_nok": None,
        }
        return candidate

    evidence_values, evidence_sources = _evidence_values(
        evidence or [], candidate.vendor_id, observed_on
    )

    # Candidate-specific checkout/quote metadata always wins over reusable vendor evidence.
    merged = {**evidence_values, **metadata}
    if candidate.vendor_id == "servershop24_de" and "shipping_eur" not in merged:
        weight = candidate.hardware.get("weight_kg") if candidate.hardware else None
        choice = cheapest_for_weight(weight, SERVERSHOP24_NO_METHODS)
        if choice is not None:
            shipping, method = choice
            merged["shipping_eur"] = shipping
            evidence_sources.append({
                "type": "shipping_weight_table",
                "observed_on": "2026-10-05",
                "source": "ServerShop24 Norway public shipping table",
                "method": method,
            })
    obs = rate_to_nok(candidate.currency, fx, observed_on)

    shipping = merged.get("shipping_eur") if candidate.currency == "EUR" else merged.get("shipping_nok")
    handling = merged.get("handling_nok")
    vat_rate = merged.get("foreign_vat_rate")
    vat_included = bool(merged.get("foreign_vat_included", False))
    vat_removed = merged.get("foreign_vat_removed_for_export")

    result = calculate_delivered_nok(DeliveredCostInput(
        item_price=candidate.item_price,
        currency=candidate.currency,
        exchange_rate_to_nok=obs.rate if obs else None,
        foreign_vat_rate=vat_rate,
        foreign_vat_included=vat_included,
        foreign_vat_removed_for_export=vat_removed,
        shipping=shipping,
        handling_nok=handling,
    ))
    result["fx_observed_on"] = obs.observed_on.isoformat() if obs else None
    result["fx_source"] = obs.source if obs else None
    result["vendor_evidence"] = evidence_sources
    metadata["delivered_cost"] = result
    return candidate
