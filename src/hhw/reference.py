N150_REFERENCE = {
    "name": "Intel N150 system",
    "configuration": {
        "memory_gb": 16,
    },
    "cores": 4,
    "threads": 4,
    "max_turbo_ghz": 3.6,
    "processor_base_power_w": 6,
    "intel_max_memory_gb": 16,
    "base_price_nok_ex_vat": 1600,
    "base_price_nok_inc_vat": 2000,
    "notes": [
        "The NOK 1,600 ex-VAT working price is specifically for an N150 system with 16 GB RAM.",
        "Storage capacity is not yet fixed in the M1 reference and must not be assumed.",
        "Price is a project working assumption, not an Intel MSRP.",
        "Intel's official maximum memory specification is 16 GB.",
    ],
}


def price_vs_n150(item_price_nok: float | None) -> dict:
    reference = N150_REFERENCE["base_price_nok_inc_vat"]
    if item_price_nok is None:
        return {"reference_nok": reference, "delta_nok": None, "ratio": None}
    return {
        "reference_nok": reference,
        "delta_nok": round(item_price_nok - reference, 2),
        "ratio": round(item_price_nok / reference, 3),
    }
