from __future__ import annotations

import re
import requests
from bs4 import BeautifulSoup

from hhw.collectors.base import Collector
from hhw.models import Candidate


_PRICE_RE = re.compile(r"(\d[\d .]*)\s*(?:kr|,-)")


class WooCommerceCategoryCollector(Collector):
    """Conservative WooCommerce category collector.

    It extracts product cards only. Detailed hardware normalization belongs to
    a later enrichment stage so the collector does not guess specifications.
    """

    def __init__(self, vendor_id: str, urls: list[str], categories: list[str], timeout: int = 20):
        self.vendor_id = vendor_id
        self.urls = urls
        self.categories = categories
        self.timeout = timeout

    def collect(self) -> list[Candidate]:
        found: dict[str, Candidate] = {}
        for source_url in self.urls:
            response = requests.get(
                source_url,
                timeout=self.timeout,
                headers={"User-Agent": "homelab-hardware-watch/0.1"},
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            for card in soup.select("li.product, .product"):
                link = card.select_one("a[href]")
                title_node = card.select_one(".woocommerce-loop-product__title, h2, h3")
                if not link or not title_node:
                    continue
                title = title_node.get_text(" ", strip=True)
                url = link.get("href")
                if not title or not url:
                    continue
                price_text = " ".join(x.get_text(" ", strip=True) for x in card.select(".price"))
                prices = [
                    float(m.replace(" ", "").replace(".", ""))
                    for m in _PRICE_RE.findall(price_text)
                ]
                found[url] = Candidate(
                    vendor_id=self.vendor_id,
                    title=title,
                    url=url,
                    item_price=min(prices) if prices else None,
                    stock_status="unknown",
                    categories=list(self.categories),
                    metadata={"collector": "woocommerce_category", "source_url": source_url},
                )
        return list(found.values())
