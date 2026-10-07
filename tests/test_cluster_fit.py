import pytest

from hhw.cluster_fit import cluster_fit
from hhw.models import Candidate


def node(title="M90q", family="lenovo_thinkcentre_tiny", price=1800, cpu="i5-10500T", memory=32, network=1):
    return Candidate(
        vendor_id="x", title=title, url=f"https://example.invalid/{title}/{price}",
        currency="NOK", item_price=price, stock_status="available",
        hardware={"model": title, "cpu_model": cpu, "memory_gb": memory, "network_max_gbps": network},
        metadata={"runner_family": family},
    )


def test_two_nodes_are_not_cluster_ready():
    result = cluster_fit([node(), node()], "proxmox_tiny")
    assert result["cluster_ready"] is False
    assert result["score"] == 0
    assert "fewer_than_minimum_nodes" in result["reasons"]


def test_three_identical_tiny_nodes_are_strong_cluster_fit():
    result = cluster_fit([node(), node(), node()], "proxmox_tiny")
    assert result["cluster_ready"] is True
    assert result["score"] == 85
    assert result["cluster_price_nok"] == 5400
    assert {"same_model", "same_cpu", "same_memory", "same_network"} <= set(result["reasons"])


def test_mixed_models_get_family_not_model_bonus():
    result = cluster_fit([node("M90q"), node("M920q"), node("M80q")], "proxmox_tiny")
    assert "same_model" not in result["reasons"]
    assert "same_family" in result["reasons"]


def test_sold_node_does_not_count():
    x = node()
    x.stock_status = "sold"
    result = cluster_fit([node(), node(), x], "proxmox_tiny")
    assert result["cluster_ready"] is False


def test_cluster_price_fails_closed_for_mixed_currency():
    nodes = [node(), node(), node()]
    nodes[2].currency = "EUR"
    assert cluster_fit(nodes, "proxmox_tiny")["cluster_price_nok"] is None


def test_rack_cluster_supported():
    nodes = [node("R740", "rack", 6000, "Xeon Gold", 128, 10) for _ in range(3)]
    assert cluster_fit(nodes, "proxmox_rack")["cluster_ready"] is True


def test_non_cluster_role_rejected():
    with pytest.raises(ValueError, match="unsupported cluster role"):
        cluster_fit([node(), node(), node()], "linux_ci")


def test_minimum_cannot_weaken_three_node_rule():
    with pytest.raises(ValueError, match="minimum_nodes"):
        cluster_fit([node(), node()], "proxmox_tiny", minimum_nodes=2)



def test_single_listing_with_quantity_three_is_cluster_ready():
    x = node(price=1800)
    x.metadata["quantity_available"] = 3
    result = cluster_fit([x], "proxmox_tiny")
    assert result["cluster_ready"] is True
    assert result["available_listings"] == 1
    assert result["available_nodes"] == 3
    assert result["selected_nodes"] == 3
    assert result["cluster_price_nok"] == 5400
    assert "same_model" in result["reasons"]


def test_large_refurb_batch_counts_physical_nodes():
    x = node()
    x.metadata["quantity_available"] = 12
    result = cluster_fit([x], "proxmox_tiny")
    assert result["available_nodes"] == 12
    assert result["cluster_ready"] is True


@pytest.mark.parametrize("quantity", [None, 0, -1, "3", True])
def test_unknown_or_invalid_quantity_fails_closed_to_one(quantity):
    x = node()
    x.metadata["quantity_available"] = quantity
    result = cluster_fit([x], "proxmox_tiny")
    assert result["available_nodes"] == 1
    assert result["cluster_ready"] is False
