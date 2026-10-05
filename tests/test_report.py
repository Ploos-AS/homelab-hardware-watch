from hhw.models import Candidate
from hhw.report import markdown_report


def test_report_sorts_by_price():
    items = [
        Candidate(vendor_id="a", title="Expensive", url="https://example/a", item_price=2000),
        Candidate(vendor_id="b", title="Cheap", url="https://example/b", item_price=1000),
    ]
    report = markdown_report(items)
    assert report.index("Cheap") < report.index("Expensive")
