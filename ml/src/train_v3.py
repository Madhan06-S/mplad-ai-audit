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
from explainability import SHAPExplainer

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "Works Sanctioned (1).csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
PLOTS_DIR = os.path.join(OUTPUTS_DIR, "plots")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

def generate_v3_plots(explainer: SHAPExplainer, X_sample: np.ndarray, feat_names: list):
    print("[Visualization V3] Generating SHAP summary plots in:", PLOTS_DIR)
    plt.style.use('ggplot')
    
    # 1. SHAP Feature Importance Summary Bar Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    shap_vals = explainer.shap_values
    mean_abs_shap = np.mean(np.abs(shap_vals), axis=0)
    top_indices = np.argsort(mean_abs_shap)[::-1][:15]
    
    top_features = [feat_names[i] for i in top_indices]
    top_scores = mean_abs_shap[top_indices]
    
    ax.barh(top_features[::-1], top_scores[::-1], color='darkslateblue')
    ax.set_title("Top 15 Most Important Anomaly Features (Mean |SHAP Value|)")
    ax.set_xlabel("Mean Absolute SHAP Value")
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "09_shap_summary_bar.png"), dpi=300)
    plt.close(fig)
    print("[Visualization V3] SHAP summary plot saved successfully.")

def generate_v3_report(df_scored: pd.DataFrame, summary_metrics: dict):
    report_path = os.path.join(OUTPUTS_DIR, "ml_v3_report.md")
    
    top10 = df_scored.sort_values(by='risk_score', ascending=False).head(10)
    top10_rows = []
    for idx, row in top10.iterrows():
        top10_rows.append(
            f"| {row['work_id']} | {row['mp_name']} | ₹ {row['sanction_amount']:,.0f} | **{row['risk_score']}** | {row['risk_level']} | `{row['shap_top_attribution']}` |"
        )
    top10_str = "\n".join(top10_rows)

    content = f"""# ML V3 Explainable Risk Engine Report — MPLAD AI Audit (SIH26102)

## 1. Executive Overview
ML V3 equips the MPLAD AI Audit platform with **Game-Theoretic Model Explainability (SHAP)**. Auditors can inspect exact feature-level attributions answering **"WHY is this specific project flagged as high risk?"**.

---

## 2. ML V3 Execution Metrics Summary

| Metric | Value |
| :--- | :--- |
| **Dataset Processed** | `Works Sanctioned (1).csv` (33,000 ground-truth works) |
| **Model Architecture** | Isolation Forest + TF-IDF Duplicate Detector + Fund Utilization Tracker |
| **Explainability Engine** | `shap.TreeExplainer` game-theoretic feature attribution |
| **Total Flagged Anomalies** | **{summary_metrics['total_anomalies']:,}** |
| **Critical Risk (Score 85–100)** | {summary_metrics['risk_levels']['Critical']:,} |
| **High Risk (Score 70–84)** | {summary_metrics['risk_levels']['High']:,} |
| **Medium Risk (Score 40–69)** | {summary_metrics['risk_levels']['Medium']:,} |
| **Low Risk (Score 0–39)** | {summary_metrics['risk_levels']['Low']:,} |

---

## 3. Top 10 High-Risk Projects with SHAP Feature Attributions

| Work ID | MP Name | Amount | Risk Score | Risk Level | Primary SHAP Feature Attribution |
| :--- | :--- | :--- | :---: | :---: | :--- |
{top10_str}

---

## 4. Production Artifacts

- **V3 Model Pipeline Bundle**: `ml/models/mplad_anomaly_model_v3.pkl`
- **Full Scored Dataset with SHAP**: `ml/outputs/scored_projects_v3.csv`
- **High-Risk Projects Dataset**: `ml/outputs/high_risk_projects_v3.csv`
- **Summary Metrics JSON**: `ml/outputs/anomaly_summary_v3.json`
- **ML V3 Report**: `ml/outputs/ml_v3_report.md`
- **Plots**: `ml/outputs/plots/09_shap_summary_bar.png`
"""
    with open(report_path, "w") as f:
        f.write(content)
    print(f"[Report V3] Saved ML V3 Report to {report_path}")

