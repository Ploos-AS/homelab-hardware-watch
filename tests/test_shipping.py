from hhw.shipping import (
    SERVERSHOP24_NO_DHL_STANDARD,
    SERVERSHOP24_NO_FREIGHT,
    price_for_weight,
)


def test_servershop24_dhl_known_range():
    assert price_for_weight(1, SERVERSHOP24_NO_DHL_STANDARD) == 19.99
    assert price_for_weight(7.5, SERVERSHOP24_NO_DHL_STANDARD) == 19.99


def test_shipping_fails_closed_above_verified_range():
    assert price_for_weight(8, SERVERSHOP24_NO_DHL_STANDARD) is None


def test_servershop24_freight_tiers():
    assert price_for_weight(80, SERVERSHOP24_NO_FREIGHT) == 129.90
    assert price_for_weight(200, SERVERSHOP24_NO_FREIGHT) == 169.90
    assert price_for_weight(400, SERVERSHOP24_NO_FREIGHT) == 299.90
    assert price_for_weight(501, SERVERSHOP24_NO_FREIGHT) is None


def test_servershop24_cheapest_carrier_for_18kg_server():
    from hhw.shipping import SERVERSHOP24_NO_METHODS, cheapest_for_weight
    assert cheapest_for_weight(18, SERVERSHOP24_NO_METHODS) == (103.99, "dhl_express")


def test_servershop24_cheapest_carrier_for_22kg_server():
    from hhw.shipping import SERVERSHOP24_NO_METHODS, cheapest_for_weight
    assert cheapest_for_weight(22, SERVERSHOP24_NO_METHODS) == (122.99, "dhl_express")
