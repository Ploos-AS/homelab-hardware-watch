from hhw.alert_report import markdown_alerts
from hhw.monitor_run import MonitorEvent


def test_empty_alert_report_is_explicit():
    assert "No actionable hardware changes." in markdown_alerts([])


def test_alert_report_contains_action_price_and_link():
    event = MonitorEvent(
        "id", "vendor", "https://example.invalid/item", "became_buy", "BUY", 2499.4
    )
    report = markdown_alerts([event])
    assert "| BUY | became_buy | vendor | 2499 NOK |" in report
    assert "[open](https://example.invalid/item)" in report
