import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from preprocess import load_and_clean_data
from feature_engineering import FeatureEngineer
from anomaly_model import MPLADAnomalyDetector
from risk_engine import RiskEngine

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "Works Sanctioned (1).csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
PLOTS_DIR = os.path.join(OUTPUTS_DIR, "plots")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

def generate_visualizations(df_scored: pd.DataFrame):
    """
    Generates required visualization plots for ML V1 pipeline.
    """
    print("[Visualization] Generating plots in:", PLOTS_DIR)
    plt.style.use('ggplot')
    
    # 1. Sanction Amount Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df_scored['sanction_amount'], kde=True, ax=ax, color='skyblue', bins=50)
    ax.set_title("Sanction Amount Distribution (INR)")
    ax.set_xlabel("Sanction Amount (INR)")
    ax.set_yscale('log')
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "01_sanction_amount_distribution.png"), dpi=300)
    plt.close(fig)

    # 2. Sanction Delay Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df_scored['sanction_delay_days'], kde=True, ax=ax, color='coral', bins=50)
    ax.set_title("Sanction Delay Distribution (Days)")
    ax.set_xlabel("Sanction Delay (Days)")
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "02_sanction_delay_distribution.png"), dpi=300)
    plt.close(fig)

    # 3. Risk Score Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df_scored['risk_score'], kde=True, ax=ax, color='purple', bins=50)
    ax.set_title("Risk Score Distribution (0-100 Index)")
    ax.set_xlabel("Risk Score")
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "03_risk_score_distribution.png"), dpi=300)
    plt.close(fig)

    # 4. Risk by State (Top 15 States by mean risk score)
    state_risk = df_scored.groupby('state')['risk_score'].mean().sort_values(ascending=False).head(15)
    fig, ax = plt.subplots(figsize=(10, 6))
    state_risk.plot(kind='barh', ax=ax, color='teal')
    ax.set_title("Top 15 States by Average Project Risk Score")
    ax.set_xlabel("Average Risk Score")
    ax.invert_yaxis()
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "04_risk_by_state.png"), dpi=300)
    plt.close(fig)

    # 5. Risk by Work Category
    cat_risk = df_scored.groupby('work_category')['risk_score'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    cat_risk.plot(kind='bar', ax=ax, color='crimson')
    ax.set_title("Average Risk Score by Work Category")
    ax.set_ylabel("Average Risk Score")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "05_risk_by_work_category.png"), dpi=300)
    plt.close(fig)
    print("[Visualization] 5 plots successfully saved.")

def generate_report(df_scored: pd.DataFrame, summary_metrics: dict):
    """
    Generates comprehensive ml_v1_report.md
    """
    report_path = os.path.join(OUTPUTS_DIR, "ml_v1_report.md")
    
    top20 = df_scored.sort_values(by='risk_score', ascending=False).head(20)
    
    top20_table_rows = []
    for idx, row in top20.iterrows():
        top20_table_rows.append(
            f"| {row['work_id']} | {row['state']} | {row['work_category']} | ₹ {row['sanction_amount']:,.0f} | {row['sanction_delay_days']:.0f} | **{row['risk_score']}** | {row['risk_level']} |"
        )
    top20_table_str = "\n".join(top20_table_rows)

    report_content = f"""# ML V1 Model Execution Report — MPLAD AI Audit (SIH26102)

## 1. Executive Objective
This report details the execution and results of **Phase 1 (ML V1)** for the MPLAD AI Audit platform. ML V1 implements an **unsupervised anomaly detection model** combining **Isolation Forest** with engineered relative cost and delay metrics.

> [!IMPORTANT]
> **DISCLAIMER**: The dataset contains no ground-truth fraud labels. Flagged records represent **statistical outliers and administrative anomalies** requiring human audit, NOT proof of illegal activity or fraud.

---

## 2. Model Execution Metrics Summary

| Metric | Value |
| :--- | :--- |
| **Dataset Processed** | `Works Sanctioned (1).csv` |
| **Total Valid Records** | **{summary_metrics['total_records']:,}** |
| **Model Algorithm** | `IsolationForest` (n_estimators=100, contamination=0.05) |
| **Anomalies Detected (Label = -1)** | **{summary_metrics['total_anomalies']:,}** |
| **Percentage Anomalous** | **{summary_metrics['anomaly_percentage']:.2f}%** |
| **Critical Risk (Score 85–100)** | {summary_metrics['risk_levels']['Critical']:,} |
| **High Risk (Score 70–84)** | {summary_metrics['risk_levels']['High']:,} |
| **Medium Risk (Score 40–69)** | {summary_metrics['risk_levels']['Medium']:,} |
| **Low Risk (Score 0–39)** | {summary_metrics['risk_levels']['Low']:,} |

---

## 3. Top 20 Highest-Risk Projects

| Work ID / Code | State | Category | Sanction Amount | Delay (Days) | Risk Score | Risk Level |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
{top20_table_str}

---

## 4. Anomaly Breakdown by Dimension

### Anomaly Distribution by State (Top 5 Anomalous States)
{json.dumps(summary_metrics['top_anomalous_states'], indent=2)}

### Anomaly Distribution by Work Category
{json.dumps(summary_metrics['anomalies_by_category'], indent=2)}

### Anomaly Distribution by Work Status
{json.dumps(summary_metrics['anomalies_by_status'], indent=2)}

---

## 5. Artifacts & Generated Files

- **Model Serialized Pipeline**: `ml/models/mplad_anomaly_model.pkl`
- **Full Scored Projects Dataset**: `ml/outputs/scored_projects.csv`
- **High-Risk Projects Dataset**: `ml/outputs/high_risk_projects.csv`
- **Summary JSON Metrics**: `ml/outputs/anomaly_summary.json`
- **Visualization Plots**: `ml/outputs/plots/`
"""
    with open(report_path, "w") as f:
        f.write(report_content)
    print(f"[Report] Saved ML V1 Report to {report_path}")

