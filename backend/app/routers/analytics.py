from fastapi import APIRouter
from app.schemas import AnalyticsOverviewSchema
from app.services.ml_service import MLService

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])

@router.get("/overview", response_model=AnalyticsOverviewSchema)
def get_analytics_overview():
    ml_svc = MLService()
    return ml_svc.get_analytics_overview()
