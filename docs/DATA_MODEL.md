# Normalized product data model

M0 defines the record later collectors will produce.

```yaml
id: vendor-specific-or-derived-id
vendor_id: serverpunt_nl
url: https://example.invalid/item
observed_at: 2026-10-05T00:00:00Z

title: Dell PowerEdge R740
condition: refurbished
stock_status: in_stock

pricing:
  currency: EUR
  item_price: 299
  shipping_price: null
  vendor_vat_included: false
  delivered_nok: null

hardware:
  vendor: Dell
  model: PowerEdge R740
  form_factor: 2U
  cpu:
    model: Xeon Gold 6138
    quantity: 2
  memory_gb: 0
  storage: []
  drive_bays:
    count: 8
    type: SFF
  pcie_slots: null
  nic: []
  remote_management: iDRAC9
  psu:
    redundant: true

classification:
  - proxmox_compute

metadata:
  warranty_months: null
  notes: []
```

Unknown data must be null/unknown, never guessed. Raw observations should remain available for debugging and later re-normalization. A listing may match multiple product classes.
