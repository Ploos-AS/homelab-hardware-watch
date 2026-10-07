import pytest

from hhw.ip_kvm_families import detect_ip_kvm_family, ip_kvm_profile


@pytest.mark.parametrize(("title", "family"), [
    ("Raritan Dominion KX III DKX3-216", "raritan_dominion_kx"),
    ("Raritan Dominion KX II 32 port", "raritan_dominion_kx"),
    ("Raritan Dominion LX II", "raritan_dominion_lx"),
    ("Avocent MergePoint Unity MPU2016", "avocent_mergepoint"),
    ("Vertiv Avocent DSR8032", "avocent_dsr"),
    ("Vertiv Avocent MPU2032DAC", "avocent_mpu"),
    ("ATEN KN2116VA 16-port KVM over IP", "aten_kn"),
    ("Lantronix SpiderDuo KVM", "lantronix_spiderduo"),
    ("Lantronix Spider KVM over IP", "lantronix_spider"),
])
def test_detect_known_ip_kvm_families(title, family):
    assert detect_ip_kvm_family(title) == family


def test_unknown_kvm_fails_closed():
    assert detect_ip_kvm_family("Generic 8 port KVM switch") is None


def test_rack_and_single_node_profiles_are_separate():
    assert ip_kvm_profile("raritan_dominion_kx") == "rack_multiport"
    assert ip_kvm_profile("aten_kn") == "rack_multiport"
    assert ip_kvm_profile("lantronix_spider") == "single_node"
    assert ip_kvm_profile("lantronix_spiderduo") == "single_node"
    assert ip_kvm_profile(None) is None
