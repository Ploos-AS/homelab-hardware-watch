from __future__ import annotations

import re
import requests
from bs4 import BeautifulSoup

from hhw.collectors.base import Collector
from hhw.models import Candidate


PRICE_EX = re.compile(r"€\s*([\d.,]+)\s*Excl\. VAT", re.I)
PRICE_INC = re.compile(r"€\s*([\d.,]+)\s*Incl\. VAT", re.I)
STOCK = re.compile(r"(\d+)\s+(?:in stock|units available)", re.I)


def _eur(value: str) -> float:
    return float(value.replace(".", "").replace(",", "."))


class ServerPuntCollector(Collector):
    vendor_id = "serverpunt"
    products_url = "https://serverpunt.com/en/products"

    def collect(self):
        response = requests.get(
            self.products_url,
            timeout=30,
            headers={"User-Agent": "homelab-hardware-watch/0.2"},
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        candidates = []
        seen = set()

        for link in soup.select('a[href*="/en/product/"]'):
            href = link.get("href")
            text = " ".join(link.stripped_strings)
            if not href or not text:
                continue
            url = requests.compat.urljoin(self.products_url, href)
            if url in seen:
                continue
            ex = PRICE_EX.search(text)
            inc = PRICE_INC.search(text)
            stock = STOCK.search(text)
            if not ex and not inc:
                continue

            title = re.split(r"€\s*[\d.,]+", text, maxsplit=1)[0].strip()
            candidates.append(Candidate(
                vendor_id=self.vendor_id,
                title=title,
                url=url,
                currency="EUR",
                item_price=_eur(ex.group(1)) if ex else _eur(inc.group(1)),
                stock_status="in_stock" if stock and int(stock.group(1)) > 0 else "unknown",
                condition="refurbished",
                categories=[],
                hardware={},
                metadata={
                    "collector": "serverpunt",
                    "country": "NL",
                    "price_ex_vat_eur": _eur(ex.group(1)) if ex else None,
                    "price_inc_vat_eur": _eur(inc.group(1)) if inc else None,
                    "stock_count": int(stock.group(1)) if stock else None,
                    "ships_to_norway": "unknown",
                    "shipping_eur": None,
                },
            ))
            seen.add(url)
        return candidates
