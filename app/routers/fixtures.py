"""Fixtures endpoint."""

import logging
from typing import Annotated

from fastapi import APIRouter, Query

from app.schemas.fixtures import FixtureOut
from app.services.fixture_service import FixtureService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/fixtures", tags=["fixtures"])
_fixture_service: FixtureService | None = None


def get_fixture_service() -> FixtureService:
    global _fixture_service
    if _fixture_service is None:
        _fixture_service = FixtureService()
    return _fixture_service


@router.get("", response_model=list[FixtureOut])
def get_fixtures(
    gameweek: Annotated[int | None, Query(description="Filter by gameweek")] = None,
) -> list[FixtureOut]:
    """Return fixtures; optional filter by gameweek."""
    return get_fixture_service().get_fixtures(gameweek=gameweek)
