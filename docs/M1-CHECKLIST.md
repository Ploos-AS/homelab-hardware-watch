# M1 completion checklist

## Collectors
- [x] Norwegian structured-store collector foundation
- [x] IT Garasjen
- [x] Axentra
- [x] Rebuild IT
- [x] ScandicTech category collector
- [x] TekAgain manual/RFQ lead
- [x] Collector failure isolation

## Marketplace
- [x] FINN watch/search plan
- [x] Marketplace identity/lifecycle model
- [x] JSON interchange/import format
- [x] Common enrichment/scoring pipeline
- [ ] Automated FINN acquisition — intentionally deferred until a stable/permitted acquisition mechanism is selected

## Normalization
- [x] CPU extraction
- [x] RAM extraction
- [x] storage extraction
- [x] Tiny/NUC/Mac runner-family detection
- [x] N150/16 GB explicit reference
- [x] 16 GB memory parity adjustment
- [x] ARM64 runner watch classes

## Output
- [x] normalized JSON
- [x] current-candidates Markdown
- [x] role-aware current-opportunities Markdown
- [x] collector errors retained in output

## Quality
- [x] pytest suite
- [x] GitHub Actions test matrix: Python 3.11–3.13
- [x] synthetic marketplace fixture clearly separated from observations

## Deferred by design
Raw historical snapshots and long-term price history belong in M5. M1 produces current observations and stable identities but does not yet build a historical database.

M1 is merge-ready when the PR test workflow is green and review finds no blocking defect.
