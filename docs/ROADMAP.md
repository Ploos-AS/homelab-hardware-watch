# Roadmap

## M0 — Foundation
- [x] Repository purpose and principles
- [x] Six target product classes
- [x] Initial Norwegian/European vendor registry
- [x] Norway delivered-cost assumptions
- [x] Initial normalized product model
- [x] Initial sourcing policy
- [x] Initial price-rule framework

## M1 — Norway collectors
- [x] Norwegian vendor collector framework
- [x] FINN/manual marketplace ingestion strategy
- [x] Marketplace identity/lifecycle model
- [x] Normalization tests
- [x] N150/16 GB configuration parity
- [x] x86, ARM64 and macOS runner families
- [x] Current-candidates report
- [x] Role-aware current-opportunities report
- [x] CI test matrix

Automated FINN acquisition is deferred until a stable/permitted acquisition mechanism is selected. Historical raw snapshots move to M5 rather than blocking M1.

## M2 — EU collectors
- Netherlands
- Germany
- Baltics
- Sweden/Denmark
- Shipping capability metadata
- ARM64/NUC/Mac mini coverage where available

## M3 — UK/import
- UK collectors
- Explicit import/VAT/handling model
- Delivered-NOK calculator
- Currency-rate input

## M4 — Classification and scoring
- Product-class matching
- N100/N150 reference comparison
- Class-specific scoring
- Missing-component cost model
- Noise/power/expandability metadata
- Architecture-coverage value

## M5 — Price history
- Historical observations/raw snapshots
- Rolling median/low
- Bargain detection
- Duplicate/listing identity handling

## M6 — Automation
- Scheduled runs
- Reports
- Bargain issues/alerts
- Sold-out lifecycle
- Optional Prometheus/notification integrations
