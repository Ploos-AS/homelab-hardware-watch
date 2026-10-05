# Vendor evidence

Vendor policy describes what information is required. Vendor evidence records dated observations of what was actually verified.

Each observation contains:

- `vendor_id`
- `observed_on`
- `evidence_type`
- `source`
- structured `values`
- optional `note`

Typical evidence types are `shipping`, `vat`, `handling`, and `norway_checkout`.

Evidence is historical. Selection uses the latest observation not later than the candidate observation date. Future evidence must never be applied retroactively.

Examples of structured values include:

- `shipping_eur`
- `shipping_nok`
- `foreign_vat_rate`
- `foreign_vat_included`
- `foreign_vat_removed_for_export`
- `handling_nok`

The repository starts with an empty evidence store. Values must be backed by an actual checkout, quote, vendor terms, or another explicit source; they must not be guessed.
