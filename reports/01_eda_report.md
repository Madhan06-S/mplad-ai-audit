# Exploratory Data Analysis (EDA) Report — MPLAD AI Audit (SIH26102)

## 1. Executive Summary

This report presents a full empirical data audit and Exploratory Data Analysis (EDA) of the official MPLADS (Members of Parliament Local Area Development Scheme) datasets provided for SIH26102. 

The analysis was performed without synthetic data generation, fake fraud assumptions, or preliminary model training. All findings are derived directly from inspecting raw CSV files using Python, Pandas, and NumPy.

---

## 2. Dataset Overview

| Dataset File Name | Row Count (Raw) | Valid Data Rows | Columns | File Size | Description |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Works Sanctioned (1).csv** | 33,001 | **33,000** | 12 | 11.45 MB | Complete dataset of works sanctioned across India (Primary dataset for ML). |
| **Works Sanctioned.csv** | 11,001 | **11,000** | 12 | 3.81 MB | Earlier export of works sanctioned (Exact subset of Works Sanctioned (1).csv). |
| **Allocated Limit for Honble MPs.csv** | 544 | **544** | 5 | 36.1 KB | MP-wise fund allocation limits containing Lok Sabha & Rajya Sabha MPs with Constituency details. |
| **Allocated Limit for Honble MPs (1).csv** | 232 | **232** | 5 | 21.3 KB | MP-wise fund allocation limits containing Nominated / Special category MPs. |
| **Amount consented for Calamity (2).csv** | 13 | **13** | 6 | 1.3 KB | MP recommendations for relief funds allocated towards natural calamities (Floods, Landslides). |

---

## 3. Dataset Comparison & Overlap Analysis

### 3.1 Works Sanctioned vs. Works Sanctioned (1)
- **Schema**: Both files share identical column names and structures.
- **Overlap**: **100% (11,000 rows)** of `Works Sanctioned.csv` exist with exact character-for-character matching inside `Works Sanctioned (1).csv`.
- **Finding**: `Works Sanctioned (1).csv` is the updated, expanded master dataset (33,000 records). `Works Sanctioned.csv` (11,000 records) is an earlier version snapshot.
- **Action**: Use **`Works Sanctioned (1).csv`** as the primary ground-truth works dataset to prevent duplicate processing.

### 3.2 Allocated Limit files
- **Allocated Limit for Honble MPs.csv** (544 rows): Includes columns `State`, `Hon'ble Members of Parliaments`, `Constituency`, `Allocated AMOUNT ( ₹ )`.
- **Allocated Limit for Honble MPs (1).csv** (232 rows): Includes columns `State`, `Hon'ble Members of Parliament`, `Elected/Nominated`, `Allocated AMOUNT ( ₹ )`.
- **Finding**: These datasets complement each other. One covers elected MPs with constituency mapping (544 MPs), while the other covers nominated/other MPs (232 MPs). Combined, they cover **776 MPs**.

---

## 4. Deep-Dive Analysis: Works Sanctioned Dataset (33,000 records)

### 4.1 Schema & Columns

| Column Name | Raw Data Type | Inferred Type | Null Count | Missing % | Unique Values |
| :--- | :--- | :--- | :---: | :---: | :---: |
| `Sr. No.` | Object / String | Identifier | 0 | 0.0% | 33,001 |
| `Work category` | Object / String | Categorical | 0 | 0.0% | 5 |
| `Work` | Object / String | Primary Key / ID | 0 | 0.0% | 33,001 |
| `State` | Object / String | Categorical | 0 | 0.0% | 34 |
| `IDA` | Object / String | Categorical | 0 | 0.0% | 649 |
| `Hon'ble Members of Parliament` | Object / String | Categorical | 0 | 0.0% | 490 |
| `Constituency` | Object / String | Categorical | 0 | 0.0% | 490 |
| `Work description` | Object / String | Free Text | 83 | 0.25% | 30,286 |
| `Recommended date` | Object / String | Datetime | 0 | 0.0% | 335 |
| `Sanction Date` | Object / String | Datetime | 0 | 0.0% | 619 |
| `Sanction Amount ( ₹ )` | Object / String | Numeric (Float) | 0 | 0.0% | 8,075 |
| `Work Status` | Object / String | Categorical | 0 | 0.0% | 7 |

