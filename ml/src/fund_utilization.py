import os
import re
import pandas as pd
import numpy as np

class FundUtilizationTracker:
    """
    Tracks MP-wise fund allocations and calculates cumulative spending vs entitlement limits.
    """
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.data_dir = data_dir
        self.mp_allocations = {}
        self.default_allocated_limit = 250000000.0 # Default ₹ 25 Crore 5-year limit

    @staticmethod
    def clean_mp_name(name: str) -> str:
        if not isinstance(name, str):
            return ""
        name = re.sub(r'^(Shri|Smt|Dr|Prof|Er|Adv)\.?', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s+', ' ', name).strip().lower()
        return name

    def load_allocations(self):
        file1 = os.path.join(self.data_dir, "Allocated Limit for Honble MPs.csv")
        file2 = os.path.join(self.data_dir, "Allocated Limit for Honble MPs (1).csv")
        
        for fpath in [file1, file2]:
            if os.path.exists(fpath):
                df = pd.read_csv(fpath)
                mp_col = [c for c in df.columns if "member" in c.lower() or "mp" in c.lower()][0]
                amt_col = [c for c in df.columns if "amount" in c.lower() or "limit" in c.lower()][0]
                
                for _, row in df.iterrows():
                    mp_clean = self.clean_mp_name(str(row[mp_col]))
                    raw_amt = str(row[amt_col]).replace(',', '').replace('₹', '').strip()
                    try:
                        amt = float(raw_amt)
                        if amt > 0:
                            self.mp_allocations[mp_clean] = amt
                    except ValueError:
                        continue
        print(f"[FundUtilization] Loaded entitlement limits for {len(self.mp_allocations)} unique MPs.")

    def calculate_utilization(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Appends mp_allocated_limit, mp_total_sanctioned, and mp_utilization_pct to dataframe.
        """
        if not self.mp_allocations:
            self.load_allocations()
            
        df_out = df.copy()
        
        # Calculate cumulative spending per MP
        mp_totals = df_out.groupby('mp_name')['sanction_amount'].sum().to_dict()
        
        # Map MP totals and limits
        df_out['clean_mp_name'] = df_out['mp_name'].apply(self.clean_mp_name)
        df_out['mp_total_sanctioned'] = df_out['mp_name'].map(mp_totals).fillna(0.0)
        df_out['mp_allocated_limit'] = df_out['clean_mp_name'].map(self.mp_allocations).fillna(self.default_allocated_limit)
        
        # Calculate utilization percentage
        df_out['mp_utilization_pct'] = (df_out['mp_total_sanctioned'] / df_out['mp_allocated_limit']) * 100.0
        df_out['mp_utilization_pct'] = df_out['mp_utilization_pct'].round(2)
        
        print("[FundUtilization] Fund utilization calculations completed.")
        return df_out

if __name__ == "__main__":
    from preprocess import load_and_clean_data
    import os
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "Works Sanctioned (1).csv")
    df_raw = load_and_clean_data(data_path)
    fut = FundUtilizationTracker()
    df_util = fut.calculate_utilization(df_raw)
    print(df_util[['mp_name', 'sanction_amount', 'mp_total_sanctioned', 'mp_allocated_limit', 'mp_utilization_pct']].head(10))
