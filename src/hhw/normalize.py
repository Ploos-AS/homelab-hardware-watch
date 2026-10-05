from __future__ import annotations

import re
from dataclasses import replace
from hhw.classify import classify_title
from hhw.enterprise import parse_enterprise_title
from hhw.families import detect_runner_family
from hhw.models import Candidate

RAM_RE = re.compile(r"(?<!\d)(\d{1,3})\s*GB\s*(?:RAM|DDR\d)?", re.I)
STORAGE_RE = re.compile(r"(?<!\d)(\d{2,4})\s*(GB|TB)\s*(SSD|NVME|HDD)", re.I)
INTEL_CPU_RE = re.compile(r"\b(i[3579]-\d{4,5}[A-Z]{0,2}|N(?:95|97|100|150|200|250|300|305|350|355))\b", re.I)
RYZEN_RE = re.compile(r"\b(Ryzen\s+(?:[3579]\s+)?(?:PRO\s+)?\d{4,5}[A-Z]{0,2})\b", re.I)

MISSING_COMPONENT_PATTERNS = {
    "memory": re.compile(r"\b(?:no|without)\s+(?:ram|memory)\b|\b(?:ram|memory)\s+not\s+included\b", re.I),
    "hba": re.compile(r"\b(?:no|without)\s+hba\b|\bhba\s+not\s+included\b", re.I),
    "nic": re.compile(r"\b(?:no|without)\s+(?:nic|network\s+card)\b|\b(?:nic|network\s+card)\s+not\s+included\b", re.I),
    "rails": re.compile(r"\b(?:no|without)\s+rails?\b|\brails?\s+not\s+included\b", re.I),
    "caddies": re.compile(r"\b(?:no|without)\s+(?:caddies|trays)\b|\b(?:caddies|trays)\s+not\s+included\b", re.I),
    "psu": re.compile(r"\b(?:no|without)\s+(?:psu|power\s+supply)\b|\b(?:psu|power\s+supply)\s+not\s+included\b", re.I),
    "gpu": re.compile(r"\b(?:no|without)\s+(?:gpu|graphics\s+card)\b|\b(?:gpu|graphics\s+card)\s+not\s+included\b", re.I),
}


def normalize_title(candidate: Candidate) -> Candidate:
    title = candidate.title
    hardware = dict(candidate.hardware)
    metadata = dict(candidate.metadata)

    cpu = INTEL_CPU_RE.search(title) or RYZEN_RE.search(title)
    if cpu:
        hardware.setdefault("cpu", {})["model"] = cpu.group(1)

    ram = RAM_RE.search(title)
    if ram:
        hardware["memory_gb"] = int(ram.group(1))

    storage = STORAGE_RE.search(title)
    if storage:
        amount = int(storage.group(1))
        unit = storage.group(2).upper()
        hardware["storage"] = [{
            "capacity_gb": amount * 1000 if unit == "TB" else amount,
            "type": storage.group(3).upper(),
        }]

    family = detect_runner_family(title)
    if family:
        metadata["runner_family"] = family
        hardware.setdefault("form_factor", "mac_mini" if family.startswith("mac_mini") else "tiny")
    elif any(x in title.lower() for x in ("tiny", "mini", "micro")):
        hardware.setdefault("form_factor", "tiny")

    enterprise = parse_enterprise_title(title)
    for key, value in enterprise.items():
        hardware[key] = value

    missing = list(metadata.get("missing_components") or [])
    existing_missing = {str(x.get("component", "")).lower() for x in missing}
    for component, pattern in MISSING_COMPONENT_PATTERNS.items():
        if component not in existing_missing and pattern.search(title):
            missing.append({
                "component": component,
                "required": True,
                "cost_nok": None,
                "note": "explicitly absent in listing title",
            })
    if missing:
        metadata["missing_components"] = missing

    detected = classify_title(title)
    if detected:
        metadata["detected_classes"] = detected

    return replace(candidate, hardware=hardware, metadata=metadata)


def normalize_all(candidates: list[Candidate]) -> list[Candidate]:
    return [normalize_title(c) for c in candidates]
