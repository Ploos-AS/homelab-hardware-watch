from hhw.component_keys import component_evidence_key, enterprise_model_key


def test_dell_poweredge_key():
    assert enterprise_model_key("Dell PowerEdge R730 2U") == "dell_r730"
    assert component_evidence_key("Dell R730 without rails", "rails") == "dell_r730_rails"


def test_hpe_and_lenovo_keys():
    assert enterprise_model_key("HPE ProLiant DL380 Gen10") == "hpe_dl380"
    assert enterprise_model_key("Lenovo ThinkSystem SR650") == "lenovo_sr650"


def test_unknown_or_ambiguous_model_has_no_key():
    assert enterprise_model_key("Dell server without rails") is None
    assert component_evidence_key("PowerEdge server without rails", "rails") is None
