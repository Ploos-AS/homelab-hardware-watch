from __future__ import annotations

import re

# Keep this intentionally narrow. A key means we believe component compatibility
# is specific enough to reuse dated cost evidence safely.
ENTERPRISE_MODELS = (
    re.compile(r"\bDell(?:\s+EMC)?\s+(?:PowerEdge\s+)?(R[56789]\d{2})\b", re.I),
    re.compile(r"\bHPE?\s+(?:ProLiant\s+)?(DL\d{3})\b", re.I),
    re.compile(r"\bLenovo\s+(?:ThinkSystem\s+)?(SR\d{3})\b", re.I),
)


def enterprise_model_key(title: str) -> str | None:
    for pattern in ENTERPRISE_MODELS:
        match = pattern.search(title)
        if match:
            model = match.group(1).lower()
            if model.startswith("r"):
                vendor = "dell"
            elif model.startswith("dl"):
                vendor = "hpe"
            else:
                vendor = "lenovo"
            return f"{vendor}_{model}"
    return None


def component_evidence_key(title: str, component: str) -> str | None:
    model = enterprise_model_key(title)
    if model is None:
        return None
    return f"{model}_{component.lower()}"
