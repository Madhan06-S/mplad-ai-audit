import os
import sys
import json
import numpy as np
import pandas as pd

from preprocess import load_and_clean_data
from feature_engineering import FeatureEngineer
from anomaly_model import MPLADAnomalyDetector
from risk_engine import RiskEngine
from duplicate_detection import DuplicateDetector
from fund_utilization import FundUtilizationTracker
from composite_risk import CompositeRiskEngine
from geographic_intelligence import GeographicIntelligenceEngine
from agency_network import AgencyNetworkEngine
from payment_anomaly import PaymentAnomalyEngine
from image_intelligence import ImageIntelligenceEngine
from document_intelligence import DocumentIntelligenceEngine
from unified_risk_engine import UnifiedRiskEngine
from explainability import ExplainabilityEngine

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "Works Sanctioned (1).csv")
AL1_PATH = os.path.join(BASE_DIR, "data", "Allocated Limit for Honble MPs.csv")
AL2_PATH = os.path.join(BASE_DIR, "data", "Allocated Limit for Honble MPs (1).csv")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
DEMO_DIR = os.path.join(BASE_DIR, "data", "demo")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(DEMO_DIR, exist_ok=True)

def run_v3_pipeline():
    print("\n==================================================")
    print("STARTING COMPLETE ML V3 & UNIFIED RISK PIPELINE")
    print("==================================================")

    # 1. Run / Load V2 base
    v2_csv_path = os.path.join(OUTPUTS_DIR, "v2_scored_projects.csv")
    if os.path.exists(v2_csv_path):
        df_v2 = pd.read_csv(v2_csv_path)
    else:
        from train_v2 import run_v2_pipeline
        run_v2_pipeline()
        df_v2 = pd.read_csv(v2_csv_path)

    df_v2['sanction_dt'] = pd.to_datetime(df_v2['sanction_dt'], errors='coerce')

    # 2. Phase B: Geographic Intelligence
    geo_engine = GeographicIntelligenceEngine()
    ida_geo_df, geo_scores, geo_summary = geo_engine.process_geographic_risk(df_v2)
    
    ida_geo_csv = os.path.join(OUTPUTS_DIR, "geographic_intelligence.csv")
    geo_json_path = os.path.join(OUTPUTS_DIR, "geographic_summary.json")
    ida_geo_df.to_csv(ida_geo_csv, index=False)
    with open(geo_json_path, "w") as f:
        json.dump(geo_summary, f, indent=2)
    print(f"[V3 Pipeline] Saved Geographic Intelligence outputs to {ida_geo_csv}")

    # 3. Phase C: Agency Network Intelligence
    agency_engine = AgencyNetworkEngine()
    df_nodes, df_edges, df_agency_risk, agency_scores = agency_engine.build_network_graph(df_v2)
    
    nodes_csv = os.path.join(OUTPUTS_DIR, "agency_nodes.csv")
    edges_csv = os.path.join(OUTPUTS_DIR, "agency_edges.csv")
    risk_csv = os.path.join(OUTPUTS_DIR, "agency_risk.csv")
    df_nodes.to_csv(nodes_csv, index=False)
    df_edges.to_csv(edges_csv, index=False)
    df_agency_risk.to_csv(risk_csv, index=False)
    print(f"[V3 Pipeline] Saved Agency Network Graph outputs ({len(df_nodes)} nodes, {len(df_edges)} edges)")

    # 4. Phase D: Payment Anomaly Demo
    pay_engine = PaymentAnomalyEngine()
    demo_pay_csv = os.path.join(DEMO_DIR, "payments_demo.csv")
    df_payments = pay_engine.generate_demo_payments(df_v2, demo_pay_csv)
    df_scored_pay, payment_scores = pay_engine.detect_payment_anomalies(df_payments)
    
    scored_pay_csv = os.path.join(OUTPUTS_DIR, "payments_demo_scored.csv")
    df_scored_pay.to_csv(scored_pay_csv, index=False)

    # 5. Phase E: Image Intelligence Demo
    img_engine = ImageIntelligenceEngine()
    df_img_eval, image_scores = img_engine.evaluate_project_images(df_v2)
    img_csv = os.path.join(OUTPUTS_DIR, "image_intelligence_demo.csv")
    df_img_eval.to_csv(img_csv, index=False)

    # 6. Phase F: Document Intelligence OCR
    doc_engine = DocumentIntelligenceEngine()
    df_doc_eval, doc_scores = doc_engine.evaluate_batch_documents(df_v2)
    doc_csv = os.path.join(OUTPUTS_DIR, "document_intelligence_demo.csv")
    df_doc_eval.to_csv(doc_csv, index=False)

    # 7. Phase H: Unified Risk Engine
    unified_engine = UnifiedRiskEngine()
    df_v3_scored = unified_engine.process_unified_risk(
        df_v2, geo_scores, agency_scores,
        payment_scores=payment_scores, image_scores=image_scores, doc_scores=doc_scores,
        demo_mode=False
    )

    # 8. Phase I: Explainability Payload Generation
    explain_engine = ExplainabilityEngine()
    explanations = []
    for idx, r in df_v3_scored.iterrows():
        exp = explain_engine.explain_project_risk(r)
        explanations.append(exp['summary_explanation'])
    df_v3_scored['unified_explanation'] = explanations

    # Save V3 outputs
    v3_scored_csv = os.path.join(OUTPUTS_DIR, "v3_scored_projects.csv")
    v3_high_risk_csv = os.path.join(OUTPUTS_DIR, "v3_high_risk_projects.csv")
    
    df_v3_scored.to_csv(v3_scored_csv, index=False)
    
    df_v3_high = df_v3_scored[df_v3_scored['risk_level'].isin(['Critical', 'High'])].sort_values(by='real_composite_risk_score', ascending=False)
    df_v3_high.to_csv(v3_high_risk_csv, index=False)

    print(f"[V3 Pipeline] Saved V3 Scored Projects to {v3_scored_csv}")
    print(f"[V3 Pipeline] Saved V3 High-Risk Projects ({len(df_v3_high)} records) to {v3_high_risk_csv}")

    print("\n==================================================")
    print("COMPLETE ML V3 PIPELINE EXECUTED SUCCESSFULLY!")
    print("==================================================")
    print(f"Total Projects Scored: {len(df_v3_scored)}")
    print(f"Critical/High Risk Flagged Projects: {len(df_v3_high)}")
    print("Top 5 Highest Unified Risk Projects:")
    print(df_v3_scored[['work_id', 'state', 'sanction_amount', 'real_composite_risk_score', 'risk_level']].head())

if __name__ == "__main__":
    run_v3_pipeline()
