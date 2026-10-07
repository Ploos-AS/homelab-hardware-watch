from __future__ import annotations

from hhw.models import Candidate


def cluster_fit(candidates: list[Candidate], role: str, minimum_nodes: int = 3) -> dict:
    """Evaluate whether candidates form a useful homogeneous Proxmox cluster."""
    if role not in {"proxmox_rack", "proxmox_tiny"}:
        raise ValueError(f"unsupported cluster role: {role}")
    if minimum_nodes < 3:
        raise ValueError("Proxmox cluster minimum_nodes must be >= 3")

    available = [c for c in candidates if c.stock_status not in {"sold", "unavailable", "out_of_stock"}]
    expanded: list[Candidate] = []
    for candidate in available:
        raw_quantity = candidate.metadata.get("quantity_available", 1)
        quantity = raw_quantity if isinstance(raw_quantity, int) and not isinstance(raw_quantity, bool) and raw_quantity >= 1 else 1
        expanded.extend([candidate] * quantity)

    result = {
        "role": role,
        "minimum_nodes": minimum_nodes,
        "available_listings": len(available),
        "available_nodes": len(expanded),
        "cluster_ready": len(expanded) >= minimum_nodes,
        "score": 0,
        "reasons": [],
    }
    if len(expanded) < minimum_nodes:
        result["reasons"].append("fewer_than_minimum_nodes")
        return result

    selected = expanded[:minimum_nodes]
    result["score"] += 30
    result["reasons"].append("minimum_cluster_size_met")

    def same(field: str) -> bool:
        values = [c.hardware.get(field) for c in selected]
        return all(v is not None for v in values) and len(set(map(str, values))) == 1

    families = [c.metadata.get("runner_family") for c in selected]
    models = [c.hardware.get("model") or c.metadata.get("model") for c in selected]

    if all(models) and len(set(map(str, models))) == 1:
        result["score"] += 20
        result["reasons"].append("same_model")
    elif all(families) and len(set(map(str, families))) == 1:
        result["score"] += 10
        result["reasons"].append("same_family")

    if same("cpu_model"):
        result["score"] += 15
        result["reasons"].append("same_cpu")
    if same("memory_gb"):
        result["score"] += 10
        result["reasons"].append("same_memory")
    if same("network_max_gbps"):
        result["score"] += 10
        result["reasons"].append("same_network")

    prices = [c.item_price for c in selected]
    if all(p is not None and c.currency == "NOK" for p, c in zip(prices, selected)):
        result["cluster_price_nok"] = sum(float(p) for p in prices)
    else:
        result["cluster_price_nok"] = None

    result["selected_nodes"] = len(selected)
    return result
