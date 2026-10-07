from __future__ import annotations

import re


MODULE_CATALOG = {
    "KA7170": {"vendor": "aten", "families": ["aten_kn"], "virtual_media": False, "bios_virtual_media": False, "video": "vga"},
    "KA7166": {"vendor": "aten", "families": ["aten_kn"], "virtual_media": True, "bios_virtual_media": True, "video": "dvi"},
    "KA7168": {"vendor": "aten", "families": ["aten_kn"], "virtual_media": True, "bios_virtual_media": True, "video": "hdmi"},
    "KA7169": {"vendor": "aten", "families": ["aten_kn"], "virtual_media": True, "bios_virtual_media": True, "video": "displayport"},
    "KA7175": {"vendor": "aten", "families": ["aten_kn"], "virtual_media": True, "bios_virtual_media": True, "video": "vga"},
    "KA7177": {"vendor": "aten", "families": ["aten_kn"], "virtual_media": True, "bios_virtual_media": True, "video": "vga"},
    "KA7188": {"vendor": "aten", "families": ["aten_kn"], "virtual_media": True, "bios_virtual_media": True, "video": "hdmi"},
    "KA7189": {"vendor": "aten", "families": ["aten_kn"], "virtual_media": True, "bios_virtual_media": True, "video": "displayport"},
    "MPUIQ-VMC": {"vendor": "avocent", "families": ["avocent_mergepoint", "avocent_mpu"], "virtual_media": True, "bios_virtual_media": True, "video": "vga"},
    "MPUIQ-VMCHS": {"vendor": "avocent", "families": ["avocent_mergepoint", "avocent_mpu"], "virtual_media": True, "bios_virtual_media": True, "video": "vga"},
    "MPUIQ-VMCHD": {"vendor": "avocent", "families": ["avocent_mergepoint", "avocent_mpu"], "virtual_media": True, "bios_virtual_media": True, "video": "hdmi"},
    "MPUIQ-VMCDV": {"vendor": "avocent", "families": ["avocent_mergepoint", "avocent_mpu"], "virtual_media": True, "bios_virtual_media": True, "video": "dvi"},
    "MPUIQ-VMCDP": {"vendor": "avocent", "families": ["avocent_mergepoint", "avocent_mpu"], "virtual_media": True, "bios_virtual_media": True, "video": "displayport"},
    "DSRIQ-USB": {"vendor": "avocent", "families": ["avocent_mergepoint", "avocent_dsr"], "virtual_media": False, "bios_virtual_media": False, "video": "vga"},
    "DSRIQ-VMC": {"vendor": "avocent", "families": ["avocent_mergepoint", "avocent_dsr"], "virtual_media": True, "bios_virtual_media": True, "video": "vga"},
    "DSAVIQ-USB2": {"vendor": "avocent", "families": ["avocent_mergepoint"], "virtual_media": True, "bios_virtual_media": True, "video": "vga"},
    "SFIQ-VGA": {"vendor": "avocent", "families": ["avocent_mergepoint"], "virtual_media": True, "bios_virtual_media": True, "video": "vga"},
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
