import os
from pathlib import Path

def _str(key, default):
    return os.environ.get(key, default).strip() or default

class Settings:
    def __init__(self):
        self.DATA_PATH = Path(_str("DATA_PATH", "data"))
        self.SEASON = _str("SEASON", "2025-2026")
        self.log_level = _str("LOG_LEVEL", "INFO").upper()

    @property
    def season_path(self):
        return self.DATA_PATH / self.SEASON

    @property
    def by_gameweek_path(self):
        return self.season_path / "By Gameweek"

settings = Settings()
