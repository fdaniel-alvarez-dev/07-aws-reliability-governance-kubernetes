from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Lineage:
    created_at_utc: str
    raw_path: str
    out_path: str
    row_count: int
    content_sha256: str


def build_lineage(*, raw_path: Path, out_path: Path, row_count: int, content_sha256: str) -> str:
    lineage = Lineage(
        created_at_utc=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        raw_path=str(raw_path),
        out_path=str(out_path),
        row_count=row_count,
        content_sha256=content_sha256,
    )
    return json.dumps(asdict(lineage), indent=2, sort_keys=True) + "\n"