---

### 4.2 Categorical Field Breakdown

#### Work Status Distribution
- **Physical Inspection**: 19,927 (60.38%)
- **Sanction**: 3,938 (11.93%)
- **Vendor Identification**: 3,814 (11.56%)
- **Work partially Completed**: 2,711 (8.22%)
- **Work Completed**: 2,416 (7.32%)
- **Time Estimation**: 194 (0.59%)
- *Corrupt Summary Row Value*: 1 (0.003%)

#### Work Category Distribution
- **Normal/Others**: 32,346 (98.02%)
- **Repair and Renovation**: 466 (1.41%)
- **Trust and Society**: 187 (0.57%)
- **Bar and Associations**: 1
- *Whitespace / Empty*: 1

#### Geographic Breakdown
- **States Covered**: 34 States/UTs (Top: Uttar Pradesh with 6,964 works, Madhya Pradesh with 2,672, Gujarat with 2,571, West Bengal with 2,400, Tamil Nadu with 1,804).
- **IDAs (Implementing Agencies)**: 649 unique IDAs (e.g., `DEPUTY COMMISSIONER DHARWAR_IDA`).
- **MPs Covered**: 490 unique Members of Parliament.
- **Constituencies Covered**: 490 unique Constituencies.

---

### 4.3 Monetary Analysis (`Sanction Amount ( ₹ )`)

- **Total Sanctioned Amount across all works**: **₹ 17,171,955,577.55** (~ ₹ 1,717.2 Crores)
- **Minimum Sanction Amount**: **₹ 10,000.00**
- **Maximum Sanction Amount**: **₹ 47,472,048.00** (~ ₹ 4.74 Crores)
- **Mean Sanction Amount**: **₹ 520,362.29** (~ ₹ 5.2 Lakhs)
- **Median Sanction Amount**: **₹ 300,000.00** (~ ₹ 3.0 Lakhs)
- **Standard Deviation**: **₹ 842,150.12**
- **IQR (Interquartile Range)**: ₹ 350,000.00 (Q25: ₹ 150,000.00, Q75: ₹ 500,000.00)
- **Statistical Outliers (> 1.5 IQR)**: 2,845 works (8.62% of works exceed ₹ 1,025,000.00)

---

### 4.4 Date & Delay Analysis

- **Recommended Date Span**: 08-Jul-2024 to 06-Feb-2026
- **Sanction Date Span**: 09-Jul-2024 to 25-Aug-2026
- **Sanction Delay (Sanction Date minus Recommended Date)**:
  - **Minimum Delay**: 0 days (Same-day sanction)
  - **Maximum Delay**: 732 days (~2 years)
  - **Mean Delay**: **122.7 days** (~4 months)
  - **Median Delay**: **91.0 days** (~3 months)
  - **Severe Delays (> 365 days)**: **1,550 works (4.70%)**
  - **Negative Delays**: 0 (No sanction pre-dates recommendation)

---

## 5. Key Empirical Observations for AI/ML

1. **High Text Granularity**: `Work description` has 30,286 unique texts out of 33,000 records. This rich natural language text enables TF-IDF / Embeddings cosine similarity to detect duplicate work recommendations and split billing.
2. **Heavy Cost Outliers**: 8.62% of works exceed 1.5 IQR upper fence, and extreme single-work sanctions reach ₹ 4.74 Crores. Grouping by `Work category` + `State` / `IDA` is essential for normalizing cost anomalies.
3. **Severe Sanction Delays**: Over 1,500 works experience delays exceeding 1 full year between recommendation and sanction date.
4. **Category Skew**: 98% of works fall under "Normal/Others". Category-specific anomalies (e.g., Trust and Society, Bar and Associations) require specialized risk weighting.
