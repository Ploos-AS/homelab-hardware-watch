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
7. UPS / homelab power protection

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

**M3 complete; M4 feature-complete and in freeze/review.**

M0 foundation and M1 Norway are complete. M2 has strong Netherlands/Germany coverage but Nordic/Baltic collector coverage remains incomplete. M3 delivered-cost/import intelligence is merged, including dated FX/evidence, Norway VAT/import modelling, ServerShop24 weight-based shipping, confidence-aware scoring integration and acceptance coverage.

M4 has unified decision scoring for Proxmox/storage, x86 and ARM64 CI runners, macOS CI, AI servers, managed switches and UPS. Opportunity reports and monitoring use the same BUY/WATCH/PASS decision path. Required missing-component costs are included in ready-cost decisions, with dated model/component evidence and fail-closed handling when a required cost is unknown. Runner roles enforce architecture boundaries, and AI price value requires actual GPU capability. M4 is now frozen for review; richer power/noise/expandability evidence and broader architecture-coverage value move to later milestones. See `docs/ROADMAP.md`.
