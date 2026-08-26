import numpy as np
import pandas as pd

class RiskEngineV2:
    """
    ML V2 Multi-Factor Composite Risk Engine combining Isolation Forest cost/delay anomalies,
    TF-IDF duplicate text similarity, MP fund utilization ratios, and category risk weights.
    """
    def __init__(self):
        pass

    @staticmethod
    def normalize_isolation_scores(raw_decision_scores: np.ndarray) -> np.ndarray:
        inverted = -raw_decision_scores
        min_val = np.min(inverted)
        max_val = np.max(inverted)
        if max_val == min_val:
            return np.full_like(inverted, 50.0)
        scaled = ((inverted - min_val) / (max_val - min_val)) * 100.0
        return np.clip(scaled, 0.0, 100.0)

    @staticmethod
    def assign_risk_level(risk_score: float) -> str:
        if risk_score >= 85.0:
            return "Critical"
        elif risk_score >= 70.0:
            return "High"
        elif risk_score >= 40.0:
            return "Medium"
        else:
            return "Low"

    def compute_composite_risk(self, row: pd.Series, base_anomaly_score: float) -> tuple[float, str]:
        reasons = []
        
        # 1. Cost & Delay Risk (from IsolationForest decision function)
        cost_delay_score = base_anomaly_score
        
        # 2. Duplicate Text Similarity Risk
        dup_sim = float(row.get('duplicate_similarity_score', 0.0))
        dup_score = dup_sim * 100.0
        if dup_sim >= 0.75:
            similar_id = row.get('similar_work_id', 'Unknown')
            reasons.append(f"High text similarity ({dup_sim*100:.1f}%) with work '{similar_id}' under the same MP (Potential duplicate recommendation / split billing).")

        # 3. Fund Utilization Risk
        util_pct = float(row.get('mp_utilization_pct', 0.0))
        if util_pct > 100.0:
            util_score = min(100.0, (util_pct - 100.0) * 2.0)
            reasons.append(f"MP cumulative spending (₹ {row.get('mp_total_sanctioned', 0):,.0f}) exceeds entitlement limit (₹ {row.get('mp_allocated_limit', 0):,.0f}) with {util_pct:.1f}% utilization.")
        else:
            util_score = 0.0

        # 4. Category Risk Weight
        cat = str(row.get('work_category', ''))
        if cat == 'Trust and Society':
            cat_score = 75.0
            reasons.append("Work belongs to special category 'Trust and Society' requiring heightened compliance verification.")
        elif cat == 'Bar and Associations':
            cat_score = 90.0
            reasons.append("Work belongs to special category 'Bar and Associations' requiring heightened compliance verification.")
        elif cat == 'Repair and Renovation':
            cat_score = 40.0
        else:
            cat_score = 10.0

        # Specific Cost & Delay Reasons
        amt_cat_ratio = row.get('amount_vs_category_median', 1.0)
        amt = row.get('sanction_amount', 0.0)
        state = row.get('state', 'State')
        amt_state_ratio = row.get('amount_vs_state_median', 1.0)
        
        if amt_cat_ratio >= 2.5:
            reasons.append(f"Sanction amount (₹ {amt:,.0f}) is {amt_cat_ratio:.1f}x higher than the typical amount for work category '{cat}'.")
        elif amt_state_ratio >= 2.5:
            reasons.append(f"Sanction amount (₹ {amt:,.0f}) is {amt_state_ratio:.1f}x higher than the median sanction amount in {state}.")

        delay_days = row.get('sanction_delay_days', 0)
        delay_ida_ratio = row.get('delay_vs_ida_median', 1.0)
        ida = row.get('ida', 'Implementing Authority')

        if delay_days >= 365:
            reasons.append(f"Severe sanction delay of {delay_days:.0f} days (> 1 year) between recommendation and approval.")
        elif delay_ida_ratio >= 2.5:
            reasons.append(f"Sanction delay ({delay_days:.0f} days) is {delay_ida_ratio:.1f}x higher than the typical approval time for authority '{ida}'.")

        # Weighted Composite Score
        composite_score = (
            0.45 * cost_delay_score +
            0.30 * dup_score +
            0.15 * util_score +
            0.10 * cat_score
        )
        
        composite_score = np.round(np.clip(composite_score, 0.0, 100.0), 1)

        if len(reasons) == 0 and row.get('anomaly_label', 1) == -1:
            reasons.append("Overall project pattern is anomalous compared with national baseline records.")
        elif len(reasons) == 0:
            reasons.append("Standard project parameters within normal baseline limits.")

        return composite_score, " | ".join(reasons)

    def process_dataset(self, df_input: pd.DataFrame, raw_scores: np.ndarray, anomaly_labels: np.ndarray) -> pd.DataFrame:
        df_res = df_input.copy()
        df_res['anomaly_label'] = anomaly_labels
        df_res['anomaly_score'] = raw_scores
        
        base_scores = self.normalize_isolation_scores(raw_scores)
        
        composite_scores = []
        anomaly_reasons = []
        
        for idx, row in df_res.iterrows():
            base_score = base_scores[df_res.index.get_loc(idx)]
            comp_score, reason_str = self.compute_composite_risk(row, base_score)
            composite_scores.append(comp_score)
            anomaly_reasons.append(reason_str)
            
        df_res['risk_score'] = composite_scores
        df_res['risk_level'] = df_res['risk_score'].apply(self.assign_risk_level)
        df_res['anomaly_reason'] = anomaly_reasons
        return df_res

if __name__ == "__main__":
    re2 = RiskEngineV2()
    print("Risk Level Test (91.2):", re2.assign_risk_level(91.2))
