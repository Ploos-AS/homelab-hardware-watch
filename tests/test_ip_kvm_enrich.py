from hhw.ip_kvm_enrich import enrich_ip_kvm
from hhw.models import Candidate


def candidate(title):
    return Candidate("x", title, "https://example.invalid", item_price=1000)


def test_raritan_dkx3_model_enriches_ports_and_family():
    c = enrich_ip_kvm(candidate("Raritan Dominion KX III DKX3-216"))
    assert c.hardware["kvm_ports"] == 16
    assert c.hardware["kvm_over_ip"] is True
    assert c.hardware["bios_level_access"] is True
    assert c.metadata["ip_kvm_family"] == "raritan_dominion_kx"
    assert c.metadata["ip_kvm_model"] == "DKX3-216"


def test_raritan_64_port_model():
    assert enrich_ip_kvm(candidate("Raritan Dominion KX III DKX3-464")).hardware["kvm_ports"] == 64


def test_aten_kn_model_enriches_port_count():
    c = enrich_ip_kvm(candidate("ATEN KN2116VA KVM over IP"))
    assert c.hardware["kvm_ports"] == 16
    assert c.metadata["ip_kvm_family"] == "aten_kn"
    assert c.metadata["ip_kvm_model"] == "KN2116VA"


def test_avocent_mpu_model_enriches_port_count():
    c = enrich_ip_kvm(candidate("Avocent MergePoint Unity MPU2032DAC"))
    assert c.hardware["kvm_ports"] == 32
    assert c.metadata["ip_kvm_family"] == "avocent_mergepoint"


def test_unknown_model_does_not_invent_specs():
    c = enrich_ip_kvm(candidate("Generic enterprise KVM"))
    assert "kvm_ports" not in c.hardware
    assert "ip_kvm_model" not in c.metadata


def test_explicit_hardware_is_not_overwritten():
    c = candidate("Raritan Dominion KX III DKX3-216")
    c.hardware["kvm_ports"] = 8
    enrich_ip_kvm(c)
    assert c.hardware["kvm_ports"] == 8
