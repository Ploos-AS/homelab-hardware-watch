# Sourcing policy

## Goal

Find unusually good-value homelab hardware from Norwegian and European sources while comparing products on total delivered cost and practical usefulness.

## Source order

1. Norwegian refurbishers and business IT resellers
2. Norwegian marketplaces and liquidation opportunities
3. EU/EEA refurbishers
4. UK refurbishers
5. Other international sources when the value proposition justifies import friction

## Product classes

- Proxmox / general compute
- CI runners
- AI server
- Storage
- Managed switches
- Tiny / Mini / Micro systems

## Comparison rule

Sticker price is never sufficient. The canonical comparison metric is **delivered NOK**.

Each candidate should eventually account for base price, required configuration, missing accessories, shipping, VAT/import handling, warranty, noise/power, expandability and target suitability.

## N100/N150 reference

N100/N150-class mini PCs are a low-power reference class, not a mandatory purchase target.

Current working assumption: relevant imported N150-class systems start around NOK 1600 before Norwegian VAT.

Used Lenovo Tiny, Dell Micro, HP Mini and similar systems should be compared directly against this reference for CI/tiny roles.

## Collector policy

- Prefer official APIs, feeds and stable listing pages.
- Avoid aggressive scraping.
- Respect rate limits and site policies.
- Keep collection vendor-specific.
- Keep normalized records separate from raw observations.
