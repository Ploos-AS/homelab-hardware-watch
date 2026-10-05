from hhw.vendor_policy import policy_for


def test_unknown_vendor_fails_closed():
    p = policy_for("unknown")
    assert p.norway_shipping == "unknown"
    assert p.export_vat_treatment == "unknown"


def test_rfq_vendor_requires_quote():
    p = policy_for("secondhandserver_eu")
    assert p.norway_shipping == "quote"
    assert p.shipping_price_source == "quote"


def test_nl_storefronts_require_checkout_shipping():
    assert policy_for("serverpunt_nl").shipping_price_source == "checkout"
    assert policy_for("serverzaak_nl").shipping_price_source == "checkout"
    assert policy_for("serverpunt_nl").export_vat_treatment == "unknown"
    assert policy_for("serverzaak_nl").export_vat_treatment == "unknown"


def test_servershop24_has_confirmed_norway_export_policy():
    p = policy_for("servershop24_de")
    assert p.norway_shipping == "confirmed"
    assert p.export_vat_treatment == "confirmed"
    assert p.shipping_price_source == "weight_table"


def test_serverando_norway_shipping_confirmed_but_vat_unknown():
    p = policy_for("serverando_de")
    assert p.norway_shipping == "confirmed"
    assert p.shipping_price_source == "weight_table"
    assert p.export_vat_treatment == "unknown"


def test_gekko_stays_checkout_until_norway_terms_are_verified():
    p = policy_for("gekko_de")
    assert p.norway_shipping == "checkout"
    assert p.export_vat_treatment == "unknown"
