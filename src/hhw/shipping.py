from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class WeightRate:
    max_kg: float
    price: float


def price_for_weight(weight_kg: float | None, rates: list[WeightRate]) -> float | None:
    if weight_kg is None or weight_kg < 0:
        return None
    for rate in sorted(rates, key=lambda x: x.max_kg):
        if weight_kg <= rate.max_kg:
            return rate.price
    return None


SERVERSHOP24_NO_DHL_STANDARD = [
    WeightRate(7.5, 19.99),
]

SERVERSHOP24_NO_FREIGHT = [
    WeightRate(100, 129.90),
    WeightRate(250, 169.90),
    WeightRate(500, 299.90),
]
