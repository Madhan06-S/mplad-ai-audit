# ML V3 Explainable Risk Engine Report — MPLAD AI Audit (SIH26102)

## 1. Executive Overview
ML V3 equips the MPLAD AI Audit platform with **Game-Theoretic Model Explainability (SHAP)**. Auditors can inspect exact feature-level attributions answering **"WHY is this specific project flagged as high risk?"**.

---

## 2. ML V3 Execution Metrics Summary

| Metric | Value |
| :--- | :--- |
| **Dataset Processed** | `Works Sanctioned (1).csv` (33,000 ground-truth works) |
| **Model Architecture** | Isolation Forest + TF-IDF Duplicate Detector + Fund Utilization Tracker |
| **Explainability Engine** | `shap.TreeExplainer` game-theoretic feature attribution |
| **Total Flagged Anomalies** | **1,650** |
| **Critical Risk (Score 85–100)** | 0 |
| **High Risk (Score 70–84)** | 2 |
| **Medium Risk (Score 40–69)** | 1,468 |
| **Low Risk (Score 0–39)** | 31,530 |

---

## 3. Top 10 High-Risk Projects with SHAP Feature Attributions

| Work ID | MP Name | Amount | Risk Score | Risk Level | Primary SHAP Feature Attribution |
| :--- | :--- | :--- | :---: | :---: | :--- |
| WS/MP18271/2025-2026/167573-Construction of community centers and community halls | JAGADISH CHANDRA BARMA BASUNIA | ₹ 5,000,000 | **70.7** | High | `work_category_Normal/Others (-1.7297)` |
| WS/MP827/2025-2026/152382-Construction of community centers and community halls | Shatrughan Sinha | ₹ 6,000,000 | **70.3** | High | `amount_vs_state_median (-1.2194)` |
| WS/MP18148/2025-2026/186567-Construction of rooms and halls in school and colleges | BALABHADRA MAJHI | ₹ 1,000,000 | **69.8** | Medium | `work_category_Normal/Others (-1.9686)` |
| WS/MP18148/2025-2026/186570-Construction of rooms and halls in school and colleges | BALABHADRA MAJHI | ₹ 500,000 | **66.5** | Medium | `work_category_Normal/Others (-1.9717)` |
| WS/MP18086/2026-2027/171271-Construction of community centers and community halls | SHREYAS. M. PATEL | ₹ 1,000,000 | **66.2** | Medium | `work_category_Normal/Others (-1.9272)` |
| WS/MP18271/2025-2026/196965-Construction of community centers and community halls | JAGADISH CHANDRA BARMA BASUNIA | ₹ 5,000,000 | **65.7** | Medium | `work_category_Normal/Others (-1.8366)` |
| WS/MP18148/2026-2027/181887-Construction of rooms and halls in school and colleges | BALABHADRA MAJHI | ₹ 500,000 | **65.7** | Medium | `work_category_Normal/Others (-1.9697)` |
| WS/MP574/2025-2026/145476-Construction of rooms and halls in school and colleges | Bharatsinhji Shankarji Dabhi | ₹ 500,000 | **62.0** | Medium | `work_category_Normal/Others (-2.1637)` |
| WS/MP574/2025-2026/145489-Construction of rooms and halls in school and colleges | Bharatsinhji Shankarji Dabhi | ₹ 500,000 | **62.0** | Medium | `work_category_Normal/Others (-2.1637)` |
| WS/MP574/2025-2026/145482-Construction of rooms and halls in school and colleges | Bharatsinhji Shankarji Dabhi | ₹ 500,000 | **62.0** | Medium | `work_category_Normal/Others (-2.1637)` |

---

## 4. Production Artifacts

- **V3 Model Pipeline Bundle**: `ml/models/mplad_anomaly_model_v3.pkl`
- **Full Scored Dataset with SHAP**: `ml/outputs/scored_projects_v3.csv`
- **High-Risk Projects Dataset**: `ml/outputs/high_risk_projects_v3.csv`
- **Summary Metrics JSON**: `ml/outputs/anomaly_summary_v3.json`
- **ML V3 Report**: `ml/outputs/ml_v3_report.md`
- **Plots**: `ml/outputs/plots/09_shap_summary_bar.png`
