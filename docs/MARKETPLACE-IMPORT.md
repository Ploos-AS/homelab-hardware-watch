# Marketplace import

M1 accepts marketplace observations through a small JSON interchange format.

This keeps acquisition separate from normalization and scoring. FINN saved-search notifications, manually reviewed links or a future permitted adapter can all produce the same format.

## Required

- title
- url

## Recommended

- source
- source_id
- price_nok
- currency
- condition
- status
- categories
- observed_at
- seller_id

Never infer missing price, RAM or storage during import. Title normalization happens later in the common pipeline.

The file `examples/finn-import.json` is synthetic and must never be treated as a live market observation.
