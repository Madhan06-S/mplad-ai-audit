import os
import json
import numpy as np
import pandas as pd

class GeographicIntelligenceEngine:
    """
    Phase B: Geographic Intelligence Engine.
    Analyzes spatial, IDA, and constituency-level risk concentration, project density,
    and peer variance without inventing fake GIS coordinates.
    """
    def __init__(self):
        pass

    def process_geographic_risk(self, df_projects: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float], dict]:
        """
        Computes regional/IDA risk concentration and assigns a geographic_risk_score (0-100)
        to every project and IDA group.
        """
        print("[GeographicIntel] Calculating regional & IDA peer risk concentration...")
        df = df_projects.copy()
        
        # Determine risk score column to use
        risk_col = 'composite_risk_score' if 'composite_risk_score' in df.columns else 'risk_score'

        # Group by IDA to calculate regional statistics
        ida_stats = df.groupby(['state', 'ida']).agg(
            total_works=('work_id', 'count'),
            total_sanction_amount=('sanction_amount', 'sum'),
            mean_work_amount=('sanction_amount', 'mean'),
            mean_risk_score=(risk_col, 'mean'),
            critical_high_count=('risk_level', lambda s: s.isin(['Critical', 'High']).sum())
        ).reset_index()

        # Compute State-level benchmarks for peer comparison
        state_benchmarks = df.groupby('state').agg(
            state_avg_risk=(risk_col, 'mean'),
            state_avg_amount=('sanction_amount', 'mean')
        ).to_dict(orient='index')

        # IDA z-score and risk concentration
        ida_stats['critical_pct'] = (ida_stats['critical_high_count'] / ida_stats['total_works']) * 100.0
        
        # State average fallbacks
        ida_stats['state_avg_risk'] = ida_stats['state'].map(lambda s: state_benchmarks.get(s, {}).get('state_avg_risk', 50.0))
        ida_stats['risk_variance_vs_state'] = ida_stats['mean_risk_score'] - ida_stats['state_avg_risk']

        # Compute 0-100 geographic risk score per IDA
        def calc_ida_geo_score(row):
            score = 20.0  # Baseline
            
            # Risk score elevation above state average
            if row['risk_variance_vs_state'] > 15.0:
                score += 35.0
            elif row['risk_variance_vs_state'] > 5.0:
                score += 20.0
                
            # High proportion of critical/high risk projects
            if row['critical_pct'] >= 25.0:
                score += 30.0
            elif row['critical_pct'] >= 10.0:
                score += 15.0
                
            # High project volume concentration
            if row['total_works'] >= 200:
                score += 15.0
            elif row['total_works'] >= 75:
                score += 10.0

            return min(100.0, score)

        ida_stats['geographic_risk_score'] = ida_stats.apply(calc_ida_geo_score, axis=1)

        def assign_geo_reason(row):
            reasons = []
            if row['risk_variance_vs_state'] > 10.0:
                reasons.append(f"IDA average risk ({row['mean_risk_score']:.1f}) is significantly higher than state baseline ({row['state_avg_risk']:.1f}).")
            if row['critical_pct'] >= 20.0:
                reasons.append(f"High concentration of flagged projects ({row['critical_pct']:.1f}% critical/high risk).")
            if row['total_works'] >= 150:
                reasons.append(f"Unusually high project concentration ({row['total_works']} works sanctioned).")
            if not reasons:
                reasons.append("District and IDA parameters match regional baseline standards.")
            return " | ".join(reasons)

        ida_stats['geographic_reason'] = ida_stats.apply(assign_geo_reason, axis=1)

        # Map back to individual projects
        ida_score_map = dict(zip(ida_stats['ida'], ida_stats['geographic_risk_score']))
        df['geographic_risk_score'] = df['ida'].map(ida_score_map).fillna(20.0)

        # Dictionary per work_id
        project_geo_scores = dict(zip(df['work_id'], df['geographic_risk_score']))

        # Summary JSON
        top_risk_idas = ida_stats.sort_values(by='geographic_risk_score', ascending=False).head(10)
        summary = {
            "total_idas_analyzed": len(ida_stats),
            "high_risk_idas_count": int((ida_stats['geographic_risk_score'] >= 70.0).sum()),
            "top_risk_idas": top_risk_idas[['state', 'ida', 'total_works', 'total_sanction_amount', 'mean_risk_score', 'geographic_risk_score', 'geographic_reason']].to_dict(orient='records')
        }

        return ida_stats, project_geo_scores, summary

if __name__ == "__main__":
    from preprocess import load_and_clean_data
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    df_w = load_and_clean_data(os.path.join(base_dir, "data", "Works Sanctioned (1).csv"))
    
    geo_engine = GeographicIntelligenceEngine()
    ida_df, geo_scores, summary = geo_engine.process_geographic_risk(df_w)
    print("Sample Geographic Intelligence Output:")
    print(ida_df[['ida', 'state', 'total_works', 'geographic_risk_score', 'geographic_reason']].head())
