# M2 — Europe collectors

M2 expands the current-opportunities pipeline beyond Norway.

## Order

1. Netherlands
2. Germany
3. Sweden/Denmark
4. Baltics

## Netherlands bootstrap

Initial sources:

- ServerPunt
- ServerZaak
- SecondHandServer.eu

ServerPunt is particularly useful because it explicitly advertises EU-wide shipping and exposes ex-VAT and inc-VAT pricing plus stock on product listings.

ServerZaak is useful for configurable Dell/HPE/Supermicro servers, components and networking. Its free-shipping statements are Netherlands-specific and must not be applied to Norway.

## M2 data requirements

European observations should preserve:

- source currency
- price ex VAT when exposed
- price inc local VAT when exposed
- stock
- shipping-to-Norway status: yes/no/unknown
- shipping cost: known value or null
- configuration completeness
- required missing components

Do not convert to a fake delivered-NOK number until exchange rate, Norwegian VAT treatment and shipping/import handling are represented explicitly.

## Product scope

M2 watches all useful homelab classes:

- x86_64 runners: Tiny/Micro/Mini/NUC
- ARM64 runners/SBCs
- Mac mini/macOS runners
- Proxmox compute
- AI-capable workstations/chassis
- storage servers/HBA/NIC
- managed 10/25GbE networking
