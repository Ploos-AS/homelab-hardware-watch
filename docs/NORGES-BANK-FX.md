# Norges Bank FX provider

The provider reads daily exchange-rate observations from Norges Bank's open-data API.

Series convention:

`EXR/B.<currency>.NOK.SP`

For EUR this is `B.EUR.NOK.SP`, i.e. NOK per EUR.

The provider requests CSV for an explicit date interval and converts each observation into an immutable `FxObservation`.

## Important

Norges Bank describes these rates as indicative middle rates. They are suitable as a reproducible reference for comparison and historical analysis, but they are not a promise of the actual card/bank conversion rate paid by Ploos AS.

The delivered-cost model can later add an explicit FX/payment margin if real purchase-cost modelling requires it.

Network access is isolated in the provider. Unit tests parse fixed fixture data and do not depend on the live service.
