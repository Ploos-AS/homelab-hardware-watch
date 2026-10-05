from hhw.families import detect_runner_family


def test_mac_mini_m1():
    assert detect_runner_family("Apple Mac mini M1 16GB 256GB") == "mac_mini_apple_silicon"


def test_intel_mac_mini():
    assert detect_runner_family("Apple Mac mini 2018 i5 16GB") == "mac_mini_intel"


def test_nuc():
    assert detect_runner_family("Intel NUC 11 Pro i5 16GB") == "intel_nuc"


def test_lenovo_tiny():
    assert detect_runner_family("Lenovo ThinkCentre M920q Tiny i5-9500T") == "generic_tiny"
