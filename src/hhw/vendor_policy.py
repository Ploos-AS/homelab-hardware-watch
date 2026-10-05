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
    "servershop24_de": VendorImportPolicy(
        "servershop24_de",
        norway_shipping="confirmed",
        export_vat_treatment="confirmed",
        shipping_price_source="weight_table",
        note="Norway is an explicit non-EU destination with parcel/freight rates. Non-EU deliveries receive a net invoice; use actual product/order weight for shipping.",
    ),
    "gekko_de": VendorImportPolicy(
        "gekko_de",
        norway_shipping="checkout",
        shipping_price_source="checkout",
        note="Shipping is destination-selectable, but Norway-specific shipping and export VAT treatment are not yet sufficiently verified.",
    ),
    "serverando_de": VendorImportPolicy(
        "serverando_de",
        norway_shipping="confirmed",
        shipping_price_source="weight_table",
        note="Norway is explicitly in shipping zone 7 with weight-based rates. Export VAT treatment is not yet verified; configurable systems also require final configuration.",
    ),
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
