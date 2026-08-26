import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from preprocess import load_and_clean_data
from duplicate_detector import DuplicateWorkDetector
from fund_utilization import FundUtilizationTracker
from feature_engineering import FeatureEngineer
from anomaly_model import MPLADAnomalyDetector
from risk_engine_v2 import RiskEngineV2

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "Works Sanctioned (1).csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
PLOTS_DIR = os.path.join(OUTPUTS_DIR, "plots")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

def generate_v2_visualizations(df_scored: pd.DataFrame):
    print("[Visualization V2] Generating ML V2 plots in:", PLOTS_DIR)
    plt.style.use('ggplot')
    
    # 1. Composite Risk Distribution V2
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df_scored['risk_score'], kde=True, ax=ax, color='crimson', bins=50)
    ax.set_title("ML V2 Multi-Factor Composite Risk Score Distribution (0-100)")
    ax.set_xlabel("Composite Risk Score")
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "06_composite_risk_distribution_v2.png"), dpi=300)
    plt.close(fig)

    # 2. Duplicate Text Similarity Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    dup_sims = df_scored[df_scored['duplicate_similarity_score'] > 0.1]['duplicate_similarity_score'] * 100.0
    sns.histplot(dup_sims, kde=True, ax=ax, color='darkorange', bins=40)
    ax.set_title("Duplicate Work Description Cosine Similarity Distribution (%)")
    ax.set_xlabel("TF-IDF Cosine Similarity (%)")
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "07_duplicate_similarity_distribution.png"), dpi=300)
    plt.close(fig)

    # 3. MP Fund Utilization Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df_scored['mp_utilization_pct'], kde=True, ax=ax, color='seagreen', bins=40)
    ax.set_title("MP Fund Utilization Percentage Distribution (%)")
    ax.set_xlabel("MP Utilization (%)")
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "08_mp_fund_utilization_distribution.png"), dpi=300)
    plt.close(fig)
    print("[Visualization V2] Plots successfully saved.")

def generate_v2_report(df_scored: pd.DataFrame, summary_metrics: dict):
    report_path = os.path.join(OUTPUTS_DIR, "ml_v2_report.md")
    
    top20 = df_scored.sort_values(by='risk_score', ascending=False).head(20)
    
    top20_rows = []
    for idx, row in top20.iterrows():
        sim_str = f"{row['duplicate_similarity_score']*100:.1f}%" if row['duplicate_similarity_score'] > 0 else "None"
        util_str = f"{row['mp_utilization_pct']:.1f}%"
        top20_rows.append(
            f"| {row['work_id']} | {row['mp_name']} | {row['state']} | ₹ {row['sanction_amount']:,.0f} | {sim_str} | {util_str} | **{row['risk_score']}** | {row['risk_level']} |"
        )
    top20_str = "\n".join(top20_rows)

    content = f"""# ML V2 Multi-Factor Risk Engine Report — MPLAD AI Audit (SIH26102)

## 1. Executive Summary
ML V2 expands the ML V1 Isolation Forest baseline into a **Multi-Factor Composite Risk Engine**. It integrates:
1. **Isolation Forest Cost & Delay Anomaly Detection**
2. **NLP Duplicate Work & Split-Billing Text Detection (TF-IDF + Cosine Similarity)**
3. **MP Fund Utilization Tracking (Spending vs Entitlement Limits)**
4. **Category Risk Weighting**

---

## 2. ML V2 Execution Metrics Summary

| Metric | Value |
| :--- | :--- |
| **Dataset Processed** | `Works Sanctioned (1).csv` (33,000 ground-truth works) |
| **Potential Duplicate / Split Works Flagged (Sim ≥ 75%)** | **{summary_metrics['total_duplicates']:,}** |
| **High Risk / Critical Risk Works (Score ≥ 70)** | **{summary_metrics['risk_levels']['Critical'] + summary_metrics['risk_levels']['High']:,}** |
| **Critical Risk (Score 85–100)** | {summary_metrics['risk_levels']['Critical']:,} |
| **High Risk (Score 70–84)** | {summary_metrics['risk_levels']['High']:,} |
| **Medium Risk (Score 40–69)** | {summary_metrics['risk_levels']['Medium']:,} |
| **Low Risk (Score 0–39)** | {summary_metrics['risk_levels']['Low']:,} |

---

## 3. Top 20 Highest Multi-Factor Risk Projects

| Work ID | MP Name | State | Sanction Amount | Dup Sim % | MP Util % | Risk Score | Risk Level |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
{top20_str}

---

## 4. Output Artifacts

- **Model Pipeline Bundle**: `ml/models/mplad_anomaly_model_v2.pkl`
- **Full Scored Dataset**: `ml/outputs/scored_projects_v2.csv`
- **High-Risk Filtered Dataset**: `ml/outputs/high_risk_projects_v2.csv`
- **Summary Metrics JSON**: `ml/outputs/anomaly_summary_v2.json`
- **ML V2 Report**: `ml/outputs/ml_v2_report.md`
- **Plots**: `ml/outputs/plots/`
"""
    with open(report_path, "w") as f:
        f.write(content)
    print(f"[Report V2] Saved ML V2 Report to {report_path}")

