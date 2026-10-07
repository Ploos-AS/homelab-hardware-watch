from __future__ import annotations

import re

from hhw.ip_kvm_module_catalog import MODULE_CATALOG, lookup_interface_module


def enrich_ip_kvm_bundle(candidate):
    """Extract conservative interface-module bundle facts from listing text."""
    text = " ".join(filter(None, [
        candidate.title,
        str((candidate.metadata or {}).get("description") or ""),
    ]))
    hw = candidate.hardware
    found: list[dict] = []

    for model in MODULE_CATALOG:
        # Accept "16x MODEL", "16 x MODEL", "16 stk MODEL", or bare MODEL.
        pattern = rf"(?:(\d+)\s*(?:x|×|stk\.?|pcs?\.?|pieces?)\s*)?\b{re.escape(model)}\b"
        for match in re.finditer(pattern, text, re.I):
            count = int(match.group(1) or 1)
            info = lookup_interface_module(model)
            found.append({"model": model, "count": count, **(info or {})})

    if found:
        total = sum(x["count"] for x in found)
        hw.setdefault("included_interface_modules", total)
        candidate.metadata["interface_modules"] = found
        families = set.intersection(*(set(x["families"]) for x in found if x.get("families")))
        if families:
            hw.setdefault("interface_module_compatible_families", sorted(families))
        vendors = {x.get("vendor") for x in found if x.get("vendor")}
        if len(vendors) == 1:
            hw.setdefault("interface_module_vendor", vendors.pop())
        return candidate

    # Generic counts are useful inventory facts but never compatibility proof.
    generic = re.search(
        r"\b(\d+)\s*(?:x|×|stk\.?|pcs?\.?)?\s*"
        r"(?:cims?|dongles?|interface\s+modules?|server\s+interface\s+modules?)\b"
        r"(?:\s+(?:included|inkludert|medfølger|følger\s+med))?",
        text, re.I,
    )
    if generic:
        hw.setdefault("included_interface_modules", int(generic.group(1)))
        candidate.metadata["interface_module_count_source"] = "generic_text"

    return candidate
