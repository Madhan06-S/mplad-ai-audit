import numpy as np
import pandas as pd

class CompositeRiskEngine:
    """
    Module 3: Composite Risk Engine.
    Aggregates V1 anomaly scores and V2 signals (Cost, Delay, Duplicate similarity, Fund utilization)
    into a transparent 0-100 composite risk score with human-readable audit explanations.
    """
    def __init__(self, weights: dict[str, float] = None):
        if weights is None:
            self.weights = {
                'v1_weight': 0.40,
                'cost_weight': 0.15,
                'delay_weight': 0.15,
                'dup_weight': 0.15,
                'fund_weight': 0.15
            }
        else:
            self.weights = weights

    @staticmethod
    def compute_cost_score(row: pd.Series) -> float:
        amt_cat_ratio = row.get('amount_vs_category_median', 1.0)
        amt_state_ratio = row.get('amount_vs_state_median', 1.0)
        max_ratio = max(amt_cat_ratio, amt_state_ratio)
        
        if max_ratio >= 5.0:
            return 100.0
        elif max_ratio >= 2.5:
            return 75.0
        elif max_ratio >= 1.5:
            return 45.0
        else:
            return 15.0

    @staticmethod
    def compute_delay_score(row: pd.Series) -> float:
        delay_days = row.get('sanction_delay_days', 0)
        delay_ida_ratio = row.get('delay_vs_ida_median', 1.0)
        
        if delay_days >= 365 or delay_ida_ratio >= 4.0:
            return 100.0
        elif delay_days >= 180 or delay_ida_ratio >= 2.5:
            return 75.0
        elif delay_days >= 90:
            return 45.0
        else:
            return 15.0

    @staticmethod
    def assign_v2_risk_level(score: float) -> str:
        if score >= 85.0:
            return "Critical"
        elif score >= 70.0:
            return "High"
        elif score >= 40.0:
            return "Medium"
        else:
            return "Low"

    def generate_v2_reasons(self, row: pd.Series) -> str:
        reasons = []
        
        # 1. Cost Anomaly
        cost_s = row.get('cost_anomaly_score', 0)
        amt_cat = row.get('amount_vs_category_median', 1.0)
        amt_state = row.get('amount_vs_state_median', 1.0)
        if cost_s >= 75.0:
            max_r = max(amt_cat, amt_state)
            reasons.append(f"🔴 Cost anomaly: Sanction amount is {max_r:.1f}x baseline median.")

        # 2. Delay Anomaly
        delay_s = row.get('delay_anomaly_score', 0)
        delay_days = row.get('sanction_delay_days', 0)
        if delay_s >= 75.0:
            reasons.append(f"🔴 Delay anomaly: Recommendation-to-sanction lag of {delay_days:.0f} days.")

        # 3. Duplicate Similarity Signal
        dup_s = row.get('duplicate_score', 0)
        if dup_s >= 70.0:
            reasons.append(f"🟠 Duplicate check: Potentially similar work detected (Similarity: {dup_s:.1f}%). Requires human verification.")

        # 4. Fund Utilization Signal
        fund_s = row.get('fund_utilization_score', 0)
        if fund_s >= 80.0:
            reasons.append("🟠 Fund utilization: MP fund utilization is high / allocation limits approaching or exceeded.")

        # 5. Category Signal
        cat = row.get('work_category', '')
        if cat in ['Trust and Society', 'Bar and Associations']:
            reasons.append(f"🟠 Category signal: Special entity category '{cat}'.")

        # 6. Global V1 Isolation Forest Signal
        v1_s = row.get('v1_anomaly_score', 0)
        if v1_s >= 75.0:
            reasons.append("🔴 Anomaly signal: Overall statistical outlier pattern detected by Isolation Forest.")

        if len(reasons) == 0:
            reasons.append("🟢 Project parameters within standard baseline bounds.")

        return " | ".join(reasons)

    def process_composite_risk(
        self,
        df_v1_scored: pd.DataFrame,
        max_sim_dict: dict[str, float],
        mp_util_scores: dict[str, float]
    ) -> pd.DataFrame:
        df_out = df_v1_scored.copy()

        # Safely extract V1 score column
        if 'v1_anomaly_score' not in df_out.columns:
            if 'risk_score' in df_out.columns:
                df_out['v1_anomaly_score'] = df_out['risk_score']
            else:
                df_out['v1_anomaly_score'] = 20.0

        # Compute component scores
        df_out['cost_anomaly_score'] = df_out.apply(self.compute_cost_score, axis=1)
        df_out['delay_anomaly_score'] = df_out.apply(self.compute_delay_score, axis=1)

        # Duplicate similarity score: max similarity * 100
        df_out['duplicate_score'] = df_out['work_id'].map(max_sim_dict).fillna(0.0) * 100.0

        # Fund utilization score
        from fund_utilization import FundUtilizationTracker
        df_out['mp_norm'] = df_out['mp_name'].apply(FundUtilizationTracker.normalize_mp_name)
        df_out['fund_utilization_score'] = df_out['mp_norm'].map(mp_util_scores).fillna(20.0)

        # Weighted composite risk score
        w = self.weights
        df_out['composite_risk_score'] = (
            w['v1_weight'] * df_out['v1_anomaly_score'] +
            w['cost_weight'] * df_out['cost_anomaly_score'] +
            w['delay_weight'] * df_out['delay_anomaly_score'] +
            w['dup_weight'] * df_out['duplicate_score'] +
            w['fund_weight'] * df_out['fund_utilization_score']
        )
        
        df_out['composite_risk_score'] = np.round(np.clip(df_out['composite_risk_score'], 0.0, 100.0), 1)
        df_out['risk_level'] = df_out['composite_risk_score'].apply(self.assign_v2_risk_level)
        df_out['risk_reasons'] = df_out.apply(self.generate_v2_reasons, axis=1)

        return df_out

if __name__ == "__main__":
    cre = CompositeRiskEngine()
    print("V2 Composite Risk Level (91.5):", cre.assign_v2_risk_level(91.5))
