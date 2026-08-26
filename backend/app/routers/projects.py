from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from app.schemas import PaginatedProjectsResponse, ProjectSchema
from app.services.ml_service import MLService

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])

@router.get("", response_model=PaginatedProjectsResponse)
def get_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    q: Optional[str] = Query(None, description="Search query across Work ID, MP Name, or Description"),
    state: Optional[str] = Query(None, description="Filter by State/UT"),
    category: Optional[str] = Query(None, description="Filter by Work Category"),
    risk_level: Optional[str] = Query(None, description="Filter by Risk Level (Low, Medium, High, Critical)"),
    sort_by: str = Query("risk_score", description="Sort field")
):
    ml_svc = MLService()
    res = ml_svc.get_projects(
        page=page,
        page_size=page_size,
        q=q,
        state=state,
        category=category,
        risk_level=risk_level,
        sort_by=sort_by
    )
    return res

@router.get("/{work_id:path}", response_model=ProjectSchema)
def get_project_by_id(work_id: str):
    ml_svc = MLService()
    project = ml_svc.get_project_by_id(work_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with ID '{work_id}' not found.")
    return project
