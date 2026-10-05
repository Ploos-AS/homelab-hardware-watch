from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Candidate:
    vendor_id: str
    title: str
    url: str
    currency: str = "NOK"
    item_price: float | None = None
    stock_status: str = "unknown"
    condition: str = "refurbished"
    categories: list[str] = field(default_factory=list)
    hardware: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
