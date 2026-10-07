from hhw.arm_server_enrich import arm_server_family, enrich_arm_server
from hhw.gpu_enrich import enrich_gpu, gpu_model
from hhw.models import Candidate


def c(title):
    return Candidate("used", title, "https://example.invalid/item")


def test_arm_server_families_are_separate():
    assert arm_server_family("Ampere Altra Max server") == "ampere_altra_max"
    assert arm_server_family("Ampere Altra server") == "ampere_altra"
    assert arm_server_family("Cavium ThunderX2 rack server") == "thunderx2"
    assert arm_server_family("Cavium ThunderX rack server") == "thunderx"


def test_arm_enrichment_sets_architecture_without_overwriting_explicit_fact():
    x = enrich_arm_server(c("Ampere Altra server"))
    assert x.hardware["architecture"] == "arm64"
    y = c("Ampere Altra server")
    y.hardware["linux_supported"] = False
    enrich_arm_server(y)
    assert y.hardware["linux_supported"] is False


def test_known_gpu_vram():
    assert gpu_model("NVIDIA RTX 3090") == ("rtx_3090", 24)
    assert gpu_model("NVIDIA RTX A6000") == ("rtx_a6000", 48)
    assert gpu_model("NVIDIA Tesla P40") == ("tesla_p40", 24)
    assert gpu_model("AMD Instinct MI60") == ("instinct_mi60", 32)


def test_ambiguous_gpu_variant_does_not_guess_vram():
    assert gpu_model("NVIDIA Tesla V100") == ("tesla_v100", None)
    x = enrich_gpu(c("Tesla V100"))
    assert "gpu_vram_gb" not in x.hardware


def test_datacenter_gpu_marks_passive_cooling():
    x = enrich_gpu(c("Tesla P40 24GB"))
    assert x.hardware["gpu_vram_gb"] == 24
    assert x.hardware["passive_cooling"] is True


def test_unknown_gpu_fails_closed():
    x = enrich_gpu(c("Mystery accelerator"))
    assert x.hardware == {}
