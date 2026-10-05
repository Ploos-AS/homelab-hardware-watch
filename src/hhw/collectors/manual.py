from hhw.collectors.base import Collector
from hhw.models import Candidate


class ManualLeadCollector(Collector):
    """Represents a source that requires human/RFQ/list signup interaction."""

    def __init__(self, vendor_id: str, url: str, categories: list[str], note: str):
        self.vendor_id = vendor_id
        self.url = url
        self.categories = categories
        self.note = note

    def collect(self) -> list[Candidate]:
        return [
            Candidate(
                vendor_id=self.vendor_id,
                title=f"Manual sourcing lead: {self.vendor_id}",
                url=self.url,
                item_price=None,
                stock_status="manual",
                categories=list(self.categories),
                metadata={"collector": "manual_lead", "note": self.note},
            )
        ]
