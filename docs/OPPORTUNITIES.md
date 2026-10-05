# Current opportunities

The opportunities layer is intentionally role-aware.

A single global "best computer" score would be misleading:

- Mac mini has strategic value for native macOS CI.
- RK3588/Pi-class systems have strategic value for native Linux ARM64 CI.
- Tiny/NUC/N150 systems compete primarily for Linux x86_64 CI.
- Proxmox, storage, networking and AI require separate scoring models.

## M1 runner score

The first score is deliberately simple and auditable:

- family fit for the requested role
- 8/16 GB memory
- configuration-parity price bands

It is **not** a final purchase recommendation.

M4 will replace/extend it with measured or sourced CPU performance, delivered cost, power, upgradeability, warranty, networking and architecture-coverage value.

## Reports

The CLI can produce a current opportunities report from the normalized collector output. Empty architecture sections are useful: they show which market/source coverage is still missing.
