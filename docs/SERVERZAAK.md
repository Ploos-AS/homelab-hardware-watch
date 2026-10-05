# ServerZaak collector

ServerZaak sells configurable refurbished servers. Product-list prices are therefore treated as **starting configuration prices**, not complete comparable systems.

The catalogue explicitly describes user-selectable processor, memory, RAID/HBA, disks and networking for models such as Dell PowerEdge R630/R640/R740XD.

## Rules

- `price_kind = starting_configuration`
- `configurable = true`
- `configuration_complete = false`
- no N150 price-parity claim from the starting price
- no delivered-NOK claim until shipping and Norwegian tax handling are known
- free shipping advertised for orders over EUR 50 applies to Netherlands addresses, not Norway

A later configurator-aware collector may calculate useful reference builds, e.g. a Proxmox configuration or storage-node configuration.
