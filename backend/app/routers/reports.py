import os
import io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Work, SyntheticPayment, SyntheticDocument, SyntheticImage

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/{work_id}/pdf")
def export_project_pdf_report(work_id: str, db: Session = Depends(get_db)):
    work = db.query(Work).filter(Work.work_id == work_id).first()
    if not work:
        raise HTTPException(status_code=404, detail="Project not found")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    story = []

    # Title
    title_style = ParagraphStyle(name='TitleStyle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#1E3A8A'))
    story.append(Paragraph("MPLADS AI AUDIT & INVESTIGATION REPORT", title_style))
    story.append(Spacer(1, 10))

    # Project Overview Table
    data = [
        ["Project Work Code:", work.work_id],
        ["State / District:", f"{work.state} / {work.district}"],
        ["Member of Parliament:", work.mp_name],
        ["Implementing Agency (IDA):", work.ida_name],
        ["Work Category:", work.work_category],
        ["Sanction Amount (INR):", f"₹ {work.sanction_amount:,.2f}"],
        ["Sanction Delay (Days):", f"{work.sanction_delay_days:.0f} days"],
        ["Work Status:", work.work_status],
        ["Composite Risk Score:", f"{work.composite_risk_score} / 100 ({work.risk_level})"],
        ["Data Source:", work.data_source]
    ]

    t = Table(data, colWidths=[180, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # Plain Language Risk Explanations
    story.append(Paragraph("DATA-BACKED RISK REASONS & AUDIT SIGNALS", styles['Heading2']))
    story.append(Spacer(1, 6))

    reasons = [r.strip() for r in (work.risk_reasons or "").split("|") if r.strip()]
    for r in reasons:
        story.append(Paragraph(f"• {r}", styles['Normal']))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 15))

    # Disclaimer
    disc_style = ParagraphStyle(name='DiscStyle', parent=styles['Italic'], fontSize=8, leading=10, textColor=colors.HexColor('#6B7280'))
    story.append(Paragraph("DISCLAIMER: AI-generated risk scores are decision-support signals based on statistical anomaly detection. They do not constitute proof of fraud or wrongdoing and must be verified by a human investigator.", disc_style))

    doc.build(story)
    buffer.seek(0)

    filename = f"audit_report_{work_id.replace('/', '_')}.pdf"
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
