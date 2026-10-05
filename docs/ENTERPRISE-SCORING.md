# Enterprise opportunity scoring

Role-specific technical scoring currently covers Proxmox compute and storage candidates. M4 will extend decision-quality scoring across all six target classes.

## Proxmox compute

Rewards include:

- 32/64/128+ GB RAM
- dual CPU where explicitly detected
- 10/25GbE
- comparable NOK price

## Storage

Rewards include:

- LFF capacity, especially 8+ and 12+ bays
- HBA rather than merely the presence of a RAID/storage controller
- 10/25GbE
- useful RAM capacity
- comparable NOK price

## Price confidence

The scoring engine never compares raw EUR prices numerically with NOK thresholds. Price signals are classified as:

- `domestic` — NOK item price
- `estimate` — delivered NOK using an indicative market FX rate
- `import_confirmed` — delivered NOK using customs-rate provenance
- `unknown`

Estimated imported prices receive a confidence penalty when they earn price points.

## Actions

Enterprise scores are converted into `BUY`, `WATCH` or `PASS`.

A high score can become `BUY` only when price confidence is `domestic` or `import_confirmed`. An attractive imported candidate with only an estimated delivered price remains `WATCH` until the cost evidence is sufficiently trustworthy.

## M4 backlog

The current enterprise model is an MVP. M4 adds missing-component cost, power/noise/expandability, architecture-coverage value, and dedicated scoring for AI/GPU hosts, managed switches and Tiny/CI runners.
