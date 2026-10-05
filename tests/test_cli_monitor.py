import json
import sys

from hhw.models import Candidate


def test_monitor_eu_reuses_collection_and_persists_state(monkeypatch, tmp_path, capsys):
    from hhw import cli

    candidate = Candidate(
        "vendor", "server", "https://example.invalid/item/1",
        currency="NOK", item_price=2500, hardware={"memory_gb": 64},
    )
    monkeypatch.setattr(cli, "collect_europe", lambda *args: ([candidate], []))

    state = tmp_path / "state.json"
    out = tmp_path / "current.json"
    report = tmp_path / "current.md"
    opportunities = tmp_path / "opportunities.md"
    monkeypatch.setattr(sys, "argv", [
        "hhw", "monitor-eu",
        "--state-file", str(state),
        "--out", str(out),
        "--report", str(report),
        "--opportunities", str(opportunities),
    ])

    cli.main()

    events = json.loads(capsys.readouterr().out)
    assert [x["event"] for x in events] == ["new_candidate"]
    assert state.exists()
    assert out.exists()
    assert report.exists()
    assert opportunities.exists()
