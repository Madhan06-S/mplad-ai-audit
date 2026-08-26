import os
import sys
import glob
import json
import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def inspect_dataset(file_path):
    filename = os.path.basename(file_path)
    print(f"\n==================================================")
    print(f"INSPECTING: {filename}")
    print(f"==================================================")
    
    df = pd.read_csv(file_path)
    rows, cols = df.shape
    print(f"Shape: {rows} rows, {cols} columns")
    
    # Missing values
    missing = df.isnull().sum()
    missing_pct = (missing / rows) * 100
    
    # Duplicates
    dup_rows = df.duplicated().sum()
    print(f"Duplicate rows: {dup_rows} ({(dup_rows/rows)*100:.2f}%)")
    
    col_info = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        null_cnt = int(missing[col])
        null_pct = float(missing_pct[col])
        n_unique = int(df[col].nunique(dropna=True))
        
        sample_vals = df[col].dropna().unique()[:5].tolist()
        
        col_summary = {
            "column": col,
            "dtype": dtype,
            "null_count": null_cnt,
            "null_pct": round(null_pct, 2),
            "n_unique": n_unique,
            "sample_values": [str(v) for v in sample_vals]
        }
        col_info.append(col_summary)
        print(f" - [{col}] ({dtype}): {null_cnt} missing ({null_pct:.1f}%), {n_unique} unique. Samples: {sample_vals[:3]}")
    
    return {
        "filename": filename,
        "rows": rows,
        "cols": cols,
        "duplicate_rows": dup_rows,
        "columns": col_info,
        "dataframe": df
    }

def analyze_works_sanctioned(df, name):
    print(f"\n--- Specific Analysis for {name} ---")
    print("Columns:", list(df.columns))
    
    # Clean monetary columns if string
    for col in df.columns:
        if 'amount' in col.lower() or 'cost' in col.lower() or 'sanction' in col.lower() or 'limit' in col.lower():
            if df[col].dtype == 'object':
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.replace('₹', '').str.strip(), errors='coerce')
    
    # Analyze Monetary stats
    monetary_cols = [c for c in df.columns if df[c].dtype in ['int64', 'float64']]
    for mcol in monetary_cols:
        series = df[mcol].dropna()
        if len(series) > 0:
            q25, q75 = series.quantile(0.25), series.quantile(0.75)
            iqr = q75 - q25
            outliers = series[(series < (q25 - 1.5 * iqr)) | (series > (q75 + 1.5 * iqr))]
            print(f"\nMonetary/Numeric Stats [{mcol}]:")
            print(f"  Count: {len(series)}")
            print(f"  Min: {series.min():,.2f}")
            print(f"  Max: {series.max():,.2f}")
            print(f"  Mean: {series.mean():,.2f}")
            print(f"  Median: {series.median():,.2f}")
            print(f"  Std: {series.std():,.2f}")
            print(f"  IQR Outliers count (>1.5 IQR): {len(outliers)} ({len(outliers)/len(series)*100:.2f}%)")
            print(f"  Zero values: {(series == 0).sum()}")
            print(f"  Negative values: {(series < 0).sum()}")

    # Analyze Categorical columns
    cat_cols = [c for c in df.columns if df[c].dtype == 'object']
    for ccol in cat_cols:
        print(f"\nCategorical Breakdown [{ccol}]: Top 7")
        print(df[ccol].value_counts(dropna=False).head(7))

    # Analyze Date columns
    date_cols = [c for c in df.columns if 'date' in c.lower() or 'year' in c.lower()]
    for dcol in date_cols:
        parsed = pd.to_datetime(df[dcol], errors='coerce', dayfirst=True)
        valid_cnt = parsed.notnull().sum()
        invalid_cnt = parsed.isnull().sum() - df[dcol].isnull().sum()
        print(f"\nDate Column [{dcol}]:")
        print(f"  Valid dates: {valid_cnt}, Invalid parsed: {invalid_cnt}, Missing: {df[dcol].isnull().sum()}")
        if valid_cnt > 0:
            print(f"  Min Date: {parsed.min()}")
            print(f"  Max Date: {parsed.max()}")

    # Check Sanction Date vs Recommended Date delay
    rec_col = [c for c in df.columns if 'recommend' in c.lower()]
    sanc_col = [c for c in df.columns if 'sanction' in c.lower() and 'date' in c.lower()]
    if rec_col and sanc_col:
        rec_dt = pd.to_datetime(df[rec_col[0]], errors='coerce', dayfirst=True)
        sanc_dt = pd.to_datetime(df[sanc_col[0]], errors='coerce', dayfirst=True)
        delay_days = (sanc_dt - rec_dt).dt.days
        valid_delay = delay_days.dropna()
        print(f"\n--- Delay Analysis (Sanction Date - Recommended Date) ---")
        print(f"  Valid pairs: {len(valid_delay)}")
        print(f"  Min Delay (days): {valid_delay.min()}")
        print(f"  Max Delay (days): {valid_delay.max()}")
        print(f"  Mean Delay (days): {valid_delay.mean():.1f}")
        print(f"  Median Delay (days): {valid_delay.median():.1f}")
        print(f"  Negative delays (Sanction before recommendation): {(valid_delay < 0).sum()}")
        print(f"  Delays > 365 days: {(valid_delay > 365).sum()}")
        print(f"  Delays > 1000 days: {(valid_delay > 1000).sum()}")

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

