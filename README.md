# homelab-hardware-watch

Configuration-driven hardware sourcing watch for a Norway-based homelab.

## M0 scope

M0 defines the sourcing model. It does **not** scrape vendors yet.

The project tracks six product classes:

1. Proxmox / general compute nodes
2. CI runners
3. AI server chassis / hosts
4. Storage servers (primary + backup)
5. Managed switches
6. Tiny / Mini / Micro systems

The system is designed around **delivered cost to Norway**, not sticker price. N100/N150-class systems are used as a reference point for low-power compute rather than as a mandatory platform.

## Repository layout

- `config/vendors.yaml` — vendor registry
- `config/targets.yaml` — hardware target definitions
- `config/price-rules.yaml` — bargain thresholds and comparison rules
- `config/norway.yaml` — Norwegian VAT/import assumptions
- `docs/SOURCING.md` — sourcing policy
- `docs/DATA_MODEL.md` — normalized product model
- `docs/ROADMAP.md` — milestones

## Principles

- Compare **NOK delivered**
- Prefer Norwegian refurb when total cost is competitive
- Treat EU/UK vendors as both sourcing channels and price references
- Keep vendor-specific collection separate from normalization and scoring
- Track price history before making long-term bargain rules
- Avoid aggressive scraping; prefer feeds/APIs/manual collectors where practical

## Status

**M0 — foundation**
