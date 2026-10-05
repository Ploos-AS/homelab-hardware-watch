from hhw.enterprise_score import score_enterprise
from hhw.opportunities import rank


CI_ROLES = ["linux_ci", "linux_arm64_ci", "macos_ci"]
ENTERPRISE_ROLES = ["proxmox_compute", "storage"]
DEFAULT_ROLES = ENTERPRISE_ROLES + CI_ROLES


def _price(candidate):
    return f"{candidate.item_price:.0f} {candidate.currency}" if candidate.item_price is not None else "unknown"


def _enterprise_rank(candidates, role):
    scored = []
    for candidate in candidates:
        result = score_enterprise(candidate, role)
        if result["score"] > 0:
            scored.append((result, candidate))
    return sorted(scored, key=lambda x: x[0]["score"], reverse=True)


def markdown_opportunities(candidates, roles=None, limit=10):
    roles = roles or DEFAULT_ROLES
    out = ["# Current opportunities", ""]

    for role in roles:
        out.extend([f"## {role}", "", "| Score | Product | Price | Confidence | Why |", "|---:|---|---:|---|---|"])

        if role in ENTERPRISE_ROLES:
            shown = _enterprise_rank(candidates, role)[:limit]
            if not shown:
                out.append("| — | No qualified candidates | — | — | — |")
            for result, candidate in shown:
                why = "; ".join(result["reasons"])
                out.append(
                    f"| {result['score']:.0f} | [{candidate.title}]({candidate.url}) | "
                    f"{result['price_nok']:.0f} NOK | {result['price_confidence']} | {why} |"
                    if result["price_nok"] is not None else
                    f"| {result['score']:.0f} | [{candidate.title}]({candidate.url}) | "
                    f"{_price(candidate)} | unknown | {why} |"
                )
        else:
            shown = [x for x in rank(candidates, role) if x.score > 0][:limit]
            if not shown:
                out.append("| — | No qualified candidates | — | — |")
            for x in shown:
                why = "; ".join(x.reasons)
                out.append(f"| {x.score:.0f} | [{x.candidate.title}]({x.candidate.url}) | {_price(x.candidate)} | — | {why} |")

        out.append("")

    return "\n".join(out)
