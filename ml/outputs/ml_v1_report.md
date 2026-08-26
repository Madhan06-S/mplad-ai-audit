# ML V1 Model Execution Report — MPLAD AI Audit (SIH26102)

## 1. Executive Objective
This report details the execution and results of **Phase 1 (ML V1)** for the MPLAD AI Audit platform. ML V1 implements an **unsupervised anomaly detection model** combining **Isolation Forest** with engineered relative cost and delay metrics.

> [!IMPORTANT]
> **DISCLAIMER**: The dataset contains no ground-truth fraud labels. Flagged records represent **statistical outliers and administrative anomalies** requiring human audit, NOT proof of illegal activity or fraud.

---

## 2. Model Execution Metrics Summary

| Metric | Value |
| :--- | :--- |
| **Dataset Processed** | `Works Sanctioned (1).csv` |
| **Total Valid Records** | **33,000** |
| **Model Algorithm** | `IsolationForest` (n_estimators=100, contamination=0.05) |
| **Anomalies Detected (Label = -1)** | **1,650** |
| **Percentage Anomalous** | **5.00%** |
| **Critical Risk (Score 85–100)** | 16 |
| **High Risk (Score 70–84)** | 105 |
| **Medium Risk (Score 40–69)** | 1,515 |
| **Low Risk (Score 0–39)** | 31,364 |

---

## 3. Top 20 Highest-Risk Projects

| Work ID / Code | State | Category | Sanction Amount | Delay (Days) | Risk Score | Risk Level |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| WS/MP352/2025-2026/138758-Construction of public libraries and reading rooms | Kerala | Trust and Society | ₹ 5,000,000 | 490 | **100.0** | Critical |
| WS/MP18159/2025-2026/194372-Construction of community centers and community halls | Rajasthan | Trust and Society | ₹ 5,000,000 | 140 | **95.9** | Critical |
| WS/MP18198/2025-2026/193991-Construction of roads, link roads, pathways or any other road with or without drainage system | Uttar Pradesh | Repair and Renovation | ₹ 9,860,000 | 83 | **95.7** | Critical |
| WS/MP431/2026-2027/149155-Construction of community centers and community halls | Haryana | Trust and Society | ₹ 1,499,787 | 575 | **94.9** | Critical |
| WS/MP18337/2025-2026/156920-Construction of public irrigation facilities | Kerala | Repair and Renovation | ₹ 5,000,000 | 175 | **93.4** | Critical |
| WS/MP18062/2026-2027/156120-Construction of community centers and community halls | Haryana | Trust and Society | ₹ 499,708 | 583 | **93.3** | Critical |
| WS/MP478/2025-2026/176954-Construction of rooms and facilities for hospitals, FWC , PHC Centers and ANM centers | Uttarakhand | Trust and Society | ₹ 5,000,000 | 52 | **91.0** | Critical |
| WS/MP18271/2025-2026/167573-Construction of community centers and community halls | West Bengal | Repair and Renovation | ₹ 5,000,000 | 213 | **88.9** | Critical |
| WS/MP591/2025-2026/197032-Construction of additional rooms and halls in the existing public and community building | Haryana | Trust and Society | ₹ 2,100,000 | 266 | **88.1** | Critical |
| WS/MP507/2025-2026/196288-Lighting of public spaces | Uttar Pradesh | Normal/Others | ₹ 47,472,048 | 54 | **87.5** | Critical |
| WS/MP827/2025-2026/152382-Construction of community centers and community halls | West Bengal | Normal/Others | ₹ 6,000,000 | 449 | **87.4** | Critical |
| WS/MP827/2025-2026/152381-Construction of community centers and community halls | West Bengal | Normal/Others | ₹ 6,000,000 | 449 | **87.4** | Critical |
| WS/MP18343/2025-2026/180022-Construction of rooms and facilities for hospitals, FWC , PHC Centers and ANM centers | Andhra Pradesh | Trust and Society | ₹ 5,000,000 | 129 | **85.9** | Critical |
| WS/MP18064/2025-2026/150852-Construction of community centers and community halls | Haryana | Trust and Society | ₹ 1,100,000 | 301 | **85.5** | Critical |
| WS/MP243/2025-2026/141110-Construction of rooms and halls in school and colleges | West Bengal | Normal/Others | ₹ 11,000,000 | 436 | **85.4** | Critical |
| WS/MP18062/2026-2027/156112-Construction of community centers and community halls | Haryana | Trust and Society | ₹ 498,031 | 530 | **85.2** | Critical |
| WS/MP18096/2025-2026/172806-Construction of rooms and facilities for hospitals, FWC , PHC Centers and ANM centers | Kerala | Repair and Renovation | ₹ 3,300,001 | 341 | **84.3** | High |
| WS/MP18148/2025-2026/186567-Construction of rooms and halls in school and colleges | Odisha | Trust and Society | ₹ 1,000,000 | 206 | **84.2** | High |
| WS/MP372/2025-2026/169577-Construction of New Building | Odisha | Repair and Renovation | ₹ 990,000 | 307 | **83.6** | High |
| WS/MP18328/2026-2027/148155-Purchase Books for Library | Himachal Pradesh | Bar and Associations | ₹ 50,000 | 641 | **83.3** | High |

---

## 4. Anomaly Breakdown by Dimension

### Anomaly Distribution by State (Top 5 Anomalous States)
{
  "Uttar Pradesh": 198,
  "West Bengal": 158,
  "Odisha": 125,
  "Karnataka": 123,
  "Maharashtra": 99
}

### Anomaly Distribution by Work Category
{
  "Normal/Others": 997,
  "Repair and Renovation": 465,
  "Trust and Society": 187,
  "Bar and Associations": 1
}

### Anomaly Distribution by Work Status
{
  "Work partially Completed": 444,
  "Physical Inspection": 430,
  "Sanction": 321,
  "Vendor Identification": 297,
  "Work Completed": 134,
  "Time Estimation": 24
}

---

## 5. Artifacts & Generated Files

- **Model Serialized Pipeline**: `ml/models/mplad_anomaly_model.pkl`
- **Full Scored Projects Dataset**: `ml/outputs/scored_projects.csv`
- **High-Risk Projects Dataset**: `ml/outputs/high_risk_projects.csv`
- **Summary JSON Metrics**: `ml/outputs/anomaly_summary.json`
- **Visualization Plots**: `ml/outputs/plots/`
