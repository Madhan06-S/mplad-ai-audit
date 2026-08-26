import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SCORED_DATA_PATH = os.path.join(BASE_DIR, "ml", "outputs", "scored_projects_v3.csv")

class MLService:
    _instance = None
    _df = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLService, cls).__new__(cls)
            cls._instance.load_data()
        return cls._instance

    def load_data(self):
        if os.path.exists(SCORED_DATA_PATH):
            print(f"[MLService] Loading scored dataset from {SCORED_DATA_PATH}")
            self._df = pd.read_csv(SCORED_DATA_PATH)
            # Fill NaN values safely
            self._df['similar_work_id'] = self._df['similar_work_id'].fillna('')
            self._df['recommended_dt'] = self._df['recommended_dt'].fillna('')
            self._df['sanction_dt'] = self._df['sanction_dt'].fillna('')
            self._df['shap_top_attribution'] = self._df['shap_top_attribution'].fillna('N/A')
            self._df['anomaly_reason'] = self._df['anomaly_reason'].fillna('')
        else:
            print(f"[MLService] Warning: Scored data file not found at {SCORED_DATA_PATH}")
            self._df = pd.DataFrame()

    def get_projects(self, page: int = 1, page_size: int = 20, q: str = None, state: str = None, 
                     category: str = None, risk_level: str = None, sort_by: str = "risk_score"):
        if self._df is None or self._df.empty:
            return {"total_records": 0, "page": page, "page_size": page_size, "total_pages": 0, "data": []}

        df_filtered = self._df.copy()

        # Apply filters
        if state:
            df_filtered = df_filtered[df_filtered['state'].str.lower() == state.lower()]
        if category:
            df_filtered = df_filtered[df_filtered['work_category'].str.lower() == category.lower()]
        if risk_level:
            df_filtered = df_filtered[df_filtered['risk_level'].str.lower() == risk_level.lower()]
        if q:
            q_clean = q.lower()
            mask = (
                df_filtered['work_id'].astype(str).str.lower().str.contains(q_clean) |
                df_filtered['mp_name'].astype(str).str.lower().str.contains(q_clean) |
                df_filtered['work_description_clean'].astype(str).str.lower().str.contains(q_clean)
            )
            df_filtered = df_filtered[mask]

        # Sorting
        ascending = False
        if sort_by in df_filtered.columns:
            df_filtered = df_filtered.sort_values(by=sort_by, ascending=ascending)

        total_records = len(df_filtered)
        total_pages = int(np.ceil(total_records / page_size)) if page_size > 0 else 1

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        df_page = df_filtered.iloc[start_idx:end_idx]
        data = df_page.to_dict(orient='records')

        return {
            "total_records": total_records,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "data": data
        }

    def get_project_by_id(self, work_id: str):
        if self._df is None or self._df.empty:
            return None
        match = self._df[self._df['work_id'].astype(str) == str(work_id)]
        if match.empty:
            return None
        return match.iloc[0].to_dict()

    def get_analytics_overview(self):
        if self._df is None or self._df.empty:
            return {}

        df = self._df
        total_works = int(len(df))
        total_sanctioned = float(df['sanction_amount'].sum())
        avg_sanctioned = float(df['sanction_amount'].mean())
        avg_delay = float(df['sanction_delay_days'].mean())
        
        anomalies_cnt = int((df['anomaly_label'] == -1).sum())
        anomalies_pct = float(round((anomalies_cnt / total_works) * 100.0, 2)) if total_works > 0 else 0.0
        
        dup_cnt = int(df['is_duplicate_flag'].sum())
        
        risk_counts = df['risk_level'].value_counts().to_dict()
        for lvl in ['Low', 'Medium', 'High', 'Critical']:
            risk_counts.setdefault(lvl, 0)
            risk_counts[lvl] = int(risk_counts[lvl])
            
        top_states = df.groupby('state')['risk_score'].agg(['count', 'mean']).reset_index()
        top_states = top_states.sort_values(by='mean', ascending=False).head(10)
        top_states_list = [
            {"state": row['state'], "works_count": int(row['count']), "avg_risk_score": float(round(row['mean'], 1))}
            for _, row in top_states.iterrows()
        ]

        cat_breakdown = df.groupby('work_category')['risk_score'].agg(['count', 'mean']).reset_index()
        cat_list = [
            {"category": row['work_category'], "works_count": int(row['count']), "avg_risk_score": float(round(row['mean'], 1))}
            for _, row in cat_breakdown.iterrows()
        ]

        return {
            "total_works": total_works,
            "total_sanctioned_amount": total_sanctioned,
            "average_sanction_amount": avg_sanctioned,
            "average_sanction_delay_days": avg_delay,
            "anomalies_count": anomalies_cnt,
            "anomalies_percentage": anomalies_pct,
            "duplicates_flagged_count": dup_cnt,
            "risk_level_counts": risk_counts,
            "top_anomalous_states": top_states_list,
            "category_risk_breakdown": cat_list
        }
