from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Work(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True, index=True)
    work_id = Column(String(255), unique=True, index=True, nullable=False)
    work_category = Column(String(100), index=True)
    state = Column(String(100), index=True)
    district = Column(String(100), index=True)
    ida_name = Column(String(255), index=True)
    mp_name = Column(String(255), index=True)
    constituency = Column(String(255), index=True)
    work_description = Column(Text)
    recommended_date = Column(String(50))
    sanction_date = Column(String(50))
    sanction_amount = Column(Float, index=True)
    sanction_delay_days = Column(Float)
    work_status = Column(String(100), index=True)
    data_source = Column(String(50), default="real_esakshi")

    # Risk derived fields
    v1_anomaly_score = Column(Float, default=0.0)
    cost_anomaly_score = Column(Float, default=0.0)
    delay_anomaly_score = Column(Float, default=0.0)
    duplicate_score = Column(Float, default=0.0)
    fund_utilization_score = Column(Float, default=0.0)
    network_score = Column(Float, default=0.0)
    composite_risk_score = Column(Float, index=True, default=0.0)
    risk_level = Column(String(20), index=True, default="Low")
    risk_reasons = Column(Text)
    investigation_status = Column(String(50), default="Pending Review")

    # Relationships
    payments = relationship("SyntheticPayment", back_populates="work")
    documents = relationship("SyntheticDocument", back_populates="work")
    images = relationship("SyntheticImage", back_populates="work")
    actions = relationship("InvestigationAction", back_populates="work")


class MP(Base):
    __tablename__ = "mps"

    id = Column(Integer, primary_key=True, index=True)
    mp_name = Column(String(255), unique=True, index=True, nullable=False)
    mp_norm = Column(String(255), index=True)
    state = Column(String(100), index=True)
    constituency = Column(String(255))
    mp_type = Column(String(100))  # Elected / Nominated
    allocated_amount = Column(Float)
    total_sanctioned_amount = Column(Float)
    utilization_percentage = Column(Float)
    remaining_amount = Column(Float)
    number_of_works = Column(Integer)
    utilization_alert = Column(String(100))
    data_source = Column(String(50), default="real_esakshi")


class ImplementingAgency(Base):
    __tablename__ = "implementing_agencies"

    id = Column(Integer, primary_key=True, index=True)
    ida_name = Column(String(255), unique=True, index=True, nullable=False)
    district = Column(String(100), index=True)
    state = Column(String(100), index=True)
    total_works_count = Column(Integer)
    total_sanctioned_amount = Column(Float)
    network_centrality = Column(Float, default=0.0)
    concentration_zscore = Column(Float, default=0.0)
    data_source = Column(String(50), default="real_esakshi")


class SyntheticPayment(Base):
    __tablename__ = "synthetic_payments"

    id = Column(Integer, primary_key=True, index=True)
    work_id = Column(String(255), ForeignKey("works.work_id"), index=True)
    installment_number = Column(Integer)
    payment_date = Column(String(50))
    amount_paid = Column(Float)
    percentage_of_total = Column(Float)
    vendor_name = Column(String(255))
    is_anomaly = Column(Boolean, default=False)
    anomaly_type = Column(String(100))
    data_source = Column(String(50), default="synthetic_demo")

    work = relationship("Work", back_populates="payments")


class SyntheticDocument(Base):
    __tablename__ = "synthetic_documents"

    id = Column(Integer, primary_key=True, index=True)
    work_id = Column(String(255), ForeignKey("works.work_id"), index=True)
    document_type = Column(String(100))
    extracted_amount = Column(Float)
    database_amount = Column(Float)
    ocr_mismatch_detected = Column(Boolean, default=False)
    audit_note = Column(Text)
    data_source = Column(String(50), default="synthetic_demo")

    work = relationship("Work", back_populates="documents")


class SyntheticImage(Base):
    __tablename__ = "synthetic_images"

    id = Column(Integer, primary_key=True, index=True)
    work_id = Column(String(255), ForeignKey("works.work_id"), index=True)
    image_url = Column(String(255))
    stated_status = Column(String(100))
    cv_detected_progress_pct = Column(Float)
    visual_mismatch_detected = Column(Boolean, default=False)
    audit_note = Column(Text)
    data_source = Column(String(50), default="synthetic_demo")

    work = relationship("Work", back_populates="images")


class InvestigationAction(Base):
    __tablename__ = "investigation_actions"

    id = Column(Integer, primary_key=True, index=True)
    work_id = Column(String(255), ForeignKey("works.work_id"), index=True)
    user_role = Column(String(100))
    action_type = Column(String(100))  # Mark for Review, Escalate, Assign, Add Note, Dismiss
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    work = relationship("Work", back_populates="actions")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_role = Column(String(100))
    action = Column(String(255))
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    role = Column(String(100), index=True)  # district_authority, mospi_central, state_nodal, auditor, public_demo
    full_name = Column(String(255))
