from hhw.alert_report import markdown_alerts
from hhw.monitor_run import MonitorEvent


def test_empty_alert_report_is_explicit():
    assert "No actionable hardware changes." in markdown_alerts([])


def test_alert_report_contains_action_price_and_link():
    event = MonitorEvent(
        "id", "vendor", "https://example.invalid/item", "became_buy", "BUY", 2499.4
    )
    report = markdown_alerts([event])
    assert "| BUY | became_buy | vendor | 2499 NOK | — |" in report
    assert "[open](https://example.invalid/item)" in report


def test_alert_report_shows_delivered_price_drop_context():
    event = MonitorEvent(
        "id", "vendor", "https://example.invalid/item", "delivered_price_down",
        "WATCH", 5400, previous_delivered_nok=6200,
    )
    report = markdown_alerts([event])
    assert "6200 → 5400 NOK (-800, -12.9%)" in report


def test_alert_report_shows_item_price_drop_with_currency():
    event = MonitorEvent(
        "id", "vendor", "https://example.invalid/item", "item_price_down",
        "BUY", None, item_price=450, previous_item_price=500, currency="EUR",
    )
    report = markdown_alerts([event])
    assert "500.00 → 450.00 EUR (-50.00, -10.0%)" in report
