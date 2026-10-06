import sys

from hhw.models import Candidate
from hhw.price_history_store import load_price_history


def test_cli_history_file_records_collection_and_deduplicates_same_day(monkeypatch, tmp_path):
    from hhw import cli

    candidate = Candidate(
        "vendor", "server", "https://example.invalid/item/42",
        currency="NOK", item_price=2500,
    )
    monkeypatch.setattr(cli, "collect_norway", lambda *args: ([candidate], []))

    history = tmp_path / "history.json"
    out = tmp_path / "current.json"
    report = tmp_path / "current.md"
    opportunities = tmp_path / "opportunities.md"
    argv = [
        "hhw", "collect-no",
        "--history-file", str(history),
        "--out", str(out),
        "--report", str(report),
        "--opportunities", str(opportunities),
    ]

    monkeypatch.setattr(sys, "argv", argv)
    cli.main()
    monkeypatch.setattr(sys, "argv", argv)
    cli.main()

    observations = load_price_history(history)
    assert len(observations) == 1
    assert observations[0].item_price == 2500


def test_cli_without_history_file_does_not_create_history(monkeypatch, tmp_path):
    from hhw import cli

    candidate = Candidate("vendor", "server", "https://example.invalid/item/42", item_price=2500)
    monkeypatch.setattr(cli, "collect_norway", lambda *args: ([candidate], []))

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", [
        "hhw", "collect-no",
        "--out", "current.json",
        "--report", "current.md",
        "--opportunities", "opportunities.md",
    ])
    cli.main()

    assert not (tmp_path / "data" / "price-history.json").exists()
