import os
import sys
import pandas as pd
import numpy as np

# Add backend and ml to path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))
sys.path.insert(0, os.path.join(BASE_DIR, "backend", "app"))
sys.path.insert(0, os.path.join(BASE_DIR, "ml"))
sys.path.insert(0, os.path.join(BASE_DIR, "ml", "src"))

from database import engine, SessionLocal, Base
from models import Work, MP, ImplementingAgency, SyntheticPayment, SyntheticDocument, SyntheticImage, AuditLog, User
from preprocess import load_and_clean_data
from feature_engineering import FeatureEngineer
from anomaly_model import MPLADAnomalyDetector
from duplicate_detection import DuplicateDetector
from fund_utilization import FundUtilizationTracker
from composite_risk import CompositeRiskEngine
from anomaly.network import AgencyNetworkDetector
from data.synthetic.generate import generate_synthetic_data

def run_full_ingestion():
    print("\n==================================================")
    print("STARTING FULL ESAKSHI DATA INGESTION & PIPELINE SEEDING")
    print("==================================================")
    
    # 1. Reset and create database schema
    print("[Ingestion] Dropping and creating database schema in mplad_audit.db...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()

    # 2. Paths
    works_path = os.path.join(BASE_DIR, "ml", "data", "Works Sanctioned (1).csv")
    al1_path = os.path.join(BASE_DIR, "ml", "data", "Allocated Limit for Honble MPs.csv")
    al2_path = os.path.join(BASE_DIR, "ml", "data", "Allocated Limit for Honble MPs (1).csv")

    # 3. Clean dataset loading
    df_raw = load_and_clean_data(works_path)
    
    # 4. ML V1 Feature Engineering & Anomaly Detection
    fe = FeatureEngineer()
    df_features, X_matrix = fe.fit_transform(df_raw)
    
    anomaly_model = MPLADAnomalyDetector(contamination=0.05, random_state=42)
    anomaly_model.fit(X_matrix)
    labels, raw_scores = anomaly_model.predict(X_matrix)
    
    # Add V1 scores
    from risk_engine import RiskEngine
    df_v1 = RiskEngine().process_dataset(df_features, raw_scores, labels)

    # 5. ML V2 Duplicate Work Detection
    dup_detector = DuplicateDetector(similarity_threshold=0.85)
    df_dup_pairs, dup_sim_dict, similar_work_dict = dup_detector.find_duplicates(df_v1)

    # 6. MP Fund Utilization Monitoring
    fund_tracker = FundUtilizationTracker()
    df_mp_util, mp_util_scores = fund_tracker.process_fund_utilization(df_v1, al1_path, al2_path)

    # 7. Agency Network Graph Analysis
    network_detector = AgencyNetworkDetector()
    network_scores, graph_data = network_detector.build_and_analyze_network(df_v1)
    df_v1['network_score'] = df_v1['work_id'].map(network_scores).fillna(15.0)

    # 8. Composite Risk Engine Aggregation
    risk_engine_v2 = CompositeRiskEngine()
    df_scored = risk_engine_v2.process_composite_risk(df_v1, dup_sim_dict, similar_work_dict, mp_util_scores)

    # 9. Synthetic Data Generation
    payments, documents, images, geo_locations = generate_synthetic_data(df_scored, seed=42)

    # 10. Seed Work Records into DB
    print(f"[Ingestion] Inserting {len(df_scored)} work records into SQLite DB...")
    work_objects = []
    for idx, row in df_scored.iterrows():
        wid = row['work_id']
        ida_name = row['ida']
        dist_name = ida_name.split('(')[0].strip() if '(' in ida_name else ida_name

        w_obj = Work(
            work_id=wid,
            work_category=row['work_category'],
            state=row['state'],
            district=dist_name,
            ida_name=ida_name,
            mp_name=row['mp_name'],
            constituency=row['constituency'],
            work_description=row['work_description_clean'],
            recommended_date=str(row['recommended_dt'])[:10],
            sanction_date=str(row['sanction_dt'])[:10],
            sanction_amount=float(row['sanction_amount']),
            sanction_delay_days=float(row['sanction_delay_days']),
            work_status=row['work_status'],
            data_source="real_esakshi",
            v1_anomaly_score=float(row['v1_anomaly_score']),
            cost_anomaly_score=float(row['cost_anomaly_score']),
            delay_anomaly_score=float(row['delay_anomaly_score']),
            duplicate_score=float(row['duplicate_score']),
            fund_utilization_score=float(row['fund_utilization_score']),
            network_score=float(row['network_score']),
            composite_risk_score=float(row['composite_risk_score']),
            risk_level=row['risk_level'],
            risk_reasons=row['risk_reasons'],
            investigation_status="Pending Review" if row['risk_level'] in ['Critical', 'High'] else "Normal"
        )
        work_objects.append(w_obj)

    # Bulk insert in chunks of 5000
    chunk_size = 5000
    for i in range(0, len(work_objects), chunk_size):
        db.bulk_save_objects(work_objects[i:i+chunk_size])
        db.commit()
    print(f"[Ingestion] Successfully inserted {len(work_objects)} works.")

    # 11. Seed MP Records
    print(f"[Ingestion] Inserting {len(df_mp_util)} MP allocation records into DB...")
    mp_objects = []
    for idx, r in df_mp_util.iterrows():
        m_obj = MP(
            mp_name=r['mp_name_works'],
            mp_norm=r['mp_norm'],
            state=r['state'],
            constituency=r.get('constituency', ''),
            mp_type="Elected MP",
            allocated_amount=float(r['allocated_amount']),
            total_sanctioned_amount=float(r['total_sanctioned_amount']),
            utilization_percentage=float(r['utilization_percentage']),
            remaining_amount=float(r['remaining_amount']),
            number_of_works=int(r['number_of_works']),
            utilization_alert=r['utilization_alert'],
            data_source="real_esakshi"
        )
        mp_objects.append(m_obj)
    db.bulk_save_objects(mp_objects)
    db.commit()

    # 12. Seed Implementing Agencies
    print("[Ingestion] Inserting Implementing Agency records into DB...")
    agency_counts = df_scored.groupby('ida').agg(
        state=('state', 'first'),
        total_works=('sanction_amount', 'count'),
        total_amount=('sanction_amount', 'sum')
    ).reset_index()

    agency_objects = []
    for idx, r in agency_counts.iterrows():
        dist = r['ida'].split('(')[0].strip() if '(' in r['ida'] else r['ida']
        a_obj = ImplementingAgency(
            ida_name=r['ida'],
            district=dist,
            state=r['state'],
            total_works_count=int(r['total_works']),
            total_sanctioned_amount=float(r['total_amount']),
            network_centrality=0.0,
            concentration_zscore=0.0,
            data_source="real_esakshi"
        )
        agency_objects.append(a_obj)
    db.bulk_save_objects(agency_objects)
    db.commit()

    # 13. Seed Synthetic Payments, Documents, Images
    print("[Ingestion] Inserting synthetic payments, documents, and images...")
    pay_objects = [SyntheticPayment(**p) for p in payments]
    doc_objects = [SyntheticDocument(**d) for d in documents]
    img_objects = [SyntheticImage(**i) for i in images]

    db.bulk_save_objects(pay_objects)
    db.bulk_save_objects(doc_objects)
    db.bulk_save_objects(img_objects)
    db.commit()

    # 14. Seed Demo Users for Role-Based Access
    print("[Ingestion] Seeding demo users for 5 system roles...")
    demo_users = [
        User(username="district_authority", role="District Authority", full_name="District Collector / Magistrate"),
        User(username="mospi_central", role="MoSPI Central Nodal", full_name="Ministry Central Audit Officer"),
        User(username="state_nodal", role="State Nodal Officer", full_name="State Nodal Planning Authority"),
        User(username="auditor", role="Auditor (CAG/Independent)", full_name="Senior Independent Auditor"),
        User(username="public_demo", role="Public Demo", full_name="Public Observer (Read Only)")
    ]
    db.bulk_save_objects(demo_users)
    db.commit()

    # Initial Audit Log Entry
    audit_entry = AuditLog(
        user_role="System",
        action="Database Ingestion & Pipeline Pipeline Seeding",
        details=f"Loaded 33,000 real works, 489 MPs, {len(payments)} synthetic payments into Database."
    )
    db.add(audit_entry)
    db.commit()

    db.close()
    print("\n==================================================")
    print("DATABASE INGESTION & PIPELINE SEEDING COMPLETED!")
    print("==================================================")

if __name__ == "__main__":
    run_full_ingestion()
