from __future__ import annotations

import re
import requests
from bs4 import BeautifulSoup

from hhw.collectors.base import Collector
from hhw.models import Candidate


STARTING_PRICE = re.compile(
    r"(?:As low as|v\.a\.|Van)\s*€\s*([\d.,]+)(?:\s*€\s*([\d.,]+))?",
    re.I,
)


def _eur(value: str) -> float:
    value = value.strip()
    if "," in value:
        return float(value.replace(".", "").replace(",", "."))
    return float(value)


class ServerZaakCollector(Collector):
    vendor_id = "serverzaak"
    urls = [
        "https://www.serverzaak.nl/english/servers/dell.html",
    ]

    def collect(self):
        candidates = []
        seen = set()
        for page_url in self.urls:
            response = requests.get(
                page_url,
                timeout=30,
                headers={"User-Agent": "homelab-hardware-watch/0.2"},
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            for product in soup.select(".product-item"):
                text = " ".join(product.stripped_strings)
                match = STARTING_PRICE.search(text)
                link = product.select_one("a.product-item-link")
                if not match or not link:
                    continue
                url = link.get("href")
                if not url or url in seen:
                    continue

                prices = [_eur(x) for x in match.groups() if x]
                starting = min(prices)
                candidates.append(Candidate(
                    vendor_id=self.vendor_id,
                    title=" ".join(link.stripped_strings),
                    url=url,
                    currency="EUR",
                    item_price=starting,
                    stock_status="unknown",
                    condition="refurbished",
                    categories=["server", "proxmox_compute"],
                    hardware={},
                    metadata={
                        "collector": "serverzaak",
                        "country": "NL",
                        "price_kind": "starting_configuration",
                        "configurable": True,
                        "configuration_complete": False,
                        "starting_price_eur": starting,
                        "ships_to_norway": "unknown",
                        "shipping_eur": None,
                    },
                ))
                seen.add(url)
        return candidates
