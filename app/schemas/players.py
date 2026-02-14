# Player-related Pydantic models
from typing import Any
from pydantic import BaseModel, ConfigDict

def _si(v):
    if v is None or (isinstance(v, float) and (v != v or v == float("inf"))):
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None

def _sf(v):
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None

def _ss(v):
    if v is None:
        return None
    return str(v).strip() or None

class PlayerOut(BaseModel):
    model_config = ConfigDict(extra="allow")
    player_code: int | None = None
    player_id: int | None = None
    first_name: str | None = None
    second_name: str | None = None
    web_name: str | None = None
    team_code: int | None = None
    position: str | None = None

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "PlayerOut":
        return cls(
            player_code=_si(record.get("player_code")),
            player_id=_si(record.get("player_id")),
            first_name=_ss(record.get("first_name")),
            second_name=_ss(record.get("second_name")),
            web_name=_ss(record.get("web_name")),
            team_code=_si(record.get("team_code")),
            position=_ss(record.get("position")),
        )

class PlayerStatsOut(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: int | None = None
    web_name: str | None = None
    total_points: float | None = None
    minutes: int | None = None
    goals_scored: int | None = None
    assists: int | None = None
    clean_sheets: int | None = None
    goals_conceded: int | None = None
    now_cost: float | None = None
    form: float | None = None
    gw: int | None = None

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> "PlayerStatsOut":
        return cls(
            id=_si(record.get("id")),
            web_name=_ss(record.get("web_name")),
            total_points=_sf(record.get("total_points")),
            minutes=_si(record.get("minutes")),
            goals_scored=_si(record.get("goals_scored")),
            assists=_si(record.get("assists")),
            clean_sheets=_si(record.get("clean_sheets")),
            goals_conceded=_si(record.get("goals_conceded")),
            now_cost=_sf(record.get("now_cost")),
            form=_sf(record.get("form")),
            gw=_si(record.get("gw")),
        )
