from __future__ import annotations

import re
from dataclasses import replace
from hhw.families import detect_runner_family
from hhw.models import Candidate

RAM_RE = re.compile(r"(?<!\d)(\d{1,3})\s*GB\s*(?:RAM|DDR\d)?", re.I)
STORAGE_RE = re.compile(r"(?<!\d)(\d{2,4})\s*(GB|TB)\s*(SSD|NVME|HDD)", re.I)
INTEL_CPU_RE = re.compile(r"\b(i[3579]-\d{4,5}[A-Z]{0,2}|N(?:95|97|100|150|200|250|300|305|350|355))\b", re.I)
RYZEN_RE = re.compile(r"\b(Ryzen\s+(?:[3579]\s+)?(?:PRO\s+)?\d{4,5}[A-Z]{0,2})\b", re.I)


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
        if family.startswith("mac_mini"):
            hardware.setdefault("form_factor", "mac_mini")
        else:
            hardware.setdefault("form_factor", "tiny")
    elif any(x in title.lower() for x in ("tiny", "mini", "micro")):
        hardware.setdefault("form_factor", "tiny")

    return replace(candidate, hardware=hardware, metadata=metadata)


def normalize_all(candidates: list[Candidate]) -> list[Candidate]:
    return [normalize_title(c) for c in candidates]
