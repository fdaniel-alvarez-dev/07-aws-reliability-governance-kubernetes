from __future__ import annotations

from datetime import datetime, timezone


ALLOWED_EVENT_TYPES = {"signup", "login", "purchase"}


def _parse_int(value: str, field: str) -> int:
    try:
        n = int(value)
    except Exception as e:
        raise ValueError(f"{field} must be an integer (got {value!r}): {e}") from e
    if n < 1:
        raise ValueError(f"{field} must be >= 1 (got {n})")
    return n


def _parse_ts(value: str) -> str:
    if not value.endswith("Z"):
        raise ValueError(f"event_ts must end with 'Z' (UTC) (got {value!r})")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception as e:
        raise ValueError(f"event_ts must be ISO-8601 (got {value!r}): {e}") from e
    dt = dt.astimezone(timezone.utc)
    return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def validate_events_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    if not rows:
        raise ValueError("input is empty")

    out: list[dict[str, object]] = []
    seen_event_ids: set[int] = set()

    for i, row in enumerate(rows, start=1):
        missing = [k for k in ("event_id", "user_id", "event_type", "event_ts") if k not in row]
        if missing:
            raise ValueError(f"row {i}: missing required columns: {', '.join(missing)}")

        event_id = _parse_int(str(row["event_id"]), "event_id")
        if event_id in seen_event_ids:
            raise ValueError(f"row {i}: duplicate event_id {event_id}")
        seen_event_ids.add(event_id)

        user_id = _parse_int(str(row["user_id"]), "user_id")
        event_type = str(row["event_type"]).strip()
        if event_type not in ALLOWED_EVENT_TYPES:
            raise ValueError(f"row {i}: event_type must be one of {sorted(ALLOWED_EVENT_TYPES)} (got {event_type!r})")

        event_ts = _parse_ts(str(row["event_ts"]).strip())
        out.append(
            {
                "event_id": event_id,
                "user_id": user_id,
                "event_type": event_type,
                "event_ts": event_ts,
            }
        )

    return out

