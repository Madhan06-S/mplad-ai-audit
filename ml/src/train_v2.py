import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from preprocess import load_and_clean_data
from feature_engineering import FeatureEngineer
from anomaly_model import MPLADAnomalyDetector
from risk_engine import RiskEngine
from duplicate_detection import DuplicateDetector
from fund_utilization import FundUtilizationTracker
from composite_risk import CompositeRiskEngine

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_DIR, "data", "Works Sanctioned (1).csv")
AL1_PATH = os.path.join(BASE_DIR, "data", "Allocated Limit for Honble MPs.csv")
AL2_PATH = os.path.join(BASE_DIR, "data", "Allocated Limit for Honble MPs (1).csv")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
PLOTS_DIR = os.path.join(OUTPUTS_DIR, "plots")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

def generate_v2_visualizations(df_v2: pd.DataFrame, df_dup: pd.DataFrame, df_util: pd.DataFrame):
    print("[Visualization V2] Generating V2 plots...")
    plt.style.use('ggplot')

    # 1. Composite Risk Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df_v2['composite_risk_score'], kde=True, ax=ax, color='crimson', bins=50)
    ax.set_title("ML V2 Composite Risk Score Distribution (0-100 Index)")
    ax.set_xlabel("Composite Risk Score")
    plt.tight_layout()
    fig.savefig(os.path.join(PLOTS_DIR, "06_composite_risk_distribution.png"), dpi=300)
    plt.close(fig)

    # 2. Duplicate Similarity Distribution
    if len(df_dup) > 0:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df_dup['similarity_score'], kde=False, ax=ax, color='indigo', bins=30)
        ax.set_title("Duplicate Candidate Pair Similarity Score Distribution")
        ax.set_xlabel("Similarity Score (0.85 - 1.00)")
        plt.tight_layout()
        fig.savefig(os.path.join(PLOTS_DIR, "07_duplicate_similarity_distribution.png"), dpi=300)
        plt.close(fig)

    # 3. MP Utilization Distribution
    if len(df_util) > 0:
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df_util['utilization_percentage'], kde=True, ax=ax, color='darkgreen', bins=40)
        ax.set_title("MP Fund Utilization Percentage Distribution (%)")
        ax.set_xlabel("Utilization Percentage (%)")
        plt.tight_layout()
        fig.savefig(os.path.join(PLOTS_DIR, "08_mp_utilization_distribution.png"), dpi=300)
        plt.close(fig)

    print("[Visualization V2] Plots successfully saved.")

def generate_fund_summary_markdown(df_util: pd.DataFrame):
    summary_path = os.path.join(OUTPUTS_DIR, "fund_utilization_summary.md")
    
    total_mps = len(df_util)
    matched_mps = int(df_util['is_allocation_matched'].sum())
    alert_counts = df_util['utilization_alert'].value_counts().to_dict()
    
    top5_util = df_util.sort_values(by='utilization_percentage', ascending=False).head(10)
    
    rows = []
    for idx, r in top5_util.iterrows():
        rows.append(
            f"| {r['mp_name_works']} | {r['state']} | ₹ {r['allocated_amount']:,.0f} | ₹ {r['total_sanctioned_amount']:,.0f} | **{r['utilization_percentage']:.1f}%** | {r['utilization_alert']} |"
        )
    table_str = "\n".join(rows)

    md_content = f"""# MP Fund Utilization Tracking Summary — MPLAD AI Audit

## 📊 Allocation & Spending Metrics

- **Total MPs Analyzed**: {total_mps}
- **Allocations Matched**: {matched_mps} / {total_mps} ({(matched_mps/total_mps)*100:.1f}%)
- **Total Allocated Amount**: ₹ {df_util['allocated_amount'].sum():,.2f}
- **Total Sanctioned Amount**: ₹ {df_util['total_sanctioned_amount'].sum():,.2f}
- **Overall Scheme Utilization**: **{(df_util['total_sanctioned_amount'].sum() / df_util['allocated_amount'].sum())*100:.1f}%**

---

## 🚨 Alert Tiers Breakdown

| Alert Category | Utilization Range | MP Count | % of MPs |
| :--- | :---: | :---: | :---: |
| **NORMAL** | 0 – 70% | {alert_counts.get('NORMAL', 0)} | {(alert_counts.get('NORMAL', 0)/total_mps)*100:.1f}% |
| **MONITOR** | 70 – 90% | {alert_counts.get('MONITOR', 0)} | {(alert_counts.get('MONITOR', 0)/total_mps)*100:.1f}% |
| **HIGH UTILIZATION** | 90 – 100% | {alert_counts.get('HIGH UTILIZATION', 0)} | {(alert_counts.get('HIGH UTILIZATION', 0)/total_mps)*100:.1f}% |
| **POTENTIAL ALLOCATION RECONCILIATION REQUIRED** | > 100% | {alert_counts.get('POTENTIAL ALLOCATION RECONCILIATION REQUIRED', 0)} | {(alert_counts.get('POTENTIAL ALLOCATION RECONCILIATION REQUIRED', 0)/total_mps)*100:.1f}% |

> [!NOTE]
> **RECONCILIATION NOTE**: The works dataset contains multi-year cumulative recommendations (2024-2027), while allocation files list single-term baseline limits. Fund utilization metrics serve as an administrative velocity tracker, NOT evidence of illegal activity or fraud.

---

## 🔝 Top 10 MPs by Fund Utilization Percentage

| MP Name | State | Allocated Amount | Sanctioned Amount | Utilization % | Alert Status |
| :--- | :--- | :--- | :--- | :---: | :--- |
{table_str}
"""
    with open(summary_path, "w") as f:
        f.write(md_content)
    print(f"[FundSummary] Saved fund summary markdown to {summary_path}")

