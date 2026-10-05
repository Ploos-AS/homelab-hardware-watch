import argparse
import json
from pathlib import Path

from hhw.normalize import normalize_all
from hhw.opportunity_report import markdown_opportunities
from hhw.parity import configuration_parity
from hhw.reference import N150_REFERENCE, price_vs_n150
from hhw.registry import norwegian_collectors
from hhw.report import markdown_report


def collect_norway():
    candidates = []
    errors = []
    for collector in norwegian_collectors():
        try:
            candidates.extend(collector.collect())
        except Exception as exc:
            errors.append({"vendor_id": collector.vendor_id, "error": str(exc)})
    candidates = normalize_all(candidates)
    for candidate in candidates:
        if candidate.currency == "NOK":
            parity = configuration_parity(candidate)
            candidate.metadata["configuration_parity"] = parity
            candidate.metadata["n150_price_comparison"] = price_vs_n150(
                parity["adjusted_price_nok"] if parity["comparable"] else None
            )
    return candidates, errors


def main():
    parser = argparse.ArgumentParser(prog="hhw")
    parser.add_argument("command", choices=["collect-no"])
    parser.add_argument("--out", default="data/current-no.json")
    parser.add_argument("--report", default="reports/current-no.md")
    parser.add_argument("--opportunities", default="reports/current-opportunities.md")
    args = parser.parse_args()

    candidates, errors = collect_norway()
    for path in (args.out, args.report, args.opportunities):
        Path(path).parent.mkdir(parents=True, exist_ok=True)

    Path(args.out).write_text(json.dumps({
        "reference": {"n150": N150_REFERENCE},
        "candidates": [c.to_dict() for c in candidates],
        "errors": errors,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    Path(args.report).write_text(markdown_report(candidates), encoding="utf-8")
    Path(args.opportunities).write_text(markdown_opportunities(candidates), encoding="utf-8")

    if errors:
        print(json.dumps(errors, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
