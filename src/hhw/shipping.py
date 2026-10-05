from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class WeightRate:
    max_kg: float
    price: float
    min_kg: float = 0.0


def price_for_weight(weight_kg: float | None, rates: list[WeightRate]) -> float | None:
    if weight_kg is None or weight_kg < 0:
        return None
    for rate in sorted(rates, key=lambda x: x.max_kg):
        if rate.min_kg < weight_kg <= rate.max_kg:
            return rate.price
    return None


def cheapest_for_weight(weight_kg: float | None, methods: dict[str, list[WeightRate]]):
    choices = [
        (price, method)
        for method, rates in methods.items()
        if (price := price_for_weight(weight_kg, rates)) is not None
    ]
    return min(choices) if choices else None


# ServerShop24 Norway public table, verified 2026-10-05.
# Only the ranges needed for current server candidates are encoded here.
SERVERSHOP24_NO_METHODS = {
    "ups_express_saver": [
        WeightRate(18, 249.99, 7.5),
        WeightRate(19, 257.99),
        WeightRate(20, 264.99),
        WeightRate(22, 278.99),
        WeightRate(24, 289.99),
        WeightRate(25, 329.99),
    ],
    "fedex": [
        WeightRate(18, 114.99, 7.5),
        WeightRate(20, 114.99),
        WeightRate(25, 170.99),
    ],
    "dhl_standard": [
        WeightRate(18, 134.99, 7.5),
        WeightRate(19, 144.99),
        WeightRate(20, 144.99),
        WeightRate(22, 154.99),
        WeightRate(24, 164.99),
        WeightRate(25, 174.99),
    ],
    "dhl_express": [
        WeightRate(18, 103.99, 7.5),
        WeightRate(19, 107.99),
        WeightRate(20, 112.99),
        WeightRate(21, 117.99),
        WeightRate(22, 122.99),
        WeightRate(23, 127.99),
        WeightRate(24, 133.99),
        WeightRate(25, 138.99),
    ],
}

SERVERSHOP24_NO_DHL_STANDARD = [WeightRate(7.5, 19.99)]
SERVERSHOP24_NO_FREIGHT = [
    WeightRate(100, 129.90),
    WeightRate(250, 169.90),
    WeightRate(500, 299.90),
]
