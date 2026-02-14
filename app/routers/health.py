"""Health check endpoint."""

from fastapi import APIRouter

from app.schemas.common import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Liveness/readiness check."""
    return HealthResponse(status="ok", service="fpl-core-insights")
