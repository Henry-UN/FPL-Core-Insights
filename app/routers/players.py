import logging
from typing import Annotated
from fastapi import APIRouter, Query
from app.schemas.players import PlayerOut, PlayerStatsOut
from app.services.player_service import PlayerService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/players", tags=["players"])
_svc: PlayerService | None = None

def get_player_service():
    global _svc
    if _svc is None:
        _svc = PlayerService()
    return _svc

@router.get("", response_model=list[PlayerOut])
def get_players():
    return get_player_service().get_players()

@router.get("/stats", response_model=list[PlayerStatsOut])
def get_player_stats(gameweek: Annotated[int | None, Query()] = None):
    return get_player_service().get_player_stats(gameweek=gameweek)
