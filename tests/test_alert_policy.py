from hhw.alert_policy import alert_worthy, filter_alerts
from hhw.monitor_run import MonitorEvent


def e(event, action=None):
    return MonitorEvent("id", "vendor", "https://example.invalid", event, action, 4000)


def test_buy_and_watch_transitions_alert():
    assert alert_worthy(e("became_buy", "BUY"))
    assert alert_worthy(e("became_watch", "WATCH"))


def test_new_actionable_candidate_alerts_after_bootstrap():
    assert alert_worthy(e("new_candidate", "BUY"))
    assert alert_worthy(e("new_candidate", "WATCH"))


def test_new_pass_candidate_stays_silent():
    assert not alert_worthy(e("new_candidate", "PASS"))
    assert not alert_worthy(e("new_candidate"))


def test_price_drop_only_alerts_for_actionable_candidate():
    assert alert_worthy(e("delivered_price_down", "WATCH"))
    assert alert_worthy(e("item_price_down", "BUY"))
    assert not alert_worthy(e("delivered_price_down", "PASS"))
    assert not alert_worthy(e("item_price_down", None))


def test_filter_alerts_removes_noise():
    events = [
        e("new_candidate"),
        e("delivered_price_down", "PASS"),
        e("became_buy", "BUY"),
    ]
    assert [x.event for x in filter_alerts(events)] == ["became_buy"]