def run_v2_pipeline():
    print("\n==================================================")
    print("STARTING ML V2 TRAINING & MULTI-FACTOR INFERENCE PIPELINE")
    print("==================================================")
    
    # 1. Preprocess
    df_raw = load_and_clean_data(DATA_PATH)
    
    # 2. Duplicate detection
    dwd = DuplicateWorkDetector(similarity_threshold=0.75)
    df_dup = dwd.detect_duplicates(df_raw)
    
    # 3. Fund utilization tracking
    fut = FundUtilizationTracker()
    df_util = fut.calculate_utilization(df_dup)
    
    # 4. Feature engineering & Isolation Forest
    fe = FeatureEngineer()
    df_features, X_matrix = fe.fit_transform(df_util)
    
    model = MPLADAnomalyDetector(contamination=0.05, random_state=42)
    model.fit(X_matrix)
    labels, raw_scores = model.predict(X_matrix)
    
    # 5. Composite Risk Engine V2
    re2 = RiskEngineV2()
    df_scored = re2.process_dataset(df_features, raw_scores, labels)
    
    # 6. Save model pipeline bundle
    v2_bundle = {
        'duplicate_detector': dwd,
        'fund_tracker': fut,
        'feature_engineer': fe,
        'anomaly_model': model,
        'risk_engine_v2': re2
    }
    model_save_path = os.path.join(MODELS_DIR, "mplad_anomaly_model_v2.pkl")
    joblib.dump(v2_bundle, model_save_path)
    print(f"[Model V2] Saved V2 pipeline bundle to {model_save_path}")
    
    # 7. Save outputs
    output_cols = [
        'work_id', 'state', 'ida', 'mp_name', 'constituency', 'work_category',
        'work_description_clean', 'recommended_dt', 'sanction_dt', 'sanction_amount',
        'sanction_delay_days', 'duplicate_similarity_score', 'similar_work_id',
        'is_duplicate_flag', 'mp_allocated_limit', 'mp_total_sanctioned',
        'mp_utilization_pct', 'work_status', 'anomaly_label', 'anomaly_score',
        'risk_score', 'risk_level', 'anomaly_reason'
    ]
    df_output = df_scored[output_cols].copy()
    
    scored_csv_path = os.path.join(OUTPUTS_DIR, "scored_projects_v2.csv")
    high_risk_csv_path = os.path.join(OUTPUTS_DIR, "high_risk_projects_v2.csv")
    
    df_output.to_csv(scored_csv_path, index=False)
    
    df_high_risk = df_output[df_output['risk_level'].isin(['Critical', 'High'])].sort_values(by='risk_score', ascending=False)
    df_high_risk.to_csv(high_risk_csv_path, index=False)
    
    print(f"[Output V2] Saved scored projects to {scored_csv_path}")
    print(f"[Output V2] Saved high-risk projects ({len(df_high_risk)} records) to {high_risk_csv_path}")

    # 8. Summary JSON
    total_records = int(len(df_output))
    total_duplicates = int(df_output['is_duplicate_flag'].sum())
    risk_level_counts = df_output['risk_level'].value_counts().to_dict()
    for level in ['Low', 'Medium', 'High', 'Critical']:
        risk_level_counts.setdefault(level, 0)
        risk_level_counts[level] = int(risk_level_counts[level])
        
    summary_metrics = {
        'total_records': total_records,
        'total_duplicates': total_duplicates,
        'risk_levels': risk_level_counts,
        'top_high_risk_count': len(df_high_risk)
    }
    
    summary_json_path = os.path.join(OUTPUTS_DIR, "anomaly_summary_v2.json")
    with open(summary_json_path, "w") as f:
        json.dump(summary_metrics, f, indent=2)
    print(f"[Output V2] Saved summary metrics JSON to {summary_json_path}")
    
    generate_v2_visualizations(df_scored)
    generate_v2_report(df_scored, summary_metrics)

    print("\n==================================================")
    print("ML V2 PIPELINE EXECUTED SUCCESSFULLY!")
    print("==================================================")
    print(f"Processed: {total_records} records")
    print(f"Duplicates Flagged: {total_duplicates}")
    print("Top 5 Highest Risk Projects V2:")
    print(df_output[['work_id', 'mp_name', 'sanction_amount', 'duplicate_similarity_score', 'risk_score', 'risk_level']].head())

if __name__ == "__main__":
    run_v2_pipeline()
