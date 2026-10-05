from hhw.models import Candidate
from hhw.opportunities import score_candidate


def candidate(family, price=1800, memory=16):
    return Candidate(
        vendor_id="x",
        title=family,
        url="https://example.invalid",
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


def test_mac_mini_scores_for_macos():
    mac = score_candidate(candidate("mac_mini_apple_silicon"), "macos_ci")
    linux = score_candidate(candidate("mac_mini_apple_silicon"), "linux_ci")
    assert mac.score > linux.score


def test_x86_is_rejected_for_arm_role():
    x = score_candidate(candidate("generic_tiny"), "linux_arm64_ci")
    assert x.score < 0


def test_tiny_under_n150_reference_gets_value():
    x = score_candidate(candidate("generic_tiny", 1900), "linux_ci")
    assert x.score >= 50
