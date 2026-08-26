import os
import sys
import pytest
import pandas as pd
import numpy as np

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from geographic_intelligence import GeographicIntelligenceEngine
from agency_network import AgencyNetworkEngine
from payment_anomaly import PaymentAnomalyEngine
from image_intelligence import ImageIntelligenceEngine
from document_intelligence import DocumentIntelligenceEngine
from unified_risk_engine import UnifiedRiskEngine
from explainability import ExplainabilityEngine

@pytest.fixture
def sample_projects():
    return pd.DataFrame([
        {
            'work_id': 'PROJ_001', 'state': 'Karnataka', 'constituency': 'Dharwad',
            'ida': 'DEPUTY COMMISSIONER DHARWAR_IDA', 'mp_name': 'Pralhad Venkatesh Joshi',
            'work_category': 'Normal/Others', 'sanction_amount': 500000.0,
            'sanction_delay_days': 120, 'sanction_dt': '2024-07-09',
            'work_status': 'Physical Inspection', 'composite_risk_score': 75.0,
            'risk_level': 'High', 'v1_anomaly_score': 70.0, 'cost_anomaly_score': 75.0,
            'delay_anomaly_score': 45.0, 'duplicate_score': 0.0, 'fund_utilization_score': 20.0
        },
        {
            'work_id': 'PROJ_002', 'state': 'Karnataka', 'constituency': 'Dharwad',
            'ida': 'DEPUTY COMMISSIONER DHARWAR_IDA', 'mp_name': 'Pralhad Venkatesh Joshi',
            'work_category': 'Trust and Society', 'sanction_amount': 5000000.0,
            'sanction_delay_days': 400, 'sanction_dt': '2024-07-15',
            'work_status': 'Sanction', 'composite_risk_score': 90.0,
            'risk_level': 'Critical', 'v1_anomaly_score': 85.0, 'cost_anomaly_score': 100.0,
            'delay_anomaly_score': 100.0, 'duplicate_score': 85.0, 'fund_utilization_score': 50.0
        }
    ])

def test_geographic_intelligence_scores(sample_projects):
    geo_engine = GeographicIntelligenceEngine()
    ida_df, geo_scores, summary = geo_engine.process_geographic_risk(sample_projects)
    assert len(ida_df) == 1
    assert 'PROJ_001' in geo_scores
    assert 0.0 <= geo_scores['PROJ_001'] <= 100.0

def test_agency_network_graph(sample_projects):
    agency_engine = AgencyNetworkEngine()
    df_nodes, df_edges, df_agency_risk, agency_scores = agency_engine.build_network_graph(sample_projects)
    assert len(df_nodes) > 0
    assert len(df_edges) > 0
    assert 'PROJ_001' in agency_scores
    assert 0.0 <= agency_scores['PROJ_001'] <= 100.0

def test_payment_anomaly_detection(tmp_path, sample_projects):
    pay_engine = PaymentAnomalyEngine()
    demo_csv = os.path.join(tmp_path, "test_payments.csv")
    df_payments = pay_engine.generate_demo_payments(sample_projects, demo_csv)
    df_scored, payment_scores = pay_engine.detect_payment_anomalies(df_payments)
    assert len(df_payments) > 0
    assert 'PROJ_001' in payment_scores

def test_image_intelligence_mismatch(sample_projects):
    img_engine = ImageIntelligenceEngine()
    df_eval, image_scores = img_engine.evaluate_project_images(sample_projects)
    assert len(df_eval) == 2
    assert 'PROJ_001' in image_scores
    assert df_eval.iloc[0]['data_source'] == "DEMO / SIMULATED EVIDENCE"

def test_document_intelligence_ocr(sample_projects):
    doc_engine = DocumentIntelligenceEngine()
    mock_text_ok = "Sanction Order for PROJ_001 Amount INR 500,000.00 Date 2024-07-09"
    res_ok = doc_engine.verify_document_text(mock_text_ok, sample_projects.iloc[0])
    assert res_ok['verification_status'] == "VERIFIED MATCH"
    assert res_ok['document_mismatch_score'] == 0.0

    mock_text_err = "Sanction Order for PROJ_001 Amount INR 650,000.00 Date 2024-07-09"
    res_err = doc_engine.verify_document_text(mock_text_err, sample_projects.iloc[0])
    assert res_err['verification_status'] == "DOCUMENT MISMATCH DETECTED"
    assert res_err['document_mismatch_score'] == 80.0

def test_unified_risk_engine(sample_projects):
    ure = UnifiedRiskEngine()
    geo_scores = {'PROJ_001': 50.0, 'PROJ_002': 80.0}
    agency_scores = {'PROJ_001': 30.0, 'PROJ_002': 75.0}
    
    df_out = ure.process_unified_risk(sample_projects, geo_scores, agency_scores)
    assert 'real_composite_risk_score' in df_out.columns
    assert (df_out['real_composite_risk_score'] >= 0.0).all()
    assert (df_out['real_composite_risk_score'] <= 100.0).all()

def test_explainability_payload(sample_projects):
    ee = ExplainabilityEngine()
    exp = ee.explain_project_risk(sample_projects.iloc[0])
    assert exp['work_id'] == 'PROJ_001'
    assert 'feature_contributions' in exp
    assert exp['audit_disclaimer'] is not None
