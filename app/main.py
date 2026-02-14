"""FPL Core Insights API - FastAPI application entrypoint."""

import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import fixtures, health, players, teams

# Structured logging to stdout (JSON-friendly in containers)
logging.basicConfig(
    level=getattr(logging, settings.log_level, logging.INFO),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    stream=sys.stdout,
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FPL Core Insights API",
    description="Data ingestion, player statistics, teams, and fixtures",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(players.router)
app.include_router(teams.router)
app.include_router(fixtures.router)


@app.on_event("startup")
async def startup() -> None:
    logger.info("FPL Core Insights API starting; data path=%s season=%s", settings.DATA_PATH, settings.SEASON)


@app.on_event("shutdown")
async def shutdown() -> None:
    logger.info("FPL Core Insights API shutting down")