def run_v3_pipeline():
    print("\n==================================================")
    print("STARTING ML V3 EXPLAINABLE RISK ENGINE PIPELINE")
    print("==================================================")
    
    # 1. Preprocess
    df_raw = load_and_clean_data(DATA_PATH)
    
    # 2. Duplicate detection
    dwd = DuplicateWorkDetector(similarity_threshold=0.75)
    df_dup = dwd.detect_duplicates(df_raw)
    
    # 3. Fund utilization
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
    
    # 6. SHAP Explainer Engine
    explainer = SHAPExplainer(model.model, fe.feature_names)
    shap_vals = explainer.compute_shap_values(X_matrix)
    
    # Extract top SHAP feature attribution per project
    top_shap_attrs = []
    for i in range(len(df_scored)):
        top_reasons = explainer.get_top_reasons_for_sample(i, top_k=1)
        if top_reasons:
            top_attr = f"{top_reasons[0]['feature']} ({top_reasons[0]['shap_value']})"
        else:
            top_attr = "Baseline"
        top_shap_attrs.append(top_attr)
        
    df_scored['shap_top_attribution'] = top_shap_attrs
    
    # 7. Save model pipeline bundle
    v3_bundle = {
        'duplicate_detector': dwd,
        'fund_tracker': fut,
        'feature_engineer': fe,
        'anomaly_model': model,
        'risk_engine_v2': re2,
        'explainer': explainer
    }
    model_save_path = os.path.join(MODELS_DIR, "mplad_anomaly_model_v3.pkl")
    joblib.dump(v3_bundle, model_save_path)
    print(f"[Model V3] Saved V3 pipeline bundle to {model_save_path}")
    
    # 8. Save output datasets
    output_cols = [
        'work_id', 'state', 'ida', 'mp_name', 'constituency', 'work_category',
        'work_description_clean', 'recommended_dt', 'sanction_dt', 'sanction_amount',
        'sanction_delay_days', 'duplicate_similarity_score', 'similar_work_id',
        'is_duplicate_flag', 'mp_allocated_limit', 'mp_total_sanctioned',
        'mp_utilization_pct', 'work_status', 'anomaly_label', 'anomaly_score',
        'risk_score', 'risk_level', 'shap_top_attribution', 'anomaly_reason'
    ]
    df_output = df_scored[output_cols].copy()
    
    scored_csv_path = os.path.join(OUTPUTS_DIR, "scored_projects_v3.csv")
    high_risk_csv_path = os.path.join(OUTPUTS_DIR, "high_risk_projects_v3.csv")
    
    df_output.to_csv(scored_csv_path, index=False)
    
    df_high_risk = df_output[df_output['risk_level'].isin(['Critical', 'High'])].sort_values(by='risk_score', ascending=False)
    df_high_risk.to_csv(high_risk_csv_path, index=False)
    
    print(f"[Output V3] Saved scored projects to {scored_csv_path}")
    print(f"[Output V3] Saved high-risk projects ({len(df_high_risk)} records) to {high_risk_csv_path}")

    # 9. Summary JSON & Plots
    total_records = int(len(df_output))
    total_anomalies = int((df_output['anomaly_label'] == -1).sum())
    risk_level_counts = df_output['risk_level'].value_counts().to_dict()
    for level in ['Low', 'Medium', 'High', 'Critical']:
        risk_level_counts.setdefault(level, 0)
        risk_level_counts[level] = int(risk_level_counts[level])
        
    summary_metrics = {
        'total_records': total_records,
        'total_anomalies': total_anomalies,
        'risk_levels': risk_level_counts,
        'top_high_risk_count': len(df_high_risk)
    }
    
    summary_json_path = os.path.join(OUTPUTS_DIR, "anomaly_summary_v3.json")
    with open(summary_json_path, "w") as f:
        json.dump(summary_metrics, f, indent=2)
    print(f"[Output V3] Saved summary metrics JSON to {summary_json_path}")
    
    generate_v3_plots(explainer, X_matrix, fe.feature_names)
    generate_v3_report(df_scored, summary_metrics)

    print("\n==================================================")
    print("ML V3 PIPELINE EXECUTED SUCCESSFULLY!")
    print("==================================================")
    print(f"Processed: {total_records} records with SHAP explainability")
    print(df_output[['work_id', 'mp_name', 'risk_score', 'risk_level', 'shap_top_attribution']].head())

if __name__ == "__main__":
    run_v3_pipeline()
