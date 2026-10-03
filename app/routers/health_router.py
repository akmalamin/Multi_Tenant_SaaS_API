"""app/routers/health_router.py — Healthcheck endpoint."""

from fastapi import APIRouter, status
from datetime import datetime

router = APIRouter(tags=["System Health"])


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "healthy",
        "service": "Multi-Tenant SaaS Engine",
        "timestamp": datetime.utcnow().isoformat(),
    }