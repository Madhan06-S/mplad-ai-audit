from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class WorkSchema(BaseModel):
    id: int
    work_id: str
    work_category: Optional[str]
    state: Optional[str]
    district: Optional[str]
    ida_name: Optional[str]
    mp_name: Optional[str]
    constituency: Optional[str]
    work_description: Optional[str]
    recommended_date: Optional[str]
    sanction_date: Optional[str]
    sanction_amount: float
    sanction_delay_days: float
    work_status: Optional[str]
    data_source: str
    v1_anomaly_score: float
    cost_anomaly_score: float
    delay_anomaly_score: float
    duplicate_score: float
    fund_utilization_score: float
    network_score: float
    composite_risk_score: float
    risk_level: str
    risk_reasons: Optional[str]
    investigation_status: str

    class Config:
        from_attributes = True

class MPSchema(BaseModel):
    id: int
    mp_name: str
    state: str
    constituency: Optional[str]
    mp_type: Optional[str]
    allocated_amount: float
    total_sanctioned_amount: float
    utilization_percentage: float
    remaining_amount: float
    number_of_works: int
    utilization_alert: str
    data_source: str

    class Config:
        from_attributes = True

class AgencySchema(BaseModel):
    id: int
    ida_name: str
    district: str
    state: str
    total_works_count: int
    total_sanctioned_amount: float
    data_source: str

    class Config:
        from_attributes = True

class KpiSchema(BaseModel):
    total_works: int
    total_sanctioned_amount: float
    completed_works_pct: float
    delayed_works_pct: float
    critical_risk_count: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    works_requiring_investigation: int

class ActionCreateSchema(BaseModel):
    user_role: str
    action_type: str
    note: Optional[str] = None
