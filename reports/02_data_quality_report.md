# Data Quality Audit Report — MPLAD AI Audit (SIH26102)

## 1. Data Quality Overview

A complete data quality inspection was conducted on all 5 CSV datasets. Below is the summary of data health, anomalies, and structural integrity issues identified.

---

## 2. Issues & Data Health Summary

### 2.1 Critical Quality Findings

#### Finding 1: Summary / Grand Total Row Appended inside CSVs (High Impact)
- **Affected Datasets**: `Works Sanctioned (1).csv` (Row 33,001) & `Works Sanctioned.csv` (Row 11,001).
- **Symptom**: The final row contains `'Grand Total'` in `Sr. No.` and places the overall sum string `'40,98,62,08,842.08'` in the `Work Status` column. All other columns contain non-breaking spaces (`\xa0`).
- **Impact**: Parsing `Work Status` as a categorical column or numeric coercion without filtering this row will inject corrupt categories and skew numerical aggregations.
- **Remediation**: Filter out any row where `Sr. No.` equals `'Grand Total'` or where `Work Status` starts with numeric characters.

#### Finding 2: Missing Values in Text Description (Medium Impact)
- **Affected Dataset**: `Works Sanctioned (1).csv` (83 missing rows = 0.25%).
- **Impact**: Duplicate detection models relying on `Work description` will encounter `NaN` values.
- **Remediation**: Impute missing descriptions with `Work` title or string placeholder `"[NO DESCRIPTION PROVIDED]"`.

#### Finding 3: Whitespace & Special Character Inconsistencies (Medium Impact)
- **Affected Columns**: `Work`, `Calamity Type`, `Work category`.
- **Symptom**: Non-breaking spaces (`\xa0`) and tab characters (`WS/\t MP620/...`) exist inside string identifiers and category names.
- **Remediation**: Strip leading/trailing whitespace, replace `\xa0` with standard spaces, and sanitize tab characters (`\t`).

#### Finding 4: Scheme/Format Inconsistency in Allocated Limits (Low Impact)
- **Affected Datasets**: `Allocated Limit for Honble MPs.csv` vs `Allocated Limit for Honble MPs (1).csv`.
- **Symptom**: Column name in file 1 is `"Hon'ble Members of Parliaments"` (plural) vs `"Hon'ble Members of Parliament"` (singular) in file 2. File 1 uses `Constituency` while file 2 uses `Elected/Nominated`.
- **Remediation**: Standardize column names to `"mp_name"`, `"state"`, `"constituency"`, `"mp_type"`, `"allocated_amount"`.

---

## 3. Detailed Data Quality Metrics Matrix

| Dataset | Missing Values Count (%) | Duplicate Rows Count | Corrupt Summary Rows | String Cleanliness | Date Parseability |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Works Sanctioned (1).csv** | 83 (0.25% in desc) | 0 | 1 row | Tab chars (`\t`) in Work ID, non-breaking spaces | 100% valid (dd-Mon-yyyy format) |
| **Works Sanctioned.csv** | 44 (0.40% in desc) | 0 | 1 row | Tab chars (`\t`) in Work ID, non-breaking spaces | 100% valid |
| **Allocated Limit MPs** | 0 (0.00%) | 0 | 0 | Clean strings, plural column header | N/A |
| **Allocated Limit MPs (1)** | 0 (0.00%) | 0 | 0 | Clean strings, `Elected/Nominated` column | N/A |
| **Calamity Consented** | 0 (0.00%) | 0 | 0 | `\xa0` in Calamity Type for 1 row | 100% valid |

---

## 4. Ground-Truth Data Cleaning Protocol

Prior to feature engineering and ML execution, the following 5-step pipeline must be applied:

```
[Raw CSV] 
   │
   ▼
1. Drop Summary Rows (`Sr. No. == 'Grand Total'`)
   │
   ▼
2. Sanitize Strings (Strip `\xa0`, `\t`, extra spaces, standardize column names)
   │
   ▼
3. Coerce Numeric (Strip '₹', ',', convert `Sanction Amount` & `Allocated Amount` to Float64)
   │
   ▼
4. Parse Dates (Convert `Recommended date` & `Sanction Date` using `%d-%b-%Y` to datetime64)
   │
   ▼
5. Handle Nulls (Fill missing `Work description` with `Work` column string)
   │
   ▼
[Cleaned & Validated DataFrame]
```
