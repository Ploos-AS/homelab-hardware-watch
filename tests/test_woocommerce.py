from hhw.collectors.woocommerce import WooCommerceCategoryCollector


def test_price_regex_is_not_used_to_invent_specs():
    collector = WooCommerceCategoryCollector("x", ["https://example.invalid"], ["tiny"])
    assert collector.vendor_id == "x"
    assert collector.categories == ["tiny"]
