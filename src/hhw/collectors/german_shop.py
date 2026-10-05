from __future__ import annotations

import re
import requests
from bs4 import BeautifulSoup

from hhw.collectors.base import Collector
from hhw.models import Candidate


EUR = re.compile(r"€?\s*([\d.]+,\d{2})\s*€?", re.I)
STOCK_EN = re.compile(r"(\d+)\s+(?:in stock|available)", re.I)
STOCK_DE = re.compile(r"(\d+)\s+(?:Stück|sofort lieferbar)", re.I)
WEIGHT = re.compile(r"(?:Weight|Gewicht)\s*:?\s*([\d.,]+)\s*kg\b", re.I)


def eur(value: str) -> float:
    return float(value.replace(".", "").replace(",", "."))


def parse_weight_kg(text: str) -> float | None:
    match = WEIGHT.search(text)
    if not match:
        return None
    return float(match.group(1).replace(",", "."))


def fetch_product_weight(url: str) -> float | None:
    r = requests.get(url, timeout=30, headers={"User-Agent": "homelab-hardware-watch/0.3"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return parse_weight_kg(" ".join(soup.stripped_strings))


class GermanCatalogueCollector(Collector):
    def __init__(self, vendor_id: str, urls: list[str], configurable: bool = False):
        self.vendor_id = vendor_id
        self.urls = urls
        self.configurable = configurable

    def collect(self):
        out = []
        seen = set()
        for page_url in self.urls:
            r = requests.get(page_url, timeout=30, headers={"User-Agent": "homelab-hardware-watch/0.2"})
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            for product in soup.select(".product-item, .product-box, .product"):
                text = " ".join(product.stripped_strings)
                link = product.select_one("a[href]")
                prices = EUR.findall(text)
                if not link or not prices:
                    continue
                href = link.get("href")
                url = requests.compat.urljoin(page_url, href)
                if url in seen:
                    continue
                title = link.get("title") or " ".join(link.stripped_strings)
                if not title:
                    continue
                price = eur(prices[-1])
                stock = STOCK_EN.search(text) or STOCK_DE.search(text)
                hardware = {}
                if self.vendor_id == "servershop24_de":
                    try:
                        weight = fetch_product_weight(url)
                        if weight is not None:
                            hardware["weight_kg"] = weight
                    except requests.RequestException:
                        pass
                out.append(Candidate(
                    vendor_id=self.vendor_id,
                    title=title.strip(),
                    url=url,
                    currency="EUR",
                    item_price=price,
                    stock_status="in_stock" if stock and int(stock.group(1)) > 0 else "unknown",
                    condition="refurbished",
                    categories=[],
                    hardware=hardware,
                    metadata={
                        "collector": "german_catalogue",
                        "country": "DE",
                        "vat_basis": "local_vat_included",
                        "configurable": self.configurable,
                        "configuration_complete": not self.configurable,
                        "stock_count": int(stock.group(1)) if stock else None,
                        "ships_to_norway": "unknown",
                        "shipping_eur": None,
                    },
                ))
                seen.add(url)
        return out
