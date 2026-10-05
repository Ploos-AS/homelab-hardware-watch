# ARM64 runner strategy

ARM64 is a first-class CI architecture.

## High-interest class: RK3588

Watch capability rather than only product names:

- RK3588
- 16 or 32 GB preferred; 8 GB minimum
- NVMe preferred
- >=1 GbE, with 2.5 GbE preferred
- stable Linux support

Initial examples are Radxa ROCK 5B/5B+ and Orange Pi 5 Plus.

## Raspberry Pi 5

Pi 5 remains a reference ARM64 runner because of ecosystem maturity and availability. Prefer 16 GB for multi-runner use; 8 GB remains interesting at a sufficiently low complete price.

## Complete-cost rule

SBC sticker price is not comparable to a ready-to-run Tiny PC. ARM candidates must include required extras:

- power supply
- active cooling/heatsink
- case if operationally required
- NVMe adapter/HAT where required
- NVMe storage
- shipping/VAT/import handling

## Architecture coverage

The desired CI pool should eventually expose at least:

- linux/x86_64
- linux/arm64
- macos/arm64
- macos/x86_64 when economically useful

Architecture coverage is a strategic value multiplier: the cheapest machine is not necessarily the most valuable runner.
