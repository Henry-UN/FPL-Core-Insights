"""Fixture-related Pydantic models."""

from typing import Any

from pydantic import BaseModel, ConfigDict


class FixtureOut(BaseModel):
    """Fixture list item (essential columns)."""

    model_config = ConfigDict(extra="allow")

    gameweek: float | None = None
    kickoff_time: str | None = None
    home_team: float | None = None
    away_team: float | None = None
    home_score: float | None = None
    away_score: float | None = None
    finished: bool | None = None
    match_id: str | None = None
    tournament: str | None = None

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "FixtureOut":
        finished = record.get("finished")
        if isinstance(finished, str):
            finished = finished.strip().lower() in ("true", "1", "yes")
        elif not isinstance(finished, bool):
            finished = None
        return cls(
            gameweek=_safe_float(record.get("gameweek")),
            kickoff_time=_safe_str(record.get("kickoff_time")),
            home_team=_safe_float(record.get("home_team")),
            away_team=_safe_float(record.get("away_team")),
            home_score=_safe_float(record.get("home_score")),
            away_score=_safe_float(record.get("away_score")),
            finished=finished,
            match_id=_safe_str(record.get("match_id")),
            tournament=_safe_str(record.get("tournament")),
        )


def _safe_float(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _safe_str(v: Any) -> str | None:
    if v is None:
        return None
    return str(v).strip() or None
