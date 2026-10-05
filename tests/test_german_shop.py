from hhw.collectors.german_shop import EUR, STOCK_DE, STOCK_EN, eur


def test_german_eur():
    assert eur("1.539,99") == 1539.99
    assert EUR.search("1.539,99 €").group(1) == "1.539,99"


def test_stock_patterns():
    assert int(STOCK_EN.search("37 in stock").group(1)) == 37
    assert int(STOCK_DE.search("14 Stück sofort lieferbar").group(1)) == 14


def test_parse_weight_kg_english():
    from hhw.collectors.german_shop import parse_weight_kg
    assert parse_weight_kg("Dimensions 50 cm Weight: 6.8 kg Warranty") == 6.8


def test_parse_weight_kg_german_decimal_comma():
    from hhw.collectors.german_shop import parse_weight_kg
    assert parse_weight_kg("Technische Daten Gewicht: 7,25 kg Zustand") == 7.25


def test_parse_weight_kg_missing_is_unknown():
    from hhw.collectors.german_shop import parse_weight_kg
    assert parse_weight_kg("Dell PowerEdge server") is None
