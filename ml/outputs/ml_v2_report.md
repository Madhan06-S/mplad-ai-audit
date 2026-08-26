# ML V2 Model Execution Report — MPLAD AI Audit (SIH26102)

## 1. Executive Summary
This report presents the execution results of **Phase 2 (ML V2)** for the MPLAD AI Audit system. ML V2 introduces a **Multi-Signal Composite Risk Engine** integrating:
1. **Module 1**: Duplicate & Similar Work Detection (TF-IDF + Cosine Similarity)
2. **Module 2**: MP Fund Utilization Tracking & Allocation Limit Alerts
3. **Module 3**: Composite Risk Scoring Engine (40% V1 Anomaly + 15% Cost + 15% Delay + 15% Duplicate + 15% Utilization)

> [!IMPORTANT]
> **AUDIT TERMINOLOGY STATEMENT**: All signals identify statistical outliers, potential duplicate candidates, or spending velocity alerts intended to prioritize human audit reviews. No system score constitutes proof of fraud.

---

## 2. ML V2 Module Execution Summary

| Dimension | Metric / Output | Value |
| :--- | :--- | :--- |
| **Total Works Processed** | Master Dataset Records | **33,000** |
| **Module 1: Duplicate Candidates** | Similarity >= 0.85 Pairs | **53,795 pairs** |
| **Module 1: Potential Split Works** | Similar & Close in Time/Cost | **39,152 pairs** |
| **Module 2: MP Matching Success** | Allocation Matching Rate | **489 / 489 (100.0%)** |
| **Module 2: Allocation Alerts** | Exceeded (> 100%) / High (90-100%) | **0 MPs** |
| **Module 3: Critical Risk (85–100)** | Composite Score | **0 projects** |
| **Module 3: High Risk (70–84)** | Composite Score | **1 projects** |
| **Module 3: Medium Risk (40–69)** | Composite Score | **1,265 projects** |
| **Module 3: Low Risk (0–39)** | Composite Score | **31,734 projects** |

---

## 3. Top 20 Highest Composite-Risk Projects

| Work ID / Code | State | Category | Amount (INR) | Composite Risk Score | Risk Level | Primary Data-Supported Reasons |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| WS/MP827/2025-2026/152382-Construction of community centers and community halls | West Bengal | Normal/Others | ₹ 6,000,000 | **70.2** | High | 🔴 Delay anomaly: Recommendation-to-sanction lag of 449 days. | 🟠 Duplicate check: Potentially similar work detected (Similarity: 100.0%). Requires human verification. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18271/2025-2026/167573-Construction of community centers and community halls | West Bengal | Repair and Renovation | ₹ 5,000,000 | **65.9** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 213 days. | 🟠 Duplicate check: Potentially similar work detected (Similarity: 92.1%). Requires human verification. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP827/2025-2026/152381-Construction of community centers and community halls | West Bengal | Normal/Others | ₹ 6,000,000 | **65.6** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 449 days. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18086/2026-2027/171271-Construction of community centers and community halls | Karnataka | Repair and Renovation | ₹ 1,000,000 | **63.9** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 467 days. | 🟠 Duplicate check: Potentially similar work detected (Similarity: 100.0%). Requires human verification. |
| WS/MP352/2025-2026/138758-Construction of public libraries and reading rooms | Kerala | Trust and Society | ₹ 5,000,000 | **62.9** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 490 days. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18148/2026-2027/181887-Construction of rooms and halls in school and colleges | Odisha | Trust and Society | ₹ 500,000 | **62.6** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 396 days. | 🟠 Duplicate check: Potentially similar work detected (Similarity: 79.3%). Requires human verification. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18148/2025-2026/186567-Construction of rooms and halls in school and colleges | Odisha | Trust and Society | ₹ 1,000,000 | **62.4** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 206 days. | 🟠 Duplicate check: Potentially similar work detected (Similarity: 81.6%). Requires human verification. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18328/2026-2027/148155-Purchase Books for Library | Himachal Pradesh | Bar and Associations | ₹ 50,000 | **62.3** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 641 days. | 🟠 Category signal: Special entity category 'Bar and Associations'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18062/2026-2027/156120-Construction of community centers and community halls | Haryana | Trust and Society | ₹ 499,708 | **60.5** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 583 days. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP431/2026-2027/149155-Construction of community centers and community halls | Haryana | Trust and Society | ₹ 1,499,787 | **59.8** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 575 days. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18148/2025-2026/186570-Construction of rooms and halls in school and colleges | Odisha | Trust and Society | ₹ 500,000 | **59.5** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 206 days. | 🟠 Duplicate check: Potentially similar work detected (Similarity: 81.6%). Requires human verification. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18051/2025-2026/165882-Construction of rooms and halls in school and colleges | Chhattisgarh | Trust and Society | ₹ 1,000,000 | **59.1** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 239 days. | 🟠 Duplicate check: Potentially similar work detected (Similarity: 70.6%). Requires human verification. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18062/2026-2027/156112-Construction of community centers and community halls | Haryana | Trust and Society | ₹ 498,031 | **57.9** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 530 days. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18216/2025-2026/169817-Construction of rooms and halls in school and colleges | Uttar Pradesh | Trust and Society | ₹ 1,000,000 | **57.6** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 402 days. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18271/2025-2026/196965-Construction of community centers and community halls | West Bengal | Repair and Renovation | ₹ 5,000,000 | **57.0** | Medium | 🟠 Duplicate check: Potentially similar work detected (Similarity: 92.1%). Requires human verification. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18064/2025-2026/150852-Construction of community centers and community halls | Haryana | Trust and Society | ₹ 1,100,000 | **56.6** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 301 days. | 🟠 Category signal: Special entity category 'Trust and Society'. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP243/2025-2026/141110-Construction of rooms and halls in school and colleges | West Bengal | Normal/Others | ₹ 11,000,000 | **56.2** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 436 days. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |
| WS/MP18216/2025-2026/169821-Construction of rooms and halls in school and colleges | Uttar Pradesh | Trust and Society | ₹ 1,000,000 | **56.1** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 402 days. | 🟠 Category signal: Special entity category 'Trust and Society'. |
| WS/MP552/2025-2026/163255-Construction of additional rooms and halls in the existing public and community building | Bihar | Repair and Renovation | ₹ 1,487,117 | **55.9** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 263 days. | 🟠 Duplicate check: Potentially similar work detected (Similarity: 86.0%). Requires human verification. |
| WS/MP18249/2025-2026/153601-Construction of rooms and facilities for hospitals, FWC , PHC Centers and ANM centers | West Bengal | Normal/Others | ₹ 20,000,000 | **55.7** | Medium | 🔴 Delay anomaly: Recommendation-to-sanction lag of 270 days. | 🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest. |

---

## 4. Generated Artifacts & Reports

- **Duplicate Candidate Pairs**: `ml/outputs/duplicate_candidates.csv`
- **MP Fund Utilization**: `ml/outputs/mp_fund_utilization.csv`
- **Fund Summary Report**: `ml/outputs/fund_utilization_summary.md`
- **V2 Full Scored Projects**: `ml/outputs/v2_scored_projects.csv`
- **V2 High-Risk Projects**: `ml/outputs/v2_high_risk_projects.csv`
- **Visualization Plots**: `ml/outputs/plots/` (`06_composite_risk_distribution.png`, `07_duplicate_similarity_distribution.png`, `08_mp_utilization_distribution.png`)
