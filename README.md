# homelab-hardware-watch

Configuration-driven hardware sourcing intelligence for a Norway-based homelab.

The project collects hardware candidates from Norwegian and European sources, normalizes them, estimates or confirms delivered cost to Norway, scores enterprise opportunities, and monitors useful candidates for price/action changes.

## Product classes

1. Proxmox / general compute nodes
2. CI runners
3. AI server chassis / hosts
4. Storage servers (primary + backup)
5. Managed switches
6. Tiny / Mini / Micro systems

N100/N150-class systems are a reference point for low-power compute, not a mandatory platform.

## Pipeline

`collect → normalize → classify → cost enrich → score → snapshot → detect changes → alert/report`

Imported candidates fail closed when required cost inputs are unknown. Indicative market-rate estimates are distinguished from import-confirmed NOK prices.

## Repository layout

- `config/` — vendors, targets, price rules, Norway assumptions and runner families
- `data/` — dated reusable evidence and rate/history inputs
- `docs/` — sourcing, import, scoring and source documentation
- `src/hhw/` — collectors, normalization, cost, scoring, monitoring and CLI
- `tests/` — unit/integration/acceptance tests
- `.github/workflows/` — Python test matrix and scheduled EU monitoring

## Principles

- Compare **delivered NOK**, never raw cross-currency sticker prices
- Prefer Norwegian refurb when total cost is competitive
- Treat EU/UK vendors as sourcing channels and price references
- Keep vendor-specific collection separate from normalization and scoring
- Preserve evidence/provenance and fail closed on unknown required inputs
- Avoid aggressive scraping; prefer feeds/APIs/manual/RFQ collectors where practical
- Track price history before making long-term bargain rules

## Status

**M3 complete.**

M0 foundation and M1 Norway are complete. M2 has strong Netherlands/Germany coverage but Nordic/Baltic collector coverage remains incomplete. M3 delivered-cost/import intelligence is merged, including dated FX/evidence, Norway VAT/import modelling, ServerShop24 weight-based shipping, confidence-aware scoring integration and acceptance coverage.

Parts of M4 classification/scoring and M6 monitoring/alerts already exist. The next development milestone is M4 decision-quality scoring; see `docs/ROADMAP.md`.
