from hhw.models import Candidate
from hhw.runner_score import runner_action, score_runner


def c(family, price=1800, memory=16, currency="NOK"):
    return Candidate(
        vendor_id="x",
        title=family,
        url="https://example.invalid",
        currency=currency,
        item_price=price,
        hardware={"memory_gb": memory},
        metadata={
            "runner_family": family,
            "configuration_parity": {
                "comparable": True,
                "adjusted_price_nok": price,
            },
        },
    )


def test_domestic_tiny_at_n150_reference_is_strong_watch():
    result = score_runner(c("generic_tiny", 1900), "linux_ci")
    assert result["score"] == 55
    assert result["price_confidence"] == "domestic"
    assert runner_action(result) == "WATCH"


def test_cheap_domestic_tiny_can_be_buy():
    result = score_runner(c("generic_tiny", 1400), "linux_ci")
    assert result["score"] == 65
    assert runner_action(result) == "BUY"


def test_arm64_role_rejects_x86_tiny():
    result = score_runner(c("generic_tiny", 1400), "linux_arm64_ci")
    assert "architecture_mismatch" in result["reasons"]
    assert runner_action(result) == "PASS"


def test_rk3588_gets_architecture_value():
    result = score_runner(c("arm64_rk3588", 1900), "linux_arm64_ci")
    assert result["score"] == 65
    assert runner_action(result) == "BUY"


def test_estimated_import_cannot_auto_buy():
    x = c("arm64_rk3588", 100, currency="EUR")
    x.metadata["delivered_cost"] = {
        "cost_status": "estimate",
        "estimated_delivered_nok": 1400,
    }
    result = score_runner(x, "linux_arm64_ci")
    assert result["score"] == 70
    assert result["price_confidence"] == "estimate"
    assert runner_action(result) == "WATCH"


def test_import_confirmed_can_buy():
    x = c("arm64_rk3588", 100, currency="EUR")
    x.metadata["delivered_cost"] = {
        "cost_status": "import_confirmed",
        "import_confirmed_delivered_nok": 1400,
    }
    result = score_runner(x, "linux_arm64_ci")
    assert result["score"] == 75
    assert runner_action(result) == "BUY"


def test_macos_requires_mac_family():
    wrong = score_runner(c("generic_tiny", 1000), "macos_ci")
    assert runner_action(wrong) == "PASS"
    right = score_runner(c("mac_mini_apple_silicon", 1900), "macos_ci")
    assert right["score"] == 70
    assert runner_action(right) == "BUY"
