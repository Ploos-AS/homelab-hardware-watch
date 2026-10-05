from bs4 import BeautifulSoup
from hhw.collectors.serverpunt import PRICE_EX, PRICE_INC, STOCK, _eur


def test_serverpunt_price_and_stock_patterns():
    text = "Dell R640 8SFF 1U Rack Server €205,00 Excl. VAT €248,05 Incl. VAT 6 in stock"
    assert _eur(PRICE_EX.search(text).group(1)) == 205.0
    assert _eur(PRICE_INC.search(text).group(1)) == 248.05
    assert int(STOCK.search(text).group(1)) == 6


def test_european_number_parser():
    assert _eur("1.234,56") == 1234.56
