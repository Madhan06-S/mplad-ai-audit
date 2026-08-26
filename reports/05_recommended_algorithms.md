# Recommended Algorithms & Technical Rationale — MPLAD AI Audit (SIH26102)

## 1. Algorithm Selection Strategy

Because the MPLADS dataset lacks pre-existing fraud labels ("unsupervised domain"), traditional supervised classification (e.g., binary cross-entropy logistic regression or standard neural nets) cannot be trained directly without producing biased or synthetic labels.

Instead, we recommend an **Unsupervised Ensemble Anomaly & NLP Pipeline** backed by **Explainable AI (XAI)**.

---

## 2. Recommended Algorithm Suite

```
                               ┌───────────────────────────────────┐
                               │     Feature Encoded Vectors       │
                               └─────────────────┬─────────────────┘
                                                 │
            ┌────────────────────────────────────┼────────────────────────────────────┐
            ▼                                    ▼                                    ▼
┌───────────────────────┐            ┌───────────────────────┐            ┌───────────────────────┐
│   Isolation Forest    │            │ Local Outlier Factor  │            │ TF-IDF + Cosine Sim / │
│ (Global Cost & Delay) │            │ (Local Density Anom.) │            │    MinHash LSH (NLP)  │
└───────────┬───────────┘            └───────────┬───────────┘            └───────────┬───────────┘
            │                                    │                                    │
            └────────────────────────────────────┼────────────────────────────────────┘
                                                 │
                                                 ▼
                               ┌───────────────────────────────────┐
                               │  Composite Risk Scoring Engine    │
                               │       (Weighted Score 0-100)      │
                               └─────────────────┬─────────────────┘
                                                 │
                                                 ▼
                               ┌───────────────────────────────────┐
                               │      SHAP / LIME Explainability   │
                               │    ("Why is this high risk?")     │
                               └───────────────────────────────────┘
```

---

## 3. Algorithm Deep-Dive & Justification

### 1. Isolation Forest (`sklearn.ensemble.IsolationForest`)
- **Use Case**: Global Cost & Delay Anomaly Detection.
- **Why Chosen**: 
  - Sub-samples data and isolates anomalies using random attribute splits. Anomalies require fewer splits (shorter path lengths) to isolate.
  - Highly efficient $O(n \log n)$ time complexity on 33,000 records.
  - Robust to high-dimensional multi-feature outlier detection.

### 2. Local Outlier Factor (`sklearn.neighbors.LocalOutlierFactor`)
- **Use Case**: Local Density Anomaly Detection (Comparing a project's cost/delay to its k-nearest neighbors within the same state/IDA).
- **Why Chosen**: 
  - Captures localized contextual anomalies (e.g., a ₹ 50 Lakh school building in a small rural district where average cost is ₹ 5 Lakhs, even if ₹ 50 Lakhs is normal in a metro state).
  - Complements Isolation Forest's global view with local spatial/district density checks.

### 3. TF-IDF Vectorization + Cosine Similarity / MinHash LSH (`sklearn.feature_extraction.text.TfidfVectorizer`)
- **Use Case**: Duplicate Work & Split-Billing Detection.
- **Why Chosen**: 
  - Converts 30,286 text descriptions into sparse n-gram term frequency vectors.
  - Cosine similarity > 0.85 between works under the same MP or Constituency flags potential duplicate recommendations or split billing.

### 4. SHAP (SHapley Additive exPlanations) (`shap.TreeExplainer` / `shap.KernelExplainer`)
- **Use Case**: Risk Explanation & Audit Reporting ("Why is Risk = 87/100?").
- **Why Chosen**: 
  - Provides exact game-theoretic feature attribution.
  - Breaks down the risk score into human-readable factors (e.g., `+35 points` due to unusual sanction amount, `+25 points` due to 450-day delay, `+20 points` due to 92% similarity with work #133166).

---

## 4. Evaluation Metrics for Unsupervised Setup

1. **Precision@K (Audit Top-K)**: Percent of top K flagged high-risk works verified as true anomalies by domain audit standards.
2. **Silhouette Score**: Evaluates cluster separation for text similarity and local density groupings.
3. **Inter-Algorithm Agreement (Consensus Score)**: Overlap ratio between Isolation Forest top 5% anomalies and LOF top 5% anomalies.
