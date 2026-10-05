from hhw.collectors.manual import ManualLeadCollector
from hhw.collectors.serverpunt import ServerPuntCollector
from hhw.collectors.shopify import ShopifyProductsCollector
from hhw.collectors.woocommerce import WooCommerceCategoryCollector


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
        ShopifyProductsCollector(
            vendor_id="rebuildit_no",
            base_url="https://www.rebuildit.no",
            collections=["desktop"],
            categories=["tiny", "ci_runner", "ai_server"],
        ),
        WooCommerceCategoryCollector(
            vendor_id="scandictech_no",
            urls=["https://www.scandictech.no/product-category/stasjonaer-pc/mini-pc/"],
            categories=["tiny", "ci_runner"],
        ),
        ManualLeadCollector(
            vendor_id="tekagain_no",
            url="https://tekagain.com/for-kjopere",
            categories=["proxmox_compute", "storage", "networking", "components", "ai_server"],
            note="Buyer-list/RFQ source for bulk business IT; do not treat as a normal storefront.",
        ),
    ]


def european_collectors():
    return [
        ServerPuntCollector(),
    ]


def all_collectors():
    return norwegian_collectors() + european_collectors()
