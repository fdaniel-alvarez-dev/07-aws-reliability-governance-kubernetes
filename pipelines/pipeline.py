from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

from pipelines.lineage import build_lineage
from pipelines.schema import validate_events_rows

ALLOWED_FORMATS = {"jsonl", "parquet"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal governed pipeline (CSV -> governed output + lineage).")
    parser.add_argument("--raw", default="data/raw/events.csv", help="Input CSV path.")
    parser.add_argument("--out-dir", default="data/processed", help="Output directory.")
    parser.add_argument("--format", default="jsonl", choices=sorted(ALLOWED_FORMATS), help="Output format.")
    args = parser.parse_args()

    raw_path = Path(args.raw)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with raw_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    validated = validate_events_rows(rows)

    data_bytes = "\n".join(
        f"{r['event_id']},{r['user_id']},{r['event_type']},{r['event_ts']}" for r in validated
    ).encode("utf-8")
    content_sha256 = hashlib.sha256(data_bytes).hexdigest()

    if args.format == "jsonl":
        out_path = out_dir / "events.jsonl"
        out_path.write_text(
            "\n".join(
                f'{{"event_id":{r["event_id"]},"user_id":{r["user_id"]},"event_type":"{r["event_type"]}","event_ts":"{r["event_ts"]}"}}'
                for r in validated
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {out_path} ({len(validated)} rows)")
    else:
        try:
            import pandas as pd  # type: ignore
            import pyarrow  # noqa: F401  # type: ignore
        except Exception as e:
            raise SystemExit(
                "Parquet output requires optional dependencies. Run `make setup` and use `make demo-rich`.\n"
                f"Import error: {e}"
            )

        df = pd.DataFrame(validated)
        out_path = out_dir / "events.parquet"
        df.to_parquet(out_path, index=False)
        print(f"Wrote {out_path} ({len(validated)} rows)")

    lineage = build_lineage(raw_path=raw_path, out_path=out_path, row_count=len(validated), content_sha256=content_sha256)
    lineage_path = out_dir / "lineage.json"
    lineage_path.write_text(lineage, encoding="utf-8")
    print(f"Wrote {lineage_path}")


if __name__ == "__main__":
    main()
