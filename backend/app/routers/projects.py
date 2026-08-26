from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Work, SyntheticPayment, SyntheticDocument, SyntheticImage, InvestigationAction, AuditLog
from schemas import WorkSchema, ActionCreateSchema

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.get("", response_model=List[WorkSchema])
def get_projects(
    state: Optional[str] = None,
    risk_level: Optional[str] = None,
    work_category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Work)
    if state:
        query = query.filter(Work.state == state)
    if risk_level:
        query = query.filter(Work.risk_level == risk_level)
    if work_category:
        query = query.filter(Work.work_category == work_category)
    if search:
        query = query.filter(Work.work_description.ilike(f"%{search}%") | Work.work_id.ilike(f"%{search}%") | Work.mp_name.ilike(f"%{search}%"))

    return query.order_by(Work.composite_risk_score.desc()).offset(offset).limit(limit).all()


@router.get("/queue", response_model=List[WorkSchema])
def get_investigation_queue(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Returns ranked investigation queue prioritized by Composite Risk Score and financial exposure.
    """
    return db.query(Work).filter(Work.risk_level.in_(["Critical", "High"])).order_by(Work.composite_risk_score.desc()).limit(limit).all()


@router.get("/detail")
def get_project_by_id_query(work_id: str, db: Session = Depends(get_db)):
    work = db.query(Work).filter(Work.work_id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Project not found")
    return work


@router.get("/explain")
def explain_project_risk_query(work_id: str, db: Session = Depends(get_db)):
    work = db.query(Work).filter(Work.work_id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Project not found")

    payments = db.query(SyntheticPayment).filter(SyntheticPayment.work_id == work_id).all()
    documents = db.query(SyntheticDocument).filter(SyntheticDocument.work_id == work_id).all()
    images = db.query(SyntheticImage).filter(SyntheticImage.work_id == work_id).all()

    reasons_list = [r.strip() for r in (work.risk_reasons or "").split("|") if r.strip()]

    return {
        "work_id": work.work_id,
        "composite_risk_score": work.composite_risk_score,
        "risk_level": work.risk_level,
        "data_source": work.data_source,
        "explainability_reasons": reasons_list,
        "dimension_scores": {
            "v1_isolation_forest": {"score": work.v1_anomaly_score, "data_source": "real_esakshi"},
            "cost_relative_median": {"score": work.cost_anomaly_score, "data_source": "real_esakshi"},
            "sanction_delay": {"score": work.delay_anomaly_score, "data_source": "real_esakshi"},
            "duplicate_similarity": {"score": work.duplicate_score, "data_source": "real_esakshi"},
            "mp_fund_utilization": {"score": work.fund_utilization_score, "data_source": "real_esakshi"},
            "agency_network_concentration": {"score": work.network_score, "data_source": "real_esakshi"}
        },
        "evidence": {
            "payments": [{"date": p.payment_date, "amount": p.amount_paid, "anomaly": p.is_anomaly, "data_source": p.data_source} for p in payments],
            "documents": [{"type": d.document_type, "ocr_mismatch": d.ocr_mismatch_detected, "note": d.audit_note, "data_source": d.data_source} for d in documents],
            "images": [{"url": i.image_url, "cv_progress": i.cv_detected_progress_pct, "visual_mismatch": i.visual_mismatch_detected, "note": i.audit_note, "data_source": i.data_source} for i in images]
        },
        "disclaimer": "AI-generated risk scores are decision-support signals based on statistical anomaly detection. They do not constitute proof of fraud or wrongdoing and must be verified by a human investigator."
    }


@router.get("/{work_id}/timeline")
def get_project_timeline(work_id: str, db: Session = Depends(get_db)):
    work = db.query(Work).filter(Work.work_id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Project not found")

    payments = db.query(SyntheticPayment).filter(SyntheticPayment.work_id == work_id).all()

    timeline_events = [
        {"event": "Work Recommended", "date": work.recommended_date, "data_source": "real_esakshi"},
        {"event": f"Sanction Approved (Lag: {work.sanction_delay_days:.0f} days)", "date": work.sanction_date, "data_source": "real_esakshi"}
    ]

    for p in payments:
        timeline_events.append({
            "event": f"Installment #{p.installment_number} Paid (₹ {p.amount_paid:,.0f})",
            "date": p.payment_date,
            "data_source": p.data_source
        })

    timeline_events.append({"event": f"Current Status: {work.work_status}", "date": "Current", "data_source": "real_esakshi"})
    return {"work_id": work_id, "timeline": timeline_events}


@router.post("/{work_id}/action")
def log_investigation_action(work_id: str, payload: ActionCreateSchema, db: Session = Depends(get_db)):
    work = db.query(Work).filter(Work.work_id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Project not found")

    action = InvestigationAction(
        work_id=work_id,
        user_role=payload.user_role,
        action_type=payload.action_type,
        note=payload.note
    )
    db.add(action)

    # Update status if applicable
    if payload.action_type in ["Under Review", "Escalated", "Dismissed"]:
        work.investigation_status = payload.action_type

    audit = AuditLog(
        user_role=payload.user_role,
        action=f"Investigator Action: {payload.action_type}",
        details=f"Project {work_id}: {payload.note or 'No notes attached'}"
    )
    db.add(audit)
    db.commit()

    return {"status": "success", "work_id": work_id, "new_investigation_status": work.investigation_status}
