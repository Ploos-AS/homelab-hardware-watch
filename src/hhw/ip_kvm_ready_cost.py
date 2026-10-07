from __future__ import annotations

import re


def kvm_module_evidence_key(family: str | None, model: str | None) -> str | None:
    """Return a narrow component-price key; never collapse all CIMs together."""
    if model:
        normalized = re.sub(r"[^a-z0-9]+", "_", model.lower()).strip("_")
        return f"kvm_module:{normalized}"
    if family:
        normalized = re.sub(r"[^a-z0-9]+", "_", family.lower()).strip("_")
        return f"kvm_module_family:{normalized}"
    return None


def add_missing_kvm_modules(candidate, *, family, missing_count, model=None, unit_cost_nok=None):
    if not isinstance(missing_count, int) or missing_count <= 0:
        return candidate
    key = kvm_module_evidence_key(family, model)
    entry = {
        "component": "kvm_interface_module",
        "quantity": missing_count,
        "required": True,
        "evidence_key": key,
        "note": model or family or "IP KVM interface module",
    }
    if unit_cost_nok is not None:
        entry["cost_nok"] = float(unit_cost_nok)
    missing = candidate.metadata.setdefault("missing_components", [])
    if not any(x.get("component") == "kvm_interface_module" for x in missing):
        missing.append(entry)
    return candidate
