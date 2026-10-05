from __future__ import annotations

import re

FAMILY_PATTERNS = [
    ("mac_mini_apple_silicon", re.compile(r"mac\s*mini.*\b(M1|M2|M3|M4)\b", re.I)),
    ("mac_mini_intel", re.compile(r"mac\s*mini", re.I)),
    ("intel_nuc", re.compile(r"\b(?:intel\s+)?NUC\b", re.I)),
    ("generic_tiny", re.compile(r"\b(?:ThinkCentre.*Tiny|OptiPlex.*Micro|EliteDesk.*Mini|ProDesk.*Mini)\b", re.I)),
]


def detect_runner_family(title: str) -> str | None:
    for family, pattern in FAMILY_PATTERNS:
        if pattern.search(title):
            return family
    return None
