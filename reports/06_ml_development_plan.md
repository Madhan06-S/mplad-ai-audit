# ML Development Roadmap & Implementation Plan — MPLAD AI Audit (SIH26102)

## 1. Roadmap Architecture

The ML development follows a phased, progressive approach to avoid premature complexity and ensure robust model validation at each stage.

```
       ┌─────────────────────────────────────────────────────────────┐
       │ PHASE 1: Baseline Anomaly Pipeline (ML V1)                 │
       │ - Data Cleaning & Preprocessing                              │
       │ - Feature Engineering (Cost Z-Score, Delay Days)             │
       │ - Isolation Forest Model Training                           │
       │ - Initial Anomaly Score Generation                          │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │ PHASE 2: Multi-Model Composite Risk Engine (ML V2)          │
       │ - TF-IDF Text Duplicate Detection                           │
       │ - Local Outlier Factor (Local Density Check)                 │
       │ - MP Fund Utilization Tracker Integration                   │
       │ - Multi-Factor Risk Score Calibration (0-100)               │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │ PHASE 3: Explainable Risk Engine & Model Packaging (ML V3)  │
       │ - SHAP Explainer Integration                                 │
       │ - Automated Risk Factor Breakdown ("WHY Risk = 87?")         │
       │ - Model Serialization (.joblib / ONNX)                       │
       │ - Inference Pipeline API Integration                         │
       └─────────────────────────────────────────────────────────────┘
```

---

## 2. Phase-by-Phase Deliverables

### Phase 1: ML V1 (Baseline Anomaly Engine)
- **Inputs**: Raw CSV files (`Works Sanctioned (1).csv`).
- **Scripts**: `ml/src/data_cleaner.py`, `ml/src/features.py`, `ml/src/train_v1.py`.
- **Outputs**: `ml/models/isolation_forest_v1.joblib`, anomaly score per record.

### Phase 2: ML V2 (Composite Risk Engine)
- **Inputs**: Cleaned data + entitlement CSVs.
- **Scripts**: `ml/src/duplicate_detector.py`, `ml/src/risk_engine.py`.
- **Outputs**: Multi-dimensional risk matrix, composite 0–100 risk score, high/medium/low risk categorizations.

### Phase 3: ML V3 (Explainability & Production Packaging)
- **Inputs**: Trained Risk Engine.
- **Scripts**: `ml/src/explainability.py`, `ml/src/pipeline.py`.
- **Outputs**: SHAP summary plots, JSON explanation payload per record, production model pipeline.
