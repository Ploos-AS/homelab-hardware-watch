from hhw.collectors.shopify import ShopifyProductsCollector


def norwegian_collectors():
    return [
        ShopifyProductsCollector(
            vendor_id="itgarasjen_no",
            base_url="https://itgarasjen.no",
            collections=["server", "servere-hjemmeside", "arbeidsstasjoner", "deler-og-komponenter"],
            categories=["proxmox_compute", "storage", "tiny", "ci_runner", "components"],
        ),
        ShopifyProductsCollector(
            vendor_id="axentra_no",
            base_url="https://axentra.no",
            collections=["servere"],
            categories=["proxmox_compute", "storage", "ai_server"],
        ),
    ]
