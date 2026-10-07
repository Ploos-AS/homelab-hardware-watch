from __future__ import annotations

import re


# Exact VRAM is only supplied for model names where the designation is
# sufficiently unambiguous for used-market listing enrichment.
GPU_MODELS = (
    (re.compile(r"\bRTX\s*3090\b", re.I), "rtx_3090", 24),
    (re.compile(r"\bRTX\s*A6000\b", re.I), "rtx_a6000", 48),
    (re.compile(r"\bQuadro\s+RTX\s*8000\b", re.I), "quadro_rtx_8000", 48),
    (re.compile(r"\bTesla\s+P40\b", re.I), "tesla_p40", 24),
    (re.compile(r"\bTesla\s+P100\b", re.I), "tesla_p100", 16),
    (re.compile(r"\bTesla\s+V100\b", re.I), "tesla_v100", None),
    (re.compile(r"\bRadeon\s+Pro\s+VII\b", re.I), "radeon_pro_vii", 16),
    (re.compile(r"\bInstinct\s+MI50\b", re.I), "instinct_mi50", None),
    (re.compile(r"\bInstinct\s+MI60\b", re.I), "instinct_mi60", 32),
    (re.compile(r"\bInstinct\s+MI100\b", re.I), "instinct_mi100", 32),
)


PASSIVE_FAMILIES = {"tesla_p40", "tesla_p100", "tesla_v100", "instinct_mi50", "instinct_mi60", "instinct_mi100"}


def gpu_model(title: str):
    for pattern, family, vram in GPU_MODELS:
        if pattern.search(title):
            return family, vram
    return None, None


def enrich_gpu(candidate):
    family, vram = gpu_model(candidate.title)
    if family is None:
        return candidate
    candidate.metadata.setdefault("gpu_family", family)
    if vram is not None:
        candidate.hardware.setdefault("gpu_vram_gb", vram)
    if family in PASSIVE_FAMILIES:
        candidate.hardware.setdefault("passive_cooling", True)
    return candidate
