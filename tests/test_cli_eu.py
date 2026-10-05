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


def test_collect_europe_passes_vendor_evidence(monkeypatch, tmp_path):
    from hhw import cli
    monkeypatch.setattr(cli, "fetch_customs_fx", lambda currency, day: None)
    from hhw.models import Candidate

    fx = tmp_path / "fx.json"
    fx.write_text(json.dumps({"observations": [{
        "base": "EUR", "quote": "NOK", "rate": 10.0,
        "observed_on": "2026-10-05", "source": "test"
    }]}))
    evidence = tmp_path / "evidence.json"
    evidence.write_text(json.dumps({"observations": [
        {"vendor_id": "vendor", "observed_on": "2026-10-05",
         "evidence_type": "shipping", "source": "checkout",
         "values": {"shipping_eur": 20}},
        {"vendor_id": "vendor", "observed_on": "2026-10-05",
         "evidence_type": "vat", "source": "terms",
         "values": {"foreign_vat_included": True, "foreign_vat_rate": 0.19,
                    "foreign_vat_removed_for_export": True}},
        {"vendor_id": "vendor", "observed_on": "2026-10-05",
         "evidence_type": "handling", "source": "policy",
         "values": {"handling_nok": 100}}
    ]}))

    class Collector:
        vendor_id = "vendor"
        def collect(self):
            return [Candidate("vendor", "server", "https://example.invalid",
                              currency="EUR", item_price=119)]

    monkeypatch.setattr(cli, "european_collectors", lambda: [Collector()])
    candidates, errors = cli.collect_europe(fx, evidence, date(2026, 10, 5))
    assert errors == []
    assert candidates[0].metadata["delivered_cost"]["delivered_nok"] == 1600.0


def test_save_fx_preserves_history_and_deduplicates(tmp_path):
    from hhw.cli import load_fx, save_fx
    from hhw.fx import FxObservation

    p = tmp_path / "fx.json"
    old = FxObservation("EUR", "NOK", 11.0, date(2026, 9, 1), "norges_bank")
    duplicate_old = FxObservation("EUR", "NOK", 11.1, date(2026, 9, 1), "norges_bank")
    new = FxObservation("EUR", "NOK", 11.5, date(2026, 10, 1), "norges_bank")

    saved = save_fx(p, [old, duplicate_old, new])
    assert len(saved) == 2
    assert saved[0].rate == 11.1
    assert [x.observed_on for x in load_fx(p)] == [date(2026, 9, 1), date(2026, 10, 1)]
