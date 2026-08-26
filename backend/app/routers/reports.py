from typing import Optional
from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from app.services.pdf_service import generate_pdf_report

router = APIRouter(prefix="/api/v1/reports", tags=["Reports"])

@router.get("/pdf")
def download_pdf_report(
    state: Optional[str] = Query(None, description="Filter by State"),
    risk_level: Optional[str] = Query(None, description="Filter by Risk Level")
):
    pdf_path = generate_pdf_report(state_filter=state, risk_level_filter=risk_level)
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="mplad_ai_audit_report.pdf"
    )
