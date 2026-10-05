from hhw.collectors.official_vendor import OfficialVendorWatchCollector


def test_official_vendor_watch_is_not_fake_price():
    c = OfficialVendorWatchCollector("dell_no", "https://www.dell.com/no-no/shop/deals", ["tiny"], "test").collect()[0]
    assert c.currency == "NOK"
    assert c.item_price is None
    assert c.condition == "new"
    assert c.metadata["source_type"] == "official_vendor"
    assert c.metadata["campaign_dynamic"] is True
