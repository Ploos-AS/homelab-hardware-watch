import json

from hhw.models import Candidate
from hhw.monitor_run import run_monitor


def c(price=500, delivered=None):
    x = Candidate("vendor", "server", "https://example.invalid/item/1",
                  currency="EUR", item_price=price, hardware={"memory_gb": 64})
    if delivered is not None:
        x.metadata["delivered_cost"] = {
            "cost_status": "estimate",
            "estimated_delivered_nok": delivered,
        }
    return x


def test_first_run_bootstraps_without_new_candidate_event(tmp_path):
    state = tmp_path / "state.json"
    assert run_monitor([c()], str(state)) == []
    assert run_monitor([c()], str(state)) == []


def test_price_drop_is_detected_across_runs(tmp_path):
    state = tmp_path / "state.json"
    run_monitor([c(delivered=6000)], str(state))
    events = run_monitor([c(delivered=5000)], str(state))
    assert [x.event for x in events] == ["delivered_price_down"]


def test_state_is_current_not_append_only_history(tmp_path):
    state = tmp_path / "state.json"
    run_monitor([c(500)], str(state))
    run_monitor([c(450)], str(state))
    payload = json.loads(state.read_text())
    assert payload["version"] == 1
    assert len(payload["candidates"]) == 1
    assert payload["candidates"][0]["item_price"] == 450


def test_state_output_is_deterministically_sorted(tmp_path):
    state = tmp_path / "state.json"
    a = c()
    b = Candidate("vendor", "server2", "https://example.invalid/item/2",
                  currency="EUR", item_price=400)
    run_monitor([b, a], str(state))
    payload = json.loads(state.read_text())
    ids = [x["candidate_id"] for x in payload["candidates"]]
    assert ids == sorted(ids)
