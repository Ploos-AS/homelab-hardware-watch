# Shipping rates

Shipping tables are evidence-backed inputs, not permanent vendor facts.

## ServerShop24 -> Norway

Source: ServerShop24 shipping information, verified 2026-10-05.

The public Norway parcel table confirms DHL Standard at EUR 19.99 for weights through at least 7.5 kg. The implementation deliberately stops at the verified range instead of extrapolating.

Published Norway freight rates include:

- up to 100 kg: EUR 129.90
- up to 250 kg: EUR 169.90
- up to 500 kg: EUR 299.90

A weight outside a verified table returns unknown. It must not silently use the nearest rate.

The vendor also warns that non-EU deliveries may incur additional taxes, customs or other charges. Those costs remain separate delivered-cost inputs.
