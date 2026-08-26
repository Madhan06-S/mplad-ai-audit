# ML V2 Multi-Factor Risk Engine Report — MPLAD AI Audit (SIH26102)

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
| **Potential Duplicate / Split Works Flagged (Sim ≥ 75%)** | **3,769** |
| **High Risk / Critical Risk Works (Score ≥ 70)** | **2** |
| **Critical Risk (Score 85–100)** | 0 |
| **High Risk (Score 70–84)** | 2 |
| **Medium Risk (Score 40–69)** | 1,468 |
| **Low Risk (Score 0–39)** | 31,530 |

---

## 3. Top 20 Highest Multi-Factor Risk Projects

| Work ID | MP Name | State | Sanction Amount | Dup Sim % | MP Util % | Risk Score | Risk Level |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| WS/MP18271/2025-2026/167573-Construction of community centers and community halls | JAGADISH CHANDRA BARMA BASUNIA | West Bengal | ₹ 5,000,000 | 88.9% | 24.9% | **70.7** | High |
| WS/MP827/2025-2026/152382-Construction of community centers and community halls | Shatrughan Sinha | West Bengal | ₹ 6,000,000 | 100.0% | 40.0% | **70.3** | High |
| WS/MP18148/2025-2026/186567-Construction of rooms and halls in school and colleges | BALABHADRA MAJHI | Odisha | ₹ 1,000,000 | 81.4% | 18.6% | **69.8** | Medium |
| WS/MP18148/2025-2026/186570-Construction of rooms and halls in school and colleges | BALABHADRA MAJHI | Odisha | ₹ 500,000 | 81.4% | 18.6% | **66.5** | Medium |
| WS/MP18086/2026-2027/171271-Construction of community centers and community halls | SHREYAS. M. PATEL | Karnataka | ₹ 1,000,000 | 100.0% | 19.1% | **66.2** | Medium |
| WS/MP18271/2025-2026/196965-Construction of community centers and community halls | JAGADISH CHANDRA BARMA BASUNIA | West Bengal | ₹ 5,000,000 | 88.9% | 24.9% | **65.7** | Medium |
| WS/MP18148/2026-2027/181887-Construction of rooms and halls in school and colleges | BALABHADRA MAJHI | Odisha | ₹ 500,000 | 79.6% | 18.6% | **65.7** | Medium |
| WS/MP574/2025-2026/145476-Construction of rooms and halls in school and colleges | Bharatsinhji Shankarji Dabhi | Gujarat | ₹ 500,000 | 100.0% | 30.5% | **62.0** | Medium |
| WS/MP574/2025-2026/145489-Construction of rooms and halls in school and colleges | Bharatsinhji Shankarji Dabhi | Gujarat | ₹ 500,000 | 100.0% | 30.5% | **62.0** | Medium |
| WS/MP574/2025-2026/145482-Construction of rooms and halls in school and colleges | Bharatsinhji Shankarji Dabhi | Gujarat | ₹ 500,000 | 100.0% | 30.5% | **62.0** | Medium |
| WS/MP574/2025-2026/145479-Construction of rooms and halls in school and colleges | Bharatsinhji Shankarji Dabhi | Gujarat | ₹ 500,000 | 100.0% | 30.5% | **62.0** | Medium |
| WS/MP18393/2024-2025/160968-Crematoriums/energy efficient crematoriums or structures on burial/cremation ground | MADHAVANENI RAGHUNANDAN RAO | Telangana | ₹ 800,000 | 100.0% | 27.7% | **61.1** | Medium |
| WS/MP827/2025-2026/152381-Construction of community centers and community halls | Shatrughan Sinha | West Bengal | ₹ 6,000,000 | 67.3% | 40.0% | **60.5** | Medium |
| WS/MP18328/2026-2027/148155-Purchase Books for Library | Kangana Ranaut | Himachal Pradesh | ₹ 50,000 | 45.8% | 19.2% | **60.2** | Medium |
| WS/MP18086/2025-2026/171273-Construction of community centers and community halls | SHREYAS. M. PATEL | Karnataka | ₹ 1,000,000 | 100.0% | 19.1% | **60.2** | Medium |
| WS/MP18051/2025-2026/165882-Construction of rooms and halls in school and colleges | ROOP KUMARI CHOUDHARY | Chhattisgarh | ₹ 1,000,000 | 55.3% | 29.1% | **60.1** | Medium |
| WS/MP852/2024-2025/154562-Construction of Government office buildings (Post office, Police station, Police chauki, etc.) | Abu Taher Khan | West Bengal | ₹ 500,569 | 94.7% | 23.1% | **59.9** | Medium |
| WS/MP18309/2024-2025/155216-Providing supply pipelines for drinking water | SALENG A SANGMA | Meghalaya | ₹ 10,000,000 | 78.5% | 32.6% | **59.2** | Medium |
| WS/MP18159/2025-2026/194372-Construction of community centers and community halls | BHUPENDER YADAV | Rajasthan | ₹ 5,000,000 | 26.6% | 30.9% | **58.6** | Medium |
| WS/MP18397/2025-2026/189572-Development of playfields and sports grounds | Bansuri Swaraj | Delhi | ₹ 180,480 | 100.0% | 10.8% | **58.4** | Medium |

---

## 4. Output Artifacts

- **Model Pipeline Bundle**: `ml/models/mplad_anomaly_model_v2.pkl`
- **Full Scored Dataset**: `ml/outputs/scored_projects_v2.csv`
- **High-Risk Filtered Dataset**: `ml/outputs/high_risk_projects_v2.csv`
- **Summary Metrics JSON**: `ml/outputs/anomaly_summary_v2.json`
- **ML V2 Report**: `ml/outputs/ml_v2_report.md`
- **Plots**: `ml/outputs/plots/`
