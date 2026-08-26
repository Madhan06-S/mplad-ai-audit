import os
import tempfile
from fpdf import FPDF
from app.services.ml_service import MLService

class AuditPDFReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 15)
        self.set_text_color(40, 53, 147) # Indigo
        self.cell(0, 10, 'SIH26102 - MPLAD AI AUDIT REPORT', border=False, new_x="LMARGIN", new_y="NEXT", align='C')
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'Executive Anomaly & Risk Monitoring Summary', border=False, new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} | Confidential Govt Audit Report', align='C')

def generate_pdf_report(state_filter: str = None, risk_level_filter: str = None) -> str:
    ml_svc = MLService()
    res = ml_svc.get_projects(page=1, page_size=50, state=state_filter, risk_level=risk_level_filter, sort_by="risk_score")
    projects = res['data']
    overview = ml_svc.get_analytics_overview()

    pdf = AuditPDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # Executive Summary Box
    pdf.set_fill_color(240, 244, 248)
    pdf.rect(10, 30, 190, 35, 'F')
    
    pdf.set_y(32)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 6, f"Total Projects Analyzed: {overview.get('total_works', 0):,}  |  Anomalies: {overview.get('anomalies_count', 0):,} ({overview.get('anomalies_percentage', 0)}%)", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Total Sanctioned Amount: Rs. {overview.get('total_sanctioned_amount', 0):,.2f}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Duplicates Flagged: {overview.get('duplicates_flagged_count', 0):,}  |  Avg Delay: {overview.get('average_sanction_delay_days', 0):.1f} days", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    # Table Header
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(51, 65, 85)
    pdf.set_text_color(255, 255, 255)
    
    col_widths = [45, 35, 30, 25, 25, 30]
    headers = ["Work Code", "MP Name", "State", "Amount (Rs)", "Score", "Risk Level"]
    
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, border=1, fill=True, align='C')
    pdf.ln()

    # Table Data
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(30, 41, 59)
    
    fill = False
    for proj in projects[:30]: # Top 30 projects
        pdf.set_fill_color(248, 250, 252) if fill else pdf.set_fill_color(255, 255, 255)
        
        work_id = str(proj['work_id'])[:22]
        mp_name = str(proj['mp_name'])[:18]
        state = str(proj['state'])[:14]
        amt = f"{proj['sanction_amount']:,.0f}"
        score = f"{proj['risk_score']:.1f}"
        level = str(proj['risk_level'])

        pdf.cell(col_widths[0], 7, work_id, border=1, fill=fill)
        pdf.cell(col_widths[1], 7, mp_name, border=1, fill=fill)
        pdf.cell(col_widths[2], 7, state, border=1, fill=fill)
        pdf.cell(col_widths[3], 7, amt, border=1, fill=fill, align='R')
        pdf.cell(col_widths[4], 7, score, border=1, fill=fill, align='C')
        pdf.cell(col_widths[5], 7, level, border=1, fill=fill, align='C')
        pdf.ln()
        fill = not fill

    # Save PDF to temporary file
    temp_dir = tempfile.gettempdir()
    pdf_path = os.path.join(temp_dir, "mplad_audit_report.pdf")
    pdf.output(pdf_path)
    return pdf_path
