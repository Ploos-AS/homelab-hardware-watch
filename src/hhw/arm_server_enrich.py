from __future__ import annotations

import re


ARM_SERVER_PATTERNS = (
    (re.compile(r"\bAmpere\s+Altra\s+Max\b", re.I), "ampere_altra_max"),
    (re.compile(r"\bAmpere\s+Altra\b", re.I), "ampere_altra"),
    (re.compile(r"\bThunderX2\b", re.I), "thunderx2"),
    (re.compile(r"\bThunderX\b", re.I), "thunderx"),
)


def arm_server_family(title: str) -> str | None:
    for pattern, family in ARM_SERVER_PATTERNS:
        if pattern.search(title):
            return family
    return None


def enrich_arm_server(candidate):
    family = arm_server_family(candidate.title)
    if family is None:
        return candidate
    candidate.metadata.setdefault("arm_server_family", family)
    candidate.hardware.setdefault("architecture", "arm64")
    candidate.hardware.setdefault("linux_supported", True)
    return candidate
