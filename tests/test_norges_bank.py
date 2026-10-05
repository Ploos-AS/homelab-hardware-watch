from hhw.providers.norges_bank import parse_csv


def test_parse_norges_bank_csv():
    text = "TIME_PERIOD;OBS_VALUE\n2026-09-29;10.8735\n2026-09-30;10.9015\n"
    x = parse_csv(text, "EUR")
    assert len(x) == 2
    assert x[0].base == "EUR"
    assert x[0].quote == "NOK"
    assert x[1].rate == 10.9015
    assert x[1].source == "norges_bank"
