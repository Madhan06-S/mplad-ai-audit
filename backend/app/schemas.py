from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ProjectSchema(BaseModel):
    work_id: str
    state: str
    ida: str
    mp_name: str
    constituency: str
    work_category: str
    work_description_clean: str
    recommended_dt: Optional[str] = None
    sanction_dt: Optional[str] = None
    sanction_amount: float
    sanction_delay_days: float
    duplicate_similarity_score: float = 0.0
    similar_work_id: Optional[str] = None
    is_duplicate_flag: bool = False
    mp_allocated_limit: float = 0.0
    mp_total_sanctioned: float = 0.0
    mp_utilization_pct: float = 0.0
    work_status: str
    anomaly_label: int
    anomaly_score: float
    risk_score: float
    risk_level: str
    shap_top_attribution: str
    anomaly_reason: str

class PaginatedProjectsResponse(BaseModel):
    total_records: int
    page: int
    page_size: int
    total_pages: int
    data: List[ProjectSchema]

class AnalyticsOverviewSchema(BaseModel):
    total_works: int
    total_sanctioned_amount: float
    average_sanction_amount: float
    average_sanction_delay_days: float
    anomalies_count: int
    anomalies_percentage: float
    duplicates_flagged_count: int
    risk_level_counts: Dict[str, int]
    top_anomalous_states: List[Dict[str, Any]]
    category_risk_breakdown: List[Dict[str, Any]]

class PDFReportRequest(BaseModel):
    state_filter: Optional[str] = None
    risk_level_filter: Optional[str] = None
