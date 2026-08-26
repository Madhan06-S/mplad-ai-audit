# SIH26102 — MPLAD AI Audit

AI-Powered Monitoring, Anomaly Detection & Analytics Platform for MPLADS (Members of Parliament Local Area Development Scheme).

## 📁 Repository Structure

```
mplad-ai-audit/
├── backend/                  # FastAPI Application Server (Phase 3)
│   ├── app/
│   ├── models/
│   ├── services/
│   └── main.py
│
├── ml/                       # Machine Learning Subsystem
│   ├── data/                 # Raw & Processed CSV Datasets
│   ├── notebooks/            # Exploratory Data Analysis Notebooks
│   ├── src/                  # Clean Modular Python Scripts
│   │   └── eda_audit.py      # Automated EDA & Data Audit Script
│   └── models/               # Serialized ML Model Artifacts (.joblib)
│
├── reports/                  # Generated EDA & Quality Audit Reports
│   ├── 01_eda_report.md
│   ├── 02_data_quality_report.md
│   ├── 03_dataset_relationship_diagram.md
│   ├── 04_ml_targets_and_features.md
│   ├── 05_recommended_algorithms.md
│   ├── 06_ml_development_plan.md
│   ├── 07_backend_architecture_plan.md
│   └── eda_summary.json
│
└── README.md
```

## 📊 Dataset Inspection & Audit Summary

- **Primary Dataset (`Works Sanctioned (1).csv`)**: 33,000 sanctioned work records across 34 States/UTs.
- **Total Sanctioned Amount**: **₹ 17,171,955,577.55** (~ ₹ 1,717 Crores).
- **Entitlement Datasets**: `Allocated Limit for Honble MPs.csv` & `(1).csv` covering 776 MPs.
- **Calamity Dataset**: 13 disaster relief consent allocations.

## 🚀 Running EDA & Data Audit Script

```bash
# Activate Virtual Environment
source venv/bin/activate

# Execute Automated Audit Script
python ml/src/eda_audit.py
```
