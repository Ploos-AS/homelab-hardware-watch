from __future__ import annotations

import re

MAC_MINI = re.compile(r"mac\s*mini", re.I)
APPLE_SILICON = re.compile(r"\b(M1|M2|M3|M4)\b", re.I)
G4 = re.compile(r"\b(?:G4|PowerPC|PPC|7447A?|7450)\b", re.I)
INTEL = re.compile(r"\b(?:Intel|Core\s*(?:2\s*)?(?:Duo|Solo)|Core\s+i[3579]|i[3579][-\s]?\d{3,5})\b", re.I)

FAMILY_PATTERNS = [
    ("dell_optiplex_micro", re.compile(r"\bOptiPlex\b.*\bMicro\b", re.I)),
    ("hp_business_mini", re.compile(r"\b(?:EliteDesk|ProDesk|Elite Mini)\b.*\b(?:Mini|Desktop Mini)\b", re.I)),
    ("lenovo_thinkcentre_tiny", re.compile(r"\bThinkCentre\b.*\bTiny\b", re.I)),
    ("fujitsu_esprimo_q", re.compile(r"\b(?:Fujitsu\s+)?ESPRIMO\s+Q\w*", re.I)),
    ("asus_expertcenter_pn", re.compile(r"\b(?:ASUS\s+)?(?:ExpertCenter\s+)?PN[- ]?\d{2,3}\w*\b", re.I)),
    ("acer_veriton_mini", re.compile(r"\bAcer\s+Veriton\b.*\b(?:Mini|NUC|N\d{3,5})\b", re.I)),
    ("minisforum_mini", re.compile(r"\bMINISFORUM\b", re.I)),
    ("beelink_mini", re.compile(r"\bBeelink\b", re.I)),
    ("gmktec_mini", re.compile(r"\bGMKtec\b|\bNucBox\b", re.I)),
    ("asus_nuc", re.compile(r"\bASUS\s+NUC\b", re.I)),
    ("intel_nuc", re.compile(r"\b(?:Intel\s+)?NUC\b", re.I)),
]

FAMILY_TIER = {
    "dell_optiplex_micro": "business_core",
    "hp_business_mini": "business_core",
    "lenovo_thinkcentre_tiny": "business_core",
    "fujitsu_esprimo_q": "business_extended",
    "asus_expertcenter_pn": "business_extended",
    "acer_veriton_mini": "business_extended",
    "intel_nuc": "business_extended",
    "asus_nuc": "business_extended",
    "minisforum_mini": "opportunistic_performance",
    "beelink_mini": "opportunistic_performance",
    "gmktec_mini": "opportunistic_performance",
}


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



def runner_family_tier(title: str) -> str | None:
    family = detect_runner_family(title)
    if family and family.startswith("mac_mini_"):
        return "mac"
    return FAMILY_TIER.get(family)
