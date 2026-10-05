from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class DeliveredCostInput:
    item_price: float
    currency: str
    exchange_rate_to_nok: float | None
    foreign_vat_rate: float | None = None
    foreign_vat_included: bool = False
    foreign_vat_removed_for_export: bool | None = None
    shipping: float | None = None
    handling_nok: float | None = None
    norwegian_vat_rate: float = 0.25


def calculate_delivered_nok(x: DeliveredCostInput) -> dict:
    if x.currency == "NOK":
        rate = 1.0
    elif x.exchange_rate_to_nok is None:
        return {"comparable": False, "reason": "exchange_rate_unknown", "delivered_nok": None}
    else:
        rate = x.exchange_rate_to_nok

    if x.shipping is None:
        return {"comparable": False, "reason": "shipping_unknown", "delivered_nok": None}
    if x.handling_nok is None:
        return {"comparable": False, "reason": "handling_unknown", "delivered_nok": None}

    item = x.item_price
    if x.foreign_vat_included:
        if x.foreign_vat_removed_for_export is None:
            return {"comparable": False, "reason": "foreign_vat_export_treatment_unknown", "delivered_nok": None}
        if x.foreign_vat_removed_for_export:
            if not x.foreign_vat_rate:
                return {"comparable": False, "reason": "foreign_vat_rate_unknown", "delivered_nok": None}
            item = item / (1.0 + x.foreign_vat_rate)

    item_nok = item * rate
    shipping_nok = x.shipping * rate
    norwegian_vat = (item_nok + shipping_nok) * x.norwegian_vat_rate
    delivered = item_nok + shipping_nok + norwegian_vat + x.handling_nok

    return {
        "comparable": True,
        "reason": None,
        "item_export_nok": round(item_nok, 2),
        "shipping_nok": round(shipping_nok, 2),
        "norwegian_vat_nok": round(norwegian_vat, 2),
        "handling_nok": round(x.handling_nok, 2),
        "delivered_nok": round(delivered, 2),
        "exchange_rate_to_nok": rate,
    }
