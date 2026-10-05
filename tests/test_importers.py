import json
from hhw.importers import import_marketplace_json


def test_import_marketplace_json(tmp_path):
    p = tmp_path / "in.json"
    p.write_text(json.dumps({"listings": [{
        "source": "finn_no",
        "source_id": "123",
        "title": "Intel NUC 11 Pro i5 16GB RAM 512GB NVMe",
        "url": "https://www.finn.no/123",
        "price_nok": 2200
    }]}))
    rows = import_marketplace_json(p)
    assert len(rows) == 1
    assert rows[0].vendor_id == "finn_no"
    assert rows[0].item_price == 2200
    assert rows[0].metadata["source_id"] == "123"
