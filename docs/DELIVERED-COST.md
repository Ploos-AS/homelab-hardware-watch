# Delivered cost to Norway

The canonical comparison price is `delivered_nok`.

For imported hardware it is not simply catalogue EUR × exchange rate.

The model records:

1. displayed item price
2. whether foreign VAT is included
3. whether that VAT is removed for export to Norway
4. explicit exchange rate
5. shipping
6. Norwegian VAT
7. handling/import fee

Norwegian VAT is calculated on item value plus shipping in the current model.

## Fail closed

A candidate is not economically comparable when a required input is unknown. Important reasons include:

- `exchange_rate_unknown`
- `shipping_unknown`
- `handling_unknown`
- `foreign_vat_export_treatment_unknown`
- `foreign_vat_rate_unknown`

The watch must not silently assume that an EU seller removes local VAT for Norway.

## Exchange rates

No hard-coded EUR/NOK rate is used. Rates must be supplied as dated observations by a later rate provider so historical comparisons remain reproducible.
