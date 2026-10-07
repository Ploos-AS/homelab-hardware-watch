from hhw.families import bargain_family_key, detect_runner_family, mac_mini_generation, runner_family_tier


def test_mac_mini_m1():
    title = "Apple Mac mini M1 16GB 256GB"
    assert detect_runner_family(title) == "mac_mini_apple_silicon"
    assert mac_mini_generation(title) == "m1"
    assert bargain_family_key(title) == "mac_mini_m1"


def test_mac_mini_m2_and_m4_have_separate_bargain_families():
    assert bargain_family_key("Mac mini M2 8GB 256GB") == "mac_mini_m2"
    assert bargain_family_key("Mac mini M4 16GB 256GB") == "mac_mini_m4"


def test_intel_mac_mini():
    title = "Apple Mac mini 2018 i5 16GB"
    assert detect_runner_family(title) == "mac_mini_intel"
    assert bargain_family_key(title) == "mac_mini_intel"


def test_g4_is_not_misclassified_as_intel():
    title = "Apple Mac mini G4 1.5GHz PowerPC 1GB"
    assert detect_runner_family(title) == "mac_mini_g4"
    assert mac_mini_generation(title) == "g4"
    assert bargain_family_key(title) == "mac_mini_g4"


def test_ambiguous_mac_mini_fails_closed():
    assert detect_runner_family("Apple Mac mini 8GB SSD") is None
    assert bargain_family_key("Apple Mac mini 8GB SSD") is None


def test_nuc():
    assert detect_runner_family("Intel NUC 11 Pro i5 16GB") == "intel_nuc"


def test_lenovo_tiny():
    assert detect_runner_family("Lenovo ThinkCentre M920q Tiny i5-9500T") == "lenovo_thinkcentre_tiny"



def test_business_core_runner_families_are_distinct():
    assert detect_runner_family("Dell OptiPlex 7090 Micro") == "dell_optiplex_micro"
    assert detect_runner_family("HP EliteDesk 800 G6 Mini") == "hp_business_mini"
    assert detect_runner_family("Lenovo ThinkCentre M90q Tiny") == "lenovo_thinkcentre_tiny"
    assert runner_family_tier("Dell OptiPlex 7090 Micro") == "business_core"


def test_extended_business_mini_families():
    assert detect_runner_family("Fujitsu ESPRIMO Q958") == "fujitsu_esprimo_q"
    assert detect_runner_family("ASUS ExpertCenter PN64") == "asus_expertcenter_pn"
    assert detect_runner_family("Acer Veriton 6000 Mini") == "acer_veriton_mini"
    assert runner_family_tier("ASUS ExpertCenter PN64") == "business_extended"


def test_opportunistic_performance_families_have_separate_tier():
    for title in ("MINISFORUM UM890 Pro", "Beelink SER9 Pro", "GMKtec NucBox K11"):
        assert runner_family_tier(title) == "opportunistic_performance"


def test_nuc_families_are_distinct():
    assert detect_runner_family("Intel NUC 12 Pro") == "intel_nuc"
    assert detect_runner_family("ASUS NUC 14 Pro") == "asus_nuc"
