# M1 — Norway collectors

## Implemented first

- IT Garasjen: Shopify collection feed collector
- Axentra: Shopify collection feed collector
- Normalized Candidate model
- JSON output
- Markdown current-candidates report
- Collector failures are isolated so one vendor cannot stop the run

## Vendor relationship note

Plan B IT and IT Garasjen are related. IT Garasjen identifies PLAN B IT AS as the operator of the store, while Plan B IT describes IT Garasjen as its refurbished consumer partner. They must therefore not be treated as independent market observations when calculating price distributions.

## Next Norwegian sources

- ScandicTech
- TekAgain
- Rebuild IT
- BruktTech
- FINN/manual ingestion

Collectors should prefer stable structured storefront/API surfaces where available. HTML parsing should be vendor-specific and covered by fixtures/tests.
