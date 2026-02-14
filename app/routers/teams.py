"""Teams endpoint."""

import logging

from fastapi import APIRouter

from app.schemas.teams import TeamOut
from app.services.team_service import TeamService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/teams", tags=["teams"])
_team_service: TeamService | None = None


def get_team_service() -> TeamService:
    global _team_service
    if _team_service is None:
        _team_service = TeamService()
    return _team_service


@router.get("", response_model=list[TeamOut])
def get_teams() -> list[TeamOut]:
    """Return all teams from the data repository."""
    return get_team_service().get_teams()
