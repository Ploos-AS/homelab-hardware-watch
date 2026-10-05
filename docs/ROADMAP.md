# Roadmap

## M0 — Foundation — complete
- [x] Repository purpose and principles
- [x] Seven target product classes
- [x] Initial Norwegian/European vendor registry
- [x] Norway delivered-cost assumptions
- [x] Initial normalized product model
- [x] Initial sourcing policy
- [x] Initial price-rule framework

## M1 — Norway collectors — complete
- [x] Norwegian vendor collector framework
- [x] FINN/manual marketplace ingestion strategy
- [x] Marketplace identity/lifecycle model
- [x] Normalization tests
- [x] N150/16 GB configuration parity
- [x] x86, ARM64 and macOS runner families
- [x] Current-candidates report
- [x] Role-aware current-opportunities report
- [x] CI test matrix

Automated FINN acquisition remains deferred until a stable/permitted acquisition mechanism is selected. Historical raw snapshots belong to M5.

## M2 — Europe collectors — active coverage
- [x] Netherlands collectors
- [x] Germany collectors
- [x] Shipping/import capability metadata foundation
- [x] ARM64/NUC/Mac mini target coverage
- [ ] Baltics automated collector coverage
- [ ] Sweden/Denmark automated collector coverage
- [ ] Broader vendor capability metadata

## M3 — Delivered cost/import intelligence — complete
- [x] Explicit import/VAT/handling model
- [x] Fail-closed delivered-NOK calculator
- [x] Historical dated FX observations
- [x] Norges Bank indicative-rate provider
- [x] Tolletaten/customs-rate distinction
- [x] Vendor import policy and dated evidence
- [x] ServerShop24 Norway weight-based shipping
- [x] Estimate vs import-confirmed price confidence
- [x] Enterprise scoring integration
- [x] End-to-end ServerShop24 R640 acceptance coverage
- [ ] UK automated collectors (coverage backlog; not an M3 blocker)

## M4 — Decision-quality classification and scoring — active
Already present:
- [x] Initial product-class matching
- [x] Initial Proxmox/storage enterprise scoring
- [x] N100/N150 reference comparison foundation
- [x] Price-confidence-aware BUY/WATCH/PASS actions

Remaining:
- [x] Class-specific decision scoring across the seven target classes
- [x] AI/GPU-host scoring
- [x] Managed-switch scoring
- [x] Tiny/CI-runner scoring (x86, ARM64 and macOS roles)
- [x] UPS scoring with required battery-replacement cost
- [x] Unified BUY/WATCH/PASS dispatcher
- [x] Unified opportunity-report integration
- [x] Unified monitor/action-transition integration
- [ ] Generalized missing-component cost model beyond UPS batteries
- [ ] Richer noise/power/expandability metadata and evidence
- [ ] Architecture-coverage value

## M5 — Price history
- [ ] Historical observations/raw snapshots
- [ ] Rolling median/low
- [ ] Bargain detection
- [ ] Stronger duplicate/listing identity handling

## M6 — Automation
Already present:
- [x] Scheduled EU monitor
- [x] Current reports/artifacts
- [x] Snapshot/change detection
- [x] Alert filtering
- [x] BUY/WATCH action-change alerts

Remaining:
- [ ] Bargain issues/alerts based on M5 history
- [ ] Sold-out lifecycle
- [ ] Optional Prometheus/notification integrations
