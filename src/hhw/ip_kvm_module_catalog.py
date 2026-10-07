from __future__ import annotations

import re


MODULE_CATALOG = {
    "D2CIM-DVUSB": {
        "vendor": "raritan",
        "families": ["raritan_dominion_kx", "raritan_dominion_lx"],
        "virtual_media": True, "bios_virtual_media": True, "video": "vga",
    },
    "D2CIM-VUSB": {
        "vendor": "raritan",
        "families": ["raritan_dominion_kx", "raritan_dominion_lx"],
        "virtual_media": True, "bios_virtual_media": False, "video": "vga",
    },
    "D2CIM-VUSB-USBC": {
        "vendor": "raritan",
        "families": ["raritan_dominion_kx", "raritan_dominion_lx"],
        "virtual_media": True, "bios_virtual_media": False, "video": "usb-c",
    },
    "D2CIM-DVUSB-DP": {
        "vendor": "raritan", "families": ["raritan_dominion_kx", "raritan_dominion_lx"],
        "virtual_media": True, "bios_virtual_media": True, "video": "displayport",
    },
    "D2CIM-DVUSB-HDMI": {
        "vendor": "raritan", "families": ["raritan_dominion_kx", "raritan_dominion_lx"],
        "virtual_media": True, "bios_virtual_media": True, "video": "hdmi",
    },
    "D2CIM-DVUSB-DVI": {
        "vendor": "raritan", "families": ["raritan_dominion_kx", "raritan_dominion_lx"],
        "virtual_media": True, "bios_virtual_media": True, "video": "dvi",
    },
    "DCIM-USBG2": {
        "vendor": "raritan", "families": ["raritan_dominion_kx", "raritan_dominion_lx"],
        "virtual_media": False, "bios_virtual_media": False, "video": "vga",
    },
}


def normalize_module_model(value: str) -> str:
    return re.sub(r"\s+", "", value.strip().upper())


def lookup_interface_module(model: str | None) -> dict | None:
    if not model:
        return None
    return MODULE_CATALOG.get(normalize_module_model(model))
