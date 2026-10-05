from hhw.collectors.serverzaak import STARTING_PRICE, _eur


def test_serverzaak_starting_price_dutch():
    m = STARTING_PRICE.search("v.a. € 240,79 € 199,00")
    assert min(_eur(x) for x in m.groups() if x) == 199.0


def test_serverzaak_starting_price_english():
    m = STARTING_PRICE.search("As low as €603.79 €499.00")
    assert min(_eur(x) for x in m.groups() if x) == 499.0
