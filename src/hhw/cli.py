import argparse
import json
from datetime import date, timedelta
from pathlib import Path

from hhw.alert_policy import filter_alerts
from hhw.cost_enrich import enrich_delivered_cost
from hhw.fx import FxObservation
from hhw.importers import import_marketplace_json
from hhw.normalize import normalize_all
from hhw.monitor_run import run_monitor
from hhw.opportunity_report import markdown_opportunities
from hhw.parity import configuration_parity
from hhw.providers.norges_bank import fetch_daily
from hhw.providers.tolletaten import fetch_current as fetch_customs_fx
from hhw.reference import N150_REFERENCE, price_vs_n150
from hhw.registry import european_collectors, norwegian_collectors
from hhw.report import markdown_report
from hhw.vendor_evidence_store import load_vendor_evidence


def enrich(candidates):
    candidates = normalize_all(candidates)
    for candidate in candidates:
        if candidate.currency == "NOK":
            parity = configuration_parity(candidate)
            candidate.metadata["configuration_parity"] = parity
            candidate.metadata["n150_price_comparison"] = price_vs_n150(
                parity["adjusted_price_nok"] if parity["comparable"] else None
            )
    return candidates


def _collect(collectors):
    candidates, errors = [], []
    for collector in collectors:
        try:
            candidates.extend(collector.collect())
        except Exception as exc:
            errors.append({"vendor_id": collector.vendor_id, "error": str(exc)})
    return candidates, errors


def collect_norway(marketplace_files=None):
    candidates, errors = _collect(norwegian_collectors())
    for path in marketplace_files or []:
        try:
            candidates.extend(import_marketplace_json(path))
        except Exception as exc:
            errors.append({"vendor_id": "marketplace_import", "file": path, "error": str(exc)})
    return enrich(candidates), errors


def load_fx(path):
    p = Path(path)
    if not p.exists():
        return []
    data = json.loads(p.read_text(encoding="utf-8"))
    return [
        FxObservation(x["base"], x["quote"], float(x["rate"]), date.fromisoformat(x["observed_on"]), x["source"])
        for x in data.get("observations", [])
    ]


def collect_europe(fx_file="data/fx.json", evidence_file="data/vendor-evidence.json", observed_on=None):
    candidates, errors = _collect(european_collectors())
    candidates = enrich(candidates)
    fx = load_fx(fx_file)
    evidence = load_vendor_evidence(evidence_file)
    day = observed_on or date.today()
    currencies = sorted({c.currency for c in candidates if c.currency not in ("NOK", None)})
    for currency in currencies:
        try:
            customs = fetch_customs_fx(currency, day)
            if customs is not None:
                fx.append(customs)
        except Exception as exc:
            errors.append({"vendor_id": "tolletaten_fx", "currency": currency, "error": str(exc)})
    for candidate in candidates:
        enrich_delivered_cost(candidate, fx, day, evidence)
    return candidates, errors


def save_fx(path, observations):
    by_key = {
        (x.base, x.quote, x.observed_on, x.source): x
        for x in observations
    }
    ordered = sorted(
        by_key.values(),
        key=lambda x: (x.observed_on, x.base, x.quote, x.source),
    )
    payload = {"observations": [
        {"base": x.base, "quote": x.quote, "rate": x.rate,
         "observed_on": x.observed_on.isoformat(), "source": x.source}
        for x in ordered
    ]}
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return ordered


def update_fx(path="data/fx.json", currency="EUR", days=14):
    end = date.today()
    start = end - timedelta(days=days)
    existing = load_fx(path)
    fetched = fetch_daily(currency, start, end)
    return save_fx(path, existing + fetched)


def write_outputs(candidates, errors, out, report, opportunities):
    for path in (out, report, opportunities):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps({
        "reference": {"n150": N150_REFERENCE},
        "candidates": [c.to_dict() for c in candidates],
        "errors": errors,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    Path(report).write_text(markdown_report(candidates), encoding="utf-8")
    Path(opportunities).write_text(markdown_opportunities(candidates), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(prog="hhw")
    parser.add_argument("command", choices=["collect-no", "collect-eu", "monitor-eu", "fx-update"])
    parser.add_argument("--marketplace", action="append", default=[])
    parser.add_argument("--fx-file", default="data/fx.json")
    parser.add_argument("--evidence-file", default="data/vendor-evidence.json")
    parser.add_argument("--out")
    parser.add_argument("--report")
    parser.add_argument("--opportunities")
    parser.add_argument("--state-file", default="data/monitor-eu-state.json")
    parser.add_argument("--role", choices=["proxmox_compute", "storage"], default="proxmox_compute")
    parser.add_argument("--alerts-only", action="store_true")
    args = parser.parse_args()

    if args.command == "fx-update":
        observations = update_fx(args.fx_file)
        print(f"stored {len(observations)} FX observations in {args.fx_file}")
        return

    if args.command in {"collect-eu", "monitor-eu"}:
        candidates, errors = collect_europe(args.fx_file, args.evidence_file)
        out = args.out or "data/current-eu.json"
        report = args.report or "reports/current-eu.md"
        opportunities = args.opportunities or "reports/current-eu-opportunities.md"
    else:
        candidates, errors = collect_norway(args.marketplace)
        out = args.out or "data/current-no.json"
        report = args.report or "reports/current-no.md"
        opportunities = args.opportunities or "reports/current-opportunities.md"

    write_outputs(candidates, errors, out, report, opportunities)

    if args.command == "monitor-eu":
        events = run_monitor(candidates, args.state_file, args.role)
        if args.alerts_only:
            events = filter_alerts(events)
        print(json.dumps([event.__dict__ for event in events], ensure_ascii=False, indent=2))

    if errors:
        print(json.dumps(errors, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
