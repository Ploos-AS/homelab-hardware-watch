from __future__ import annotations

from typing import Iterable
import requests

from hhw.collectors.base import Collector
from hhw.models import Candidate


class ShopifyProductsCollector(Collector):
    """Collector for public Shopify products.json feeds.

    M1 deliberately uses a documented/stable storefront surface where available
    rather than scraping rendered HTML.
    """

    def __init__(
        self,
        vendor_id: str,
        base_url: str,
        collections: Iterable[str],
        categories: list[str],
        timeout: int = 20,
    ):
        self.vendor_id = vendor_id
        self.base_url = base_url.rstrip("/")
        self.collections = list(collections)
        self.categories = categories
        self.timeout = timeout

    def collect(self) -> list[Candidate]:
        found: dict[str, Candidate] = {}
        for collection in self.collections:
            url = f"{self.base_url}/collections/{collection}/products.json?limit=250"
            response = requests.get(url, timeout=self.timeout, headers={"User-Agent": "homelab-hardware-watch/0.1"})
            response.raise_for_status()
            for product in response.json().get("products", []):
                variants = product.get("variants") or []
                prices = []
                available = False
                for variant in variants:
                    try:
                        prices.append(float(variant["price"]))
                    except (KeyError, TypeError, ValueError):
                        pass
                    available = available or bool(variant.get("available", False))
                handle = product.get("handle", "")
                product_url = f"{self.base_url}/products/{handle}" if handle else self.base_url
                found[product_url] = Candidate(
                    vendor_id=self.vendor_id,
                    title=product.get("title", "Unknown product"),
                    url=product_url,
                    item_price=min(prices) if prices else None,
                    stock_status="in_stock" if available else "unknown",
                    categories=list(self.categories),
                    metadata={
                        "collector": "shopify_products_json",
                        "collection": collection,
                        "product_type": product.get("product_type"),
                        "vendor": product.get("vendor"),
                    },
                )
        return list(found.values())
