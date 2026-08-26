# Recommended ML Targets & Feature Engineering — MPLAD AI Audit (SIH26102)

## 1. Feasible AI/ML Tasks Derived from Actual Data

Based on empirical data inspection, 6 realistic AI/ML tasks can be formulated from the available fields without assuming ground-truth fraud labels.

```
                   ┌──────────────────────────────────────────────┐
                   │           Ground-Truth CSV Data              │
                   └──────────────────────┬───────────────────────┘
                                          │
    ┌──────────────────┬──────────────────┼──────────────────┬──────────────────┐
    ▼                  ▼                  ▼                  ▼                  ▼
1. Cost Anomaly   2. Delay Risk    3. Duplicate Work    4. Fund Outliers  5. Category Risk
 (Z-Score / IQR) (Sanction Lag)  (TF-IDF/MinHash)  (MP Utilization)   (Trust/Renovation)
    │                  │                  │                  │                  │
    └──────────────────┴──────────────────┼──────────────────┴──────────────────┘
                                          │
                                          ▼
                         6. Composite Risk Score Engine
                                (0 - 100 Index)
```

---

## 2. Detailed ML Tasks & Targets

### Task 1: Cost Anomaly Detection (Unsupervised)
- **Objective**: Flag works whose sanction amount significantly deviates from expected norms for that specific work description, category, or state.
- **Target Variable**: `cost_anomaly_score` (Continuous float [0, 1] or Binary flag).
- **Rationale**: Single works range from ₹ 10,000 to ₹ 4.74 Crores. Standardizing cost relative to category and state exposes disproportionate allocations.

### Task 2: Project Delay & Timeline Anomaly Detection
- **Objective**: Flag works experiencing abnormal delay between recommendation date and sanction date.
- **Target Variable**: `sanction_delay_days` (Continuous int) & `delay_anomaly_score` (Continuous float [0, 1]).
- **Rationale**: 1,550 works (>4.7%) experience over 365 days lag before approval. Extreme delays signal administrative bottlenecks or delayed sanction risks.

### Task 3: Duplicate / Split Work Detection (NLP / Fuzzy Matching)
- **Objective**: Detect duplicate work descriptions or split-billing tactics (e.g., splitting a ₹ 15 Lakh project into three ₹ 5 Lakh sanctions to bypass approval thresholds).
- **Target Variable**: `text_similarity_score` (Float [0, 1]) & `is_potential_duplicate` (Boolean).
- **Rationale**: 30,286 text descriptions exist. Clustering work descriptions by MP / Constituency / IDA with high TF-IDF / Cosine similarity identifies identical or repetitive work entries.

### Task 4: Fund Utilization Anomaly Detection
- **Objective**: Compare cumulative sanctions by MP against their entitlement limits (`Allocated Limit`).
- **Target Variable**: `mp_utilization_pct` (Float [%]) & `over_allocation_risk` (Boolean).
- **Rationale**: Identifies MPs exceeding or rapidly exhausting their 5-year entitlement threshold.

### Task 5: Work Category Risk Scoring
- **Objective**: Identify high-risk work categories (e.g., "Trust and Society", "Bar and Associations") vs standard public infrastructure ("Normal/Others").
- **Target Variable**: `category_risk_weight` (Categorical risk multiplier: 1.0x to 2.5x).
- **Rationale**: Funds allocated to private trusts/societies carry higher compliance oversight requirements under MPLADS guidelines.

### Task 6: Overall Project Risk Scoring (Composite Risk Engine)
- **Objective**: Compute a unified Risk Score (0–100) per work item combining all 5 individual risk dimensions.
- **Target Index Formula**:

$$\text{Composite Risk Score} = w_1 \cdot \text{CostRisk} + w_2 \cdot \text{DelayRisk} + w_3 \cdot \text{DupRisk} + w_4 \cdot \text{UtilRisk} + w_5 \cdot \text{CatRisk}$$

---

## 3. Recommended Feature Matrix

| Feature Name | Source Column(s) | Calculation / Transformation | ML Purpose |
| :--- | :--- | :--- | :--- |
| `sanction_amount_log` | `Sanction Amount ( ₹ )` | $\log(1 + \text{amount})$ | Normalizes skewed monetary distribution |
| `cost_zscore_by_category` | `Sanction Amount`, `Work category` | $\frac{x - \mu_{\text{cat}}}{\sigma_{\text{cat}}}$ | Standardized cost variance within category |
| `cost_zscore_by_state` | `Sanction Amount`, `State` | $\frac{x - \mu_{\text{state}}}{\sigma_{\text{state}}}$ | Standardized cost variance within state |
| `sanction_delay_days` | `Recommended date`, `Sanction Date` | $\text{Sanction Date} - \text{Recommended date}$ | Quantifies administrative approval delay |
| `delay_zscore_by_ida` | `sanction_delay_days`, `IDA` | $\frac{\text{delay} - \mu_{\text{ida}}}{\sigma_{\text{ida}}}$ | Identifies sluggish implementing agencies |
| `desc_tfidf_vector` | `Work description` | TF-IDF (1,3-grams) on cleaned text | Semantic representation for duplicate detection |
| `desc_char_length` | `Work description` | $\text{len}(\text{text})$ | Identifies vague or minimal work descriptions |
| `is_trust_society` | `Work category` | $1 \text{ if category == 'Trust and Society' else } 0$ | High-risk entity indicator |
| `mp_total_sanctioned_amt` | `Hon'ble Members of Parliament` | $\sum \text{Sanction Amount for MP}$ | Cumulative MP spending |
| `mp_utilization_ratio` | `mp_total_sanctioned_amt`, `Allocated Limit` | $\frac{\text{mp\_total\_sanctioned\_amt}}{\text{allocated\_limit}}$ | Fund exhaustion ratio |
