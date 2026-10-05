import pytest

from hhw.decision import VALID_ROLES, decide
from hhw.models import Candidate


def c(price=1000, hardware=None, metadata=None):
    return Candidate(
        vendor_id="x", title="candidate", url="https://example.invalid",
        currency="NOK", item_price=price,
        hardware=hardware or {}, metadata=metadata or {},
    )


def test_dispatcher_exposes_all_m4_roles():
    assert {
        "proxmox_compute", "storage",
        "linux_ci", "linux_arm64_ci", "macos_ci",
        "ai_server", "ai_host", "managed_switch", "ups",
    } <= VALID_ROLES


def test_dispatches_enterprise():
    result = decide(c(3000, {"memory_gb": 128, "cpu_count": 2}), "proxmox_compute")
    assert result["role"] == "proxmox_compute"
    assert result["action"] in {"BUY", "WATCH", "PASS"}


def test_dispatches_runner():
    x = c(1400, {"memory_gb": 16}, {
        "runner_family": "generic_tiny",
        "configuration_parity": {"comparable": True, "adjusted_price_nok": 1400},
    })
    result = decide(x, "linux_ci")
    assert result["role"] == "linux_ci"
    assert result["action"] == "BUY"


def test_dispatches_ai_switch_and_ups():
    ai = decide(c(5000, {"gpu_vram_gb": 24, "memory_gb": 64}), "ai_host")
    switch = decide(c(1500, {
        "managed": True, "vlan": True, "lacp": True,
        "uplink_max_gbps": 25, "ports_25gbe": 4,
    }), "managed_switch")
    ups = decide(c(1000, {
        "output_watts": 1500, "ups_topology": "line_interactive",
        "replaceable_battery": True,
        "management_interfaces": ["usb", "snmp"],
        "nut_compatible": True,
    }), "ups")
    assert ai["action"] == "BUY"
    assert switch["action"] == "BUY"
    assert ups["action"] == "BUY"


def test_unknown_role_fails_closed():
    with pytest.raises(ValueError, match="unknown decision role"):
        decide(c(), "gaming_pc")


def test_ai_server_is_canonical_public_role():
    result = decide(c(5000, {"gpu_vram_gb": 24}), "ai_server")
    assert result["role"] == "ai_server"
    assert result["action"] == "BUY"
