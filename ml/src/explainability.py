import numpy as np
import pandas as pd

class ExplainabilityEngine:
    """
    Phase I: Explainable AI Engine.
    Provides feature attribution contributions and human-readable audit reasons
    written strictly in neutral, non-accusatory governance language.
    """
    def __init__(self):
        pass

    def explain_project_risk(self, row: pd.Series) -> dict:
        """
        Generates structured breakdown payload for a single project.
        """
        wid = row.get('work_id', '')
        score = float(row.get('composite_risk_score', row.get('risk_score', 0.0)))
        level = row.get('risk_level', 'Low')

        # Feature contributions
        contributions = {
            'Isolation Forest Anomaly': float(row.get('v1_contrib', row.get('v1_anomaly_score', 0) * 0.40)),
            'Cost Baseline Variance': float(row.get('cost_contrib', row.get('cost_anomaly_score', 0) * 0.15)),
            'Sanction Delay Lag': float(row.get('delay_contrib', row.get('delay_anomaly_score', 0) * 0.15)),
            'Duplicate Similarity Check': float(row.get('duplicate_contrib', row.get('duplicate_score', 0) * 0.15)),
            'MP Fund Utilization': float(row.get('fund_contrib', row.get('fund_utilization_score', 0) * 0.15)),
            'Geographic Risk Concentration': float(row.get('geo_contrib', row.get('geographic_score', 0) * 0.10)),
            'Agency Network Centrality': float(row.get('agency_contrib', row.get('agency_score', 0) * 0.10))
        }

        # Human-readable reasons using neutral audit terminology
        reasons = []
        
        amt_cat = row.get('amount_vs_category_median', 1.0)
        amt_state = row.get('amount_vs_state_median', 1.0)
        max_r = max(amt_cat, amt_state)
        if max_r >= 2.5:
            reasons.append(f"Sanction amount is {max_r:.1f}x higher than category/state baseline median.")

        delay_days = row.get('sanction_delay_days', 0)
        if delay_days >= 180:
            reasons.append(f"Recommendation-to-sanction approval delay of {delay_days:.0f} days.")

        dup_s = row.get('duplicate_score', 0)
        if dup_s >= 85.0:
            reasons.append(f"Potentially duplicate work candidate detected (Similarity: {dup_s:.1f}%). Requires human verification.")
        elif dup_s >= 50.0:
            reasons.append(f"Similar work candidate detected in regional database.")

        geo_s = row.get('geographic_score', 0)
        if geo_s >= 70.0:
            reasons.append("Project located in an Implementing Authority (IDA) displaying elevated risk concentration.")

        agency_s = row.get('agency_score', 0)
        if agency_s >= 70.0:
            reasons.append("High degree centrality and project volume concentration in agency network graph.")

        if not reasons:
            reasons.append("Project metrics align with regional baseline standards.")

        summary_explanation = " | ".join(reasons)

        recommendation = "PRIORITY FOR HUMAN AUDIT VERIFICATION" if level in ['Critical', 'High'] else "ROUTINE MONITORING"

        return {
            'work_id': wid,
            'composite_risk_score': round(score, 1),
            'risk_level': level,
            'recommendation': recommendation,
            'summary_explanation': summary_explanation,
            'feature_contributions': contributions,
            'audit_disclaimer': "AI-generated risk indicators support human decision-making and do not independently establish fraud, misconduct, or non-compliance."
        }

if __name__ == "__main__":
    ee = ExplainabilityEngine()
    sample = pd.Series({'work_id': 'W1', 'composite_risk_score': 88.5, 'risk_level': 'Critical', 'amount_vs_category_median': 3.5, 'sanction_delay_days': 400})
    print(ee.explain_project_risk(sample))
