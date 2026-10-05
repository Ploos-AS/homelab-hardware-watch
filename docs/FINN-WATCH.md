# FINN watch strategy

FINN is a high-value opportunistic source, but M1 deliberately does not depend on brittle HTML scraping.

## Collection strategy

Use FINN saved searches as the acquisition edge. Normalize resulting listings into the same Candidate/marketplace pipeline as shop collectors.

FINN supports saved searches and notifications for new matching listings. This is preferable to hard-coding rendered-page selectors into the core collector.

## Search families

Saved searches are defined in `config/finn-watch.yaml` for:

- x86 Linux runners
- Mac mini runners
- ARM64 SBC runners
- Proxmox/workstation/server compute
- storage/HBA/NIC
- managed switching
- AI-capable workstation chassis

## Listing lifecycle

A marketplace listing is not inventory in the shop sense. Track:

- new
- active
- price_changed
- gone
- relisted

Prefer FINN code as stable identity, then canonical URL. Fallback title/seller fingerprints are weaker and should be marked accordingly.

## Search quality

Do not rely on one broad query. Product-family searches are intentional: marketplace search relevance can introduce unrelated results, while narrow saved searches make classification and alerts easier to audit.

## Next

Add a small import format for saved-search notifications/exported links, then build the first current-opportunities report across shops + FINN.
