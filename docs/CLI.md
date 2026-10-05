# CLI workflow

## Norway

```sh
hhw collect-no
```

## Update EUR/NOK reference observations

```sh
hhw fx-update
```

This stores recent dated Norges Bank observations in `data/fx.json`.

## Europe

```sh
hhw collect-eu
```

Outputs:

- `data/current-eu.json`
- `reports/current-eu.md`
- `reports/current-eu-opportunities.md`

EU collection may use the FX observation immediately, but a candidate still receives no comparable `delivered_nok` when shipping, handling, or export-VAT treatment is unknown.

The two commands are deliberately separate so an old observation remains reproducible and network failures in the FX provider do not corrupt collection logic.
