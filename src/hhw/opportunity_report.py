from hhw.decision import decide


DEFAULT_ROLES = [
    "proxmox_compute",
    "storage",
    "linux_ci",
    "linux_arm64_ci",
    "macos_ci",
    "ai_server",
    "managed_switch",
    "ups",
    "ip_kvm",
]


def _price(candidate):
    return f"{candidate.item_price:.0f} {candidate.currency}" if candidate.item_price is not None else "unknown"


def _rank(candidates, role):
    scored = []
    for candidate in candidates:
        result = decide(candidate, role)
        if result["score"] > 0:
            scored.append((result, candidate))
    return sorted(scored, key=lambda x: x[0]["score"], reverse=True)


def markdown_opportunities(candidates, roles=None, limit=10):
    roles = roles or DEFAULT_ROLES
    out = ["# Current opportunities", ""]

    for role in roles:
        out.extend([
            f"## {role}",
            "",
            "| Action | Score | Product | Price | Bargain | Confidence | Why |",
            "|---|---:|---|---:|---|---|---|",
        ])

        shown = _rank(candidates, role)[:limit]
        if not shown:
            out.append("| — | — | No qualified candidates | — | — | — | — |")

        for result, candidate in shown:
            why = "; ".join(result["reasons"])
            price = (
                f"{result['price_nok']:.0f} NOK"
                if result.get("price_nok") is not None
                else _price(candidate)
            )
            bargain = (candidate.metadata or {}).get("bargain", {}).get("signal", "—")
            out.append(
                f"| {result['action']} | {result['score']:.0f} | "
                f"[{candidate.title}]({candidate.url}) | {price} | {bargain} | "
                f"{result.get('price_confidence', 'unknown')} | {why} |"
            )

        out.append("")

    return "\n".join(out)
