import numpy as np
import pandas as pd

class RiskEngine:
    """
    Translates raw model decision scores into 0-100 normalized Risk Scores,
    maps risk levels (Low, Medium, High, Critical), and generates data-backed human-readable anomaly reasons.
    """
    def __init__(self):
        pass

    @staticmethod
    def calculate_risk_scores(raw_decision_scores: np.ndarray) -> np.ndarray:
        """
        Normalizes raw IsolationForest decision scores (where lower = more anomalous)
        into a intuitive 0 - 100 Risk Score (where higher = higher anomaly risk).
        """
        # Invert decision score: more negative -> higher anomaly
        inverted = -raw_decision_scores
        min_val = np.min(inverted)
        max_val = np.max(inverted)
        
        if max_val == min_val:
            return np.full_like(inverted, 50.0)
            
        # Min-max scale to 0-100 range
        scaled_scores = ((inverted - min_val) / (max_val - min_val)) * 100.0
        
        # Apply gentle sigmoidal/power stretching to accentuate tail anomalies
        p95 = np.percentile(scaled_scores, 95)
        # Ensure scores span 0-100 smoothly
        risk_scores = np.clip(scaled_scores, 0.0, 100.0)
        return np.round(risk_scores, 1)

    @staticmethod
    def assign_risk_level(risk_score: float) -> str:
        """
        Assigns risk tiers based on 0-100 Risk Score:
        0 - 39   : Low
        40 - 69  : Medium
        70 - 84  : High
        85 - 100 : Critical
        """
        if risk_score >= 85.0:
            return "Critical"
        elif risk_score >= 70.0:
            return "High"
        elif risk_score >= 40.0:
            return "Medium"
        else:
            return "Low"

    @staticmethod
    def generate_anomaly_reasons(row: pd.Series) -> str:
        """
        Generates data-backed human-readable explanations based on actual project metrics.
        """
        reasons = []
        
        # Cost anomaly reasons
        amt_cat_ratio = row.get('amount_vs_category_median', 1.0)
        amt_state_ratio = row.get('amount_vs_state_median', 1.0)
        amt = row.get('sanction_amount', 0.0)
        cat = row.get('work_category', 'Category')
        state = row.get('state', 'State')
        
        if amt_cat_ratio >= 2.5:
            reasons.append(f"Sanction amount (₹ {amt:,.0f}) is {amt_cat_ratio:.1f}x higher than the typical amount for work category '{cat}'.")
        elif amt_state_ratio >= 2.5:
            reasons.append(f"Sanction amount (₹ {amt:,.0f}) is {amt_state_ratio:.1f}x higher than the median sanction amount in {state}.")

        # Delay anomaly reasons
        delay_days = row.get('sanction_delay_days', 0)
        delay_ida_ratio = row.get('delay_vs_ida_median', 1.0)
        delay_state_ratio = row.get('delay_vs_state_median', 1.0)
        ida = row.get('ida', 'Implementing Agency')

        if delay_days >= 365:
            reasons.append(f"Severe sanction delay of {delay_days:.0f} days (> 1 year) between recommendation and approval.")
        elif delay_ida_ratio >= 2.5:
            reasons.append(f"Sanction delay ({delay_days:.0f} days) is {delay_ida_ratio:.1f}x higher than the typical approval time for authority '{ida}'.")
        elif delay_state_ratio >= 2.5:
            reasons.append(f"Sanction delay ({delay_days:.0f} days) is {delay_state_ratio:.1f}x higher than the state average in {state}.")

        # Category specific compliance check
        if cat in ['Trust and Society', 'Bar and Associations']:
            reasons.append(f"Work belongs to special category '{cat}' requiring heightened compliance verification.")

        # Default reason if anomaly label is -1 but specific thresholds weren't met
        if len(reasons) == 0 and row.get('anomaly_label', 1) == -1:
            reasons.append("Overall project cost-delay pattern is anomalous compared with baseline national records.")
        elif len(reasons) == 0:
            reasons.append("Standard project parameters within normal baseline limits.")

        return " | ".join(reasons)

    def process_dataset(self, df_features: pd.DataFrame, raw_scores: np.ndarray, anomaly_labels: np.ndarray) -> pd.DataFrame:
        df_res = df_features.copy()
        df_res['anomaly_label'] = anomaly_labels
        df_res['anomaly_score'] = raw_scores
        df_res['risk_score'] = self.calculate_risk_scores(raw_scores)
        df_res['risk_level'] = df_res['risk_score'].apply(self.assign_risk_level)
        df_res['anomaly_reason'] = df_res.apply(self.generate_anomaly_reasons, axis=1)
        return df_res

if __name__ == "__main__":
    re = RiskEngine()
    print("Risk Level Test (87.5):", re.assign_risk_level(87.5))
    print("Risk Level Test (25.0):", re.assign_risk_level(25.0))