def generate_v2_report(df_v2: pd.DataFrame, df_dup: pd.DataFrame, df_util: pd.DataFrame):
    report_path = os.path.join(OUTPUTS_DIR, "ml_v2_report.md")
    
    total_records = len(df_v2)
    risk_counts = df_v2['risk_level'].value_counts().to_dict()
    for lvl in ['Low', 'Medium', 'High', 'Critical']:
        risk_counts.setdefault(lvl, 0)

    top20 = df_v2.sort_values(by='composite_risk_score', ascending=False).head(20)
    top20_rows = []
    for idx, r in top20.iterrows():
        top20_rows.append(
            f"| {r['work_id']} | {r['state']} | {r['work_category']} | ₹ {r['sanction_amount']:,.0f} | **{r['composite_risk_score']}** | {r['risk_level']} | {r['risk_reasons']} |"
        )
    top20_str = "\n".join(top20_rows)

    matched_mps = int(df_util['is_allocation_matched'].sum())
    total_mps = int(len(df_util))

    md_content = f"""# ML V2 Model Execution Report — MPLAD AI Audit (SIH26102)

## 1. Executive Summary
This report presents the execution results of **Phase 2 (ML V2)** for the MPLAD AI Audit system. ML V2 introduces a **Multi-Signal Composite Risk Engine** integrating:
1. **Module 1**: Duplicate & Similar Work Detection (TF-IDF + Cosine Similarity with Domain Stop Words)
2. **Module 2**: MP Fund Utilization Tracking & Non-Accusatory Reconciliation Alerts
3. **Module 3**: Calibrated Composite Risk Scoring Engine (Max-Boosted 5-Signal Blend)

> [!IMPORTANT]
> **AUDIT TERMINOLOGY STATEMENT**: All signals identify statistical outliers, potential duplicate candidates, or spending velocity alerts intended to prioritize human audit reviews. No system score constitutes proof of fraud.

---

## 2. ML V2 Module Execution Summary

| Dimension | Metric / Output | Value |
| :--- | :--- | :--- |
| **Total Works Processed** | Master Dataset Records | **{total_records:,}** |
| **Module 1: Duplicate Candidates** | Similarity >= 0.85 Pairs | **{len(df_dup):,} pairs** |
| **Module 1: Potential Split Works** | Similar & Close in Time/Cost | **{int(df_dup['potential_split_work'].sum()):,} pairs** |
| **Module 2: MP Matching Success** | Allocation Matching Rate | **{matched_mps} / {total_mps} ({(matched_mps/total_mps)*100:.1f}%)** |
| **Module 2: Allocation Alerts** | Monitor (70-90%) / High (>90%) | **{(df_util['utilization_percentage'] >= 70).sum():,} MPs** |
| **Module 3: Critical Risk (85–100)** | Composite Score | **{risk_counts['Critical']:,} projects** |
| **Module 3: High Risk (70–84)** | Composite Score | **{risk_counts['High']:,} projects** |
| **Module 3: Medium Risk (40–69)** | Composite Score | **{risk_counts['Medium']:,} projects** |
| **Module 3: Low Risk (0–39)** | Composite Score | **{risk_counts['Low']:,} projects** |

---

## 3. Top 20 Highest Composite-Risk Projects

| Work ID / Code | State | Category | Amount (INR) | Composite Risk Score | Risk Level | Primary Data-Supported Reasons |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
{top20_str}

---

## 4. Generated Artifacts & Reports

- **Duplicate Candidate Pairs**: `ml/outputs/duplicate_candidates.csv`
- **MP Fund Utilization**: `ml/outputs/mp_fund_utilization.csv`
- **Fund Summary Report**: `ml/outputs/fund_utilization_summary.md`
- **V2 Full Scored Projects**: `ml/outputs/v2_scored_projects.csv`
- **V2 High-Risk Projects**: `ml/outputs/v2_high_risk_projects.csv`
- **Visualization Plots**: `ml/outputs/plots/` (`06_composite_risk_distribution.png`, `07_duplicate_similarity_distribution.png`, `08_mp_utilization_distribution.png`)
"""
    with open(report_path, "w") as f:
        f.write(md_content)
    print(f"[Report V2] Saved ML V2 Report to {report_path}")