def run_pipeline():
    print("\n==================================================")
    print("STARTING ML V1 TRAINING & INFERENCE PIPELINE")
    print("==================================================")
    
    # 1. Load and clean
    df_raw = load_and_clean_data(DATA_PATH)
    
    # 2. Feature engineering
    fe = FeatureEngineer()
    df_features, X_matrix = fe.fit_transform(df_raw)
    
    # 3. Model training
    model = MPLADAnomalyDetector(contamination=0.05, random_state=42)
    model.fit(X_matrix)
    labels, raw_scores = model.predict(X_matrix)
    
    # 4. Risk scoring engine
    re = RiskEngine()
    df_scored = re.process_dataset(df_features, raw_scores, labels)
    
    # 5. Save model pipeline bundle
    pipeline_bundle = {
        'feature_engineer': fe,
        'anomaly_model': model,
        'risk_engine': re
    }
    model_save_path = os.path.join(MODELS_DIR, "mplad_anomaly_model.pkl")
    joblib.dump(pipeline_bundle, model_save_path)
    print(f"[Model] Saved pipeline bundle to {model_save_path}")
    
    # 6. Save scored outputs
    output_cols = [
        'work_id', 'state', 'ida', 'mp_name', 'constituency', 'work_category',
        'work_description_clean', 'recommended_dt', 'sanction_dt', 'sanction_amount',
        'sanction_delay_days', 'work_status', 'anomaly_label', 'anomaly_score',
        'risk_score', 'risk_level', 'anomaly_reason'
    ]
    df_output = df_scored[output_cols].copy()
    
    scored_csv_path = os.path.join(OUTPUTS_DIR, "scored_projects.csv")
    high_risk_csv_path = os.path.join(OUTPUTS_DIR, "high_risk_projects.csv")
    
    df_output.to_csv(scored_csv_path, index=False)
    
    df_high_risk = df_output[df_output['risk_level'].isin(['Critical', 'High'])].sort_values(by='risk_score', ascending=False)
    df_high_risk.to_csv(high_risk_csv_path, index=False)
    
    print(f"[Output] Saved scored projects to {scored_csv_path}")
    print(f"[Output] Saved high-risk projects ({len(df_high_risk)} records) to {high_risk_csv_path}")

    # 7. Summary metrics & JSON
    total_records = int(len(df_output))
    total_anomalies = int((df_output['anomaly_label'] == -1).sum())
    anomaly_pct = float((total_anomalies / total_records) * 100)
    
    risk_level_counts = df_output['risk_level'].value_counts().to_dict()
    for level in ['Low', 'Medium', 'High', 'Critical']:
        risk_level_counts.setdefault(level, 0)
        risk_level_counts[level] = int(risk_level_counts[level])
        
    top_anom_states = df_output[df_output['anomaly_label'] == -1]['state'].value_counts().head(5).to_dict()
    anom_cats = df_output[df_output['anomaly_label'] == -1]['work_category'].value_counts().to_dict()
    anom_status = df_output[df_output['anomaly_label'] == -1]['work_status'].value_counts().to_dict()
    
    summary_metrics = {
        'total_records': total_records,
        'total_anomalies': total_anomalies,
        'anomaly_percentage': round(anomaly_pct, 2),
        'risk_levels': risk_level_counts,
        'top_anomalous_states': {k: int(v) for k, v in top_anom_states.items()},
        'anomalies_by_category': {k: int(v) for k, v in anom_cats.items()},
        'anomalies_by_status': {k: int(v) for k, v in anom_status.items()},
    }
    
    summary_json_path = os.path.join(OUTPUTS_DIR, "anomaly_summary.json")
    with open(summary_json_path, "w") as f:
        json.dump(summary_metrics, f, indent=2)
    print(f"[Output] Saved summary metrics JSON to {summary_json_path}")
    
    # 8. Visualizations & Report
    generate_visualizations(df_scored)
    generate_report(df_scored, summary_metrics)

    print("\n==================================================")
    print("ML V1 PIPELINE EXECUTED SUCCESSFULLY!")
    print("==================================================")
    print(f"Processed: {total_records} records")
    print(f"Anomalies: {total_anomalies} ({anomaly_pct:.2f}%)")
    print("Top 5 Highest Risk Projects:")
    print(df_output[['work_id', 'state', 'sanction_amount', 'risk_score', 'risk_level']].head())

if __name__ == "__main__":
    run_pipeline()
