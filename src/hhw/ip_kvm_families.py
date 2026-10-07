from __future__ import annotations

import re


IP_KVM_PATTERNS = [
    ("raritan_dominion_kx", re.compile(r"\bRaritan\b.*\bDominion\s+KX(?:\s*III|\s*II|3|2)?\b", re.I)),
    ("raritan_dominion_lx", re.compile(r"\bRaritan\b.*\bDominion\s+LX(?:\s*II|2)?\b", re.I)),
    ("avocent_mergepoint", re.compile(r"\b(?:Vertiv\s+)?Avocent\b.*\bMergePoint\b", re.I)),
    ("avocent_dsr", re.compile(r"\b(?:Vertiv\s+)?Avocent\b.*\bDSR\w*\b", re.I)),
    ("avocent_mpu", re.compile(r"\b(?:Vertiv\s+)?Avocent\b.*\bMPU\w*\b", re.I)),
    ("aten_kn", re.compile(r"\bATEN\b.*\bKN\d{4}\w*\b", re.I)),
    ("lantronix_spiderduo", re.compile(r"\bLantronix\b.*\bSpider\s*Duo\b", re.I)),
    ("lantronix_spider", re.compile(r"\bLantronix\b.*\bSpider\b", re.I)),
]


def detect_ip_kvm_family(title: str) -> str | None:
    for family, pattern in IP_KVM_PATTERNS:
        if pattern.search(title):
            return family
    return None


def ip_kvm_profile(family: str | None) -> str | None:
    if family in {"lantronix_spider", "lantronix_spiderduo"}:
        return "single_node"
    if family in {
        "raritan_dominion_kx", "raritan_dominion_lx",
        "avocent_mergepoint", "avocent_dsr", "avocent_mpu", "aten_kn",
    }:
        return "rack_multiport"
    return None
