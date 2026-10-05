from __future__ import annotations

import json
from pathlib import Path
from hhw.models import Candidate


def import_marketplace_json(path: str | Path) -> list[Candidate]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = data if isinstance(data, list) else data.get("listings", [])
    candidates = []
    for row in rows:
        title = row.get("title")
        url = row.get("url")
        if not title or not url:
            continue
        candidates.append(Candidate(
            vendor_id=row.get("source", "marketplace"),
            title=title,
            url=url,
            currency=row.get("currency", "NOK"),
            item_price=row.get("price_nok"),
            stock_status=row.get("status", "active"),
            condition=row.get("condition", "used"),
            categories=row.get("categories", []),
            hardware=row.get("hardware", {}),
            metadata={
                "collector": "marketplace_import",
                "source_id": row.get("source_id"),
                "seller_id": row.get("seller_id"),
                "observed_at": row.get("observed_at"),
            },
        ))
    return candidates
