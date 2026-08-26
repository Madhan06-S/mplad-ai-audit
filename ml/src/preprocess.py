import os
import pandas as pd
import numpy as np

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """
    Loads raw Works Sanctioned CSV dataset, performs data cleaning, date parsing,
    sanitizes string values, and handles missing values safely.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at path: {file_path}")
        
    df = pd.read_csv(file_path)
    print(f"[Preprocessing] Raw rows loaded: {len(df)}")
    
    # 1. Remove summary row ("Grand Total")
    if 'Sr. No.' in df.columns:
        df = df[df['Sr. No.'].astype(str).str.strip().str.lower() != 'grand total'].copy()
    print(f"[Preprocessing] Rows after dropping 'Grand Total' summary row: {len(df)}")
    
    # 2. String sanitization (strip whitespace, tab chars, non-breaking spaces \xa0)
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.replace('\xa0', ' ', regex=False)
        df[col] = df[col].str.replace('\t', ' ', regex=False)
        df[col] = df[col].str.strip()
        
    # 3. Clean monetary values: Sanction Amount ( ₹ ) -> float
    amt_col = 'Sanction Amount ( ₹ )'
    if amt_col in df.columns:
        df['sanction_amount'] = pd.to_numeric(
            df[amt_col].astype(str).str.replace(',', '').str.replace('₹', '').str.strip(),
            errors='coerce'
        )
    else:
        raise KeyError(f"Expected column '{amt_col}' not found in dataset.")
        
    # Drop records where sanction amount is missing/invalid
    df = df.dropna(subset=['sanction_amount']).copy()
    
    # 4. Parse dates: Recommended date & Sanction Date
    rec_col = 'Recommended date'
    sanc_col = 'Sanction Date'
    
    df['recommended_dt'] = pd.to_datetime(df[rec_col], errors='coerce', dayfirst=True)
    df['sanction_dt'] = pd.to_datetime(df[sanc_col], errors='coerce', dayfirst=True)
    
    # 5. Compute sanction_delay_days
    df['sanction_delay_days'] = (df['sanction_dt'] - df['recommended_dt']).dt.days
    
    # Fill missing dates/delays with median delay if any parsing failed
    median_delay = df['sanction_delay_days'].median()
    if pd.isna(median_delay):
        median_delay = 0
    df['sanction_delay_days'] = df['sanction_delay_days'].fillna(median_delay)
    
    # Ensure delay is non-negative
    df['sanction_delay_days'] = df['sanction_delay_days'].clip(lower=0)
    
    # 6. Safely handle missing Work description
    desc_col = 'Work description'
    if desc_col in df.columns:
        df['work_description_clean'] = df[desc_col].replace({'nan': np.nan, 'NaN': np.nan, '': np.nan})
        df['work_description_clean'] = df['work_description_clean'].fillna(df['Work'])
    else:
        df['work_description_clean'] = df['Work']
        
    # Rename key columns for clean downstream code
    df['work_category'] = df['Work category']
    df['state'] = df['State']
    df['ida'] = df['IDA']
    df['mp_name'] = df["Hon'ble Members of Parliament"]
    df['constituency'] = df['Constituency']
    df['work_status'] = df['Work Status']
    df['work_id'] = df['Work']
    
    print(f"[Preprocessing] Cleaning completed successfully. Final records: {len(df)}")
    return df

if __name__ == "__main__":
    import sys
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "Works Sanctioned (1).csv")
    cleaned_df = load_and_clean_data(data_path)
    print(cleaned_df[['work_id', 'sanction_amount', 'sanction_delay_days', 'work_status']].head())
