from __future__ import annotations

import json
from pathlib import Path

from hhw.monitoring import Snapshot


def load_state(path: str | Path) -> dict[str, Snapshot]:
    path = Path(path)
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        row["candidate_id"]: Snapshot(**row)
        for row in payload.get("candidates", [])
    }


def save_state(path: str | Path, snapshots: list[Snapshot]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [x.to_dict() for x in sorted(snapshots, key=lambda x: x.candidate_id)]
    payload = {"version": 1, "candidates": rows}
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
