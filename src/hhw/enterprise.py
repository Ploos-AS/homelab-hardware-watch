from __future__ import annotations
import re

RAM_GB = re.compile(r"(?<!\d)(\d+(?:[.,]\d+)?)\s*(TB|GB)\s*(?:DDR\d|RAM|MEMORY)?", re.I)
CPU_COUNT = re.compile(r"\b([12])\s*[x×]\s*(?:Intel\s+)?(?:Xeon|EPYC)", re.I)
BAYS = re.compile(r"\b(\d{1,2})\s*[x×]\s*(2[.,]5|3[.,]5)["″']?\s*(?:SFF|LFF)?", re.I)
BAYS_NAMED = re.compile(r"\b(\d{1,2})\s*(SFF|LFF)\b", re.I)
NVME = re.compile(r"\bNVMe\b", re.I)
CONTROLLER = re.compile(r"\b(HBA\d{3,4}[A-Z]?|H\d{3,4}P?|PERC\s+[A-Z]?\d{3,4}P?|LSI\s*\d{4}[-\w]*)\b", re.I)
NETWORK = re.compile(r"\b(1|2\.5|5|10|25|40|50|100)\s*GbE\b", re.I)


def parse_enterprise_title(title: str) -> dict:
    out = {}

    cpu = CPU_COUNT.search(title)
    if cpu:
        out["cpu_count"] = int(cpu.group(1))

    ram = RAM_GB.search(title)
    if ram:
        amount = float(ram.group(1).replace(",", "."))
        out["memory_gb"] = int(amount * 1024 if ram.group(2).upper() == "TB" else amount)

    bays = BAYS.search(title)
    if bays:
        out["drive_bays"] = {
            "count": int(bays.group(1)),
            "size_in": float(bays.group(2).replace(",", ".")),
        }
    else:
        named = BAYS_NAMED.search(title)
        if named:
            kind = named.group(2).upper()
            out["drive_bays"] = {
                "count": int(named.group(1)),
                "size_in": 2.5 if kind == "SFF" else 3.5,
                "kind": kind,
            }

    if NVME.search(title):
        out["nvme_capable_or_present"] = True

    controller = CONTROLLER.search(title)
    if controller:
        out["storage_controller"] = controller.group(1)

    speeds = [float(x) for x in NETWORK.findall(title)]
    if speeds:
        out["network_max_gbps"] = max(speeds)

    return out
