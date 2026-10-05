from hhw.vendor_policy import policy_for


def test_unknown_vendor_fails_closed():
    p = policy_for("unknown")
    assert p.norway_shipping == "unknown"
    assert p.export_vat_treatment == "unknown"


def test_rfq_vendor_requires_quote():
    p = policy_for("secondhandserver_eu")
    assert p.norway_shipping == "quote"
    assert p.shipping_price_source == "quote"