def main():
    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    print("Found CSV files:", [os.path.basename(f) for f in csv_files])
    
    results = {}
    dataframes = {}
    
    for fpath in sorted(csv_files):
        fname = os.path.basename(fpath)
        info = inspect_dataset(fpath)
        results[fname] = info
        dataframes[fname] = info.pop("dataframe", None) if "dataframe" in info else pd.read_csv(fpath)
        analyze_works_sanctioned(dataframes[fname], fname)
        
    # Dataset Comparison & Overlap Check
    print("\n==================================================")
    print("DATASET COMPARISON & OVERLAP CHECK")
    print("==================================================")
    
    # 1. Works Sanctioned vs Works Sanctioned (1)
    ws1_name = "Works Sanctioned.csv"
    ws2_name = "Works Sanctioned (1).csv"
    if ws1_name in dataframes and ws2_name in dataframes:
        df1 = dataframes[ws1_name]
        df2 = dataframes[ws2_name]
        print(f"\nComparing {ws1_name} ({len(df1)} rows) vs {ws2_name} ({len(df2)} rows):")
        print(f"  Columns match: {list(df1.columns) == list(df2.columns)}")
        if list(df1.columns) != list(df2.columns):
            print(f"  Columns in {ws1_name}: {list(df1.columns)}")
            print(f"  Columns in {ws2_name}: {list(df2.columns)}")
        
        # Check subset / duplicate rows between files
        common_cols = [c for c in df1.columns if c in df2.columns]
        merged = pd.merge(df1[common_cols], df2[common_cols], how='inner', on=common_cols)
        print(f"  Exact overlapping rows between both files: {len(merged)}")
        print(f"  Overlap ratio with {ws1_name}: {len(merged)/len(df1)*100:.2f}%")
        print(f"  Overlap ratio with {ws2_name}: {len(merged)/len(df2)*100:.2f}%")

    # 2. Allocated Limit vs Allocated Limit (1)
    al1_name = "Allocated Limit for Honble MPs.csv"
    al2_name = "Allocated Limit for Honble MPs (1).csv"
    if al1_name in dataframes and al2_name in dataframes:
        df1 = dataframes[al1_name]
        df2 = dataframes[al2_name]
        print(f"\nComparing {al1_name} ({len(df1)} rows) vs {al2_name} ({len(df2)} rows):")
        print(f"  Columns match: {list(df1.columns) == list(df2.columns)}")
        print(f"  Columns in {al1_name}: {list(df1.columns)}")
        print(f"  Columns in {al2_name}: {list(df2.columns)}")

    # Save metadata JSON for reporting
    with open(os.path.join(REPORTS_DIR, "eda_summary.json"), "w") as f:
        json.dump(results, f, indent=2, cls=NpEncoder)
    print(f"\nSaved EDA Summary JSON to {os.path.join(REPORTS_DIR, 'eda_summary.json')}")

if __name__ == "__main__":
    main()
