# Configuration parity

Price comparisons against the N150 reference must compare reasonably equivalent configurations.

The current reference is:

- Intel N150
- 16 GB RAM
- NOK 1,600 ex VAT / NOK 2,000 inc VAT
- storage unspecified

## M1 rule

Listings with less than 16 GB RAM receive a transparent estimated upgrade adjustment before price comparison.

Listings with unknown RAM are **not comparable** until memory is known.

The initial RAM-upgrade estimate is a working assumption, not a market observation:

- upgrade to 16 GB: NOK 400

This value is intentionally isolated in code. A later component-price collector can replace the static assumption.

## Why this matters

A NOK 1,500 Tiny with 8 GB RAM should not be presented as NOK 500 cheaper than the NOK 2,000 N150/16 GB reference. Under the current working assumption its comparison price is NOK 1,900.

Likewise, systems with 16 GB or more require no RAM adjustment.

Storage parity will be added once the N150 reference storage configuration is known.
