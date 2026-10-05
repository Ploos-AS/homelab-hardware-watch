import argparse
import json
from pathlib import Path

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
    return candidates, errors


def main():
    parser = argparse.ArgumentParser(prog="hhw")
    parser.add_argument("command", choices=["collect-no"])
    parser.add_argument("--out", default="data/current-no.json")
    parser.add_argument("--report", default="reports/current-no.md")
    args = parser.parse_args()

    candidates, errors = collect_norway()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps({
        "candidates": [c.to_dict() for c in candidates],
        "errors": errors,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    Path(args.report).write_text(markdown_report(candidates), encoding="utf-8")

    if errors:
        print(json.dumps(errors, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
