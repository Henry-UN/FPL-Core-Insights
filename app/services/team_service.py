"""Service layer: team data from repository."""

import logging
from pathlib import Path

import pandas as pd

from app.config import settings
from app.schemas.teams import TeamOut

logger = logging.getLogger(__name__)


class TeamService:
    """Reads teams from CSV (existing data layout)."""

    def __init__(self, data_path: Path | None = None) -> None:
        self._data_path = data_path or settings.season_path

    def get_teams_path(self) -> Path:
        return self._data_path / "teams.csv"

    def get_teams(self) -> list[TeamOut]:
        """Return all teams from teams.csv."""
        path = self.get_teams_path()
        if not path.exists():
            logger.warning("Teams file not found: %s", path)
            return []
        try:
            df = pd.read_csv(path)
            records = df.to_dict("records")
            return [TeamOut.from_record(r) for r in records]
        except Exception as e:
            logger.exception("Failed to load teams from %s: %s", path, e)
            raise
