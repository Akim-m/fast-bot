from fastapi import APIRouter, status
from datetime import datetime
from services.db_service import check_database_health
from schemas import HealthCheckOut

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", response_model=HealthCheckOut, status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint to verify API and database status
    """
    db_healthy = check_database_health()
    
    return HealthCheckOut(
        status="healthy" if db_healthy else "degraded",
        database="connected" if db_healthy else "disconnected",
        timestamp=datetime.utcnow().isoformat()
    )

@router.get("/ping")
async def ping():
    """
    Simple ping endpoint for basic connectivity check
    """
    return {"message": "pong"}