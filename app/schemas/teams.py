"""Team-related Pydantic models."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class TeamOut(BaseModel):
    """Team list item."""

    model_config = ConfigDict(extra="allow")

    code: int | None = None
    id: int | None = None
    name: str | None = None
    short_name: str | None = None
    strength: int | None = None

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "TeamOut":
        return cls(
            code=_safe_int(record.get("code")),
            id=_safe_int(record.get("id")),
            name=_safe_str(record.get("name")),
            short_name=_safe_str(record.get("short_name")),
            strength=_safe_int(record.get("strength")),
        )


def _safe_int(v: Any) -> int | None:
    if v is None or (isinstance(v, float) and (v != v or v == float("inf"))):
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _safe_str(v: Any) -> str | None:
    if v is None:
        return None
    return str(v).strip() or None
