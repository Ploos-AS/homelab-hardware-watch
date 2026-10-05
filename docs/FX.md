# FX observations

Currency conversion is based on dated observations.

The repository deliberately contains no pretend "current EUR/NOK" constant. A candidate observation uses the newest FX observation that is not newer than the candidate date.

The preferred provider is Norges Bank. Provider acquisition is a separate adapter so tests and historical reports remain deterministic.

Each delivered-cost record stores both the FX observation date and source.
