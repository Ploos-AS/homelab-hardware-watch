from __future__ import annotations

import re

MAC_MINI = re.compile(r"mac\s*mini", re.I)
APPLE_SILICON = re.compile(r"\b(M1|M2|M3|M4)\b", re.I)
G4 = re.compile(r"\b(?:G4|PowerPC|PPC|7447A?|7450)\b", re.I)
INTEL = re.compile(r"\b(?:Intel|Core\s*(?:2\s*)?(?:Duo|Solo)|Core\s+i[3579]|i[3579][-\s]?\d{3,5})\b", re.I)

FAMILY_PATTERNS = [
    ("intel_nuc", re.compile(r"\b(?:intel\s+)?NUC\b", re.I)),
    ("generic_tiny", re.compile(r"\b(?:ThinkCentre.*Tiny|OptiPlex.*Micro|EliteDesk.*Mini|ProDesk.*Mini)\b", re.I)),
]


def mac_mini_generation(title: str) -> str | None:
    if not MAC_MINI.search(title):
        return None
    silicon = APPLE_SILICON.search(title)
    if silicon:
        return silicon.group(1).lower()
    if G4.search(title):
        return "g4"
    if INTEL.search(title) or re.search(r"\b20(?:0[6-9]|1\d|20)\b", title):
        return "intel"
    return None


def detect_runner_family(title: str) -> str | None:
    generation = mac_mini_generation(title)
    if generation == "g4":
        return "mac_mini_g4"
    if generation in {"m1", "m2", "m3", "m4"}:
        return "mac_mini_apple_silicon"
    if generation == "intel":
        return "mac_mini_intel"
    for family, pattern in FAMILY_PATTERNS:
        if pattern.search(title):
            return family
    return None


def bargain_family_key(title: str) -> str | None:
    """Compatibility-safe family key for cross-listing price history."""
    generation = mac_mini_generation(title)
    if generation:
        return f"mac_mini_{generation}"
    return None
