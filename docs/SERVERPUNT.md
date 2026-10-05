# ServerPunt collector

Source: ServerPunt, Netherlands.

The public catalogue exposes product links, EUR prices excluding and including VAT, and stock counts. M2 preserves these separately.

## Important

ServerPunt states that it ships throughout the EU. Norway is not an EU member, so the collector must **not** translate that statement into `ships_to_norway: yes`. Norway remains `unknown` until shipping to Norway is explicitly verified.

Likewise, the Dutch VAT-inclusive price is not the canonical Norwegian delivered price.

## Useful inventory classes

Current catalogue examples show:

- Dell/HPE rack servers
- Xeon CPUs
- HDD/storage
- 10/25GbE NICs
- PCIe/NVMe expansion cards

Classification remains in the common normalization/scoring layer rather than being hard-coded into this collector.
