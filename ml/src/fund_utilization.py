import os
import re
import numpy as np
import pandas as pd

class FundUtilizationTracker:
    """
    Module 2: MP Fund Utilization Monitor.
    Calculates allocation vs total sanctioned amount, utilization percentage,
    remaining amount, and flags allocation alerts.
    """
    def __init__(self):
        pass

    @staticmethod
    def normalize_mp_name(name: str) -> str:
        """
        Normalizes MP name by removing honorifics, titles, punctuation, and extra spaces.
        """
        if pd.isna(name) or not str(name).strip():
            return ""
        s = str(name).strip()
        # Remove common honorific titles
        titles = [
            r'\bshri\b', r'\bsmt\b', r'\bdr\b', r'\ber\b', r'\bprof\b', r'\bsh\b',
            r'\bkm\b', r'\badv\b', r'\bjustice\b', r'\bgen\b', r'\blt\b', r'\bhon\'ble\b',
            r'\bhonble\b', r'\bmp\b', r'\bms\b', r'\bmr\b', r'\bmrs\b'
        ]
        s_lower = s.lower()
        for title in titles:
            s_lower = re.sub(title, '', s_lower)
            
        s_lower = re.sub(r'[^\w\s]', ' ', s_lower)
        s_lower = re.sub(r'\s+', ' ', s_lower).strip()
        return s_lower

    def process_fund_utilization(
        self,
        df_works: pd.DataFrame,
        al1_path: str,
        al2_path: str
    ) -> tuple[pd.DataFrame, dict[str, float]]:
        """
        Loads allocation limit CSVs, matches MP records, and calculates utilization metrics.
        
        Returns:
            df_mp_util: Summary DataFrame per MP
            mp_util_scores: Dict mapping normalized MP name -> fund utilization score (0-100)
        """
        print("[FundUtilization] Loading allocation datasets...")
        df_al1 = pd.read_csv(al1_path)
        df_al2 = pd.read_csv(al2_path)

        # Helper to clean allocated amount
        def clean_amt(s):
            return pd.to_numeric(s.astype(str).str.replace(',', '').str.replace('₹', '').str.strip(), errors='coerce')

        df_al1['allocated_amt'] = clean_amt(df_al1['Allocated AMOUNT ( ₹ )'])
        df_al1['mp_name_raw'] = df_al1["Hon'ble Members of Parliaments"] if "Hon'ble Members of Parliaments" in df_al1.columns else df_al1["Hon'ble Members of Parliament"]
        df_al1['mp_norm'] = df_al1['mp_name_raw'].apply(self.normalize_mp_name)

        df_al2['allocated_amt'] = clean_amt(df_al2['Allocated AMOUNT ( ₹ )'])
        df_al2['mp_name_raw'] = df_al2["Hon'ble Members of Parliament"]
        df_al2['mp_norm'] = df_al2['mp_name_raw'].apply(self.normalize_mp_name)

        # Combine allocation limits
        al_combined = pd.concat([
            df_al1[['mp_name_raw', 'mp_norm', 'State', 'allocated_amt']],
            df_al2[['mp_name_raw', 'mp_norm', 'State', 'allocated_amt']]
        ], ignore_index=True)

        # Drop duplicates in allocation list keeping max allocation
        al_combined = al_combined.sort_values(by='allocated_amt', ascending=False).drop_duplicates(subset=['mp_norm']).copy()
        print(f"[FundUtilization] Total unique allocation MP entries loaded: {len(al_combined)}")

        # Group works by MP
        df_w = df_works.copy()
        df_w['mp_norm'] = df_w['mp_name'].apply(self.normalize_mp_name)

        mp_works_stats = df_w.groupby('mp_norm').agg(
            mp_name_works=('mp_name', 'first'),
            state=('state', 'first'),
            total_sanctioned_amount=('sanction_amount', 'sum'),
            number_of_works=('sanction_amount', 'count'),
            average_work_amount=('sanction_amount', 'mean'),
            maximum_work_amount=('sanction_amount', 'max')
        ).reset_index()

        # Merge allocation data with works stats
        merged = pd.merge(mp_works_stats, al_combined[['mp_norm', 'allocated_amt']], on='mp_norm', how='left')

        # Fallback allocation if missing (default 5 Crores = ₹ 50,000,000 for 5-year term)
        DEFAULT_ALLOCATION = 50000000.0
        merged['allocated_amount'] = merged['allocated_amt'].fillna(DEFAULT_ALLOCATION)
        merged['is_allocation_matched'] = merged['allocated_amt'].notnull()

        # Calculate metrics
        merged['utilization_percentage'] = (merged['total_sanctioned_amount'] / merged['allocated_amount']) * 100.0
        merged['remaining_amount'] = merged['allocated_amount'] - merged['total_sanctioned_amount']

        # Alert categories
        def assign_alert(util_pct):
            if util_pct > 100.0:
                return "ALLOCATION EXCEEDED — VERIFY"
            elif util_pct >= 90.0:
                return "HIGH UTILIZATION"
            elif util_pct >= 70.0:
                return "MONITOR"
            else:
                return "NORMAL"

        merged['utilization_alert'] = merged['utilization_percentage'].apply(assign_alert)

        # Compute 0-100 fund utilization score for composite risk engine
        def compute_fund_score(row):
            util = row['utilization_percentage']
            if util > 100.0:
                return 100.0
            elif util >= 90.0:
                return 80.0
            elif util >= 70.0:
                return 50.0
            else:
                return 20.0

        merged['fund_utilization_score'] = merged.apply(compute_fund_score, axis=1)

        matched_cnt = int(merged['is_allocation_matched'].sum())
        total_mp_cnt = int(len(merged))
        print(f"[FundUtilization] Successfully matched {matched_cnt} / {total_mp_cnt} MPs ({(matched_cnt/total_mp_cnt)*100:.1f}%)")

        mp_util_scores = dict(zip(merged['mp_norm'], merged['fund_utilization_score']))
        return merged, mp_util_scores

if __name__ == "__main__":
    from preprocess import load_and_clean_data
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_path = os.path.join(base_dir, "data", "Works Sanctioned (1).csv")
    al1 = os.path.join(base_dir, "data", "Allocated Limit for Honble MPs.csv")
    al2 = os.path.join(base_dir, "data", "Allocated Limit for Honble MPs (1).csv")
    
    df_w = load_and_clean_data(data_path)
    tracker = FundUtilizationTracker()
    df_res, scores = tracker.process_fund_utilization(df_w, al1, al2)
    print("Sample MP Fund Utilization output:")
    print(df_res[['mp_name_works', 'allocated_amount', 'total_sanctioned_amount', 'utilization_percentage', 'utilization_alert']].head())
