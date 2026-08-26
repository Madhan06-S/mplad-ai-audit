# ML V2 Model Execution Report — MPLAD AI Audit (SIH26102)

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
| **Total Works Processed** | Master Dataset Records | **33,000** |
| **Module 1: Duplicate Candidates** | Similarity >= 0.85 Pairs | **53,114 pairs** |
| **Module 1: Potential Split Works** | Similar & Close in Time/Cost | **39,000 pairs** |
| **Module 2: MP Matching Success** | Allocation Matching Rate | **489 / 489 (100.0%)** |
| **Module 2: Allocation Alerts** | Monitor (70-90%) / High (>90%) | **1 MPs** |
| **Module 3: Critical Risk (85–100)** | Composite Score | **2 projects** |
| **Module 3: High Risk (70–84)** | Composite Score | **4,555 projects** |
| **Module 3: Medium Risk (40–69)** | Composite Score | **5,737 projects** |
| **Module 3: Low Risk (0–39)** | Composite Score | **22,706 projects** |

---

## 3. Top 20 Highest Composite-Risk Projects

| Work ID / Code | State | Category | Amount (INR) | Composite Risk Score | Risk Level | Primary Data-Supported Reasons |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| WS/MP827/2025-2026/152382-Construction of community centers and community halls | West Bengal | Normal/Others | ₹ 6,000,000 | **87.8** | Critical | 🔴 Delay anomaly: Recommendation-to-sanction lag of 449 days. | 🟠 Duplicate check: Potential duplicate work detected (Similarity: 100.0%). Requires human verification. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18086/2026-2027/171271-Construction of community centers and community halls | Karnataka | Repair and Renovation | ₹ 1,000,000 | **85.3** | Critical | 🔴 Delay anomaly: Recommendation-to-sanction lag of 467 days. | 🟠 Duplicate check: Potential duplicate work detected (Similarity: 100.0%). Requires human verification. |
| WS/MP352/2025-2026/138758-Construction of public libraries and reading rooms | Kerala | Trust and Society | ₹ 5,000,000 | **83.8** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 490 days. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP431/2026-2027/149155-Construction of community centers and community halls | Haryana | Trust and Society | ₹ 1,499,787 | **83.0** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 575 days. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18062/2026-2027/156120-Construction of community centers and community halls | Haryana | Trust and Society | ₹ 499,708 | **82.7** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 583 days. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18148/2026-2027/181887-Construction of rooms and halls in school and colleges | Odisha | Trust and Society | ₹ 500,000 | **82.2** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 396 days. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP827/2025-2026/152381-Construction of community centers and community halls | West Bengal | Normal/Others | ₹ 6,000,000 | **81.8** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 449 days. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18086/2025-2026/171273-Construction of community centers and community halls | Karnataka | Repair and Renovation | ₹ 1,000,000 | **81.6** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 361 days. | 🟠 Duplicate check: Potential duplicate work detected (Similarity: 100.0%). Requires human verification. |
| WS/MP243/2025-2026/141110-Construction of rooms and halls in school and colleges | West Bengal | Normal/Others | ₹ 11,000,000 | **81.5** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 436 days. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18062/2026-2027/156112-Construction of community centers and community halls | Haryana | Trust and Society | ₹ 498,031 | **81.4** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 530 days. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18120/2025-2026/169210-Construction of roads, link roads, pathways or any other road with or without drainage system | Maharashtra | Normal/Others | ₹ 4,974,167 | **81.3** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 389 days. | 🟠 Duplicate check: Potential duplicate work detected (Similarity: 100.0%). Requires human verification. |
| WS/MP18120/2025-2026/169208-Construction of roads, link roads, pathways or any other road with or without drainage system | Maharashtra | Normal/Others | ₹ 4,978,547 | **81.3** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 389 days. | 🟠 Duplicate check: Potential duplicate work detected (Similarity: 100.0%). Requires human verification. |
| WS/MP18328/2026-2027/148155-Purchase Books for Library | Himachal Pradesh | Bar and Associations | ₹ 50,000 | **81.1** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 641 days. | 🟠 Category signal: Special entity category 'Bar and Associations'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18271/2025-2026/167573-Construction of community centers and community halls | West Bengal | Repair and Renovation | ₹ 5,000,000 | **81.1** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 213 days. | 🟠 Duplicate check: Potential duplicate work detected (Similarity: 91.8%). Requires human verification. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP574/2025-2026/145479-Construction of rooms and halls in school and colleges | Gujarat | Trust and Society | ₹ 500,000 | **81.0** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 321 days. | 🟠 Duplicate check: Potential duplicate work detected (Similarity: 100.0%). Requires human verification. | 🟠 Category signal: Special entity category 'Trust and Society'. |
| WS/MP574/2025-2026/145482-Construction of rooms and halls in school and colleges | Gujarat | Trust and Society | ₹ 500,000 | **81.0** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 321 days. | 🟠 Duplicate check: Potential duplicate work detected (Similarity: 100.0%). Requires human verification. | 🟠 Category signal: Special entity category 'Trust and Society'. |
| WS/MP574/2025-2026/145489-Construction of rooms and halls in school and colleges | Gujarat | Trust and Society | ₹ 500,000 | **81.0** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 321 days. | 🟠 Duplicate check: Potential duplicate work detected (Similarity: 100.0%). Requires human verification. | 🟠 Category signal: Special entity category 'Trust and Society'. |
| WS/MP574/2025-2026/145476-Construction of rooms and halls in school and colleges | Gujarat | Trust and Society | ₹ 500,000 | **81.0** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 321 days. | 🟠 Duplicate check: Potential duplicate work detected (Similarity: 100.0%). Requires human verification. | 🟠 Category signal: Special entity category 'Trust and Society'. |
| WS/MP18345/2026-2027/155578-Construction of roads, link roads, pathways or any other road with or without drainage system | Uttar Pradesh | Repair and Renovation | ₹ 2,225,000 | **80.9** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 543 days. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18309/2026-2027/155237-Construction of footpaths and pedestrian ways | Meghalaya | Normal/Others | ₹ 200,000 | **80.9** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 504 days. | 🟠 Duplicate check: Potential duplicate work detected (Similarity: 100.0%). Requires human verification. |

---

## 4. Generated Artifacts & Reports

- **Duplicate Candidate Pairs**: `ml/outputs/duplicate_candidates.csv`
- **MP Fund Utilization**: `ml/outputs/mp_fund_utilization.csv`
- **Fund Summary Report**: `ml/outputs/fund_utilization_summary.md`
- **V2 Full Scored Projects**: `ml/outputs/v2_scored_projects.csv`
- **V2 High-Risk Projects**: `ml/outputs/v2_high_risk_projects.csv`
- **Visualization Plots**: `ml/outputs/plots/` (`06_composite_risk_distribution.png`, `07_duplicate_similarity_distribution.png`, `08_mp_utilization_distribution.png`)
