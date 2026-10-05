from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class VendorImportPolicy:
    vendor_id: str
    norway_shipping: str = "unknown"
    export_vat_treatment: str = "unknown"
    shipping_price_source: str = "unknown"
    handling_source: str = "unknown"
    note: str = ""


POLICIES = {
    "serverpunt_nl": VendorImportPolicy(
        "serverpunt_nl",
        norway_shipping="checkout",
        shipping_price_source="checkout",
        note="Terms state shipping/additional costs are communicated before purchase; Norway availability and export VAT treatment still require checkout/vendor confirmation.",
    ),
    "serverzaak_nl": VendorImportPolicy(
        "serverzaak_nl",
        norway_shipping="checkout",
        shipping_price_source="checkout",
        note="International shipments have destination/product-specific shipping costs; Norway availability and export VAT treatment still require checkout/vendor confirmation.",
    ),
    "servershop24_de": VendorImportPolicy("servershop24_de", note="Require Norway checkout/quote before delivered-cost comparison."),
    "gekko_de": VendorImportPolicy("gekko_de", note="Require Norway checkout/quote before delivered-cost comparison."),
    "serverando_de": VendorImportPolicy("serverando_de", note="Configurable systems; require final configuration and Norway checkout/quote."),
    "secondhandserver_eu": VendorImportPolicy(
        "secondhandserver_eu",
        norway_shipping="quote",
        export_vat_treatment="quote",
        shipping_price_source="quote",
        handling_source="quote",
        note="RFQ source: use explicit quote values only.",
    ),
}


def policy_for(vendor_id: str) -> VendorImportPolicy:
    return POLICIES.get(vendor_id, VendorImportPolicy(vendor_id))
