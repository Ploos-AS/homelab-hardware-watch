# Delivered cost to Norway

The canonical comparison price is `delivered_nok`.

For imported hardware it is not simply catalogue EUR × exchange rate. The model records displayed item price, foreign VAT/export treatment, dated exchange rate, shipping, Norwegian VAT basis, customs/import inputs and handling.

## VAT basis

The current calculator applies Norwegian VAT to:

- export-adjusted item value
- shipping
- customs duty
- import fees that are part of the taxable basis

Carrier/handling cost is represented separately as `handling_nok` and is added after the calculated Norwegian VAT. Evidence must determine whether a real fee belongs in `import_fees_nok` or `handling_nok`; do not silently assume zero.

## Fail closed

A candidate is not economically comparable when a required input is unknown. Important reasons include:

- `item_price_unknown`
- `exchange_rate_unknown`
- `shipping_unknown`
- `handling_unknown`
- `foreign_vat_export_treatment_unknown`
- `foreign_vat_rate_unknown`

The watch must not silently assume that an EU seller removes local VAT for Norway.

## Exchange-rate confidence

Rates are dated observations so historical comparisons remain reproducible.

- Norges Bank observations are treated as `indicative_market_rate` and produce an `estimate`.
- Tolletaten/customs observations are treated as `customs_rate` and can produce `import_confirmed` cost status when the other required inputs are known.

Raw foreign-currency prices are never compared directly with NOK thresholds.

## Evidence

Reusable vendor evidence is dated and source-attributed. Candidate-specific checkout or quote metadata overrides reusable vendor evidence. Future evidence is never applied retroactively to an older candidate observation.
