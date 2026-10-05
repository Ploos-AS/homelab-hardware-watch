from __future__ import annotations
import re

SERVER = re.compile(r"\b(R[67][234]0(?:xd)?|DL3[68]0|DL380|PowerEdge|ProLiant)\b", re.I)
NIC = re.compile(r"\b(XXV710|X710|X520|X540|X550|ConnectX[- ]?[3456]|10\s*GbE|25\s*GbE)\b", re.I)
HBA = re.compile(r"\b(HBA|LSI\s*\d{4}|SAS\s*(?:HBA|controller))\b", re.I)
SWITCH = re.compile(r"\b(Aruba\s+29\d\d|EX(?:2300|3300|3400|4300)|ICX(?:6610|7250|7450)|S4048|S4148|QFX5100|SX10\d\d|SN2\d\d\d)\b", re.I)
WORKSTATION = re.compile(r"\b(Precision\s+(?:5820|7820)|Z[46]\s*G4|P(?:520|720))\b", re.I)


def classify_title(title: str) -> list[str]:
    classes = []
    if SERVER.search(title):
        classes.extend(["server", "proxmox_compute"])
    if NIC.search(title):
        classes.extend(["network_adapter", "networking_component"])
    if HBA.search(title):
        classes.extend(["storage_controller", "storage_component"])
    if SWITCH.search(title):
        classes.extend(["managed_switch", "networking"])
    if WORKSTATION.search(title):
        classes.extend(["workstation", "proxmox_compute", "ai_server"])
    return list(dict.fromkeys(classes))