def run_v2_pipeline():
    print("\n==================================================")
    print("STARTING ML V2 COMPOSITE RISK PIPELINE")
    print("==================================================")

    v1_scored_path = os.path.join(OUTPUTS_DIR, "scored_projects.csv")
    if os.path.exists(v1_scored_path):
        df_v1 = pd.read_csv(v1_scored_path)
        print(f"[V2 Pipeline] Loaded V1 scored projects ({len(df_v1)} records)")
    else:
        print("[V2 Pipeline] V1 scored projects not found. Running V1 pipeline...")
        from train_v1 import run_pipeline as run_v1
        run_v1()
        df_v1 = pd.read_csv(v1_scored_path)

    df_v1['sanction_dt'] = pd.to_datetime(df_v1['sanction_dt'], errors='coerce')
    df_v1['recommended_dt'] = pd.to_datetime(df_v1['recommended_dt'], errors='coerce')

    # Module 1: Duplicate & Similar Work Detection
    dup_detector = DuplicateDetector(similarity_threshold=0.85)
    df_dup_pairs, dup_sim_dict, similar_work_dict = dup_detector.find_duplicates(df_v1)
    
    dup_csv_path = os.path.join(OUTPUTS_DIR, "duplicate_candidates.csv")
    df_dup_pairs.to_csv(dup_csv_path, index=False)
    print(f"[V2 Pipeline] Saved duplicate candidate pairs to {dup_csv_path}")

    # Module 2: MP Fund Utilization Tracking
    fund_tracker = FundUtilizationTracker()
    df_mp_util, mp_util_scores = fund_tracker.process_fund_utilization(df_v1, AL1_PATH, AL2_PATH)
    
    util_csv_path = os.path.join(OUTPUTS_DIR, "mp_fund_utilization.csv")
    df_mp_util.to_csv(util_csv_path, index=False)
    print(f"[V2 Pipeline] Saved MP fund utilization to {util_csv_path}")
    generate_fund_summary_markdown(df_mp_util)

    # Module 3: Composite Risk Engine
    risk_engine_v2 = CompositeRiskEngine()
    df_v2_scored = risk_engine_v2.process_composite_risk(df_v1, dup_sim_dict, similar_work_dict, mp_util_scores)

    v2_scored_csv = os.path.join(OUTPUTS_DIR, "v2_scored_projects.csv")
    v2_high_risk_csv = os.path.join(OUTPUTS_DIR, "v2_high_risk_projects.csv")

    v2_cols = [
        'work_id', 'state', 'ida', 'mp_name', 'constituency', 'work_category',
        'work_description_clean', 'recommended_dt', 'sanction_dt', 'sanction_amount',
        'sanction_delay_days', 'work_status', 'v1_anomaly_score', 'cost_anomaly_score',
        'delay_anomaly_score', 'duplicate_score', 'fund_utilization_score',
        'v1_contrib', 'cost_contrib', 'delay_contrib', 'duplicate_contrib', 'fund_contrib',
        'base_weighted_sum', 'max_signal', 'composite_risk_score', 'risk_level', 'risk_reasons'
    ]
    df_v2_out = df_v2_scored[v2_cols].copy()
    df_v2_out.to_csv(v2_scored_csv, index=False)

    df_v2_high_risk = df_v2_out[df_v2_out['risk_level'].isin(['Critical', 'High'])].sort_values(by='composite_risk_score', ascending=False)
    df_v2_high_risk.to_csv(v2_high_risk_csv, index=False)

    print(f"[V2 Pipeline] Saved V2 scored projects to {v2_scored_csv}")
    print(f"[V2 Pipeline] Saved V2 high-risk projects ({len(df_v2_high_risk)} records) to {v2_high_risk_csv}")

    generate_v2_visualizations(df_v2_out, df_dup_pairs, df_mp_util)
    generate_v2_report(df_v2_out, df_dup_pairs, df_mp_util)

    print("\n==================================================")
    print("ML V2 COMPOSITE RISK PIPELINE COMPLETED SUCCESSFULLY!")
    print("==================================================")
    print(f"Total Works Processed: {len(df_v2_out)}")
    print(f"Duplicate Candidate Pairs: {len(df_dup_pairs)}")
    print(f"MPs Analyzed: {len(df_mp_util)}")
    print(f"V2 High-Risk Flagged Works (Critical/High): {len(df_v2_high_risk)}")
    print("Top 5 Highest Composite Risk Projects:")
    print(df_v2_out[['work_id', 'state', 'sanction_amount', 'composite_risk_score', 'risk_level']].head())

if __name__ == "__main__":
    run_v2_pipeline()
