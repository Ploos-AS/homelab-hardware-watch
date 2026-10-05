from __future__ import annotations
from dataclasses import dataclass
import hashlib
import re


@dataclass
class MarketplaceListing:
    source: str
    title: str
    url: str
    price_nok: float | None = None
    source_id: str | None = None
    seller_id: str | None = None

    def identity(self) -> str:
        if self.source_id:
            return f"{self.source}:{self.source_id}"
        normalized_url = self.url.split("?")[0].rstrip("/")
        if normalized_url:
            return f"{self.source}:url:{normalized_url}"
        key = f"{self.source}|{self.seller_id or ''}|{normalize_title(self.title)}"
        return f"{self.source}:fallback:{hashlib.sha256(key.encode()).hexdigest()[:20]}"


def normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip().lower())


def lifecycle(previous_price: float | None, current_price: float | None, seen_before: bool) -> str:
    if not seen_before:
        return "new"
    if previous_price is not None and current_price is not None and previous_price != current_price:
        return "price_changed"
    return "active"
