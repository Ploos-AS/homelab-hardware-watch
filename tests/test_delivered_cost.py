from hhw.delivered_cost import DeliveredCostInput, calculate_delivered_nok


def test_eu_vat_removed_then_norwegian_vat_added():
    x = DeliveredCostInput(
        item_price=119.0, currency="EUR", exchange_rate_to_nok=10.0,
        foreign_vat_rate=0.19, foreign_vat_included=True,
        foreign_vat_removed_for_export=True, shipping=20.0, handling_nok=100.0,
    )
    r = calculate_delivered_nok(x)
    assert r["item_export_nok"] == 1000.0
    assert r["shipping_nok"] == 200.0
    assert r["norwegian_vat_nok"] == 300.0
    assert r["delivered_nok"] == 1600.0


def test_unknown_export_vat_blocks_comparison():
    x = DeliveredCostInput(
        item_price=119.0, currency="EUR", exchange_rate_to_nok=10.0,
        foreign_vat_rate=0.19, foreign_vat_included=True,
        foreign_vat_removed_for_export=None, shipping=20.0, handling_nok=100.0,
    )
    r = calculate_delivered_nok(x)
    assert r["comparable"] is False
    assert r["reason"] == "foreign_vat_export_treatment_unknown"


def test_unknown_exchange_rate_blocks_eur():
    x = DeliveredCostInput(item_price=100, currency="EUR", exchange_rate_to_nok=None, shipping=10, handling_nok=50)
    assert calculate_delivered_nok(x)["reason"] == "exchange_rate_unknown"
