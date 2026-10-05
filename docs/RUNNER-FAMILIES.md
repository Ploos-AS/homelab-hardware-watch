# Runner families

Hardware Watch treats runner hardware as a set of competing families rather than assuming N100/N150.

## Linux/general CI

- N100/N150 mini PCs
- Lenovo ThinkCentre Tiny
- Dell OptiPlex Micro
- HP EliteDesk/ProDesk Mini
- Intel/ASUS NUC

Intel-branded NUC 7-13 support transitioned to ASUS. Exact model support status should be checked when older NUCs appear at bargain prices.

## macOS CI

Mac mini is a separate high-value category because it enables native macOS runners.

### Apple Silicon

High-interest watch:

- M1 Mac mini, especially 16 GB
- M2 Mac mini with 16 GB+
- newer 16 GB+ models when unusually cheap

Memory is part of the SoC/unified-memory configuration and cannot be treated like a cheap later SO-DIMM upgrade. An 8 GB M1 must therefore remain an 8 GB configuration in parity/scoring.

### Intel Mac mini

The 2018 Mac mini remains interesting at sufficiently low prices because it can provide x86 macOS runner capacity and supports configurable DDR4 memory up to 64 GB.

However, macOS support lifecycle is more important than raw purchase price. Old Intel Macs must not receive a high runner score solely because they are cheap.

## Scoring implication

M4 should score at least two runner purposes separately:

- `linux_ci`
- `macos_ci`

A Mac mini may be poor value as generic Linux compute while being excellent value as the lab's only native macOS CI node.
