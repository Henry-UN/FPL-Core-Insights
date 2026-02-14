"""Service layer: player and player stats data from repository."""

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from app.config import settings
from app.schemas.players import PlayerOut, PlayerStatsOut

logger = logging.getLogger(__name__)


class PlayerService:
    """Reads player and playerstats from CSV (existing data layout)."""

    def __init__(self, data_path: Path | None = None, season: str | None = None) -> None:
        self._data_path = data_path or settings.season_path
        self._season = season or settings.SEASON

    def get_players_path(self) -> Path:
        return self._data_path / "players.csv"

    def get_playerstats_path(self) -> Path:
        return self._data_path / "playerstats.csv"

    def get_players(self) -> list[PlayerOut]:
        """Return all players from players.csv."""
        path = self.get_players_path()
        if not path.exists():
            logger.warning("Players file not found: %s", path)
            return []
        try:
            df = pd.read_csv(path)
            records = df.to_dict("records")
            return [PlayerOut.from_record(r) for r in records]
        except Exception as e:
            logger.exception("Failed to load players from %s: %s", path, e)
            raise

    def get_player_stats(self, gameweek: int | None = None) -> list[PlayerStatsOut]:
        """Return player stats; optionally filter by gameweek (gw column)."""
        path = self.get_playerstats_path()
        if not path.exists():
            logger.warning("Playerstats file not found: %s", path)
            return []
        try:
            df = pd.read_csv(path, low_memory=False)
            if gameweek is not None and "gw" in df.columns:
                df = df[df["gw"] == gameweek]
            records = df.to_dict("records")
            return [PlayerStatsOut.from_record(r) for r in records]
        except Exception as e:
            logger.exception("Failed to load playerstats from %s: %s", path, e)
            raise
