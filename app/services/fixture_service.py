"""Service layer: fixture data from repository."""

import logging
from pathlib import Path

import pandas as pd

from app.config import settings
from app.schemas.fixtures import FixtureOut

logger = logging.getLogger(__name__)


class FixtureService:
    """Reads fixtures from By Gameweek GW*/fixtures.csv (existing data layout)."""

    def __init__(self, data_path: Path | None = None) -> None:
        self._by_gameweek = (data_path or settings.season_path) / "By Gameweek"

    def get_fixtures_paths(self) -> list[Path]:
        """All GW*/fixtures.csv under By Gameweek."""
        if not self._by_gameweek.exists():
            return []
        paths: list[Path] = []
        for child in sorted(self._by_gameweek.iterdir()):
            if child.is_dir() and child.name.startswith("GW"):
                f = child / "fixtures.csv"
                if f.exists():
                    paths.append(f)
        return paths

    def get_fixtures(self, gameweek: int | None = None) -> list[FixtureOut]:
        """Return fixtures; optionally filter by gameweek."""
        paths = self.get_fixtures_paths()
        if not paths:
            logger.warning("No fixture files under By Gameweek: %s", self._by_gameweek)
            return []
        dfs: list[pd.DataFrame] = []
        for p in paths:
            try:
                df = pd.read_csv(p, low_memory=False)
                dfs.append(df)
            except Exception as e:
                logger.warning("Skip %s: %s", p, e)
        if not dfs:
            return []
        combined = pd.concat(dfs, ignore_index=True)
        if gameweek is not None and "gameweek" in combined.columns:
            combined = combined[combined["gameweek"] == float(gameweek)]
        records = combined.to_dict("records")
        return [FixtureOut.from_record(r) for r in records]
