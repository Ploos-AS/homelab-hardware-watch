from hhw.collectors.german_shop import EUR, STOCK_DE, STOCK_EN, eur


def test_german_eur():
    assert eur("1.539,99") == 1539.99
    assert EUR.search("1.539,99 €").group(1) == "1.539,99"


def test_stock_patterns():
    assert int(STOCK_EN.search("37 in stock").group(1)) == 37
    assert int(STOCK_DE.search("14 Stück sofort lieferbar").group(1)) == 14
