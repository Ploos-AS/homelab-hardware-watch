from hhw.marketplace import MarketplaceListing, lifecycle


def test_finn_code_wins_identity():
    x = MarketplaceListing("finn_no", "M920q", "https://finn.no/x?foo=1", source_id="123")
    assert x.identity() == "finn_no:123"


def test_url_query_is_ignored_for_identity():
    a = MarketplaceListing("finn_no", "M920q", "https://finn.no/abc?x=1")
    b = MarketplaceListing("finn_no", "M920q", "https://finn.no/abc?x=2")
    assert a.identity() == b.identity()


def test_price_change():
    assert lifecycle(2000, 1500, True) == "price_changed"
    assert lifecycle(None, 1500, False) == "new"
