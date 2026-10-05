from __future__ import annotations

from hhw.collectors.base import Collector
from hhw.models import Candidate


class OfficialVendorWatchCollector(Collector):
    """Conservative watch entry for official vendors with dynamic campaigns."""

    def __init__(self, vendor_id: str, url: str, categories: list[str], note: str):
        self.vendor_id = vendor_id
        self.url = url
        self.categories = categories
        self.note = note

    def collect(self) -> list[Candidate]:
        return [Candidate(
            vendor_id=self.vendor_id,
            title=f"Official vendor campaign watch: {self.vendor_id}",
            url=self.url,
            currency="NOK",
            item_price=None,
            stock_status="watch",
            condition="new",
            categories=list(self.categories),
            hardware={},
            metadata={
                "collector": "official_vendor_watch",
                "source_type": "official_vendor",
                "country": "NO",
                "campaign_dynamic": True,
                "normal_price_nok": None,
                "campaign_price_nok": None,
                "discount_pct": None,
                "coupon": None,
                "valid_until": None,
                "note": self.note,
            },
        )]
