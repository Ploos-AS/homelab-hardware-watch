from datetime import date

from hhw.ip_kvm_evidence import observe_kvm_module_cost
from hhw.models import Candidate


def c(title, price=800, currency="NOK"):
    return Candidate("market", title, "https://example.invalid/listing", item_price=price, currency=currency)


def test_explicit_bundle_becomes_unit_cost_evidence():
    e = observe_kvm_module_cost(c("4x D2CIM-DVUSB", 1200), date(2026, 10, 7))
    assert e.evidence_key == "kvm_module:d2cim_dvusb"
    assert e.cost_nok == 300
    assert e.component == "kvm_interface_module"


def test_single_module_listing_is_valid():
    e = observe_kvm_module_cost(c("D2CIM-DVUSB HDMI? no, standard module", 350), date(2026, 10, 7))
    assert e.cost_nok == 350


def test_ambiguous_bundle_without_quantity_fails_closed():
    assert observe_kvm_module_cost(c("bundle D2CIM-DVUSB", 1000), date(2026, 10, 7)) is None


def test_multiple_different_models_fail_closed():
    assert observe_kvm_module_cost(c("D2CIM-DVUSB + D2CIM-DVUSB-DP", 800), date(2026, 10, 7)) is None


def test_unconfirmed_foreign_price_is_not_evidence():
    assert observe_kvm_module_cost(c("4x D2CIM-DVUSB", 100, "EUR"), date(2026, 10, 7)) is None
