import json
from datetime import date

from hhw.cli import load_fx
from hhw.fx import rate_to_nok


def test_load_fx(tmp_path):
    p = tmp_path / "fx.json"
    p.write_text(json.dumps({"observations": [{
        "base": "EUR", "quote": "NOK", "rate": 11.5,
        "observed_on": "2026-10-01", "source": "norges_bank"
    }]}))
    observations = load_fx(p)
    assert rate_to_nok("EUR", observations, date(2026, 10, 2)).rate == 11.5
