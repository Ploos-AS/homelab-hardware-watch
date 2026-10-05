from hhw.opportunities import rank


def markdown_opportunities(candidates, roles=None, limit=10):
    roles = roles or ["linux_ci", "linux_arm64_ci", "macos_ci"]
    out = ["# Current opportunities", ""]
    for role in roles:
        out.extend([f"## {role}", "", "| Score | Product | Price | Why |", "|---:|---|---:|---|"])
        shown = [x for x in rank(candidates, role) if x.score > 0][:limit]
        if not shown:
            out.append("| — | No qualified candidates | — | — |")
        for x in shown:
            c = x.candidate
            price = f"{c.item_price:.0f} {c.currency}" if c.item_price is not None else "unknown"
            why = "; ".join(x.reasons)
            out.append(f"| {x.score:.0f} | [{c.title}]({c.url}) | {price} | {why} |")
        out.append("")
    return "\n".join(out)
